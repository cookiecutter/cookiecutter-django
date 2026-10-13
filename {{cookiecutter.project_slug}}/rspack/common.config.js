const path = require('path');
const rspack = require('@rspack/core');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  target: 'web',
  context: path.join(__dirname, '../'),
  entry: {
    project: path.resolve(__dirname, '../{{cookiecutter.project_slug}}/static/js/project'),
    vendors: path.resolve(__dirname, '../{{cookiecutter.project_slug}}/static/js/vendors'),
  },
  output: {
    path: path.resolve(
      __dirname,
      '../{{cookiecutter.project_slug}}/static/webpack_bundles/',
    ),
    publicPath: '/static/webpack_bundles/',
    filename: 'js/[name]-[fullhash].js',
    chunkFilename: 'js/[name]-[hash].js',
    clean: false,
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(path.join(__dirname, '../')),
      filename: 'webpack-stats.json',
    }),
    new rspack.CssExtractRspackPlugin({
      filename: 'css/[name].[contenthash].css',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'builtin:swc-loader',
        options: {
          jsc: {
            parser: {
              syntax: 'ecmascript',
            },
            target: 'es2015',
          },
        },
      },
      {
        test: /\.s?css$/i,
        use: [
          rspack.CssExtractRspackPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['postcss-preset-env', 'autoprefixer', 'pixrem'],
              },
            },
          },
          'sass-loader',
        ],
        type: 'javascript/auto',
      },
    ],
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx'],
  },
};
