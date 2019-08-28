from mongoengine import connect, disconnect

from twigator.envconfig import EnvConfig

class MongoConnection(object):
    def __init__(self, db=None, host=None, port=None):
        env_config = EnvConfig()
        db = db if db else env_config.MONGO_DATABASE
        host = host if host else env_config.MONGO_HOST
        port = port if port else int(env_config.MONGO_PORT)
        connect(db, host=host, port=port)

    def __enter__(self):
        # return self.obj
        return None

    def __exit__(self, type, value, traceback):
        disconnect()
