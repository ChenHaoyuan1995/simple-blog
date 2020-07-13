import sys

import tornado.ioloop
import tornado.web

from blog.libs.error import NotFoundHandler
from blog.url import urls
from blog.url import ui_modules

settings = {
    "handlers": urls,
    "cookie_secret": "change-to-random",
    "template_path": "blog/templates",
    "static_path": "blog/static",
    "ui_modules": ui_modules,
    "debug": True,
    "default_handler_class": NotFoundHandler,
    "default_handler_args": dict(status_code=404)
}

if __name__ == "__main__":

    try:
        subcommand = sys.argv[1]
    except IndexError:
        subcommand = 'runserver'

    if subcommand == "createdb":
        from blog.libs.database import Base, engine

        Base.metadata.create_all(engine)
        print("DataBase has been create")

    elif subcommand == "makedata":
        from faker_data import make_data

        try:
            make_data()
        except:
            print("must create database first\nplease try createdb first")

    elif subcommand == "runserver":
        app = tornado.web.Application(**settings)
        app.listen(5000, "0.0.0.0")
        tornado.ioloop.IOLoop.current().start()

    else:
        print("runserver for run\ncreatedb for create database\nmakedata for make faker data")
