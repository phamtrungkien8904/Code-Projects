from datetime import datetime

# Today's date
today = datetime.today()

# Target date
target_date = datetime(2025, 3, 2)

# Difference in days
days_until = (target_date - today).days
print(days_until)