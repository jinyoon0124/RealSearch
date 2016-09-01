"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Reit import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^home$', views.home, name='home'),
    url(r'^search_name$', views.search_name, name='search_name'),
    url(r'^search_name_info$', views.search_name_info, name='search_name_info'),
    url(r'^search_range$', views.search_range, name='search_range'),
    url(r'^search_range_matrix$', views.serach_range_matrix, name='search_range_matrix'),
    url(r'^search_range_detail$', views.search_range_detail, name='search_range_detail'),


]
