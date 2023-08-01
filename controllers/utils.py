from controllers.config import config

from views.views_authentication import AuthenticationView

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Utils:
    params = config()

    def server_connection(self):
        try:
            engine = create_engine(
                f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}"
            )
            return engine
        except Exception:
            AuthenticationView().authentication_error()

    def session_init(self):
        engine = self.server_connection()
        Session = sessionmaker(bind=engine)
        return Session()
