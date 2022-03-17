const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

module.exports = merge(commonConfig, {
  mode: 'production',
  devtool: 'source-map',
  bail: true,
})
