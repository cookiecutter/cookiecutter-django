const { merge } = require('webpack-merge');
const devConfig = require('./common.config');

module.exports = merge(devConfig, {
  mode: 'production',
  devtool: 'source-map',
  bail: true,
})
