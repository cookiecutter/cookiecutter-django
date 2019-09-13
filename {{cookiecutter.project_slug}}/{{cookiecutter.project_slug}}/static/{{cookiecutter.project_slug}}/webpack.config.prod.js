const path = require('path');
const dev_exports = require('./webpack.config.dev');

dev_exports['mode'] = 'production';
module.exports = dev_exports;
