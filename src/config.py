import os

ENV = os.getenv("ENV")

SQLALCHEMY_DATABASE_URI = (
    "postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
        db_name=os.getenv("DB_NAME"),
        db_user=os.getenv("DB_USER"),
        db_pass=os.getenv("DB_PASS"),
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=os.getenv("DB_PORT", 5432),
    )
)
