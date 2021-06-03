from django.contrib import admin
from admin_view_permission.admin import AdminViewPermissionAdminSite
from .forms import CustomAuthenticationForm

class MyAdminSite(admin.AdminSite):
# class MyAdminSite(AdminViewPermissionAdminSite):
    site_header = 'BillRun Admin'
    login_form = CustomAuthenticationForm
    login_template = 'api/login.html'

admin_site = MyAdminSite()
