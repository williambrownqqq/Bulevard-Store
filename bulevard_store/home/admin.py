from django.contrib import admin

from .models import Item, Category, Image

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Image)
