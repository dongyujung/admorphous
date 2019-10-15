import psycopg2
import config
import numpy as np
import matplotlib.pyplot as plt

# Postgres settings
db_host_ip = "10.0.0.5"
db_port = "5432"
db_type = "postgres"
usr = config.username
pwrd = config.password

connection = None
cursor = None

connection = psycopg2.connect(user=usr,
                              password=pwrd,
                              host=db_host_ip,
                              port=db_port,
                              database=db_type)
cursor = connection.cursor()
query1 = "SELECT produce_time, consume_time FROM views_page;"
cursor.execute(query1)
rows1 = cursor.fetchall()

[doc_p_ts, doc_c_ts] = map(list, zip(*rows1))

np_doc_p_ts = np.array(doc_p_ts)
np_doc_c_ts = np.array(doc_c_ts)

doc_dt = (np_doc_c_ts - np_doc_p_ts) / 1e3

plt.hist(doc_dt, normed=True, bins=30)
plt.savefig('doc_1s.png')


"""
    doc_ts = [datetime.fromtimestamp(x / 1e3) for x in doc_ts_raw]

    print(doc_ts)

    query2 = "SELECT produce_time, count FROM impressions_ad WHERE ad_id='149541';"
    cursor.execute(query2)
    rows2 = cursor.fetchall()

    [ad_ts1, ad_count1] = map(list, zip(*rows2))

"""