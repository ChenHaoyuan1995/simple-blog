from blog import BaseHandler


class IndexHandler(BaseHandler):
    """博客主页"""

    def get(self):
        return self.render("index.html")
