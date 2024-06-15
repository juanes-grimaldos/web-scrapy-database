import json
import os
import logging

class GeneralFunctions:
    '''
    General functions that can be used in the project.
    '''
    def __init__(self):
        pass

    @staticmethod
    def scroll_smooth(
            driver, i:int,
            scroll_multiplayer:float,
            initial_scroll: int
            ):
        '''
        scrolling function to go down the page and load more games
        :param driver: selenium driver
        :param i: iteration number
        :param scroll_multiplayer: how many times pixels are going to be 
        scrolled
        '''
        scroll_to = initial_scroll * (i + 1)
        start = (i * initial_scroll) 
        for number in range(start,  scroll_to, scroll_multiplayer):
            scrollingScript = f""" 
              window.scrollTo(0, {number})
            """
            driver.execute_script(scrollingScript)
    
    @staticmethod
    def store_product_info(file_name: str, product_info: dict):
        """
        Stores the product information in a JSON file.

        Args:
            file_name (str): The name of the JSON file.
            product_info (dict): The product information to be stored.

        Returns:
            None
        """
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            
            data.append(product_info)

            with open(file_name, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                logging.info(f"Product info appended in {file_name}")
        else:
            data = [product_info]

            with open(file_name, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                logging.info(f"Product info stored in {file_name}")
