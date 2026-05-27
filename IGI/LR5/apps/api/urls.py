from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.external_data_view, name='external_data'),
]
