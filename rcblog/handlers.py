import tornado.web


class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, World!')


handler_map = [
    (r'/', HelloHandler)
]