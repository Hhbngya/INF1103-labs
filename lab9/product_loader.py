import csv

from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row in reader:
                # each row gets its own try, so one bad row doesn't stop the rest
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipped row {row}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")