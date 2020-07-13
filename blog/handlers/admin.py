from blog import BaseHandler
from blog.libs.user_verification import login_required
from blog.models import User, Post, Tag, Category
import hashlib

Classify = {
    "category": Category,
    "tag": Tag
}


class AdminLoginHandler(BaseHandler):
    """后台管理员登录"""

    def get(self):
        if self.has_login:
            return self.redirect(self.reverse_url("admin"))
        return self.render("admin/login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return self.ajax_alert(data="用户不存在", error="username")
        if hashlib.md5((username + password).encode('utf-8')).hexdigest() != user.password:
            return self.ajax_alert(data="密码错误", error="password")
        self.session["id"] = user.id
        return self.ajax_redirect(data="登录成功", url=self.reverse_url("admin"))


class AdminRegisterHandler(BaseHandler):
    """后台管理员注册"""

    def get(self):
        return self.render("admin/register.html")

    def post(self):
        username = self.get_argument("username")
        nickname = self.get_argument("nickname")
        password = self.get_argument("password")
        password = hashlib.md5((username + password).encode('utf-8')).hexdigest()
        if self.db.query(User).filter(User.username == username).count():
            return self.ajax_alert(data="用户名已存在")
        try:
            user = User(username=username, nickname=nickname, password=password)
            self.db.add(user)
            self.db.commit()
        except:
            return self.ajax_alert(data="注册出错")
        self.session["id"] = user.id
        return self.ajax_redirect(data="注册成功", url=self.reverse_url("admin"))


class AdminLogoutHandler(BaseHandler):
    """后台管理员登出"""

    def post(self):
        if self.has_login:
            del self.session["id"]
        return self.ajax_redirect(data="已登出", url=self.reverse_url("admin"))


class AdminHandler(BaseHandler):
    """后台主页面"""

    @staticmethod
    def handle_none(i):
        """把None字段替换为-，把标签用分号分隔"""
        if not i:
            return "-"
        elif isinstance(i, list):
            names = (tag.name for tag in i if tag.name)
            return ";".join(names)
        else:
            return i

    @login_required
    def get(self):
        user = self.current_user()
        args = self.pagination("posts", Post)
        args["user"] = user
        args["handle_none"] = self.handle_none

        return self.render("admin/admin.html", **args)


class AdminEditHandler(BaseHandler):
    """文章管理(新增，编辑，删除)"""

    @login_required
    def get(self, pk=None):
        post = self.db.query(Post).filter(Post.author_id == self.session["id"],
                                          Post.id == int(pk)).first() if pk else None
        tags = post.tags if post else []
        category = post.category if post else None
        all_tags = self.db.query(Tag).all()
        all_categories = self.db.query(Category).all()

        args = {
            "pk": pk,
            "post": post,
            "tags": tags,
            "category": category,
            "all_tags": all_tags,
            "all_categories": all_categories
        }
        return self.render("admin/edit.html", **args)

    @login_required
    def post(self, pk=None):
        content = self.get_argument("content")
        title = self.get_argument("title")
        category = self.get_argument("category", None)
        tag = self.get_arguments("tag")
        new_category = self.get_argument("new-category")
        new_tag = self.get_argument("new-tag")

        if new_category:
            if self.db.query(Category).filter(Category.name == new_category, Category == 0).count():
                return self.ajax_alert("分类名已经存在")
            else:
                c = Category(name=new_category)
                self.db.add(c)
                self.db.flush()
                category = c.id

        if new_tag:
            all_new_tag = new_tag.split()
            if len(all_new_tag) != len(set(all_new_tag)) or self.db.query(Tag).filter(
                    Tag.name.in_(all_new_tag)).count():
                return self.ajax_alert("标签名有重复")
            else:
                tag_list = [
                    Tag(name=i) for i in all_new_tag
                ]
                self.db.add_all(tag_list)
                self.db.flush()
                tag.extend([i.id for i in tag_list])

        tag = list(map(int, tag))
        tags = self.db.query(Tag).filter(Tag.id.in_(tag)).all()

        if pk:
            post = self.db.query(Post).filter(Post.author_id == self.session["id"],
                                              Post.id == int(pk)).first() if pk else None
            if post:
                post.title = title
                post.content = content
                post.category_id = category
                post.tags = tags
                self.db.add(post)
                self.db.commit()
                return self.ajax_redirect(url=self.reverse_url("admin"))
            else:
                return self.ajax_alert("这篇文章不存在")
        else:
            post = Post(
                title=title,
                content=content,
                author_id=self.session["id"],
                del_flag=False
            )
            post.category_id = category
            post.tags = tags
            self.db.add(post)
            self.db.commit()
            return self.ajax_redirect(url=self.reverse_url("admin"))

    @login_required
    def delete(self, pk):
        if pk:
            post = self.db.query(Post).filter(Post.author_id == self.session["id"],
                                              Post.id == int(pk)).first() if pk else None
            if post:
                post.del_flag = 1
                self.db.add(post)
                self.db.commit()
                return self.ajax_ok()
        return self.ajax_alert(data="删除出错")


class AdminClassifyHandler(BaseHandler):
    """分类标签管理"""

    @login_required
    def get(self):
        user = self.current_user()
        categories = self.db.query(Category).all()
        tags = self.db.query(Tag).all()
        args = {
            "categories": categories,
            "tags": tags,
            "user": user
        }
        return self.render("admin/classify.html", **args)

    @login_required
    def delete(self, types, pk):
        if pk:
            classify = self.db.query(Classify[types]).filter(Classify[types].id == int(pk)).first() if pk else None
            if classify:
                classify.all_posts = []
                self.db.add(classify)
                self.db.delete(classify)
                self.db.commit()
                return self.ajax_ok()
        return self.ajax_alert(data="删除出错")
