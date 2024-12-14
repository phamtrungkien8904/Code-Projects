from datetime import datetime
from plyer import notification
import schedule
import time

def show_notification():
    # Today's date
    today = datetime.now()

    # Target date
    target_date = datetime(2025, 3, 2)

    # Days remaining
    days_left = (target_date - today).days

    # Display notification
    notification.notify(
        title="Loa Loa!!!",
        message=f"Còn {days_left} ngày để hai em bé gặp nhau.",
        app_name="Vietnam Coundown",
        timeout=10
    )

# Schedule the notification at 6:00 PM every day
schedule.every().day.at("18:09").do(show_notification)

print("Notification scheduler is running...")
while True:
    schedule.run_pending()
    time.sleep(1)
