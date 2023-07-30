import time

def _format_datetime(datetime):
    return "{:02}/{:02}/{} {:02}:{:02}:{:02}".format(
        datetime.tm_mday,
        datetime.tm_mon,
        datetime.tm_year,
        datetime.tm_hour,
        datetime.tm_min,
        datetime.tm_sec,
    )

class ConsoleLogger:       
    def info(self, message):
        current_unix_time = time.localtime()
        current_struct_time = time.struct_time(current_unix_time)
        current_date = "{}".format(_format_datetime(current_struct_time))
        print('INFO[{}]: {}'.format(current_date, message))