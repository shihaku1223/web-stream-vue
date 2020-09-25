const webpack = require('webpack');
const path = require('path');
const express = require('express');
const middleware = require('webpack-dev-middleware');
const hotMiddleware = require('webpack-hot-middleware');

const configPromise = require('./webpack.dev.conf.js');

configPromise.then((config) => {

const app = express();
const compiler = webpack(config);

app.use(middleware(compiler, {
    noInfo: false,
    publicPath: config.output.publicPath,
    stats: { colors: true }
}));


app.use(hotMiddleware(compiler));


const staticPath = path.posix.join('/', 'static')
app.use(staticPath, express.static('./static'))

const port = config.devServer.port
module.exports = app.listen(port, function (err) {
  if (err) {
    console.log(err)
    return
  }
  console.log('Listening at http://localhost:' + port + '\n')
})

})
