import psycopg2
import config

# Postgres settings
table = 'views_page'
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
    query1 = "SELECT created_on, count FROM views_page WHERE document_id='42744';"
    cursor.execute(query1)
    rows = cursor.fetchall()

    [timestamp, count] = map(list, zip(*rows))
    print(timestamp)
    print(count)
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()