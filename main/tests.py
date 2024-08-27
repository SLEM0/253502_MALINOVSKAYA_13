from django.test import TestCase
from .models import *

class NewsTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        self.news = News.objects.create(
            title='Test Title',
            content='test content'
        )

    def test_news_str(self):
        """Тестирование метода __str__ модели News"""
        self.assertEqual(str(self.news), 'Test Title')

class TermTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        self.term = Term.objects.create(
            term = 'Test Term',
            definition = 'Test definition'
        )

    def test_term_str(self):
        """Тестирование метода __str__ модели Term"""
        self.assertEqual(str(self.term), 'Test Term')

class VacancyTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        self.vacancy = Vacancy.objects.create(
            title = 'Test Title',
            description = 'Test description'
        )

    def test_vacancy_str(self):
        """Тестирование метода __str__ модели Vacancy"""
        self.assertEqual(str(self.vacancy), 'Test Title')

class PromocodeTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        self.promocode = Promocode.objects.create(
            code = 'Test',
            is_active = True,
            sale = 0
        )

    def test_promocode_str(self):
        """Тестирование метода __str__ модели Term"""
        self.assertEqual(str(self.promocode), 'Test')

class CategoryTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        self.category = Category.objects.create(
            name = 'Test Name'
        )

    def test_category_str(self):
        """Тестирование метода __str__ модели Category"""
        self.assertEqual(str(self.category), 'Test Name')

class OwnerTest(TestCase):
    def setUp(self):
        # Создаем объект модели для тестирования
        self.owner = Owner.objects.create(
            name = 'Test Name',
            email = 'test@gmail.com',
            phone_number = '+375291234567'
        )

    def test_owner_str(self):
        """Тестирование метода __str__ модели Owner"""
        self.assertEqual(str(self.owner), 'Test Name')