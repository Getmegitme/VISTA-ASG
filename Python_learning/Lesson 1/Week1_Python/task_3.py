import csv

input_file = "D:\\My_Python\\VISTA-ASG\\Python_learning\\Lesson 1\\Week1_Python\\customers_raw.csv"
log_file = "bad_records.log"


def main():
    # Open log file in write mode
    with open(log_file, mode="w", encoding="utf-8") as log:

        # Open CSV file
        with open(input_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            print("Processing records...\n")

            for row_number, row in enumerate(reader, start=1):
                errors = []

                # ---- Check missing values ----
                if not row["name"].strip():
                    errors.append("Missing name")

                if not row["city"].strip():
                    errors.append("Missing city")

                # ---- Risky conversion: age ----
                try:
                    age = int(row["age"])
                except ValueError:
                    errors.append(f"Invalid age: {row['age']}")

                # ---- If errors exist, log them ----
                if errors:
                    log_message = f"Row {row_number} | Data: {row} | Errors: {errors}\n"
                    log.write(log_message)
                    print(f"Logged bad record at row {row_number}")
                    continue  # move to next row

                # ---- If row is valid ----
                print(f"Valid row {row_number}: {row}")

    print("\nProcessing complete. Check bad_records.log for issues.")


if __name__ == "__main__":
    main()