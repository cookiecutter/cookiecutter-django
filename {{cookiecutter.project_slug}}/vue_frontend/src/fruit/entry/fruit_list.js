import Vue from "vue/dist/vue.js";
import {VuexAsPlugin, registerModules} from "../../store/vuex_usage_utils";
import FruitModule from "../store/module_fruit"
const FruitInspector = () => import( /* webpackChunkName: "chunk-fruit-inspector" */ "../components/FruitInspector.vue");

Vue.config.productionTip = false

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
    components: {FruitInspector}
});

