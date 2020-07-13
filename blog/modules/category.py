import tornado.web

from blog.libs.database import db
from blog.models import Category


class CategoryModule(tornado.web.UIModule):
    """分类模版"""

    def render(self):
        categories = db.query(Category).all()
        if not categories:
            return ""
        else:
            return self.render_string(
                "modules/category.html",
                categories=categories
            )

    def css_files(self):
        return "css/modules/category.css"
