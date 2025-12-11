from datetime import datetime

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("[%H:%M:%S]")
print(f"Formatted Current Time: {formatted_time}")