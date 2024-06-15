from data_bases.model.declarative_base import Session, engine, Base
from data_bases.model.data_model import Fridges
from data_bases.model.data_model import Specs
import logging

class DataCreation:
   """
   This class is used to create the tables in the database and 
   populate them with data
   """
   Base.metadata.create_all(engine)

   def __init__(self):
      self.session = Session()

   def insert_main_data(self, data: dict):
       """
       Insert main data into the database
       """
       input_data = Fridges(
           link = data['link'],
           product = data['product'],
           price = data['price'],
           seller = data['seller']
         )

       try:
           self.session.add(input_data)
           self.session.commit()
           logging.info('Main Data inserted into the database')
       except Exception as e:
           self.session.rollback()
           logging.error(f'Error inserting main data into the database: {str(e)}')
           pass

       self.session.close()
   
   def insert_meta_data(self, data: dict):
       """
       Insert metadata into the database
       """
       input_data = Specs(
           fridge_link = data['link'] if 'link' in data else None,
           storage = data['storage'] if 'storage' in data else None,
           size = data['size'] if 'size' in data else None,
           energy = data['energy'] if 'energy' in data else None,
           color = data['color'] if 'color' in data else None,
           date = data['date'] if 'date' in data else None
       )

       try:
           self.session.add(input_data)
           self.session.commit()
           logging.info('Meta Data inserted into the database')
       except Exception as e:
           self.session.rollback()
           logging.error(f'Error inserting meta data into the database: {str(e)}')
           pass

       self.session.close()
