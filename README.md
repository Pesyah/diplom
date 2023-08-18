## orders_on_optic/view.py

from django.views.generic import DetailView, ListView
from .models import Optics_order
from django.shortcuts import render, HttpResponse 
from optics.models import Optics
from django.views.decorators.csrf import csrf_exempt
import re
from django.core.mail import send_mail

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        optic = Optics.objects.get(id=request.POST['optic_id'])
        result = re.match(r'[0-9]{10,10}', request.POST['phone'])
        if result:
            pass
        res = Optics_order.objects.create_order(optic, request.POST['phone'], request.POST['email'])
        response = HttpResponse('Запись успешно создана, номер - ' + str(res.id))
        send_mail(
            'Ирис',
            f'Ваша почта была указана в заказе на "{optic.name}"\nНомер вашего заказа - {res.id}',
            'iriy.online@gmail.com',
            [request.POST['email']],
            fail_silently=False,
        )
        return response
    optic = Optics.objects.get(id=request.GET.get("opticId"))
    return render(request, 'optics_order_create_view.html',
                  {'name': optic.name,
                   'picture': optic.picture,
                   'description': optic.description,
                   'price': optic.price,
                   'id': optic.id})
    
class OpticsOrderDetailView(DetailView):
    model = Optics_order
    template_name = 'optics_order_detail_view.html'

## orders_on_optic/models.py

from django.db import models
from optics.models import Optics

def validate_phone_number(value):
    return

    
class Optics_order_Manager(models.Manager):
    def create_order(self, optic, phone, email):
        order = self.create(optic=optic, phone=phone, email=email, current_price=optic.price)
        
        return order
        
class Optics_order(models.Model):
    
    optic = models.ForeignKey(Optics, models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, validators=[validate_phone_number])
    email = models.EmailField(max_length=254)
    current_price = models.IntegerField()
    is_processed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    objects = Optics_order_Manager()

    def __str__(self) -> str:
        return self.phone

## ## orders_on_optic/urls.py

from django.urls import path
from .views import create_order, OpticsOrderDetailView

urlpatterns = [
    path('optics/createOrder', create_order),
    path('optics/order/<int:pk>/', OpticsOrderDetailView.as_view(), name='optics_order_detail'),
]

## orders_on_optic/templates/optics_order_create_view.html

{% extends "base.html" %}
{% load static %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
{% block content %}
<script>
  function sendOrder() {
    var xhr = new XMLHttpRequest();
    var body = 'phone=' + encodeURIComponent(document.getElementById('phone').value) + '&email=' + encodeURIComponent(document.getElementById('email').value) + '&optic_id=' + encodeURIComponent(document.getElementsByClassName('optic_id')['0'].id);
    xhr.open("POST", 'createOrder');

    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 
    
    xhr.send(body);
    xhr.onload = function() {
      if (xhr.status != 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
        console.log(xhr)
        alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
      } else {
        alert(xhr.response); // response -- это ответ сервера
        location.href = '/optics/' + document.getElementsByClassName('optic_id')['0'].id
      }
    };
    return true
  }
</script>
<div style="margin: 5vw; border-radius: 15px; background-color: #fffbed; padding: 2vw">
  <h1 id={{ id }} class="optic_id">{{ name }}</h1>
  <div style="display: flex">
    <img style="max-width: 45vw; max-height: 40vh" src="{{ picture.url }}" alt="{{ object.name }}">
    <span style="max-width: 45vw; margin-left: 2vw; font-size: 1.5rem">{{ description}}</span>
  </div>
  <p>Цена: {{ price }} ₽</p>
    <div class="form-group" style="max-width: 20vw">
      <label for="exampleInputEmail1">Телефон</label>
      <input id="phone" type="phone" class="form-control" aria-describedby="emailHelp" placeholder="Введите телефон для связи">
    </div>
    <div class="form-group" style="max-width: 25vw">
      <label for="exampleInputPassword1">Почтовый адрес</label>
      <input id="email" type="email" class="form-control" placeholder="example@example.com">
    </div>
    <br>
    <button onclick="sendOrder()" class="btn btn-primary">
      Сделать заказ
    </button>
  </div>
{% endblock %}

## orders_on_optic/templates/optics_order_detail_view.html

{% extends "base.html" %}
{% load static %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
{% block content %}
  <p style="font-size: 4rem; margin: 1vw 0 1vw 3vw">Статус заказа</p>
  <div style="margin: 3vw; border-radius: 15px; background-color: #fffbed; padding: 2vw">
    <style>
      .order_status li {
        font-size: 1.5rem
      }
    </style>
    <ul class='order_status'>
    {% if object.is_processed == False %}
    <li> Заказ ещё в обработке!</li>
    {% else %}
    <li> Заказ уже обработан!</li>
    {% if object.is_completed == False %}
      <li> Товар ещё не передан.</li>
      {% else %}
      <li> Заказ получен!</li>
      {% endif %}
    {% endif %}
    </ul>
    <div style="display: flex; align-items: center">
      <img style="max-width: 45vw" src="{{ object.optic.picture.url }}">
      <p style="font-size: 2rem; margin-left: 2vw;">Стоимость: {{ object.current_price }} ₽</p>
    </div>
</div>
{% endblock %}

## settings.py

"""
Django settings for diplomProject project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dakr9h+3=dcb-l=0vd+w_qmw$ik_)9o#q%vi@cxgm!glvnqlir'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DJANGO_ALLOW_ASYNC_UNSAFE=True

ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'iriy.online@gmail.com'
EMAIL_HOST_PASSWORD = 'dpiwmipxazwqzanh'
EMAIL_PORT = 587       
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CORS_ORIGIN_ALLOW_ALL = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'
STATICFILES_DIRS = ("static/admin/css", )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'optics.apps.OpticsConfig',
    'services.apps.ServicesConfig',
    'orders_on_optic.apps.OrdersOnOpticConfig',
    'orders_on_services.apps.OrdersOnServicesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'diplomProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'diplomProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'diplomdb',
        'PORT': 2023,
        'USER': 'postgres',
        'PASSWORD': 'postgres'
        # "OPTIONS": {
        #     "service": "~/.pg_service.conf",
        #     "passfile": ".my_pgpass",
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'