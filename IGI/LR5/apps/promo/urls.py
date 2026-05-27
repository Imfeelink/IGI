from django.urls import path

from . import views

app_name = 'promo'

urlpatterns = [
    path('', views.promo_list_view, name='promo_list'),
]
