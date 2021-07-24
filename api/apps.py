from django.apps import AppConfig
# from django.contrib.admin.apps import AdminConfig
from django.contrib.admin import apps


class ApiConfig(AppConfig):
    name = 'api'

class MyAdminConfig(apps.AdminConfig):
    default_site = 'BillRun_back.api.MyAdminSite'