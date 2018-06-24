import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ServerConfig:
    SECRET_KEY = "pBw%E7feV!!tJZuP3f&QPz2%ola*2IyE"
    PORT = 80
    # CC_SERVER_IP = "192.168.1.31"
    CC_SERVER_IP = "192.168.3.2"
    CC_SERVER_PORT = 6000
    CC_PROTOCOL = "UDP"



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