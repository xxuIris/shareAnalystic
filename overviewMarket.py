
# coding: utf-8

# In[11]:

import dash


# In[12]:

import tushare as ts


# In[13]:

import dash_core_components as dcc


# In[14]:

import dash_html_components as html


# In[15]:

from dash.dependencies import Output, Input, State


# In[16]:

from datetime import datetime


# In[21]:

import plotly.graph_objs as go


# In[17]:

import dash_table_experiments as dt


# In[22]:

from datetime import datetime


# In[ ]:

index_names = ts.get_index()


# In[18]:

app = dash.Dash(__name__)


# In[19]:

app.layout = html.Div([
        html.Div([
            html.H1('STOCK MARKET OVERVIEW')
            ], style={
                'background-color':'#7FFFD4', 
                'height':'100px',
                'border-style':'solid 1px',
                'font-style':'Georgia',
                'color':'white'
            }),
        html.Div([
            html.H2('INDEX OVERVIEW')
            ],
                style={
                'background-color':'#7FFFD4',
                'height':'60px',
                'margin-top':'5px',
                'font-style':'Georgia',
                'color':'white'
            }),
        #index
        html.Div([
                #controler
                html.Div([
                        html.H3('Period'),
                        dcc.DatePickerRange(
                            id = 'index_k_date',
                            min_date_allowed = datetime(1995,8,5),
                            max_date_allowed = datetime(datetime.today().year, datetime.today().month, datetime.today().day),
                            initial_visible_month = datetime(datetime.today().year, datetime.today().month, datetime.today().day),
                            end_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
                        ),
                        html.H3('Index'),
                        dcc.Dropdown(
                            id = 'index_k_name'
                        ),
                        html.H3('K Line Type'),
                        dcc.Dropdown(
                            id = 'k_type_select',
                            options = ({'label':'Day', 'value':'D'},
                                      {'label':'Week', 'value':'W'},
                                      {'label':'Month', 'value':'M'}),
                            value = 'D',
                            placeholder='select a stock...'
                        )
                    ], style = {
                                'font_size':'10px',
                                'font-style':'Georgia'
                            }),
                #graph
                html.Div([
                        dcc.Graph(id = 'index_k_line')
                    ])
            ], style = {
                'height':'500px',
                'background-color':'#F0F8FF'
            })
        
    ], style = {
        'width':'70%',
        'margin':'0 auto'
    })


# In[20]:

if __name__=='__main__':
    app.run_server(debug=True)


# In[ ]:



