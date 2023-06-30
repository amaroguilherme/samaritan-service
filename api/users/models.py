import logging
from flask import jsonify

from sqlalchemy import ARRAY, Column, Float, ForeignKey, Integer, String, select
from storage.base import Base, db_session

log = logging.getLogger()
log.setLevel(logging.INFO)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String(120))
    salt = Column(String(120))
    about = Column(String(120))
    likes = Column(ARRAY(String))
    dislikes = Column(ARRAY(String))
    total_amount = Column(Float(2))

    def __repr__(self):
        return "<User(id='{}', username='{}', password='{}', salt='{}', about='{}', likes='{}', dislikes='{}', total_amount='{}'"\
                .format(self.id, self.username, self.password, self.salt, self.about, self.likes, self.dislikes, self.total_amount)

    @classmethod
    def add(cls, _username=None, _password=None, _salt=None, _about=None, _likes=None, _dislikes=None, _total_amount=None, db_session=db_session):
      user = User()
      user.username = _username
      user.password = _password
      user.salt = _salt
      user.about = _about
      user.likes = _likes
      user.dislikes = _dislikes
      user.total_amount = _total_amount

      db_session.flush()
      db_session.add(user)
      db_session.commit()

      return user
    
    @classmethod
    def get(cls, _id=None):
      user = (
              db_session.query(User)
                  .filter(User.id == _id)
                      .first()
            )
      
      return user
    
    @classmethod
    def update(cls, _id, _fields={}):
        try:
          key = list(_fields.keys())[0]
          value = _fields[key]
        
          stmt = (
                  db_session.query(User)
                      .filter_by(id=_id)
                      .update({
                        "{}".format(key): value
                      })
                  )
          
          db_session.commit()

        except Exception as e:
           log.exception(e)
           return jsonify(dict(message=f'{e}'))

      