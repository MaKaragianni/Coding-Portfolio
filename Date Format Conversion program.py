# This is a program that asks a user to insert a full date and then converts this date to the format "YYYY-MM-DD".

def get_month_number(month_name):
    # Dictionary to map month names to numbers
    months = {
        "january": "01", "february": "02", "march": "03",
        "april": "04", "may": "05", "june": "06",
        "july": "07", "august": "08", "september": "09",
        "october": "10", "november": "11", "december": "12"
    }
    return months.get(month_name.lower())

def validate_and_format_date(date_string):
    # Splitting the date string into components
    parts = date_string.split()
    
    # Check if the date has three parts: day, month, year
    if len(parts) != 3:
        return "Invalid date format. Please use 'day month year'."

    day, month_name, year = parts

    # Remove any st, nd, rd, th from day
    day = ''.join(filter(str.isdigit, day))

    # Convert month name to a number
    month_number = get_month_number(month_name)
    if not month_number:
        return "Invalid month name."

    # Return formatted date
    return f"{year}-{month_number}-{day.zfill(2)}"

def main():
    # Asking user to input the date
    user_input = input("Please enter the date in 'day month year' format: ")
    converted_date = validate_and_format_date(user_input)
    print(f"Converted date: {converted_date}")

# Running the main function
main()
