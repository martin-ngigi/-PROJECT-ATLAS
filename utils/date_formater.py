from datetime import datetime

# convert date from "2023-01-01" format to "20230101" format
def convert_date_format(date_str):
    # Parse the input date string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # Format datetime object to the new date string format
    new_date_str = date_obj.strftime("%Y%m%d")
    return new_date_str

# Example usage
converted_date = convert_date_format("2023-01-01")
print(converted_date)  # Output: 20230101
