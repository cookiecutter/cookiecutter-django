from django.views.generic import ListView
from fruit.models import Fruit


class FruitList(ListView):
    model = Fruit
