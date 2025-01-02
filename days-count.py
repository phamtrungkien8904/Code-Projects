from datetime import datetime

# Today's date
today = datetime.today()

start_date = datetime(2024, 6, 12)

# Target date
target_date = datetime(2025, 3, 2)

# Difference in days
days_duration = (target_date - today).days
print(days_duration)
