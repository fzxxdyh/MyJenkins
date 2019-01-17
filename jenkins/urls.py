"""MyJenkins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.jenkins_index, name='jenkins_index'),
    url(r'^project/new/', views.project_new, name='project_new'),
    url(r'^project/build/(\d+)/', views.project_build, name='project_build'),
    url(r'^project/delete/(\d+)/', views.project_delete, name='project_delete'),
    url(r'^project/modify/(\d+)/', views.project_modify, name='project_modify'),
    url(r'^project/(\d+)/', views.project_info, name='project_info'),
    url(r'^history/delete/(?P<projectname>\w+)/(?P<filename>\d+.\d+)/', views.history_del, name='history_del'),
    url(r'^history/', views.history, name='history'),
    # url(r'^history/(?P<projectname>\w+)/(?P<filename>\d+.\d+)/', views.history, name='history'),
    # url(r'^admin/(\w+)/(\w+)/(\d+)/change/', views.table_change, name='table_change'),
    # url(r'^admin/(\w+)/(\w+)/add/', views.table_add, name='table_add'),
    # url(r'^admin/(\w+)/(\w+)/', views.table_detail, name='table_detail'),
    # url(r'^admin/', views.admin, name='jenkins_admin'),

]
