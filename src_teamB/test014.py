import MySQLdb

connection = MySQLdb.connect(
    #host='localhost', user='root', passwd='yourpass', db='sample_db', charset='utf8')
    host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')
    
try:
    with connection.cursor() as cursor:
        sql = "SELECT CITY_CODE FROM CITY_CODE_TABLE WHERE CITY_NAME =" + "'東京'"
        cursor.execute(sql)
        result = cursor.fetchall()

        print(result[0][0])
        
        for data in result:
            city_code = data[0]
            print("{0}".format(city_code))
except:
    print("ERROR")
