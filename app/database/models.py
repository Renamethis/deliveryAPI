from app import db

# ORM model
class Entry(db.Model):
    __tablename__ = 'delivery'
    query = db.session.query_property()
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False, unique=False)
    pdate = db.Column(db.Date, nullable=False, unique=False)
    priced = db.Column(db.Float, nullable=False, unique=False)
    pricer = db.Column(db.Float, nullable=False, unique=False)
    expired = db.Column(db.Boolean, nullable=False, unique=False)
    def to_json(self):
        return {
            'id': self.id,
            'num': self.num,
            'priced': self.priced,
            'date': self.pdate,
            'pricer': self.pricer,
            'expired': self.expired
        }