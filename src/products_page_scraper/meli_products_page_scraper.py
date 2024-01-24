from products_page_scraper.products_page_scraper import ProductsPageScraper
from products_page_scraper.product import Product
from bs4 import BeautifulSoup
from time import sleep

class MeliProductsPageScraper(ProductsPageScraper):

    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        sleep(10)
        content = self.driver.page_source
        html = BeautifulSoup(content, "html.parser")
        self.driver.close()
        return html

    def get_products(self, html_content: BeautifulSoup) -> list[Product]:
        products: list[Product] = []
        products_div_list = html_content.find_all("div", {"class": "ui-search-result__wrapper"})
        for index, item in enumerate(products_div_list):
            try:
                item_name = item.find("h2", {"class": "ui-search-item__title"}).text
                item_price = item.find("span", {"class": "andes-money-amount__fraction"}).text.replace(".", "")
                try:
                    item_price_cents = item.find("span", {"class": "andes-money-amount__cents"}).text
                    item_price = item_price + "." + item_price_cents
                except:
                    pass

                item_url = item.find("a", {"class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"}).attrs["href"]
                products.append(Product(id=index+1, name=item_name, price=float(item_price), url=item_url))
            except Exception as e:
                pass
        return products
    

    def get_current_price(self, html_content: BeautifulSoup) -> float:
        price = html_content.find("span", {"class": "andes-money-amount__fraction"}).text.replace(".", "")
        try:
            price_cents = html_content.find("span", {"class": "andes-money-amount__cents"}).text
            price = price + "." + price_cents
        except:
            pass
        return float(price)