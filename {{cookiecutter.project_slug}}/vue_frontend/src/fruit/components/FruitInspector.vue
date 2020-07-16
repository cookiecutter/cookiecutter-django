<template>
    <div class="card bg-light mb-3">

        <div class="card-header"><h3>{% raw %}{{ title }}{% endraw %}</h3></div>
        <div class="card-body">

            <form>
                <div class="form-group row">
                    <label for="fruitChoice" class="col-sm-3 col-form-label font-weight-bold">Fruit</label>
                    <div class="col-sm-9">
                        <select id="fruitChoice"
                                class="form-control"
                                @change="setActiveFruit"
                                :value="activeFruit ? activeFruit.id: -1"
                        >
                            <option v-if="activeFruit == null" :value="-1">Select a fruit</option>
                            <option
                                    v-for="f in fruits"
                                    :key="f.id"
                                    :selected="activeFruit != null ? f.id === activeFruit.id: false"
                                    :value="f.id"
                            >
                                {% raw %}{{ f.name }}{% endraw %}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="form-group row" v-if="activeFruit">
                    <label for="fruitDescription" class="col-sm-3 col-form-label font-weight-bold">Description</label>
                    <div class="col-sm-9">
                        <input type="text" readonly class="form-control-plaintext" id="fruitDescription"
                               :value="activeFruit.description"
                        >
                    </div>
                </div>
                <div class="form-group row" v-if="activeFruit">
                    <label for="fruitDetail" class="col-sm-3 col-form-label font-weight-bold">Detail</label>
                    <div class="col-sm-9">
                        <textarea type="text" readonly class="form-control-plaintext"
                                  rows=8
                                  id="fruitDetail"
                                  :value="activeFruit.detail"
                        ></textarea>
                    </div>
                </div>
                <div class="form-group row" v-if="activeFruit">
                    <label for="fruitLink" class="col-sm-3 col-form-label font-weight-bold">Detail Source Link</label>
                    <div class="col-sm-9">
                        <a id="fruitLink" :href="activeFruit.detail_link"
                           target="_blank">{% raw %}{{ activeFruit.detail_link }}{% endraw %}</a>
                    </div>
                </div>

            </form>
        </div>
    </div>
</template>

<script>

    import {ACTION_GET_FRUITS, ACTION_SET_ACTIVE_FRUIT} from "../store/module_fruit";

    export default {
        name: 'FruitInspector',
        components: {},
        mounted() {
            this.$store.dispatch(ACTION_GET_FRUITS);

        },
        props: {
            title: String,
        },
        computed: {
            fruits() {
                return this.$store.state.fruit.fruits
            },
            activeFruit() {
                // TODO: should check if active fruit is in list of fruits
                return this.$store.state.fruit.activeFruit
            },

        },
        methods: {
            setActiveFruit(e) {
                this.$store.dispatch(ACTION_SET_ACTIVE_FRUIT, e.target.value);
            }

        },
    }
</script>

<style scoped lang="scss">
    {% if cookiecutter.custom_bootstrap_compilation == 'y' -%}
    /* We may import partials from our source to use variables, mixins, etc */
    @import '../../../../{{cookiecutter.project_slug}}/static/sass/custom_bootstrap_vars';

    {% endif -%}
    .card-header {
        {%- if cookiecutter.custom_bootstrap_compilation == 'y' %}
        background-color: $vue-green;
        {% else %}
        background-color: #42b883;
        {%- endif %}
        color: white;
    }
</style>
