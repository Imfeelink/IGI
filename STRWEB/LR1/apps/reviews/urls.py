from django.urls import path, re_path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list_view, name='review_list'),
    path('create/', views.review_create_view, name='review_create'),
    re_path(r'^(?P<pk>\d+)/$', views.review_detail_view, name='review_detail'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.review_update_view, name='review_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.review_delete_view, name='review_delete'),
]
