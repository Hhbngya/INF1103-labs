from product import Product
from discount import DiscountStrategy, NoDiscount

LINE = "-" * 45


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        # The OrderLine refers to a Product but does not own it
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} "
              f"= ${self.calculate_subtotal():.2f}")


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        # composition: the Order creates and owns its OrderLines
        self.__order_lines: list[OrderLine] = []
        # association: the Order uses a discount strategy but doesn't own it
        if discount is None:
            discount = NoDiscount()
        self.__discount: DiscountStrategy = discount

    def get_id(self) -> str:
        return self.__order_id

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> None:
        for order_line in self.__order_lines:
            if order_line.get_product().get_id() == product_id:
                self.__order_lines.remove(order_line)
                return
        print("Order line not found.")

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        # Order doesn't know how the discount works, it just asks the strategy
        return self.__discount.apply(self.calculate_subtotal())

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print(LINE)
        if len(self.__order_lines) == 0:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(LINE)
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Total after discount: ${self.calculate_total():.2f}")