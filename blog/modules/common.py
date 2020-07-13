import tornado.web

from blog import setting
from blog.libs.database import db
from blog.models import Post

recent_post = setting["setting"]["recent_post"]


class RowDistanceModule(tornado.web.UIModule):
    """空一格"""

    def render(self, style, percent):
        return '<div class="clearfix" style="{}: {}%;"></div>'.format(style, percent)


class RecentPostModule(tornado.web.UIModule):
    """最新发布"""

    def render(self):
        posts = db.query(Post).order_by(Post.create_time.desc()).limit(recent_post)
        html = ""
        for i in posts:
            html += "<li><a href="">{}</a></li>".format(i.title)
        return html
