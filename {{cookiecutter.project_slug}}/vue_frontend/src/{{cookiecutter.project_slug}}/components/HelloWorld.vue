<template>

  <div id="app" class="text-center">
    <img class="logo" alt="Vue logo" src="../assets/logo.png">
    <span class="plus">+</span>
    <img class="logo" alt="Django logo" :src="`${staticRoot}/images/django_logo.png`">
    <div class="hello">
      <h1>{% raw %}{{ msg }}{% endraw %}</h1>
      <p>
        This cookiecutter implements the techniques discussed in the series of articles "Vue + Django: The Best of Both Frontends."
      </p>
      <ul class="articles">
        <li><a href="https://medium.com/js-dojo/vue-django-best-of-both-frontends-701307871478" target="_blank" rel="noopener">Part 1: Basics</a></li>
        <li><a href="https://medium.com/js-dojo/django-vue-vuex-best-of-both-frontends-part-2-1dcb78215575" target="_blank" rel="noopener">Part 2: Persistent State</a></li>
        <li><a href="https://medium.com/js-dojo/django-vue-blazing-content-rich-interactivity-b34e45d8c602" target="_blank" rel="noopener">Part 3: Deferred Loading</a></li>
      </ul>

      <p>
        In addition to the base options provided by the wonderful <a href="https://github.com/pydanny/cookiecutter-django">Cookiecutter Django</a>, this cookiecutter providees the following options:
      </p>
      <div class="container col-md-8 text-left">
        <ul class="options">

          <li>
            <span class="opt">use_vue</span> -- <span class="expl">provides Vue integration using <a href="https://github.com/owais/django-webpack-loader">django-webpack-loader</a>, featuring:</span>
            <ul>
              <li>Harmonious coexistence of Django templates and Vue components</li>
              <li>Vue Single File Components (SFCs)</li>
              <li>Multi-page App (MPA) layout</li>
              <li>Vue Loader Hot Reload</li>
              <li>Property passing from Django -> Vue</li>
              <li>Sass/SCSS pre-compilation</li>
              <li>Vue DevTools support</li>
              <li>Chunked resource loading</li>
              <li>Deferred loading of Vue and/or Vue components</li>
            </ul>
          </li>

          <li>
            <span class="opt">use_vuex</span> -- <span class="expl">provides <a href="https://vuex.vuejs.org/">Vuex</a> integration, featuring:</span>
            <ul>
              <li>Shared state across components on the same page</li>
              <li>Persistent state across pages</li>
              <li>Rest support via <a href="https://github.com/axios/axios">Axios</a> -> <a href="https://www.django-rest-framework.org/">DRF</a> (if <i>use_drf</i> enabled)</li>
            </ul>
          </li>
          <li>
            <span class="opt">use_fruit_demo</span> -- <span class="expl">provides a sample app, demonstrating:</span>
            <ul>
              <li>All basic features from selected options above</li>
              <li>Deferred loading </li>
              <li>Static asset loading from Django or Vue</li>
              <li>If <i>use_drf</i> enabled, a sample API integration</li>
              <li>If <i>custom_bootstrap_compilation</i> enabled, SCSS partials import in SFCs</li>
              <li>Useless information about fruit</li>
            </ul>
          </li>
        </ul>
      </div>


    </div>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    props: {
      msg: String
    },
    data () {
      return {
        staticRoot: process.env.VUE_APP_STATIC_ROOT
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  h1 {
    margin: 40px 0 0;
    font-style: italic;
  }
  h3 {
    margin: 40px 0 0;
  }
  ul.articles {
    list-style-type: none;
    padding: 0;
    li {
      display: inline-block;
      margin: 0 10px;
    }
  }
  .opt {
    font-weight: bold;
  }
  p {
    margin-top: 1.5em;
    margin-bottom: .5em;
  }
  a {
    color: #42b983;
  }
  .logo {
    height: 150px;
    margin-top: 25px;
  }
  .plus {
    font-size: 44px;
    padding-left: 10px;
    padding-right: 20px;
  }
</style>
