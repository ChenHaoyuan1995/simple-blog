from tornado.web import url
from blog.handlers import *
from blog.modules import *

urls = [
    url(r"/", IndexHandler, name="index"),
    url(r"/about", AboutHandler, name="about"),
    url(r"/blog", BlogIndexHandler, name="blog"),
    url(r"/blog/detail/([0-9]*)", BlogDetailHandler, name="blog_detail"),
    url(r"/blog/search/(.*)", BlogSearchHandler, name="blog_search"),
    url(r"/blog/(tag|category)/([0-9]*)", BlogClassifyHandler, name="blog_classify"),
    url(r"/admin/register", AdminRegisterHandler, name="register"),
    url(r"/admin/login", AdminLoginHandler, name="login"),
    url(r"/admin/logout", AdminLogoutHandler, name="logout"),
    url(r"/admin", AdminHandler, name="admin"),
    url(r"/admin/add", AdminEditHandler, name="add"),
    url(r"/admin/edit/([0-9]*)", AdminEditHandler, name="edit"),
    url(r"/admin/classify", AdminClassifyHandler, name="classify"),
    url(r"/admin/classify/(tag|category)/([0-9]*)", AdminClassifyHandler, name="classify_edit"),
]

ui_modules = {
    'RowDistance': RowDistanceModule,
    'Tags': TagModule,
    'Categories': CategoryModule,
    'Pagination': PaginateModule,
    'RecentPost': RecentPostModule
}
