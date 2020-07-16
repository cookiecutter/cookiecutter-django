import Vue from "vue/dist/vue.js";
import storePlugin from "../../store/vuex_store_as_plugin";
import createPersistedState from "vuex-persistedstate";
import FruitModule from "../store/module_fruit"
const FruitInspector = () => import( /* webpackChunkName: "chunk-fruit-inspector" */ "../components/FruitInspector.vue");

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
  components: {FruitInspector}
});

