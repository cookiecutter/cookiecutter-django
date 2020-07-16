const BundleTracker = require("webpack-bundle-tracker");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;


const pages = {
    'main': {
        entry: './src/{{cookiecutter.project_slug}}/entry/main.js',
        chunks: ['chunk-common']
    },
    {%- if cookiecutter.use_fruit_demo == 'y' %}
    'fruit-counter': {
        entry: './src/fruit/entry/fruit_counter.js',
        chunks: ['chunk-common', 'chunk-state']
    },
    {%- endif %}{%- if cookiecutter.use_fruit_demo == 'y' and cookiecutter.use_drf == 'y' %}
    'fruit-list': {
        entry: './src/fruit/entry/fruit_list.js',
        chunks: ['chunk-common', 'chunk-state']
    },
    {%- endif %}
}

module.exports = {
    pages: pages,
    filenameHashing: true,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === 'production'
        ? '/static/vue'
        : 'http://localhost:8080/',
    outputDir: '../{{cookiecutter.project_slug}}/static/vue/',

    chainWebpack: config => {

        config.optimization
            .splitChunks({
                cacheGroups: {
                    state: {
                        /* As vuex state is not needed in all our entry points, we isolate it
                         * in a separate chunk to be loaded only where needed. 
                         */
                        test: /[\\/]node_modules[\\/](vuex|vuex-persisted-state)/,
                        name: "chunk-state",
                        chunks: "all",
                        priority: 5
                    },
                    vendor: {
                        /* This chunk contains modules that may be used in all entry points,
                         * including Vue itself 
                         */
                        test: /[\\/]node_modules[\\/]/,
                        name: "chunk-common",
                        chunks: "all",
                        priority: 1
                    },
                },
            });

        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        })

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{
                path: '../vue_frontend/',
                filename: 'webpack-stats.json'
            }]);

        // Uncomment below to analyze bundle sizes
        // config.plugin("BundleAnalyzerPlugin").use(BundleAnalyzerPlugin);

        // config.resolve.alias
        // .set('__STATIC__', 'static')

        config.devServer
            .public('http://localhost:8080')
            .host('localhost')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})

    }
};   
    
