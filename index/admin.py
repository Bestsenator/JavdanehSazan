from django.contrib import admin
from index.models import *
from django.contrib.auth import models  # for delete user and group admin panel

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Family', 'Phone']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'ArbName', 'PerName']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'ArbName', 'PerName']


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Family', 'Expertise']


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Developers, DeveloperAdmin)
admin.site.register(APIKEY)
admin.site.unregister(models.User)
admin.site.unregister(models.Group)

