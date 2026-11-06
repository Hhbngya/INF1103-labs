LINE = "-" * 45


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        # Return the Product with this ID, or None if not found.
        for product in self.__products:
            if product.get_id() == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        if len(self.__products) == 0:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print(LINE)

    def get_products(self):
        return self.__products