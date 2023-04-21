from sqlalchemy import Column, Float, Integer, String
from storage.base import Base, db_session

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String(120))
    salt = Column(String(120))
    total_amount = Column(Float(2))
    contributions = Column(Integer)

    def __repr__(self):
        return "<User(id='{}', username='{}', password='{}', salt='{}', total_amount='{}', contributions='{}'"\
                .format(self.id, self.username, self.password, self.salt, self.total_amount, self.contributions)

    @classmethod
    def add(cls, _username=None, _password=None, _salt=None, _total_amount=None, _contributions=None, db_session=db_session):
      user = User()
      user.username = _username
      user.password = _password
      user.salt = _salt
      user.total_amount = _total_amount
      user.contributions = _contributions

      db_session.flush()
      db_session.add(user)
      db_session.commit()

      return user