from configparser import ConfigParser


def config():
    cp = ConfigParser()
    cp.read('config.cfg')
    if "setting" not in cp.sections():
        return Exception("not set setting in config.cfg")
    if "mysql" not in cp.sections():
        return Exception("not set mysql in config.cfg")
    return cp


setting = config()
