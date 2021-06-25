"""certik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
# from analysis.views import sentimental_analysis, word_cloud
from analysis.views import index, sa_process, wc_process

urlpatterns = [
    # path('', index, name='index'),
    path('sentimental_analysis/', sa_process),
    path('word_cloud/', wc_process),
    path('', index),
	# url(r'^sentimental_analysis/', sentimental_analysis),
    # url(r'^word_cloud/', word_cloud),
    # path('admin/', admin.site.urls),
]
