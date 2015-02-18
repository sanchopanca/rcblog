import tornado.web


class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, World!')


class MongoTestHandler(tornado.web.RequestHandler):

    def get(self):
        pass 

handler_map = [
    (r'/', HelloHandler)
]