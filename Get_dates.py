from datetime import date, timedelta
import calendar

def get_dates(frequency, detail):
    today = date.today()
    start_date = today - timedelta(days=365)  # One year ago
    dates_list = []

    if frequency.lower() == "weekly":
        days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                "Friday": 4, "Saturday": 5, "Sunday": 6}

        if detail not in days:
            return f"Invalid day name: {detail}. Please enter a valid day."

        while start_date.weekday() != days[detail]:
            start_date += timedelta(days=1)

        while start_date <= today:
            dates_list.append(start_date)
            start_date += timedelta(days=7)

    elif frequency.lower() == "monthly":
        for month_offset in range(12):
            month = (start_date.month + month_offset) % 12 or 12
            year = start_date.year if month >= start_date.month else start_date.year + 1

            if detail.lower() == "last business day":
                last_day = date(year, month, calendar.monthrange(year, month)[1])
                while last_day.weekday() in [5, 6]:  # Skip weekends
                    last_day -= timedelta(days=1)
                dates_list.append(last_day)
            else:
                try:
                    specific_day = int(detail)
                    if 1 <= specific_day <= 31:
                        try:
                            dates_list.append(date(year, month, specific_day))
                        except ValueError:
                            pass  # Skip invalid dates (e.g., Feb 30)
                    else:
                        return "Invalid day of the month. Enter a number between 1 and 31."
                except ValueError:
                    return "Invalid input for monthly frequency. Enter 'last business day' or a specific date."

    else:
        return "Invalid frequency. Choose 'weekly' or 'monthly'."

    return dates_list

# Example usage
freq = input("Enter frequency (Weekly/Monthly): ").title()
detail = input("Enter the specific day (e.g., 'Friday' for weekly, 'Last Business Day' or a number for monthly): ").title()
dates = get_dates(freq, detail)
print(dates)