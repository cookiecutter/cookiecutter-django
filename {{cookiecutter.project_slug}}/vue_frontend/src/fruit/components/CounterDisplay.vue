<template>
  <div>
    <!-- Because our project css is loaded from our Django base template, we may use those inherited styles -->
    <div id="display" class="display-4 rounded-circle">{% raw %}{{ count }}{% endraw %}</div>
    
  </div>
</template>

<script>
export default {
  name: 'CounterDisplay',
  props: {
    msg: String
  },
  computed: {
    count() { return this.$store.state.fruit.count }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  {% if cookiecutter.custom_bootstrap_compilation == 'y' -%}
  /* We may import partials from our source to use variables, mixins, etc */
  @import '../../../../{{cookiecutter.project_slug}}/static/sass/custom_bootstrap_vars';

  {% endif -%}
  #display {
    {%- if cookiecutter.custom_bootstrap_compilation == 'y' %}
    background-color: $vue-green;
    {% else %}
    background-color: #42b883;
    {%- endif %}
    color: white;
    font-size: 4rem;
    font-weight: bold;
    line-height: 6rem;
    height: 6rem;
    width: 6rem;
    text-align: center;
    vertical-align: baseline;
}
</style>
