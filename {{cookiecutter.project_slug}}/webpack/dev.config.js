const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

module.exports = merge(commonConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    port: 3000,
    proxy: {
      {%- if cookiecutter.use_docker == 'n' %}
      '/': 'http://0.0.0.0:8000',
      {%- else %}
      '/': 'http://django:8000',
      {%- endif %}
    },
    // We need hot=false (Disable HMR) to set liveReload=true
    hot: false,
    liveReload: true,
  },
});
