from models.database import db


class Hardware(db.Model):
    __tablename__ = 'hardware'

    id = db.Column(db.String(100), unique=True, primary_key=True)
    machine = db.Column(db.String(100))
    gpu = db.Column(db.String(100))

    db_product_addtocar = db.relationship("UsageLog", backref="hardware")
