import Vue from "vue/dist/vue.js";
import Vuex from "vuex";

Vue.use(Vuex);

let store = new Vuex.Store({
    modules: {
    },
    strict: process.env.NODE_ENV !== "production",
});

export default {
    store,
    install(Vue) { //resetting the default store to use this plugin store
        Vue.prototype.$store = store;
    }
}