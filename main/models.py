from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class About_Company(models.Model):
    content = models.TextField()
    def __str__(self):
        return self.content
    class Meta:
        verbose_name_plural = 'О компании'

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images', default='3.jpg')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Новости'

class Term(models.Model):
    term = models.CharField(max_length=200)
    definition = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.term
    class Meta:
        verbose_name_plural = 'Термины'

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Вакансии'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    def __str__(self):
        return self.text
    class Meta:
        verbose_name_plural = 'Отзывы'


class Promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    sale = models.IntegerField(default=0)
    def __str__(self):
        return self.code
    class Meta:
        verbose_name_plural = 'Промокоды'

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Категории'

class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Владельцы'

class RealEstate(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owners = models.ManyToManyField(Owner)
    def __str__(self):
        return f"{self.category.name}: {self.id}"
    class Meta:
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['category']

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    date_of_birth = models.DateField()
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Клиенты'
        ordering = ['user']

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE) 
    date = models.DateTimeField()
    price = models.DecimalField(default=1000000, decimal_places=2, max_digits=10)
    def __str__(self):
        return f"{self.real_estate} для клиента {self.user.username}"
    class Meta:
        verbose_name_plural = 'Заказы'
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_description = models.TextField()
    photo = models.ImageField(upload_to='employees', default='employees/employee.jpg')
    phone = models.CharField(max_length=13)
    date_of_birth = models.DateField(null=True, blank=True, default="2000-01-01")
    email = models.EmailField()
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Сотрудники'