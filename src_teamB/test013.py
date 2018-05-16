import pymysql.cursors

connection= pymysql.connect(host="localhost", user="root")

try:
    with conection.cursor() as cursor:
        sql = "SELECT * FROM CITY_CODE_TABLE"
        cursor.execute(sql)
        result = cursor.fetchall()

        for data in result:
            city_name = data[0]
            city_code = data[1]
            print("{0},{1}".format(city_name, city_code))
except:
    print("ERROR")
