from models.database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(100), unique=True, primary_key=True)
    token = db.Column(db.String(100))
    account_type = db.Column(db.String(100))
    chinese_name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    db_product_addtocar = db.relationship("UsageLog", backref="user")
