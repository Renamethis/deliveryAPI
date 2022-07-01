from app import db

# ORM model
class Entry(db.Model):
    __tablename__ = 'delivery'
    query = db.session.query_property()
    id = db.Column(db.String(40), primary_key=True)
    num = db.Column(db.Float, nullable=False, unique=False)
    pdate = db.Column(db.Date, nullable=False, unique=False)
    priced = db.Column(db.Float, nullable=False, unique=False)
    pricer = db.Column(db.Float, nullable=False, unique=False)
    def to_json(self):
        return {
            'id': self.id,
            'num': self.num,
            'priced': self.priced,
            'date': self.pdate,
            'pricer': self.pricer,
        }