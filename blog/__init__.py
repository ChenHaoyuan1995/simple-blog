import math

from tornado.web import RequestHandler

from blog.libs.setting import setting
from blog.libs.session import Session, RedisSession
from blog.libs.database import Base, db
from blog.models import User

PAGESIZE = int(setting["setting"]["pagesize"])


class BaseHandler(RequestHandler):

    def initialize(self):
        if "redis" not in setting.sections():
            self.session = Session(self)
        else:
            self.session = RedisSession(self)

    def prepare(self):
        self.db = db

    def on_finish(self):
        self.db.remove()

    def write_error(self, status_code: int, **kwargs):
        self.render("error.html")

    def ajax_ok(self, data=None, **args):
        info = {'status': 200, 'msg': data}
        info.update(args)
        return self.write(info)

    def ajax_redirect(self, url=None, data=None, **args):
        info = {'status': 300, 'msg': data, 'url': url}
        info.update(args)
        return self.write(info)

    def ajax_alert(self, data=None, **args):
        info = {'status': 400, 'msg': data}
        info.update(args)
        return self.write(info)

    @property
    def has_login(self):
        return True if self.session["id"] else False

    def current_user(self):
        if self.has_login:
            user = self.db.query(User).filter(User.id == self.session["id"]).first()
            if user:
                return user
        return None

    def pagination(self, name, model, conditions=None):
        """
        分页
        :param name: 返回的对象里的名字，用于模版渲染
        :param model: 用于分页的数据库模型
        :param conditions: 分页的条件，list类型
        :return: args: 返回渲染模版的键值对
        """
        current_page = self.get_argument("page", default="1")
        try:
            current_page = int(current_page)
        except (TypeError, ValueError):
            current_page = 1
        if current_page < 1: current_page = 1
        objects = self.db.query(model)
        if hasattr(model, "del_flag"):
            objects = objects.filter(model.del_flag == 0)
        if conditions:
            for i in conditions:
                objects = objects.filter(i)
        pages = objects.count()
        pages = math.ceil(pages / PAGESIZE)

        if hasattr(model, "create_time"):
            objects = objects.order_by(model.create_time.desc())

        objects = objects.limit(PAGESIZE).offset((current_page - 1) * PAGESIZE)

        args = {
            name: objects,
            "page": current_page,
            "pages": pages
        }
        return args
