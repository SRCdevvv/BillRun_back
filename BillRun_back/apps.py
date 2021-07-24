#  from django.contrib.admin.apps import AdminConfig
from django.contrib.admin import apps
from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = 'api'

class MyAdminConfig(apps.AdminConfig):
    default_site = 'BillRun_back.admin.MyAdminSite'