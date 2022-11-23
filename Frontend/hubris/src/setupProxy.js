const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/',
    createProxyMiddleware({
      target: 'http://192.168.0.18:80/',
    }),
  );
  app.listen(3000)
};