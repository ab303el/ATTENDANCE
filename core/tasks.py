from celery import shared_task
import time


@shared_task
def send_clock_in_alert(employee_name , time_clocked_in):
    """
    This simulates a task that takes 10 seconds to finish.
    (e.g., generating a PDF, contacting a 3rd party HR API, sending an email)
    """
    print(f"starting heavy task for {employee_name}...")

    # Simulate a slow process
    time.sleep(10)

    print(f"SUCCESS: Alert email sent to HR for {employee_name} at {time_clocked_in}")
    return "Task Completed"