from datetime import datetime, timedelta
import mysql.connector


def execute_sql_command(command, operation="read"):
    conn = mysql.connector.connect(host="localhost", user="root", database="Alvaro_DB")
    cursor = conn.cursor()
    cursor.execute(command)
    if operation in ('insert', 'delete'):
        conn.commit()
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


class Date:
    start_hour = False  # datetime.now()
    end_hour = False  # datetime.now()
    start_register = True
    register = 0

    def __init__(self, date):
        self.date = date

    def check_date(self, date_format):
        try:
            reg_time = datetime.strptime(self.date, date_format)
        except ValueError:
            return False
        else:
            return reg_time

    def check_date_existance(self, reg_date):
        sql_command = f"SELECT * FROM Job_Hour_Register WHERE Date = '{reg_date}'"
        return execute_sql_command(sql_command)

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
            Date.register = hours_number
            register = f"Day: {Date.start_hour.strftime('%d-%b-%Y')} Start: {Date.start_hour.strftime('%H:%M')} End: {Date.end_hour.strftime('%H:%M')} Hours_number: {hours_number}\n"
            msg = f"""!!Record entered successfully!!\n\n{register}\n\nDo you want to save this record ? (yes/no)"""
            return msg
        else:
            cancel()
            return 'The init-time should be greater than end-time please start again'

    def manage_file_storage():
        a = Date.start_hour.strftime('%Y-%m-%d')
        b = Date.start_hour.strftime('%H:%M')
        c = Date.end_hour.strftime('%H:%M')
        sql_command = f"INSERT INTO Job_Hour_Register VALUES ('{a}', '{b}', '{c}', {Date.register});"
        execute_sql_command(sql_command, 'insert')


class Report:
    names_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                    9: 'September', 10: 'October', 11: 'November', 12: 'December', }
    wage_hour = 9.5

    def validate_month(self, input_user):
        month_name = input_user[0:3]
        try:
            month_number = datetime.strptime(month_name, '%b').month
        except ValueError:
            return 'Month name is incorrect, try again: '
        else:
            return self.review_month_info(month_number)

    def review_month_info(self, month_number):  # check month existance
        sql_command = f"SELECT * FROM Job_Hour_Register WHERE MONTH(Date) = {month_number}"
        month_data = execute_sql_command(sql_command)
        info = ""
        total_month_hour = 0
        if month_data:
            for item in month_data:
                info += f"Date:{item[0].strftime('%d-%b-%Y')}, Start:{item[1]}, End:{item[2]}, Hours:{item[3]}\n"
                total_month_hour += item[-1]
        else:
            msg = f'Sorry I do not have information about {Report.names_months[month_number]}'
            return msg

        total_hour = round(total_month_hour, 2)
        total_wages = round(total_month_hour * Report.wage_hour, 2)
        return f'{info}\nSummary\nMonth: {self.names_months[month_number]}\nTotal Hours : {total_hour}\nTotal Wages: {total_wages}£'

    def get_day_info(self, day_data):
        info = f"Date:{day_data[0][0].strftime('%d-%b-%Y')}, Start:{day_data[0][1]}, End:{day_data[0][2]}, Hours:{day_data[0][3]}"
        total_day_hour = day_data[0][3]
        total_wages = round(total_day_hour * Report.wage_hour, 2)
        return f'{info}\nTotal Wages: {total_wages}£\n\nAre you sure delete this date (yes/no): '

    def delete_record(self, day):
        sql_command = f"DELETE FROM Job_Hour_Register WHERE Date = '{day}'"
        execute_sql_command(sql_command, 'delete')


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


def fibo(n):
    if n in (1, 2):
        return 1
    if n > 2:
        return fibo(n-2) + fibo(n-1)

    return ValueError





