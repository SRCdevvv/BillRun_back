from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ApiConfig(AppConfig):
    name = 'api'

class MyAdminConfig(AdminConfig):
    default_site = 'BillRun_back.api.MyAdminSite'