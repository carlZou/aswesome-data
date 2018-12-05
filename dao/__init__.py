from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from webapp import app

app.config.from_object(Config)
db = SQLAlchemy(app)
# 数据库迁移 flask db init
migrate = Migrate(app, db)


