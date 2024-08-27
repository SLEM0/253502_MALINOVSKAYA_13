"""
URL configuration for real_estate_agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from main.views import *
from django.urls import path,include, re_path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('admin/', news_view, name='admin'),
    path('', homeView, name='home'),
    re_path(r'^news', news_view, name='news'),
    re_path(r'^about_company', about_company_view, name='about_company'),
    re_path(r'^contacts', contactsView, name='contacts'),
    re_path(r'^dict_of_terms', dict_of_terms_view, name='dict_of_terms'),
    re_path(r'^privacy_policy', privacy_policy_view, name='privacy_policy'),
    re_path(r'^promocodes', promocodes_view, name='promocodes'),
    re_path(r'^vacancies', vacancies_view, name='vacancies'),
    re_path(r'^accounts', include('django.contrib.auth.urls')),
    re_path(r'^signup_employee', EmployeeSignUp.as_view(), name='signup_employee'),
    re_path(r"^signup", SignUp.as_view(), name="signup"),
    re_path(r'^orders/user', orders_user, name='user_orders'),
    re_path(r'^orders/admin', admin_orders, name='admin_orders'),
    re_path(r'^reviews', review_view, name='reviews'),
    re_path(r'^category', read, name='category'),
    re_path(r'^add_review', add_review, name='add_review'),
    re_path(r"^create", create),
    re_path(r'^index', index, name='index'),
    path('<int:real_estate_id>/', create_order, name='create_order'),
    path("edit/<int:id>/", edit),
    path("delete/<int:id>/", delete),
]

from django.conf.urls.static import static
from real_estate_agency import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)