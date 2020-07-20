import Vue from "vue/dist/vue.js";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

let store = new Vuex.Store({
    modules: {},
    strict: process.env.NODE_ENV !== "production",
});

function registerModule(moduleName, module) {
    Vue.prototype.$store.registerModule(moduleName, module);
}

function persistState(persistentPaths) {
    createPersistedState({paths: persistentPaths})(Vue.prototype.$store)
}

export const VuexAsPlugin = {
    store,
    install(Vue) { //resetting the default store to use this plugin store
        Vue.prototype.$store = store;
    }
}

export function registerModules(modulesDef) {
    let persisted = [];
    for (let [mName, mDef] of Object.entries(modulesDef)) {
        if ('module' in mDef) {
            registerModule(mName, mDef['module']);
        }
        if ('persistedPaths' in mDef) {
            persisted = persisted.concat(mDef['persistedPaths'].map(p => mName + "." + p))
        }
    }
    persistState(persisted);
}
