/* eslint-env node */
const webpackConfig = require('./webpack.config.js');


module.exports = function (config) {
  config.set({
    basePath: './static/app',
    frameworks: ['mocha', 'sinon'],
    browsers: ['PhantomJS'],

    reporters: ['progress', 'mocha'],

    logLevel: config.LOG_INFO,

    port: 9876,
    autoWatch: true,
    singleRun: false,
    colors: true,


    files: [
      '../../node_modules/mock-socket/dist/mock-socket.min.js',
      '../../node_modules/babel-core/browser-polyfill.js',
      './**/tests/test*.js'
    ],

    preprocessors: {
      './**/tests/test*.js': ['webpack', 'sourcemap']
    },

    webpack: webpackConfig,

    webpackMiddleware: {
      noInfo: true
    },

    plugins: [
      'karma-mocha',
      'karma-sinon',
      'karma-webpack',
      'karma-mocha-reporter',
      'karma-chrome-launcher',
      'karma-phantomjs-launcher',
      'karma-sourcemap-loader'
    ],
  });
};
