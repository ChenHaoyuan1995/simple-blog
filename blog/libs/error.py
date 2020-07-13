import tornado.web


class NotFoundHandler(tornado.web.ErrorHandler):
    def initialize(self, status_code):
        self.set_status(status_code)

    def write_error(self, status_code, **kwargs):
        self.render("error.html")
