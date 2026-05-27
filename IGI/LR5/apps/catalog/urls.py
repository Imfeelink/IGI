from django.urls import path, re_path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('properties/', views.property_list_view, name='property_list'),
    path('properties/create/', views.property_create_view, name='property_create'),
    re_path(r'^properties/(?P<pk>\d+)/$', views.property_detail_view, name='property_detail'),
    re_path(r'^properties/(?P<pk>\d+)/edit/$', views.property_update_view, name='property_update'),
    re_path(r'^properties/(?P<pk>\d+)/delete/$', views.property_delete_view, name='property_delete'),
    path('owners/', views.owner_list_view, name='owner_list'),
    path('owners/create/', views.owner_create_view, name='owner_create'),
    re_path(r'^owners/(?P<pk>\d+)/edit/$', views.owner_update_view, name='owner_update'),
    re_path(r'^owners/(?P<pk>\d+)/delete/$', views.owner_delete_view, name='owner_delete'),
    path('sales/', views.sale_list_view, name='sale_list'),
    path('sales/create/', views.sale_create_view, name='sale_create'),
    re_path(r'^sales/(?P<pk>\d{1,8})/edit/$', views.sale_update_view, name='sale_update'),
    re_path(r'^sales/(?P<pk>\d{1,8})/delete/$', views.sale_delete_view, name='sale_delete'),
    path('purchase/', views.purchase_create_view, name='purchase_create'),
]
