from data_bases.model.declarative_base import Session, engine, Base
from data_bases.model.data_model import Fridges


if __name__ == '__main__':
  session = Session()
  fridges = session.query(Fridges).all()

  print('Las neveras almacenadas son:')
  for fridge in fridges:
    print(f'{fridge.id} -{fridge.product} - {fridge.date} - {fridge.price} - {fridge.seller}')

  session.close()