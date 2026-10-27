from django.urls import path, re_path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/create/', views.news_create_view, name='news_create'),
    re_path(r'^news/(?P<pk>\d+)/$', views.news_detail_view, name='news_detail'),
    re_path(r'^news/(?P<pk>\d+)/edit/$', views.news_update_view, name='news_update'),
    re_path(r'^news/(?P<pk>\d+)/delete/$', views.news_delete_view, name='news_delete'),
    path('faq/', views.faq_list_view, name='faq_list'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('vacancies/', views.vacancy_list_view, name='vacancy_list'),
    path('vacancies/create/', views.vacancy_create_view, name='vacancy_create'),
    re_path(r'^vacancies/(?P<pk>\d+)/$', views.vacancy_detail_view, name='vacancy_detail'),
    re_path(r'^vacancies/(?P<pk>\d+)/edit/$', views.vacancy_update_view, name='vacancy_update'),
    re_path(r'^vacancies/(?P<pk>\d+)/delete/$', views.vacancy_delete_view, name='vacancy_delete'),
    path('calendar/', views.calendar_view, name='calendar'),
]
