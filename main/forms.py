from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_regex = r'^\+375(29)\d{3}\d{2}\d{2}$'
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year)))
    phone = forms.CharField(
        validators=[RegexValidator(phone_regex, 'Номер телефона должен быть в формате'
                                                ': +375 (29) XXX-XX-XX')])

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'phone', 'date_of_birth')

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) < 18:
            raise ValidationError('Вам должно быть не менее 18 лет для регистрации.')
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        client = Client.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        )

        return client

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

class EmployeeCreationForm(UserCreationForm):
    job_description = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField()
    email = forms.EmailField(required=True)
    phone_regex = r'^\+375(29)\d{3}\d{2}\d{2}$'
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year)))
    phone = forms.CharField(
        validators=[RegexValidator(phone_regex, 'Номер телефона должен быть в формате'
                                                ': +375 (29) XXX-XX-XX')])

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('job_description', 'photo', 'phone', 'email', 'date_of_birth')

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) < 18:
            raise ValidationError('Сотруднику должно быть не менее 18 лет для регистрации.')
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.save()

        employee = Employee.objects.create(
            user=user,
            job_description=self.cleaned_data['job_description'],
            photo=self.cleaned_data['photo'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        )
        return employee
