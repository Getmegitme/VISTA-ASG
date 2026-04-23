import csv
import json

# Input files
vendor1_file = "D:\\My_Python\\VISTA-ASG\\Python_learning\\Lesson 1\\Week1_Python\\Vendor_1.csv"
vendor2_file = "D:\\My_Python\\VISTA-ASG\\Python_learning\\Lesson 1\\Week1_Python\\Vendor_2.csv"
vendor3_file = "D:\\My_Python\\VISTA-ASG\\Python_learning\\Lesson 1\\Week1_Python\\Vendor_3.csv"

# Output file
output_file = "merged_products.json"

# Standard column mapping
header_mapping = {
    "Product ID": "product_id",
    "Product Name": "product_name",
    "Price": "price",
    "Category": "category",

    "id": "product_id",
    "name": "product_name",
    "price": "price",
    "category": "category",

    "item_code": "product_id",
    "item_name": "product_name",
    "item_group": "category",
    "cost": "price"
}


def standardize_row(row):
    """Convert vendor-specific headers into common business headers."""
    cleaned = {}

    for old_key, value in row.items():
        new_key = header_mapping.get(old_key)
        if new_key:
            value = value.strip() if value is not None else ""

            if new_key == "product_id":
                cleaned[new_key] = int(value) if value else None
            elif new_key == "price":
                cleaned[new_key] = float(value) if value else 0.0
            else:
                cleaned[new_key] = value if value else "Unknown"

    return cleaned


def read_vendor_file(file_name, vendor_name):
    """Read one vendor file and return standardized rows."""
    rows = []

    with open(file_name, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print(f"\nReading {vendor_name}")
        print("Original headers:", reader.fieldnames)

        standardized_headers = [header_mapping.get(h, h) for h in reader.fieldnames]
        print("Mapped headers:", standardized_headers)

        for row in reader:
            cleaned_row = standardize_row(row)

            if cleaned_row.get("price") == 0.0:
                print(f"Missing price found for product_id {cleaned_row.get('product_id')} - defaulted to 0.0")

            rows.append(cleaned_row)

    return rows


def remove_duplicates(products):
    """Remove duplicates based on product_id."""
    unique_products = {}
    duplicates = []

    for product in products:
        product_id = product.get("product_id")

        if product_id not in unique_products:
            unique_products[product_id] = product
        else:
            duplicates.append(product)

    print(f"\nDuplicates found: {len(duplicates)}")
    for dup in duplicates:
        print(f"Duplicate skipped: product_id {dup.get('product_id')}")

    return list(unique_products.values())


def main():
    all_products = []

    # Read all vendor files
    all_products.extend(read_vendor_file(vendor1_file, "Vendor 1"))
    all_products.extend(read_vendor_file(vendor2_file, "Vendor 2"))
    all_products.extend(read_vendor_file(vendor3_file, "Vendor 3"))

    print(f"\nTotal rows before removing duplicates: {len(all_products)}")

    # Remove duplicates
    final_products = remove_duplicates(all_products)

    print(f"Total rows after removing duplicates: {len(final_products)}")

    # Write output to JSON
    with open(output_file, mode="w", encoding="utf-8") as file:
        json.dump(final_products, file, indent=4)

    print(f"\nMerged clean data written to {output_file}")


if __name__ == "__main__":
    main()