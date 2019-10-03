import psycopg2
import config

# Postgres settings
table = 'test'
db_host_ip = "10.0.0.5"
db_port = "5432"
db_type = "postgres"
usr = config.username
pwrd = config.password

try:
    print("1")
    connection = psycopg2.connect(user=usr,
                                  password=pwrd,
                                  host=db_host_ip,
                                  port=db_port,
                                  database=db_type)
    print("2")
    cursor = connection.cursor()
    print(3)
    query1 = "SELECT id, count FROM test WHERE platform = 2;"
    print(4)
    result = cursor.execute(query1)
    print(5)
    rows = result.fetchall()
    print(6)
    print(rows)

    connection.commit()
    print(7)
except Exception as e: print(e)
finally:
    cursor.close()
    connection.close()
