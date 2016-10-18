# coding=utf-8
from django.conf.urls import url
from book import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^list/$', views.book_list, name="list"),
    url(r'^addbook/$', views.add_book, name="add"),
    url(r'^addauthor/', views.add_author, name="addauthor"),
    url(r'^book/(?P<pk>\w+)/detail/$', views.detail, name="detail"),
    url(r'^book/(?P<pk>\w+)/delete/$', views.delete, name="delete"),
]