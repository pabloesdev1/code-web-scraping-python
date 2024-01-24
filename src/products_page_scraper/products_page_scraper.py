from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .product import Product


class ProductsPageScraper(ABC):

    @abstractmethod
    def get_html(self, url: str) -> BeautifulSoup:
        ...
    
    @abstractmethod
    def get_products(self, html_content: BeautifulSoup) -> list[Product]:
        ...
    
    @abstractmethod
    def get_current_price(self, html_content: BeautifulSoup) -> float:
        ...
    