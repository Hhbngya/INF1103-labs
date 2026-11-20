from product import Product

LINE = "-" * 45


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
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
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        # composition: the Order creates and owns its OrderLines
        self.__order_lines: list[OrderLine] = []

    def get_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The OrderLine is created here, inside the Order, not passed in
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> None:
        for order_line in self.__order_lines:
            if order_line.get_product().get_id() == product_id:
                self.__order_lines.remove(order_line)
                return
        print("Order line not found.")

    def get_order_lines(self) -> list[OrderLine]:
        # Return a copy so code outside the Order can't add or remove lines directly
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print(LINE)
        if len(self.__order_lines) == 0:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(LINE)
        print(f"Total: ${self.calculate_total():.2f}")