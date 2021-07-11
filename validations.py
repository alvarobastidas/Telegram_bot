import re
from datetime import datetime, timedelta


class Date:
    start_hour = False  # datetime.now()
    end_hour = False  # datetime.now()
    start_register = True
    register = ""

    def __init__(self, date):
        self.date = date
        self.months = []
        self.database = []

    def check_date(self, date_format):
        try:
            reg_time = datetime.strptime(self.date, date_format)
        except ValueError:
            return False
        else:
            return reg_time

    def correct_date_format(self, to_validate):  # to_validate = 3-jul-2021
        date_list = to_validate.split("-")  # = ['3', 'jul', '2021']
        date_list[1] = date_list[1].capitalize()  # = 'Jul'
        if len(date_list[0]) == 1:  # = '3'
            date_list[0] = '0' + date_list[0]  # = '03'
        return "-".join(date_list)  # = '03-Jul-2021'

    def check_date_existance(self, reg_date):
        self.months = Report().months
        if reg_date in self.months:
            return True
        else:
            return False

    def set_hour(self, reg_time):
        if Date.start_register and not Date.start_hour and not Date.end_hour:
            Date.start_hour = reg_time
            msg = f"Enter the end time and date:"
            return msg

        if Date.start_register and Date.start_hour and not Date.end_hour:
            Date.end_hour = reg_time
            return self.calculate_job_hours()

        return 'Sorry I do not recognise your input'

    def calculate_job_hours(self):
        job_time = Date.end_hour - Date.start_hour
        if job_time > timedelta(0):
            hours_number = round(job_time.seconds / 3600, 2)
            Date.register = f"Day: {Date.start_hour.strftime('%d-%b-%Y')} Start: {Date.start_hour.strftime('%H:%M')} End: {Date.end_hour.strftime('%H:%M')} Hours_number: {hours_number}\n"
            msg = f"""!!Record entered successfully!!\n\n{Date.register}\n\nDo you want to save this record ? (yes/no)"""
            return msg
        else:
            cancel()
            return 'The init-time should be greater than end-time please start again'

    def manage_file_storage():
        with open('job_hours_register.txt', 'a') as file:
            file.write(Date.register)


class Report:
    names_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                    9: 'September', 10: 'October', 11: 'November', 12: 'December', }
    wage_hour = 9.5

    def __init__(self):
        with open('job_hours_register.txt', 'r') as file:
            self.database = file.readlines()
        pattern = '[0-9]+[-][a-z,A-Z]+[-][0-9]+'
        self.months = [re.findall(pattern, line)[0] for line in self.database]

    def validate_month(self, input_user):
        month_name = input_user[0:3]
        try:
            month_number = datetime.strptime(month_name, '%b').month
        except ValueError:
            return 'Month name is incorrect, try again: '
        else:
            return self.review_month_info(month_number)

    def review_month_info(self, month_number): # check month existance
        for item in self.months:
            stored_month = datetime.strptime(item, '%d-%b-%Y').month
            if month_number == stored_month:
                return self. get_month_info(month_number)
        else:
            msg = f'Sorry I do not have information about {Report.names_months[month_number]}'
            return msg

    def get_month_info(self, month_number):
        pattern = '[0-9]+[-][a-z,A-Z]+[-][0-9]+'
        info = ""
        total_month_hour = 0
        for item in self.database:
            month_name = re.findall(pattern, item)[0]
            if month_number == datetime.strptime(month_name, '%d-%b-%Y').month:
                info += item
                item_hour_str = item.strip('\n')
                total_month_hour += float(item_hour_str.split(" ")[-1])

        total_hour = round(total_month_hour, 2)
        total_wages = round(total_month_hour * Report.wage_hour, 2)
        return f'{info}\nSummary\nMonth: {self.names_months[month_number]}\nTotal Hours : {total_hour}\nTotal Wages: {total_wages}£'

    def get_day_info(self, day_number, month_number):
        pattern = '[0-9]+[-][a-z,A-Z]+[-][0-9]+'
        info = ""
        total_day_hour = 0
        for item in self.database:
            date_str = re.findall(pattern, item)[0]
            if day_number == datetime.strptime(date_str, '%d-%b-%Y').day and month_number == datetime.strptime(
                    date_str, '%d-%b-%Y').month:
                info += item
                item_hour_str = item.strip('\n')
                total_day_hour += float(item_hour_str.split(" ")[-1])

        total_wages = round(total_day_hour * Report.wage_hour, 2)
        return f'{info}\nTotal Wages: {total_wages}£\n\nAre you sure delete this date (yes/no): '

    def delete_record(self, date):
        new_database = [item for item in self.database if item.find(date) == -1]
        with open('job_hours_register.txt', 'w') as file:
            for item in new_database:
                file.write(item)


class Bike:
    roi_bike_unit = 2.05
    bicycle_cost = 154.96 + 29.99 + 26.92

    def __init__(self):
        with open('bike_trips.txt', 'r') as file:
            database = file.readlines()
        trips = []
        for item in database:
            a = item.strip('\n').split(',')
            try:
                trips.append(a[1])
            except IndexError:
                break

        self.one_way = int(trips[0])
        self.roi = round(float(trips[1]), 2)
        self.last_update = database[-1].strip('\n')
        self.register = ''

    def add_trip(self, number):
        self.one_way += number
        self.roi = self.one_way * Bike.roi_bike_unit - Bike.bicycle_cost
        self.last_update = datetime.now().strftime('%d-%b-%Y %H:%M')
        self.register = f'one_way, {self.one_way}\nROI, {self.roi}\n{self.last_update}'
        return self.load_trip()

    def delete_trip(self, mode, number):
        self.one_way -= number
        self.roi = self.one_way * Bike.roi_bike_unit - Bike.bicycle_cost
        self.last_update = datetime.now().strftime('%d-%b-%Y %H:%M')
        self.register = f'one_way,{self.one_way}\nround_trip,{self.roi}\n{self.last_update}'
        return self.load_trip()

    def load_trip(self):
        with open('bike_trips.txt', 'w') as file:
            file.write(self.register)
        return 'Journey added successfully'

    def show_roi(self):
        return f'Bike one_way: {self.one_way}\nROI: £{self.roi}\nLast update: {self.last_update}'


def cancel():
    Date.start_hour = False
    Date.end_hour = False
    Date.start_register = False

