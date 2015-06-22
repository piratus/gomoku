# coding: utf-8
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):

    def get(self):
        self.render('index.html', debug=self.settings['debug'])
