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

    [doc_ts, doc_count] = map(list, zip(*rows))
    print(doc_ts)
    print(doc_count)

    query2 = "SELECT created_on, count FROM impressions_ad WHERE ad_id='149541';"
    cursor.execute(query2)
    rows = cursor.fetchall()

    [ad_ts, ad_count] = map(list, zip(*rows))
    print(ad_ts)
    print(ad_count)



except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Pageviews Plot
doc_trace = go.Scatter(
    x=doc_ts, y=doc_count,
    name='doc_counts',
    line={'width': 2, 'color': 'rgb(229, 151, 50)'}
)
doc_layout = go.Layout(title='Platform View: Pageviews / page / 10 min',
                   template='plotly_white',
                   hovermode='closest')
doc_fig = go.Figure(data=[doc_trace],
                layout=doc_layout)

# Impressions Plot
ad_trace = go.Scatter(
    x=ad_ts, y=ad_count,
    name='ad_counts',
    line={'width': 2, 'color': '#00cccc'}
)
ad_layout = go.Layout(title='Advertiser View: Impressions / Ad',
                   template='plotly_white',
                   hovermode='closest')
ad_fig = go.Figure(data=[ad_trace],
                layout=ad_layout)


# Create a layout
app.layout = html.Div([
    html.Div([
        # Header
        html.H1("AdMorphous Dashboard")
    ],
        style={'padding': '10px',
               'backgroundColor': '#FFFFFF'}
    ),

    # Pageviews Plot
    dcc.Graph(id='pageviews',
              figure=doc_fig),

    # Impressions Plot
    dcc.Graph(id='impressions',
              figure=ad_fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=80, host='0.0.0.0')