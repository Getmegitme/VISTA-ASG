import csv
import json

# with open("D:\\My_Python\\VISTA-ASG\\Python learning\\product.csv", "r") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         print(row)

input_file = "products_raw.csv"
output_file = "products_cleaned.json"


def clean_header(header: str) -> str:
    """Convert headers to lowercase_with_underscores."""
    return header.strip().lower().replace(" ", "_")


def clean_row(row: dict) -> dict:
    """Clean missing values and standardize row data."""
    cleaned = {}

    for key, value in row.items():
        new_key = clean_header(key)
        value = value.strip() if value is not None else ""

        # Handle missing values with reasonable defaults
        if new_key == "price":
            cleaned[new_key] = float(value) if value else 0.0
        elif new_key == "stock":
            cleaned[new_key] = int(value) if value else 0
        elif new_key == "product_id":
            cleaned[new_key] = int(value) if value else None
        else:
            cleaned[new_key] = value if value else "Unknown"

    return cleaned


def main():
    cleaned_data = []
    seen = set()

    with open(input_file, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        print("Original headers:", reader.fieldnames)
        print("Cleaned headers:", [clean_header(h) for h in reader.fieldnames])

        for row in reader:
            cleaned_row = clean_row(row)

            # Track missing fields
            missing_fields = []
            for key, value in row.items():
                if value is None or value.strip() == "":
                    missing_fields.append(clean_header(key))

            if missing_fields:
                print(f"Missing fields in product_id {cleaned_row.get('product_id')}: {missing_fields}")

            # Remove duplicates based on full cleaned row
            row_tuple = tuple(cleaned_row.items())
            if row_tuple not in seen:
                seen.add(row_tuple)
                cleaned_data.append(cleaned_row)
            else:
                print(f"Duplicate found and skipped: product_id {cleaned_row.get('product_id')}")

    with open(output_file, mode="w", encoding="utf-8") as jsonfile:
        json.dump(cleaned_data, jsonfile, indent=4)

    print(f"\nCleaned data written to {output_file}")


if __name__ == "__main__":
    main()
