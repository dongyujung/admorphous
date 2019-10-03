import psycopg2
import config

# Postgres settings
table = 'test'
db_host_ip = "10.0.0.5"
db_port = "5432"
db_type = "postgres"
usr = config.username
pwrd = config.password

connection = psycopg2.connect(user=usr,
                              password=pwrd,
                              host=db_host_ip,
                              port=db_port,
                              database=db_type)

cursor = connection.cursor()

query1 = "SELECT id, count FROM test " \
         "WHERE platform = 2;"

result = cursor.execute(query)
rows = result.fetchall()
print(rows)

connection.commit()
cursor.close()
connection.close()