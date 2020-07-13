import tornado.web

from blog.libs.database import db
from blog.models import Tag


class TagModule(tornado.web.UIModule):
    """标签模版"""

    def render(self):
        tags = db.query(Tag).all()
        if not tags:
            return ""
        else:
            return self.render_string(
                "modules/tag.html",
                tags=tags
            )

    def css_files(self):
        return "css/modules/tag.css"
