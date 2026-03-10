class Config:
    SECRET_KEY = "secret"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:simple@localhost/event_scheduler"

    SQLALCHEMY_TRACK_MODIFICATIONS = False