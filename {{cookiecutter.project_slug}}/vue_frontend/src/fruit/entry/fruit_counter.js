import Vue from "vue/dist/vue.js";
import {VuexAsPlugin, registerModules} from "../../store/vuex_usage_utils";
import FruitModule from "../store/module_fruit"
const Counter = () => import( /* webpackChunkName: "chunk-counter" */ "../components/Counter.vue");
const CounterBanner = () => import( /* webpackChunkName: "chunk-counter-banner" */ "../components/CounterBanner.vue");

Vue.config.productionTip = false

// Vuex state will be used in this entry point
Vue.use(VuexAsPlugin);

registerModules( {
    'fruit' : {
        module: FruitModule,
        persistedPaths: ['count', 'activeFruit']
    },
})

// Mount top level components
new Vue({
    el: "#app",
    components: {Counter}
});

new Vue({
    el: "#counter_banner",
    components: {CounterBanner}
});
