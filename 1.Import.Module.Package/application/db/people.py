from datetime import datetime as date

def get_employees():
    print(date.today().strftime('%Y-%m-%d'))
    return f'its fuction {__name__}'
