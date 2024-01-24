from selenium import webdriver
from products_page_scraper.amazon_products_page_scraper import AmazonProductsPageScraper
from products_page_scraper.meli_products_page_scraper import MeliProductsPageScraper
from products_page_scraper.product_repository import ProductRepository
from products_page_scraper.products_price_checker import ProductsPriceChecker


def init():
    item_name = input("Ingrese el nombre del producto a buscar: ")
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"

    amazon_search_result_url = "https://www.amazon.com/s?k={}".format(item_name)
    meli_search_result_url = "https://listado.mercadolibre.com.ec/{}".format(item_name)

    amazon_products_page_scraper = AmazonProductsPageScraper(driver=webdriver.Chrome(options=options))
    amazon_search_result_html = amazon_products_page_scraper.get_html(amazon_search_result_url)

    amazon_products = amazon_products_page_scraper.get_products(html_content=amazon_search_result_html)
    for item in amazon_products:
        print("{}. Producto: {} Precio ${}".format(item.id, item.name, item.price), end="\n\n")
    
    amazon_product_id = input("Ingrese el id del producto de amazon a escoger: ")
    amazon_product = next(filter(lambda product: product.id == int(amazon_product_id), amazon_products))

    meli_products_page_scraper = MeliProductsPageScraper(driver=webdriver.Chrome(options=options))
    meli_search_result_html = meli_products_page_scraper.get_html(meli_search_result_url)
    meli_products = meli_products_page_scraper.get_products(html_content=meli_search_result_html)

    for item in meli_products:
        print("{}. Producto: {} Precio ${}".format(item.id, item.name, item.price), end="\n\n")

    meli_product_id = input("Ingrese el id del producto de mercado libre a escoger: ")
    meli_product = next(filter(lambda product: product.id == int(meli_product_id), meli_products))

    ProductRepository().save_product(
        name=item_name,
        amazon_url=amazon_product.url,
        meli_url=meli_product.url,
        meli_price=meli_product.price,
        amazon_price=amazon_product.price,
    )
    
if __name__=="__main__":
    init()
    # product_price_checker = ProductsPriceChecker()
    # product_price_checker.check()