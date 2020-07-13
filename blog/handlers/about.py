from blog import BaseHandler


class AboutHandler(BaseHandler):
    """关于页面"""

    def get(self):
        return self.render("about.html")
