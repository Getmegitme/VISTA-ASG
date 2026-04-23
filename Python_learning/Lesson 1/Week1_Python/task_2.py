import csv

# File name
input_file = "D:\\My_Python\\VISTA-ASG\\Python_learning\\task2_data.csv"

# Step 1: Expected columns
expected_columns = ["product_id", "product_name", "category", "price", "stock"]

def main():
    print("Expected columns:", expected_columns)

    # Open and read the CSV file
    with open(input_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Step 2: Get actual columns from file
        actual_columns = reader.fieldnames
        print("Actual columns:", actual_columns)

        # Compare expected vs actual
        missing_columns = [col for col in expected_columns if col not in actual_columns]
        extra_columns = [col for col in actual_columns if col not in expected_columns]

        print("Missing columns:", missing_columns if missing_columns else "None")
        print("Extra columns:", extra_columns if extra_columns else "None")

        # Step 3: Read all rows and count them
        rows = list(reader)
        row_count = len(rows)
        print("Total number of rows:", row_count)

        # Step 4: Check valid and invalid rows
        valid_rows = []
        invalid_rows = []

        for row_number, row in enumerate(rows, start=1):
            # A row is valid only if all expected columns exist
            # and required values are not empty
            row_is_valid = True
            reasons = []

            # First check if any expected column is missing in the file itself
            if missing_columns:
                row_is_valid = False
                reasons.append(f"Missing column(s) in file: {missing_columns}")

            # Check empty values for columns that do exist
            for col in actual_columns:
                if row[col] is None or row[col].strip() == "":
                    row_is_valid = False
                    reasons.append(f"Empty value in column: {col}")

            if row_is_valid:
                valid_rows.append((row_number, row))
            else:
                invalid_rows.append((row_number, row, reasons))

        # Print results
        print("\nValid rows:")
        if valid_rows:
            for row_number, row in valid_rows:
                print(f"Row {row_number}: {row}")
        else:
            print("No valid rows found.")

        print("\nInvalid rows:")
        if invalid_rows:
            for row_number, row, reasons in invalid_rows:
                print(f"Row {row_number}: {row}")
                print("Reason(s):", reasons)
        else:
            print("No invalid rows found.")

if __name__ == "__main__":
    main()