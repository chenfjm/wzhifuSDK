import os
import tornado.ioloop
import tornado.web
import pay


settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

class MainHandler(tornado.web.RequestHandler):

    application = tornado.web.Application(pay.URLS, **settings)

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
