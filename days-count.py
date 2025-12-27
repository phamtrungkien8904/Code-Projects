from datetime import datetime

# Today's date
today = datetime.today()

start_date = datetime(2025, 3, 5)

# Target date
target_date = datetime(2026, 1, 1)

# Difference in days
days_duration = (target_date - start_date).days
print(days_duration)
