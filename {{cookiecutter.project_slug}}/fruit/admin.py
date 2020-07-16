from django.contrib import admin
from fruit.models import Fruit


@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]
