import re
from datetime import datetime, timedelta
from validations import Date, Report, Bike


start_msg = """Choose your option:
a) Register a day and worked hours
b) Review your hours and days worked
c) Delete a existent record
d) Bicycle ROI
"""

message = """Time and Day format: 
"hour:min day-month-year" -> 15:30 20-may-2021
use abbreviate months name eg. jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec"""

regex_date_time = '[0-9]+[:][0-9]+.[0-9]+[-][a-z,A-Z]+[-][0-9]+'
regex_date = '[0-9]+[-][a-z,A-Z]+[-][0-9]+'
delete_flag = False
bike_flag = False
report_flag = False
delete_date = ""


def default_responses(input_user):
    global message, delete_flag, bike_flag, report_flag, delete_date

    if input_user in ('hello', 'hi'):
        return "Hi it's a Wage_Bot to help you job hour registration"

    if input_user in ['time', 'date']:
        return datetime.now().strftime('%d-%b-%Y %H:%M:%S')

    if input_user == 'a':
        msg = f"""Enter the start time and date:\n\n{message}\n"""
        return msg

    if re.match(regex_date_time, input_user):
        in_date = Date(input_user)
        date_format = '%H:%M %d-%b-%Y'
        reg_time = in_date.check_date(date_format)
        if reg_time:
            to_validate = input_user.split(" ")[-1]
            reg_date = in_date.correct_date_format(to_validate)
            if in_date.check_date_existance(reg_date):
                return f'Error!! There is already a record with this date {reg_date}'
            else:
                return in_date.set_hour(reg_time)
        else:
            msg = f"""Your input is incorrect\n{message}\nEnter again your time:"""
            return msg

    if re.match(regex_date, input_user):  # Check Date 20-may-2021 for deleting
        del_date = Date(input_user)
        date_format = '%d-%b-%Y'
        reg_time = del_date.check_date(date_format)
        if reg_time:
            day_number = reg_time.day
            month_number = reg_time.month
            reg_date = del_date.correct_date_format(input_user)
            if del_date.check_date_existance(reg_date):
                delete_flag = True
                delete_date = reg_date
                return Report().get_day_info(day_number, month_number)
            else:
                return f'The date: {reg_date} not exist in the database!!'
        else:
            msg = 'Your date format is incorrect\nEnter again your date:'
            return msg

    if input_user == 'yes':
        if delete_flag:
            delete_flag = False
            Report().delete_record(delete_date)
            return 'Record deleted!!'

        if Date.start_register:
            Date.manage_file_storage()
            Date.start_register = False
            Date.start_hour, Date.end_hour = False, False
            Date.register = ""
            return 'Register saved!!'

    if input_user == 'b':
        report_flag = True
        msg = 'x). View current month\ny). Select a month\n\nEnter your option:'
        return msg

    if input_user == 'x':
        if bike_flag:
            return 'Enter the number of journey: '

        if report_flag:
            report_flag = False
            current_month = datetime.now().month
            return Report().review_month_info(current_month)

    if input_user == 'y':
        if bike_flag:
            bike_flag = False
            return Bike().show_roi()

        if report_flag:
            report_flag = False
            return 'Enter a month name: '

    if input_user.capitalize() in Report.names_months.values():
        return Report().validate_month(input_user)

    if input_user == 'c':
        return 'Enter the date for deleting:'

    if input_user in ['cancel', 'no']:
        Date.start_hour = False
        Date.end_hour = False
        Date.start_register = False
        bike_flag, delete_flag, report_flag = False, False, False
        return 'Operation cancelled!!'

    if input_user == 'd':
        bike_flag = True
        return 'x) Add one-way trip\ny)Check Bike ROI\n\nEnter your option:'

    if input_user.isdigit():
        number = int(input_user)
        bike_flag = False
        return Bike().add_trip(number)

    return 'Sorry I do not recognise your input'