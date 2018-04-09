
# coding: utf-8

# In[4]:

import os


# In[5]:

import sqlite3


# In[20]:

import dash


# In[21]:

import pandas as pd


# In[7]:

import dash_core_components as dcc


# In[8]:

import dash_html_components as html


# In[9]:

import plotly.graph_objs as go


# In[10]:

import pandas as pd


# In[11]:

import tushare as ts


# In[12]:

import dash_table_experiments as dt


# In[13]:

from dash.dependencies import Output, Input


# In[14]:

from datetime import datetime


# In[15]:

shareIndex = ts.get_index()


# In[16]:

app = dash.Dash(__name__)


# In[17]:

app.layout = html.Div([
        #page title
        html.Title("Share Analystic"),
        
        #Page top
        html.Div([
                #Logo
                html.Div([
                        html.Label('Shares Analytic')
                    ], style = {'height':'20px', 'width':'20%', 'background-color':'rgb(120,120,120)'}),
                
                html.Div([],style = {'height':'20px', 'width':'60%', 'background-color':'rgb(120,120,120)'}),
                
                #User Management
                html.Div([
                        #User Message
                        html.Div([
                                html.Label('Message')
                            ]),
                        #User Infor
                        html.Div([
                                html.Label('Info')
                            ])
                    ],style = {'height':'20px', 'width':'20%', 'background-color':'rgb(120,120,120)'})
            ]),
        #Page medium
        html.Div([
                #Left 
                html.Div([
                        
                        #global view
                        html.Label('Global View'),
                        
                        #Self chosse
                        html.Label('Global View'),
                        
                        #Dragon data
                        html.Label('Global View'),
                        
                        #investment data
                        html.Label('Global View'),
                        
                        #classification data
                        html.Label('Global View'),
                        
                        #basic info
                        html.Label('Global View'),
                        
                        #macro data
                        html.Label('Global View'),
                        
                        #entre bank
                        html.Label('Global View'),
                    ], style = {'height':'1200px', 'width':'200px', 'background-color':'rgb(240,240,240)'}),
                
                #Main page
                html.Div([
                        #Global View
                        html.Div([
                                html.Div([
                                        
                                        html.Label("Choose Index:"),
                                        dcc.Dropdown(
                                            id = "choose_index",
                                            options = [{'label': i, 'value':i} for i in shareIndex['code'] + shareIndex['name']],
                                            value = str(shareIndex['code'][0] + shareIndex['name'][0])
                                        ),
                                        dcc.RadioItems(
                                            id = 'choose_index_type',
                                            options = [{'label': i, 'value': i} for i in ['day', 'week', 'month']],
                                            value = 'day',
                                            labelStyle = {'display': 'inline-block'}
                                        )  
                                    ], style = {'width':'400px'}),
                                
                                dcc.Graph(id = 'global_view_graph'),
                                
                                
                            ]),
                        #selfchoose items
                        html.Div([
                                                                
                                #left choose bar
                                html.Div([
                                        
                                        html.Div([
                                                html.Label('Search ...'),
                                                dcc.Input(id = 'search_key_word', type = 'text', value = ''),
                                                dt.DataTable(
                                                    id = 'search_result_table',
                                                    rows = [{}],
                                                    row_selectable = True,
                                                    filterable = True,
                                                    sortable = True,
                                                    selected_row_indices = []
                                                )
                                            ])
                                    ]),
                                
                                #right real-time performance
                                html.Div([
                                        dcc.Graph(id='search_real_time')
                                    ])
                            ])
                        
                        
                        
                    ])
            ], style = {'height':'70%', 'width':'80%', 'background-color':'rgb(255,255,255)'}),
        #Page Bottom
        html.Div([
                #Copyright
                html.Div([], style = {'height':'10%', 'width':'100%', 'background-color':'rgb(240,240,240)'})
            ])
        
        
        
    ])


# In[18]:

#global view choose index
@app.callback(
Output('global_view_graph', 'figure'),
    [Input('choose_index', 'value'),
    Input('choose_index_type', 'value')]
)
def change_global_view(choose_index, choose_index_type):
    #shareCode = shareIndex.loc[shareIndex['name'] == choose_index]['code']
    shareCode = str(choose_index[0:6])
    sharePeriodType = choose_index_type[0].upper()
    
    shareChooseData = ts.get_k_data(shareCode, '2016-01-01',datetime.now().strftime('%Y-%m-%d'),sharePeriodType)
    
    return {
        'data':[
            go.Candlestick(
                x = shareChooseData['date'],
                open = shareChooseData['open'],
                high = shareChooseData['high'],
                low = shareChooseData['low'],
                close = shareChooseData['close']
                
            )
        ],
        'layout': go.Layout(
            xaxis = {
                'title': 'Date'
            },
            yaxis = {
                'title': 'Index'
            },
            margin = {'l':40, 'b': 40, 't': 10, 'r': 0},
            hovermode = 'closest'
        )
    }
    


# In[22]:

@app.callback(
Output('search_result_table', 'rows'),
[Input('search_key_word', 'value')])
def search_share(search_key_word):
    shareList = ts.get_stock_basics()
    shareList['search'] = str(shareList['name']).find(search_key_word)
    result = shareList.loc[shareList['search'] > -1]
    result['code'] = result.index
    result = result[['code', 'name','industry']]
    return result.to_dict('records')


# In[23]:

@app.callback(
Output('search_real_time','figure'),
[Input('search_result_table', 'selected_row_indices')])
def create_real_time_graph(selected_row_indices):
    search_code = str(selected_row_indices)
    shareChooseData = ts.get_k_data(search_code, '2016-01-01',datetime.now().strftime('%Y-%m-%d'),'D')
    return {
        'data':[
            go.Candlestick(
                x = shareChooseData['date'],
                open = shareChooseData['open'],
                high = shareChooseData['high'],
                low = shareChooseData['low'],
                close = shareChooseData['close']
                
            )
        ],
        'layout': go.Layout(
            xaxis = {
                'title': 'Date'
            },
            yaxis = {
                'title': 'Index'
            },
            margin = {'l':40, 'b': 40, 't': 10, 'r': 0},
            hovermode = 'closest'
        )
    }
    


# In[35]:

if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:



