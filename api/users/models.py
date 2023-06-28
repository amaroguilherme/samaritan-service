from sqlalchemy import ARRAY, Column, Float, ForeignKey, Integer, String, select
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
    
class UserProfile(Base):
   __tablename__ = 'profiles'
   id = Column(Integer, primary_key=True)
   user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
   about = Column(String(120))
   likes = Column(ARRAY(String))
   dislikes = Column(ARRAY(String))

   def __repr__(self):
        return "<UserProfile(id='{}', user_id='{}', about='{}', likes='{}', dislikes='{}'"\
                .format(self.id, self.user_id, self.about, self.likes, self.dislikes)
   
   @classmethod
   def add(cls, _user_id=None, _about=None, _likes=None, _dislikes=None):
      user_profile = UserProfile()
      user_profile.user_id = _user_id
      user_profile.about = _about
      user_profile.likes = _likes
      user_profile.dislikes = _dislikes

      db_session.flush()
      db_session.add(user_profile)
      db_session.commit()

      return user_profile
   
   @classmethod
   def update(cls, _id, _fields={}):
      key = list(_fields.keys())[0]
      value = _fields[key]

      stmt = (
              db_session.query(UserProfile)
                  .filter_by(user_id=_id)
                  .update({
                      "{}".format(key): value
                  })
              )
      
      db_session.commit()


   
   

      