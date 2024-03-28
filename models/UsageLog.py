from models.database import db


class UsageLog(db.Model):
    __tablename__ = 'usage_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    hardware_id = db.Column(db.String(100), db.ForeignKey('hardware.id'), nullable=False)
    date = db.Column(db.Date)
    period = db.Column(db.Integer)
