/*eslint-env node */
const path = require('path');
const webpack = require('webpack');
const WebpackNotifierPlugin = require('webpack-notifier');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const STATIC_DIR = path.resolve(__dirname, './static/');
const DIST_DIR = path.resolve(__dirname, './dist/');
const APP_ROOT = path.resolve(STATIC_DIR, 'app');

const DEBUG = process.env.NODE_ENV !== 'production';
const HOT = DEBUG && process.argv.indexOf('--hot') !== -1;


const loaders = {
  js: (HOT ? 'react-hot!' : '') + 'babel?cacheDirectory',
  scss: DEBUG ? 'style!css!autoprefixer!sass' :
    ExtractTextPlugin.extract('style', 'css!autoprefixer!sass'),
  files: 'url?limit=10000',
};


const plugins = {
  core: [
    new WebpackNotifierPlugin({name: 'Gomoku', alwaysNotify: true}),
    new webpack.DefinePlugin({
      DEBUG: JSON.stringify(DEBUG),
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
    })
  ],
  debug: HOT ? [
    new webpack.NoErrorsPlugin()
  ] : [
  ],
  prod: [
    new ExtractTextPlugin('app.css', {allChunks: true}),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.OccurenceOrderPlugin(true),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: false,
      compress: {
        warnings: false
      }
    })
  ]
};


const entries = !HOT ? [] : [
  'webpack-dev-server/client?http://localhost:7777',
  'webpack/hot/only-dev-server'
];


module.exports = {
  entry: entries.concat([path.join(APP_ROOT, 'main.js')]),

  output: {
    filename: 'app.bundle.js',
    path: DIST_DIR,
    publicPath: (HOT ? 'http://localhost:7777' : '') + '/static/',
  },

  resolve: {
    root: APP_ROOT
  },

  plugins: plugins.core.concat(DEBUG ? plugins.debug : plugins.prod),

  module: {
    preLoaders: DEBUG ? [] : [
      {
        test: /\.js$/,
        loader: 'eslint',
        include: APP_ROOT
      }
    ],
    loaders: [
      {
        test: /\.js$/,
        loader: loaders.js,
        include: APP_ROOT
      },
      {
        test: /\.scss$/,
        loader: loaders.scss
      },
      {
        test: /\.woff$|\.png$/,
        loader: loaders.files,
      }
    ]
  },

  devtool: DEBUG ? '#inline-source-map' : '',
  debug: DEBUG,

  devServer: {
    contentBase: DIST_DIR,
    port: 7777,
    hot: true,
    inline: true,
    noInfo: true,
  },

  stats: {
    colors: true,
    modules: true,
    reasons: true,
  },

  progress: true,
};
