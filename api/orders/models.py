from sqlalchemy import Column, Float, Integer, String, Boolean
from storage.base import Base, db_session

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    owner_id = Column(String)
    buyer_id = Column(String)
    description = Column(String(120))
    amount = Column(Float(2))
    is_active = Column(Boolean)

    def __repr__(self):
        return "<User(id='{}', owner_id='{}', buyer_id='{}', description='{}', amount='{}', is_active='{}'"\
                .format(self.id, self.owner_id, self.buyer_id, self.description, self.amount, self.is_active)
    
    def to_dict(self):
        return {
           "id": self.id,
           "owner_id": self.owner_id,
           "buyer_id": self.buyer_id,
           "description": self.description,
           "amount": self.amount,
           "is_active": self.is_active
        }
    
    @classmethod
    def add(cls, _owner_id=None, _buyer_id=None, _description=None, _amount=None, _is_active=None, db_session=db_session):
      order = Order()
      order.owner_id = _owner_id
      order.buyer_id = _buyer_id
      order.description = _description
      order.amount = _amount
      order.is_active = _is_active

      db_session.flush()
      db_session.add(order)
      db_session.commit()

      return order
    
    @classmethod
    def get(cls, _id=None):
      order = (
              db_session.query(Order)
                  .filter(Order.id == _id)
                      .first()
            )
      
      return order.to_dict()
    
    @classmethod
    def update(cls, _id, _fields={}):
        key = list(_fields.keys())[0]
        value = _fields[key]

        stmt = (
                db_session.query(Order)
                    .filter_by(id=_id)
                    .update({
                       "{}".format(key): value
                    })
                )
        
        db_session.commit()

    @classmethod
    def list(cls):
        orders = list()

        all_orders = (
          db_session.query(Order)
            .all()
        )

        for order in all_orders:
          order_obj = order.to_dict()
          orders.append(order_obj)

        return orders
    
    @classmethod
    def delete(cls, _id=None):
       (
          db_session.query(Order)
            .filter_by(id=_id)
            .delete(synchronize_session=False)
       )

       db_session.commit()
