from django.contrib import admin
from django.contrib import admin
from django import forms
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django.urls import path
from .models import *
from django.contrib.auth.models import Permission, Group


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]
    list_filter = ["id"]

class UserAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]
    list_filter = ["id"]

class TodayNewsAdminSite(admin.AdminSite):
    site_header = 'TodayNews'
    index_title = 'Trang web quản trị today news'


admin_site = TodayNewsAdminSite('todaynews')
admin_site.register(Article,ArticleAdmin)
admin_site.register(User,UserAdmin)
