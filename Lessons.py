import datetime, config, pymysql

def get_weekday(days):
    raw_week_num = datetime.datetime.today().weekday()+1
    week_num = raw_week_num + days
    if week_num > 7:
        week_num -= 7
    return config.weekday_translator[week_num]

def get_lessons(days=0):
    try:
        weekday = get_weekday(days)
        con = pymysql.connect(config.db_addr, config.db_user, config.db_password, config.db_name)
        cur = con.cursor()
        cur.execute("SELECT * FROM "+weekday)
        result = cur.fetchall()
        if result == ():
            result = "no_data_for_day"
        return result

    except pymysql.err.ProgrammingError as e:
        if eval(str(e))[0] == 1146:
            return "table_not_exists"
        else:
            return "unknown_err"
