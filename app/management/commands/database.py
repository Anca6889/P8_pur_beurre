from django.core.management.base import BaseCommand
from django.db.utils import DataError, IntegrityError
from app.models import Product, Category
from progress.bar import FillingSquaresBar
from app.config import config as c
import requests


class Command(BaseCommand):

    def launch_process(self):

        print("regen database process launched...")
        self.clear_db()

    def clear_db(self):

        print("dropping actual database...")
        product_obj = Product.objects.all()
        product_obj.delete()

        cat_obj = Category.objects.all()
        cat_obj.delete()
        print("database cleared !")

        self.request_off_api()

    def request_off_api(self):
        help = 'feel the database with OFF products'

        categories = c.CATEGORIES
        payload = c.PAYLOAD
        url = c.URL
        products = []

        with FillingSquaresBar(
            "Downloading products from OFF...",
                max=len(categories), suffix="%(percent)d%%") as bar:

            for category in categories:
                payload["tag_0"] = category

                try:
                    data = requests.get(url, params=payload)
                    results = data.json()
                    products.append(results['products'])
                    bar.next()

                except ValueError as err:
                    print("Error: {}".format(err))
        
        bar.finish()
        print("downloading completed !")
        self.delete_uncomplete_products(products)
    
    def delete_uncomplete_products(self, products):

        complete_products = []
        with FillingSquaresBar(
            "Removing corrupted products...",
                max=len(products), suffix="%(percent)d%%") as bar:

            for list in products:
                for p in list:
                    if (
                        p.get("product_name_fr")
                        and p.get("brands")
                        and p.get("nutriscore_grade")
                        and p.get("url")
                        and p.get('image_front_url')
                        and p.get("nutriscore_grade") is not None
                    ):
                        complete_products.append(p)

                    bar.next()
        bar.finish()
        self.get_categories(complete_products)

    def get_categories(self, products):
        
        categories = []
        with FillingSquaresBar(
            "Insering products in database...",
                max=len(products), suffix="%(percent)d%%") as bar:

            for product in products:
                prod_cats = []
                min_cats = product["categories"].lower().split(
                    ", " and ",")
                for min_cat in min_cats:
                    category = min_cat.strip()
                    if category.startswith("en") or category.startswith("fr"):
                        pass
                    else:
                        prod_cats.append(category)
                        if category not in categories:
                            categories.append(category)
                product["categories"] = prod_cats
    
                self.insert_categories(prod_cats, product)

                bar.next()
            bar.finish()

        print("Process achieved with succsess !")

    def insert_categories(self, categories, product):

        for category in categories:
            cat = Category.objects.get_or_create(
            name=category)

            self.insert_product_in_db(product, cat[0])
            

    def insert_product_in_db(self, product, cat):
    
        try:
            product_name_fr = product['product_name_fr']
            brands = product['brands']
            nutriscore_grade = product['nutriscore_grade']
            stores = product['stores']
            url = product['url']
            image = product['image_front_url']
            
            try:

                prod = Product.objects.get_or_create(
                    product_name_fr=product_name_fr,
                    brands=brands,
                    nutriscore_grade=nutriscore_grade,
                    stores=stores,
                    url=url,
                    image=image,
                )[0]

                prod.categories.add(cat)

            except KeyError:
                pass

            except DataError:
                pass

            except IntegrityError:
                pass

        except KeyError:
            pass


    def handle(self, *args, **options):

        self.launch_process()
