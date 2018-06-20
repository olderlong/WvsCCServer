import os

basedir = os.path.abspath(os.path.dirname(__file__))


class config:
    SECRET_KEY = "pBw%E7feV!!tJZuP3f&QPz2%ola*2IyE"
    PORT = 80



class DevelopmentConfig(config):
    DEBUG = True


class TestingConfig(config):
    TESTING = True


class ProductionConfig(config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

if __name__ == '__main__':
    print(basedir)