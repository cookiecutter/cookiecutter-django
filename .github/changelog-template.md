{%- for change_type, pulls in grouped_pulls.items() %}
{%- if pulls %}

### {{ change_type }}

{%- for pull_request in pulls %}

- {{ pull_request.title }} ([#{{ pull_request.number }}]({{ pull_request.html_url }}))
  {%- endfor -%}
  {% endif -%}
  {% endfor -%}
