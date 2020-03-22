import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

#query to pull spc_commons names
soql_get_spc = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=685000' +\
        '&$select=spc_common' +\
        '&$group=spc_common').replace(' ', '%20')

#pull data for spc_options
spc_names = list((pd.read_json(soql_get_spc)).spc_common)
spc_names = list([spc for spc in spc_names if type(spc) == type('str')])

#set spc
spc = spc_names[0]

#Dash app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([

    html.Label('Tree Species'),
    #div for dropdown
    dcc.Dropdown(
        id='spc_common_dropdown',
        options=[{'label': tree, 'value': tree} for tree in spc_names],
        value=spc_names[0]
    ),

    html.Label('Proportion of Trees in Good, Fair and Poor Health by Borough'),
    #div for chart question 1
    html.Div(
        dcc.Graph(id='question1'
              )
    ),

    html.Label('Steward Impact on Tree Health'),
    #div for chart question 2
    html.Div(
        dcc.Graph(id='question2'
              )
    )
])

#call backs

#callback for question 1
@app.callback(dash.dependencies.Output('question1', 'figure'),
              [dash.dependencies.Input('spc_common_dropdown', 'value')]
              )

#update for question 1 figure
def update_fig(input_value):

    #creat qy to pull data specific to spc_common selected
    update_soql = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=685000' + \
                   '&$select=boroname,spc_common,health,count(tree_id) as total' + \
                   '&$where=spc_common=' + "'" + input_value + "'" + \
                   '&$group=boroname,spc_common,health').replace(' ', '%20')

    #create df from qy
    update_soql_df = pd.read_json(update_soql)

    #create go.Bar for each Good, Fair and Poor health trees
    data =[
        #good tree health
        go.Bar(name='Good',
               x=list((update_soql_df[(update_soql_df.health == 'Good')]).boroname),
               y=list((update_soql_df[(update_soql_df.health == 'Good')]).total),
               marker_color='#6B7A8F'
               ),
        #fair tree health
        go.Bar(name='Fair',
               x=list((update_soql_df[(update_soql_df.health == 'Fair')]).boroname),
               y=list((update_soql_df[(update_soql_df.health == 'Fair')]).total),
               marker_color='#F7882F'
               ),
        #poor tree health
        go.Bar(name='Poor',
               x=list((update_soql_df[(update_soql_df.health == 'Poor')]).boroname),
               y=list((update_soql_df[(update_soql_df.health == 'Poor')]).total),
               marker_color='#DCC7AA'
               )
    ]

    layout = {'title': 'Tree Health by Borough for ' + input_value,
              'barmode': 'stack'
              }

    return {
        "data": data,
        "layout": layout
    }


#call back for question 2
@app.callback(dash.dependencies.Output('question2', 'figure'),
              [dash.dependencies.Input('spc_common_dropdown', 'value')]
              )

#update for question 1 figure
def update_fig(input_value):

    #creat qy to pull data specific to spc_common selected
    update_soql = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=685000' + \
                   '&$select=steward,health,count(tree_id) as total' + \
                   '&$where=spc_common=' + "'" + input_value + "'" + \
                   '&$group=steward,health').replace(' ', '%20')

    #create df from qy
    update_soql_df = pd.read_json(update_soql)

    #create go.Bar for each Good, Fair and Poor health trees
    data =[
        #Good
        go.Bar(name='Good',
               x=list((update_soql_df[(update_soql_df.health == 'Good')]).steward),
               y=list((update_soql_df[(update_soql_df.health == 'Good')]).total),
               marker_color='#6B7A8F'
               ),
        #Fair
        go.Bar(name='Fair',
               x=list((update_soql_df[(update_soql_df.health == 'Fair')]).steward),
               y=list((update_soql_df[(update_soql_df.health == 'Fair')]).total),
               marker_color='#F7882F'
               ),
        #Poor
        go.Bar(name='Poor',
               x=list((update_soql_df[(update_soql_df.health == 'Poor')]).steward),
               y=list((update_soql_df[(update_soql_df.health == 'Poor')]).total),
               marker_color='#DCC7AA'
               )

    ]

    layout = {'title': 'Tree Health by Steward Across All Boroughs for ' + input_value,
              'barmode': 'stack'
              }

    return {
        "data": data,
        "layout": layout
    }


if __name__ == '__main__':
    app.run_server(debug=True)