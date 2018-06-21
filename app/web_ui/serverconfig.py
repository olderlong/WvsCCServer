import os

basedir = os.path.abspath(os.path.dirname(__file__))

def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class ServerConfig:
    SECRET_KEY = "pBw%E7feV!!tJZuP3f&QPz2%ola*2IyE"
    PORT = 80
    CC_SERVER_IP = "192.168.1.31"
    CC_SERVER_PORT = 6000
    CC_PROTOCOL = "UDP"


@singleton
class ScanSetting:
    def __init__(self, url="", policy="Normal"):
        self.start_url = url
        self.scan_policy = policy



class DevelopmentConfig(ServerConfig):
    DEBUG = True


class TestingConfig(ServerConfig):
    TESTING = True


class ProductionConfig(ServerConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

if __name__ == '__main__':
    print(basedir)