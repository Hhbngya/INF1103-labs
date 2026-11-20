from product import Product

LINE = "-" * 45


class Inventory:
    def __init__(self) -> None:
        # aggregation: the Inventory holds Products but doesn't create or own them
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_id() == product_id:
                return product
        return None

    def remove_product(self, product_id: str) -> Product | None:
        # Only removes the reference from this inventory.
        # The Product object itself is not destroyed and is returned.
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print(LINE)
        if len(self.__products) == 0:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print(LINE)

    def get_products(self) -> list[Product]:
        return self.__products