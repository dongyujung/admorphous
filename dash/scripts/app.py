import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.io as pio

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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Pageviews Plot
trace_1 = go.Scatter(
    x=timestamp, y=count,
    name='counts',
    line={'width': 2, 'color': 'rgb(229, 151, 50)'}
)
layout = go.Layout(title='Platform View: Pageviews / page / 10 min',
                   template='plotly_white',
                   hovermode='closest')
fig = go.Figure(data = [trace_1],
                layout = layout)

# Create a layout
app.layout = html.Div([
    html.Div([
        # Header
        html.H1("AdMorphous Dashboard")
    ],
        style={'padding': '10px',
               'backgroundColor': '#FFFFFF'}
    ),

    # Plot
    dcc.Graph(id='plot',
              figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=80, host='0.0.0.0')