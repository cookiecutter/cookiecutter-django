import Vue from "vue/dist/vue.js";
import storePlugin from "../../../../vue_frontend/src/store/vuex_store_as_plugin";
import createPersistedState from "vuex-persistedstate";
import FruitModule from "../store/module_fruit"
const Counter = () => import( /* webpackChunkName: "chunk-counter" */ "../components/Counter.vue");
const CounterBanner = () => import( /* webpackChunkName: "chunk-counter-banner" */ "../components/CounterBanner.vue");

Vue.config.productionTip = false

// Vuex state will be used in this entry point
Vue.use(storePlugin);

// Include Vuex modules as needed for this entry point
Vue.prototype.$store.registerModule('fruit', FruitModule);

// Designate what state should persist across page loads
createPersistedState({
        paths: [
            "fruit.count",
            "fruit.activeFruit",
        ]
    }
)(Vue.prototype.$store);

// Mount top level components
new Vue({
  el: "#app",
  components: {Counter}
});

new Vue({
  el: "#counter_banner",
  components: {CounterBanner}
});
