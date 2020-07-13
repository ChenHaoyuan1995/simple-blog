from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(handler, *args, **kwargs):
        if not handler.has_login:
            return handler.redirect(handler.reverse_url("login"))

        func(handler, *args, **kwargs)

    return wrapper
