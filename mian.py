from datetime import datetime, timedelta

start_date = datetime(2000, 1, 1)
end_date = datetime(2025, 12, 31)

delta = timedelta(days=1)

with open("date_wordlist.txt", "w") as f:
    current_date = start_date
    while current_date <= end_date:
        f.write(current_date.strftime("%d%m%Y") + "\n")
        current_date += delta