from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import logging
import re
from datetime import datetime
import logging
from database.product import Product
import concurrent.futures
import logging.handlers
import threading
from database.dbHandler import DBHandler
from config.app_contex import image_location
import os

size_order = ["XS", "S", "M", "L", "XL", "XXL"]


MAX_WORKER = 5

log = logging.getLogger(__name__)
# Create a RotatingFileHandler that rotates the log file when it reaches 10MB
handler = logging.handlers.RotatingFileHandler('webScrapeLog.log', maxBytes=10*1024*1024, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(thread)d - %(module)s:%(lineno)d - %(message)s')
handler.setFormatter(formatter)
# Add the handler to the logger
log.addHandler(handler)
# Set the logging level to DEBUG
log.setLevel(logging.DEBUG)

class TrekomaniaScrapper:
    """
    class that scrapes data from a website using the Selenium WebDriver and Beautiful Soup libraries.
    The class defines several methods to scrape and process the data, and also includes a method to 
    insert the data into a database. its scrape trekomania page and get all the products from that page
    and push it into the db
    """
    def __init__(self):
        self.base_url = 'https://www.trekomania.co.il/product-category/%d7%a2%d7%95%d7%93%d7%a4%d7%99%d7%9d/page/'
        self.common_attributes_class_name = 'gtm4wp_productdata'  # to find the span class
        # span string to locate the data
        self.common_attributes_data_string = 'data-gtm4wp_product'
        # cat is department of clothes # price her is after discount
        self.common_attributes = ['id', 'price',
                                  'name', 'cat', 'url', 'listposition']
        self.size_class_name = "badge-inner callout-new-bg is-small new-bubble"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.number_of_pages = self.get_number_of_pages()
        self.product_info_dict = {}
        self.db_handler = DBHandler()



    def get_number_of_pages(self) -> int:
        """
        get the number of page in order to know how many page should scrape
        """
        web_driver = webdriver.Chrome(options=self.options)
        try:
            web_driver.get(f'{self.base_url}1/') # there is alway one page at least
        except Exception as e:
            log.exception("There are no more outlet products")
            raise e
        html = web_driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        shop_container = soup.find(
            'ul', class_='page-numbers nav-pagination links text-center') # page navigation bar
        pages = shop_container.find_all("li", recursive=False) # including the -> li
        web_driver.quit()
        num_pages = len(pages) - 1
        log.info(f'got number of page: {num_pages}')
        return num_pages


    def get_products_obj_by_page(self, page) -> None:
        """
        get all the product html's (obj) by page
        """
        products_html_obj = []
        try: 
            web_driver = webdriver.Chrome(options=self.options)
            web_driver.get(f'{self.base_url}/{page}/')
            html = web_driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            shop_container = soup.find('div', class_='shop-container')
            elements = shop_container.find_all("div", recursive=False)
            # there is three element, searching fo the right one
            for child in elements:
                if 'class' in child.attrs and 'products row' in ' '.join(child['class']):
                    log.info(f'found products of page {page}')
                    # get all div's every div is a product
                    products_html_obj.extend(
                        child.find_all("div", recursive=False))
        except Exception as e:
            print("got exception :" + str(e))
        # ensure that the browser process is fully terminated
        web_driver.quit()
        return products_html_obj

    def get_product_dict(self, element) -> tuple:
        """
            this function create a dict for element with all his relevant data
        """
        dict = {}
        span = element.find('span', class_=self.common_attributes_class_name)
        id = span[f'{self.common_attributes_data_string}_id']
        # iterate over common values
        for attr in self.common_attributes:
            # one of common value is id
            if attr == 'id':
                continue
            dict[attr] = (span[f'{self.common_attributes_data_string}_{attr}'])
        dict['actual_price'] = self.get_actual_price(element)
        dict['sizes'] = self.get_sizes_of_product(element, dict['url'], id)
        dict['image_url'] = self.get_image_url(element)
        return dict, id

    def get_image_url(self, element):
        img_tag = element.find('img')
        if img_tag is not None and 'src' in img_tag.attrs:
            return img_tag['data-src']
        else:
            return None

    def get_actual_price(self, element) -> str:
        price_del = element.find('del')
        if not price_del:
            return 0
        price_del = price_del.text.strip()
        price = price_del.split(' ')[0][:]
        price = re.sub(r'[^\d\.]+', '', price)
        return price

    def get_sizes_of_product(self, element, url, id) -> str:
        if (text := element.find('div', class_=self.size_class_name)) is not None:
            text = text.text
            try:
                sizes = text.split(': ')[1]
                return sizes.replace(',', ' ')
            except Exception as e:
                log.info(f'could not render the actual sizes with ":" for {id} try to render inside the url-{url}')
        # if not so need to get size from the actual product page
        all_sizes = []
        web_driver = webdriver.Chrome(options=self.options)
        web_driver.get(url)
        html = web_driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        options = soup.find('select', id='pa_%d7%9e%d7%99%d7%93%d7%94')
        if options:
            for option in options:
                size = option['value'].strip().upper()
                if not size:
                    continue
                
                if '-' in size: # in case size can be 39-45 for example
                    start, end = map(str.strip, size.split('-'))
                    if start.isalpha() and end.isalpha():
                        start = start.upper()
                        end = end.upper()
                        # Handle size ranges like "S-L" (alphabetical sizes)
                        if start in size_order and end in size_order:
                            start_index = size_order.index(start)
                            end_index = size_order.index(end)
                            all_sizes.extend(size_order[start_index:end_index + 1])
                    else:
                        start, end = map(int, size.split('-'))
                        all_sizes.extend(str(i) for i in range(start, end+1))
                else:
                    all_sizes.append(size)
        web_driver.quit()
        return ' '.join(all_sizes).strip().upper()
        
    def run_for_page(self, page):
        log.info(f"web scrapper started for thread {threading.current_thread().ident}")
        products_html_obj = self.get_products_obj_by_page(page)
        for element in products_html_obj:
            dict, id = self.get_product_dict(element)
            image_location = self.download_image(dict['image_url'], id)
            dict['image_location'] = image_location
            self.product_info_dict[id] = dict
        # for each elemnt get all his data and create json dict
        log.info(f"Finished scraping for thread {threading.current_thread().ident}")


    def insert_data_to_db(self) -> None:
        
        """
        This method inserts the scraped data into a database table. It checks if each product
        already exists in the database and updates its attributes if necessary, or creates a
        new record if the product is not already in the database.
        """
        log.info('Start insert data to db')
        new_product_list = []
        existing_product_list = []
        scraped_product_ids = set(self.product_info_dict.keys())

        try:
            
            products_to_delete = self.db_handler.session.query(Product).filter(~Product.id.in_(scraped_product_ids))
            deleted_products = list(products_to_delete)
            products_to_delete.delete(synchronize_session=False)
            for product_id, product_info in self.product_info_dict.items():
                # Try to get an existing product from the database
                product = self.db_handler.session.query(Product).filter_by(id=product_id).first()
                # If the product is not in the database, create a new one
                if not product:
                    product = Product(
                        id=product_id,
                        category=product_info['cat'],
                        name=product_info['name'],
                        original_price=product_info['actual_price'],
                        current_price=product_info['price'],
                        gender=self.get_product_gender(product_id),
                        sizes=product_info['sizes'],
                        image_location=product_info['image_location']
                    )
                    new_product_list.append(product)
                else:
                    log.info(f'product {product_id} is in the database, update his data')
                    product.id = product_id
                    product.category = product_info['cat']
                    product.name = product_info['name']
                    product.original_price = product_info['actual_price']
                    product.current_price = product_info['price']
                    product.gender = self.get_product_gender(product_id)
                    product.sizes = product_info['sizes']
                    product.image_location = product_info['image_location']
                    product.last_update =  datetime.now()
                    existing_product_list.append({
                        'id': product_id,
                        'original_price': product_info['actual_price'],
                        'current_price': product_info['price'],
                        'sizes': product_info['sizes'],
                        'last_update': datetime.now()
                    })            
                # Fields that can be updated are: actual price, current_price, sizes
            self.db_handler.session.commit()
                   # Bulk insert new products into the database
            if new_product_list:
                self.db_handler.session.bulk_save_objects(new_product_list)
                self.db_handler.session.commit()
            # Bulk update existing products
            if existing_product_list:
                self.db_handler.session.bulk_update_mappings(Product, existing_product_list)
                self.db_handler.session.commit()
        finally:
            # Close the database session
            self.db_handler.session.close()
        log.info(f'added the following new ids {[product.id for product in new_product_list]}')
        log.info(f'update data for the following ids {[product["id"] for product in existing_product_list]}')
        log.info(f'deleted the following ids {[product.id for product in deleted_products]}')
        

    def get_product_gender(self, product_id) -> str:
        
        """
        This method determines the gender of a product based on its name.
        It returns "M" if the product is for men, "F" if the product is for women,
        or "U" if the gender cannot be determined.
        """
        
        name = self.product_info_dict[product_id]['name']
        if "גברים" in name:
            return 'M'
        elif "נשים" in name:
            return 'F'
        else:
            return 'U'

    def download_image(self, image_url, product_id):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            # Extract the file extension from the URL
            file_extension = image_url.split('.')[-1]

            # Save the image to a specific location with the product_id as the file name
            image_filename = f"{product_id}.{file_extension}"
            image_path = os.path.join(image_location, image_filename)

            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            log.info(f"Image for product {product_id} downloaded successfully.")
            return image_path
        except Exception as e:
            log.error(f"Failed to download image for product {product_id}: {e}")

    def check_and_delete_unused_images(self, valid_ids):

        # Get a list of all image files in the specified location
        all_images = [f for f in os.listdir(image_location) if os.path.isfile(os.path.join(image_location, f)) and not f.startswith('.')]

        # Extract product IDs from image file names
        existing_ids = [os.path.splitext(image)[0] for image in all_images]

        # Find IDs that are present in the image location but not in the valid_ids array
        unused_ids = set(existing_ids) - set(valid_ids)

        # Delete images corresponding to unused IDs
        for unused_id in unused_ids:
            # Find the image file with any extension for the unused ID
            matching_files = [image for image in all_images if image.startswith(f"{unused_id}.")]

            for matching_file in matching_files:
                image_path = os.path.join(image_location, matching_file)
                try:
                    os.remove(image_path)
                    log.info(f"Deleted unused image: {image_path}")
                except FileNotFoundError:
                    log.warning(f"Image not found for ID: {unused_id}")


    def run(self) -> None:
        # threads params are a list of all pages in the website
        threads_params = [str(i) for i in range(1, self.number_of_pages + 1)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            futures = [executor.submit(self.run_for_page, param) for param in threads_params]
        concurrent.futures.wait(futures)
        log.info("all threads finished")
        self.check_and_delete_unused_images(set(self.product_info_dict.keys()))
        self.insert_data_to_db()
        log.info("Web Bot Finished Successfully")
        print("Finish")


if __name__ == '__main__':
    scraper = TrekomaniaScrapper()
    scraper.run()