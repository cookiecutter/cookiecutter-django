const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

module.exports = merge(commonConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    port: 3000,
    proxy: [
      {
        context: ['/'],
        {%- if cookiecutter.use_docker == 'n' %}
        target: 'http://0.0.0.0:8000',
        {%- else %}
        target: 'http://django:8000',
        {%- endif %}
      },
    ],
    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: true,
      },
    },
    // We need hot=false (Disable HMR) to set liveReload=true
    hot: false,
    liveReload: true,
  },
});
