import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

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

    [pvid, count] = map(list, zip(*rows))
    print(pvid)
    print(count)
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

trace_1 = go.Scatter(
    x = pvid, y = count,
    name = 'counts',
    line = {width = 2, color = 'rgb(229, 151, 50)'}
)
layout = go.Layout(title = 'Pageview Counts',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)

# Create a layout
app.layout = html.Div([
                dcc.Graph(id = 'plot', figure = fig)
                      ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')