from bs4 import BeautifulSoup
from products_page_scraper.product import Product
from products_page_scraper.products_page_scraper import ProductsPageScraper
from time import sleep


class AmazonProductsPageScraper(ProductsPageScraper):

    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        self.driver.refresh()
        self.driver.get(url)
        sleep(10)
        content = self.driver.page_source
        html = BeautifulSoup(content, "html.parser")
        self.driver.close()
        return html
    
    def get_products(self, html_content: BeautifulSoup) -> list[Product]:
        products: list[Product] = []
        products_div_list = html_content.find_all("div", {"class": "s-result-item"})
        for index, item in enumerate(products_div_list):
            try:
                item_name = item.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text
                item_price = item.find("span", {"class": "a-price-whole"}).text.replace(",", "") \
                    + item.find("span", {"class": "a-price-fraction"}).text
                item_url = item.find("a", {"class": "a-link-normal s-no-outline"}).attrs["href"]
                products.append(Product(id=index+1, name=item_name, price=float(item_price), url=item_url))
            except Exception as e:
                pass
        return products
    

    def get_current_price(self, html_content: BeautifulSoup) -> float:
        price = html_content.find("span", {"class": "a-price-whole"}).text.replace(",", "") \
                    + html_content.find("span", {"class": "a-price-fraction"}).text
        return float(price)