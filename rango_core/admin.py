from django.contrib import admin

from . import models


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Category, CategoryAdmin)
