import math

from blog import BaseHandler
from blog.models import Post, Category, Tag

Classify = {
    "category": Category,
    "tag": Tag
}


class BlogIndexHandler(BaseHandler):
    """博客主页"""

    def get(self):
        args = self.pagination("posts", Post)
        return self.render("blog/blog_index.html", **args)


class BlogClassifyHandler(BaseHandler):
    """博客分类页面"""

    def get(self, types, pk):
        pk = int(pk)

        classify = self.db.query(Classify[types]).filter(Classify[types].id == pk).first()
        conditions = []
        if types == "category":
            conditions.append(Post.category == classify)
        if types == "tag":
            conditions.append(Post.tags.contains(classify))

        args = self.pagination("posts", Post, conditions)
        args["classify"] = classify
        return self.render("blog/blog_classify.html", **args)


class BlogSearchHandler(BaseHandler):
    """博客搜索页面"""

    def get(self, keywords):
        conditions = [Post.title.like("%{}%".format(keywords))]
        args = self.pagination("posts", Post, conditions)
        args["keywords"] = keywords
        return self.render("blog/blog_search.html", **args)


class BlogDetailHandler(BaseHandler):
    """博客文章详情"""

    def get(self, pk):
        pk = int(pk)
        post = self.db.query(Post).filter(Post.del_flag == 0, Post.id == pk).first()
        return self.render("blog/blog_detail.html", post=post)
