from django.urls import path
from django.views.generic import TemplateView
{%- if cookiecutter.use_drf == "y" %}
from fruit.views import FruitList
{%- endif %}

app_name = "fruit"

urlpatterns = [
    {%- if cookiecutter.use_drf == "y" %}
    path(
        "fruits/",
        FruitList.as_view(extra_context={"title": "Fruit Inspector"}),
        name="list",
    ),
    {% endif -%}
    path(
        "fruit-counter/",
        TemplateView.as_view(
            template_name="fruit/counter.html",
            extra_context={"counter_message": "How many fruits could you eat?"},
        ),
        name="counter",
    ),
]
