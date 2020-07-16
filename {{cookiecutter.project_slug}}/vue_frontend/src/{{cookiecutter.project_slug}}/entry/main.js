import Vue from "vue/dist/vue.js";
const HelloWorld = () => import( /* webpackChunkName: "chunk-hello-world" */ "../components/HelloWorld.vue");

Vue.config.productionTip = false

// Mount top level components
new Vue({
  el: "#app",
  components: {HelloWorld}
});
