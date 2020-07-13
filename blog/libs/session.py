import uuid
import pickle
import redis

from blog import setting


def redis_setting():
    args = {
        "host": setting["redis"]["host"],
        "port": setting["redis"]["port"],
        "db": setting["redis"]["db"]
    }
    return args


try:
    r = redis.Redis(**redis_setting())
except KeyError:
    r = None

SESSION = {}


class Session:
    def __init__(self, handler):
        self.handler = handler

    @staticmethod
    def __random_str():
        return str(uuid.uuid4())

    def _get_cookie_sid(self):
        cookie_sid = self.handler.get_secure_cookie("__session", None)
        return str(cookie_sid, encoding="utf-8") if cookie_sid else None

    def __setitem__(self, key, value):
        cookie_sid = self._get_cookie_sid()
        if not cookie_sid:
            cookie_sid = self.__random_str()
        self.handler.set_secure_cookie("__session", cookie_sid)
        SESSION.setdefault(cookie_sid, {}).__setitem__(key, value)

    def __getitem__(self, key):
        cookie_sid = self._get_cookie_sid()
        content = SESSION.get(cookie_sid, None)
        return content.get(key, None) if content else None

    def __delitem__(self, key):
        cookie_sid = self._get_cookie_sid()
        if not cookie_sid or not SESSION.get(cookie_sid):
            raise KeyError(key)
        del SESSION[cookie_sid][key]


class RedisSession(Session):
    @staticmethod
    def get_session_content(cookie_sid, key):
        session_data = r.hget("_tornado_session_" + cookie_sid, key=key)
        if session_data:
            session_content = pickle.loads(session_data)
            return session_content if session_content is not None else {}
        return {}

    def __setitem__(self, key, value):
        cookie_sid = self._get_cookie_sid()
        if not cookie_sid:
            cookie_sid = self.__random_str()
        self.handler.set_secure_cookie("__session", cookie_sid)
        session_content = self.get_session_content(cookie_sid, key)
        session_content.__setitem__(key, value)
        r.hset("_tornado_session_" + cookie_sid, key, pickle.dumps(session_content))
        r.expire("_tornado_session_" + cookie_sid, 60 * 60 * 24)

    def __getitem__(self, key):
        cookie_sid = self._get_cookie_sid()
        if not cookie_sid:
            return None
        content = self.get_session_content(cookie_sid, key)
        return content.get(key, None) if content else None

    def __delitem__(self, key):
        cookie_sid = self._get_cookie_sid()
        if not cookie_sid:
            raise KeyError(key)
        session_content = self.get_session_content(cookie_sid, key)
        session_content.__delitem__(key)
        r.hset("_tornado_session_" + cookie_sid, key, pickle.dumps(session_content))
