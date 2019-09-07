from typing import Optional
from mongoengine import connect, disconnect  # type: ignore

from twigator.envconfig import EnvConfig


class MongoConnection:
    """
    MongoDB connection context manager class
    """
    def __init__(self,
                 db: Optional[str] = None,
                 host: Optional[str] = None,
                 port: Optional[int] = None) -> None:
        env_config = EnvConfig()
        db = db if db else env_config.MONGO_DATABASE
        host = host if host else env_config.MONGO_HOST
        port = port if port else int(env_config.MONGO_PORT)
        connect(db, host=host, port=port)

    def __enter__(self) -> None:
        """
        Context manager magic
        :return:
        """
        # return self.obj
        return None

    def __exit__(self, type, value, traceback) -> None:
        """
        Close connection on exit

        :param type:
        :param value:
        :param traceback:
        :return:
        """
        disconnect()
