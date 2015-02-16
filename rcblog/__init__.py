import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options, parse_command_line
import tornado.web
import tornado.httpclient

from rcblog.handlers import handler_map


def main():
    define('port', default=8080, help='run on given port', type=int)
    parse_command_line()
    app = tornado.web.Application(handler_map)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()