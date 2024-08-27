from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from statistics import mean, median, mode, StatisticsError
from datetime import datetime
import calendar
import logging
import requests
import matplotlib.pyplot as plt
import os
from real_estate_agency import settings
from django.utils.timezone import get_current_timezone
from decimal import Decimal
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def homeView(request):
    logger.info('Rendering home view')
    try:
        latest_news = News.objects.latest('id')
        all_real_estate = RealEstate.objects.all()
        categories = Category.objects.all()
        selected_category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if selected_category:
            all_real_estate = RealEstate.objects.filter(category__name=selected_category)
        if min_price:
            all_real_estate = all_real_estate.filter(price__gte=min_price)
        
        if max_price:
            all_real_estate = all_real_estate.filter(price__lte=max_price)
        
        return render(request, 'home.html',
        {'latest_news': latest_news, 'all_items':all_real_estate, 'categories': categories})
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')

def create_order(request, real_estate_id):
    if request.user.is_authenticated:
        user = request.user  # Получаем текущего пользователя
        real_estate = get_object_or_404(RealEstate, id=real_estate_id)  # Получаем объект недвижимости или возвращаем 404 ошибку, если объект не найден
        if request.method == 'POST':
            promo_code = request.POST.get('promo_code', None)  # Получаем введенный пользователем промокод
            try:
                order = Order(user=user, real_estate=real_estate, date=datetime.now())
                
                if promo_code and Promocode.objects.filter(code=promo_code).exists():
                    promo = Promocode.objects.get(code=promo_code)
                    if promo.is_active:
                        # Предположим, что promo.sale представляет собой процент скидки (например, 20%)
                        promo_sale_decimal = Decimal(promo.sale) / 100  # Преобразование процента в десятичную дробь
                        # Затем вы можете использовать это значение для расчета цены заказа
                        order.price = real_estate.price * (1 - promo_sale_decimal)
                    else:
                        order.price = real_estate.price    
                else:
                    order.price = real_estate.price
                order.save()
                logger.info(f'Order created successfully for user {user.username} and real estate {real_estate.id}')
                return HttpResponseRedirect('/orders/user/')
            except Promocode.DoesNotExist:
                logger.error('Promo code not found')
                # Обработка ситуации, когда промокод не найден
                return HttpResponseRedirect('/orders/user/')
            except Exception as e:
                logger.error(f'Error creating order: {str(e)}')
                # Дополнительная обработка ошибки или возврат страницы с сообщением об ошибке
                return HttpResponseRedirect('/orders/user/')
    else:
        return redirect('login')  # перенаправление на страницу входа, если пользователь не авторизован

def contactsView(request):
    employees = Employee.objects.all()
    logger.info('Viewing contacts page')
    return render(request, 'contacts.html', {'employees': employees})

def privacy_policy_view(request):
    logger.info('Viewing privacy policy page')
    return render(request, 'privacy_policy.html')

def news_view(request):
    all_news = News.objects.all()
    logger.info('Viewing news page')
    return render(request, 'news.html', {'all_items': all_news})

def about_company_view(request):
    all_about_company = About_Company.objects.all()
    logger.info('Viewing about company page')
    return render(request, 'about_company.html', {'all_items': all_about_company})

def dict_of_terms_view(request):
    all_dict_of_terms = Term.objects.all()
    logger.info('Viewing dictionary of terms page')
    return render(request, 'dict_of_terms.html', {'all_items': all_dict_of_terms})

def promocodes_view(request):
    all_promocodes = Promocode.objects.all()
    logger.info('Viewing promocodes page')
    return render(request, 'promocodes.html', {'all_items': all_promocodes})

def vacancies_view(request):
    all_vacancies = Vacancy.objects.all()
    logger.info('Viewing vacancies page')
    return render(request, 'vacancies.html', {'all_items': all_vacancies})

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EmployeeSignUp(CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup_employee.html'

@login_required
def orders_user(request):
    user = request.user  # Получаем текущего пользователя
    orders = Order.objects.filter(user=user)  # Получаем все заказы, принадлежащие текущему пользователю
    len_ord = len(orders)
    logger.info(f"User {user.username} accessed their orders. Number of orders: {len_ord}")
    return render(request, 'user_orders.html', {'orders':orders, 'len_ord':len_ord})

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all()
    prices = [order.real_estate.price for order in orders]
    total_sales = sum(prices)
    try:
        sales_mode = mode(prices)
    except StatisticsError:
        sales_mode = "Мода не определена, так как все значения уникальны"

    current_date = datetime.now()
    clients = Client.objects.all()
    ages = []
    for client in clients:
        age = current_date.year - client.date_of_birth.year - ((current_date.month, current_date.day) < (client.date_of_birth.month, client.date_of_birth.day))
        ages.append(age)

    categories = Category.objects.all()
    popular_dict = dict()
    for category in categories:
        popular_dict[category.name] = 0
    for order in orders:
        popular_dict[order.real_estate.category.name] += 1
    sort_popular_dict = {k: v for k, v in sorted(popular_dict.items(), key=lambda item: item[1], reverse=True)}
    k = list(sort_popular_dict.keys())
    v = list(sort_popular_dict.values())
    plt.figure(figsize=(8, 6))
    plt.pie(v, labels=k, autopct='%1.1f%%')
    plt.axis('equal') 
    save_path1 = os.path.join(settings.MEDIA_ROOT, 'diag1.png')
    image_path1 = os.path.join(settings.MEDIA_URL, 'diag1.png')
    plt.savefig(save_path1)

    price_dict = dict()
    for category in categories:
        price_dict[category.name] = 0
    for order in orders:
        price_dict[order.real_estate.category.name] += order.price
    sort_price_dict = {k: v for k, v in sorted(price_dict.items(), key=lambda item: item[1], reverse=True)}
    k = list(sort_price_dict.keys())
    v = list(sort_price_dict.values())
    plt.figure(figsize=(8, 6))
    plt.pie(v, labels=k, autopct='%1.1f%%')
    plt.axis('equal') 
    save_path2 = os.path.join(settings.MEDIA_ROOT, 'diag2.png')
    image_path2 = os.path.join(settings.MEDIA_URL, 'diag2.png')
    plt.savefig(save_path2)

    try:
        mean_prices = mean(prices)
        median_prices = median(prices)
    except:
        mean_prices = 0
        median_prices = 0
    try:
        mean_ages = mean(ages)
        median_ages = median(ages)
    except:
        mean_ages = 0
        median_ages = 0
    
    logger.info(f"Admin accessed the orders. Total sales: {total_sales}, Average sales: {mean_prices}, Sales mode: {sales_mode}, Sales median: {mean_prices}, Average ages: {mean_ages}, Ages median: {median_ages}")
    return render(request, 'admin_orders.html',
                  {'total_sales':total_sales, 'average_sales':mean_prices, 'sales_mode':sales_mode, 'sales_median':median_prices,
                   'average_ages':mean_ages, 'ages_median':median_ages,
                   'popular_dict':sort_popular_dict.items(), 'price_dict':sort_price_dict.items(), 'orders':orders, 'clients':clients,
                   'image1':image_path1, 'image2':image_path2})

def review_view(request):
    all_reviews = Review.objects.all()
    return render(request, 'reviews.html', {'all_items':all_reviews})

def add_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.created_at = datetime.now()  # Сохраняем текущую дату и время в UTC
                review.user = request.user
                review.save()
                logger.info(f"User {request.user.username} added a review.")
                return redirect('home')  # перенаправление на нужную страницу после добавления отзыва
        else:
            form = ReviewForm()
        return render(request, 'add_review.html', {'form': form})
    else:
        logger.warning("Anonymous user tried to add a review. Redirecting to login page.")
        return redirect('login')  # перенаправление на страницу входа, если пользователь не авторизован

def read(request):
    category = Category.objects.all()
    return render(request, "crud.html", {"category": category})

def create(request):
    if request.method == "POST":
        category = Category()
        category.name = request.POST.get("name")
        category.save()
        logger.info(f"Category '{category.name}' created.")
    return HttpResponseRedirect("/")

def edit(request, id):
    try:
        category = Category.objects.get(id=id)

        if request.method == "POST":
            category.name = request.POST.get("name")
            category.save()
            logger.info(f"Category '{category.name}' edited.")
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"category": category})
    except Category.DoesNotExist:
        logger.error(f"Category with id {id} not found.")
        return HttpResponseNotFound("<h2>Category not found</h2>")

def delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category_name = category.name
        category.delete()
        logger.info(f"Category '{category_name}' deleted.")
        return HttpResponseRedirect("/")
    except Category.DoesNotExist:
        logger.error(f"Category with id {id} not found.")
        return HttpResponseNotFound("<h2>Category not found</h2>")
    
def index(request):
    appid = '9f7316effdaacece680141736f86f1ec'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    city = 'Minsk'
    res = requests.get(url.format(city)).json()
    city_info = {
        'city' : city,
        'temp' : res["main"]["temp"],
        'icon' : res["weather"][0]["icon"]
    }
    url = 'https://favqs.com/api/qotd'
    response = requests.get(url)
    quote_data = response.json()
    quote = quote_data['quote']['body']  # Текст цитаты

    c = calendar.HTMLCalendar()
    d = datetime.today()
    html_out = c.formatmonth(datetime.today().year, datetime.today().month)

    tz = get_current_timezone()
    stored_date = datetime.now()
    desired_date = stored_date + tz.utcoffset(stored_date)
    timezone_name=desired_date.astimezone().tzinfo

    context = {'info': city_info, 'd': d, 'html_out': html_out, 'quote':quote, 'timezone':timezone_name, 'date':desired_date}
    return render(request, 'index.html', context)
