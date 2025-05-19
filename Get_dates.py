from datetime import date, timedelta
import calendar

def get_past_dates(frequency, detail):
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    dates_list = []

    if frequency.lower() == "weekly":
        # Map day names to weekday numbers
        days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                "Friday": 4, "Saturday": 5, "Sunday": 6}

        if detail not in days:
            return f"Invalid day name: {detail}. Please enter a valid day."

        # Find the most recent occurrence of the given day
        while today.weekday() != days[detail]:
            today -= timedelta(days=1)

        # Collect all occurrences within the past year
        while today >= one_year_ago:
            dates_list.append(today)
            today -= timedelta(days=7)

    elif frequency.lower() == "monthly":
        if detail.lower() == "last business day":
            # Find last business day of each month
            for month in range(1, 13):
                last_day = date(today.year - 1, month, calendar.monthrange(today.year - 1, month)[1])
                while last_day.weekday() in [5, 6]:  # Skip weekends
                    last_day -= timedelta(days=1)
                dates_list.append(last_day)
        else:
            try:
                specific_day = int(detail)
                if specific_day < 1 or specific_day > 31:
                    return "Invalid day of the month. Enter a number between 1 and 31."

                for month in range(1, 13):
                    try:
                        dates_list.append(date(today.year - 1, month, specific_day))
                    except ValueError:
                        pass  # Skip invalid dates (e.g., Feb 30)
            except ValueError:
                return "Invalid input for monthly frequency. Enter 'last business day' or a specific date."

    else:
        return "Invalid frequency. Choose 'weekly' or 'monthly'."

    return dates_list

# Example usage
freq = input("Enter frequency (Weekly/Monthly): ").title()
detail = input("Enter the specific day (e.g., 'Friday' for weekly, 'Last Business Day' or a number for monthly): ").title()
past_dates = get_past_dates(freq, detail)
print(past_dates)