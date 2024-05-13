from datetime import datetime

def get_current_date():
    current_date = datetime.now().date()
    return {"current_date": current_date}