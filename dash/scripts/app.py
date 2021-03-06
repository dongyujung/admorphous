import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime

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
    query1 = "SELECT window_end, max(count) " \
             "FROM views_page " \
             "WHERE document_id='42744'" \
             "GROUP BY window_end " \
             "ORDER BY window_end;"
    #"SELECT produce_time, count FROM views_page WHERE document_id='42744';"
    cursor.execute(query1)
    rows1 = cursor.fetchall()

    [doc_ts_raw, doc_count] = map(list, zip(*rows1))
    print(doc_ts_raw)

    doc_ts = [datetime.fromtimestamp(x / 1e3) for x in doc_ts_raw]

    print(doc_ts)

    query2 = "SELECT produce_time, count FROM impressions_ad WHERE ad_id='149541';"
    cursor.execute(query2)
    rows2 = cursor.fetchall()

    [ad_ts1, ad_count1] = map(list, zip(*rows2))

    query3 = "SELECT produce_time, count FROM impressions_ad WHERE ad_id='149539';"
    cursor.execute(query3)
    rows3 = cursor.fetchall()

    [ad_ts2, ad_count2] = map(list, zip(*rows3))


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
doc_layout = go.Layout(title='Pageviews (10 minute window)',
                   template='plotly_white',
                   hovermode='closest')
doc_fig = go.Figure(data=[doc_trace],
                layout=doc_layout)

# Impressions Plot1
ad_trace1 = go.Scatter(
    x=ad_ts1, y=ad_count1,
    name='ad_counts1',
    line={'width': 2, 'color': '#00cccc'}
)
ad_layout1 = go.Layout(title='Impressions: Ad_ID 149541 ',
                   template='plotly_white',
                   hovermode='closest')
ad_fig1 = go.Figure(data=[ad_trace1],
                    layout=ad_layout1)

# Impressions Plot2
ad_trace2 = go.Scatter(
    x=ad_ts2, y=ad_count2,
    name='ad_counts2',
    line={'width': 2, 'color': '#00cccc'}
)
ad_layout2 = go.Layout(title='Impressions: Ad_ID 149539 ',
                   template='plotly_white',
                   hovermode='closest')
ad_fig2 = go.Figure(data=[ad_trace2],
                    layout=ad_layout2)


# Create a layout
app.layout = html.Div([
    html.Div([
        # Header
        html.H3("AdMorphous Dashboard")
    ],
        style={'padding': '5px',
               'backgroundColor': '#FFFFFF',
               'textAlign': 'center'}
    ),


    html.Div([
        html.Div([
            # Header
            html.H3("Advertiser view")
        ],
            style={'padding': '5px',
                   'backgroundColor': '#00cccc',
                   'textAlign': 'center'}
        ),

        # Header
        html.H5("Advertiser #2670: Your Metrics"),

        # Impressions Plot
        dcc.Graph(id='impressions1',
                  figure=ad_fig1),

        # Impressions Plot
        dcc.Graph(id='impressions2',
                  figure=ad_fig2)
    ],
        className="five columns"
    ),

    html.Div([
        html.Div([
            # Header
            html.H3("Platform view")
        ],
            style={'padding': '5px',
                   'backgroundColor': 'rgb(229, 151, 50)',
                   'textAlign': 'center'}
        ),

        # Header
        html.H5("Page #42744"),

        # Pageviews Plot
        dcc.Graph(id='pageviews',
                  figure=doc_fig)
    ],
        className="five columns"
    )
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True, port=80, host='0.0.0.0')