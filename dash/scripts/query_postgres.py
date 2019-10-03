import psycopg2
import config

# Postgres settings
table = 'test'
db_host_ip = "10.0.0.5"
db_port = "5432"
db_type = "postgres"
usr = config.username
pwrd = config.password

connection = None
cursor = None

try:
    connection = psycopg2.connect(user=usr,
                                  password=pwrd,
                                  host=db_host_ip,
                                  port=db_port,
                                  database=db_type)
    cursor = connection.cursor()
    query1 = "SELECT id, count FROM test WHERE platform = 2;"
    cursor.execute(query1)
    rows = cursor.fetchall()

    (id, count) = zip(*rows)
    print(id)
    print(count)
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()
