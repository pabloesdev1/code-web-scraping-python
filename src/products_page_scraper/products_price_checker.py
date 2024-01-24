import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from selenium import webdriver
from products_page_scraper.amazon_products_page_scraper import AmazonProductsPageScraper
from products_page_scraper.meli_products_page_scraper import MeliProductsPageScraper
from products_page_scraper.product_repository import ProductRepository

load_dotenv()

class ProductsPriceChecker:

    def __init__(self) -> None:
        self.repository = ProductRepository()

    def check(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/google-chrome"
        products = self.repository.list_products()
        for product in products:
            amazon_product_page_scraper = AmazonProductsPageScraper(webdriver.Chrome(options=options))
            amazon_product_html = amazon_product_page_scraper.get_html("https://amazon.com"+product["amazon_url"])
            new_amazon_price = amazon_product_page_scraper.get_current_price(amazon_product_html)

            meli_product_page_scraper = MeliProductsPageScraper(webdriver.Chrome(options=options))
            meli_product_html = meli_product_page_scraper.get_html(product["meli_url"])
            new_meli_price = meli_product_page_scraper.get_current_price(meli_product_html)

            if new_amazon_price != product["amazon_price"]:
                self.notify(f"El precio del producto {product['name']} en amazon ha cambiado")
                self.repository.update_product(product["_id"], { "amazon_price": new_amazon_price })

            if new_meli_price != product["meli_price"]:
                self.notify(f"El precio del producto {product['name']} en mercado libre ha cambiado")
                self.repository.update_product(product["_id"], { "meli_price": new_meli_price })


    def notify(self, msg: str):
        user = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        email_message = EmailMessage()
        email_message.set_content(msg)
        email_message["subject"] = "Actualización de precios de productos"
        email_message["to"] = user
        email_message["from"] = user

        server =smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(email_message)
        server.quit()