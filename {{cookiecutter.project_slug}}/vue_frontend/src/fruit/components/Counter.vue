<template>
    <div>
        <h1>{% raw %}{{ msg }}{% endraw %}</h1>
        <br/>

        <div class="adjustor d-inline-block">
            <counter-adjustor mode="dec"></counter-adjustor>
        </div>
        <div class="display d-inline-block">
            <counter-display></counter-display>
        </div>
        <div class="adjustor d-inline-block">
            <counter-adjustor mode="inc"></counter-adjustor>
        </div>

    </div>
</template>

<script>
    import CounterAdjustor from "../components/CounterAdjustor";
    import CounterDisplay from "../components/CounterDisplay";

    export default {
        name: 'Counter',
        components: {CounterAdjustor, CounterDisplay},
        props: {
            msg: String
        },
        computed: {},
        methods: {},
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
    {% if cookiecutter.custom_bootstrap_compilation == 'y' -%}
    /* We may import partials from our source to use variables, mixins, etc */
    @import '../../../../{{cookiecutter.project_slug}}/static/sass/custom_bootstrap_vars';
    
    {% endif -%}
    h1 {
        margin: 40px 0 0;
        {%- if cookiecutter.custom_bootstrap_compilation == 'y' %}
        color: $vue-green;
        {% else %}
        color: #42b883;
        {%- endif %}
    }
    
    .adjustor {
        height: 5rem;
        padding-left:2rem;
        padding-right:2rem;
        vertical-align: middle;
    }
</style>
