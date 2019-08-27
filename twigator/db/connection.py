from mongoengine import connect, disconnect

class MongoConnection(object):
    def __init__(self, db, host, port):
        connect(db, host=host, port=port)

    def __enter__(self):
        # return self.obj
        return None

    def __exit__(self, type, value, traceback):
        disconnect()
