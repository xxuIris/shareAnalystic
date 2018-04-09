
# coding: utf-8

# In[1]:

import dash


# In[2]:

import dash_core_components as dcc


# In[3]:

import dash_html_components as html


# In[4]:

import pandas as pd


# In[5]:

from dash.dependencies import Output, Input


# In[6]:

from datetime import datetime


# In[7]:

import tushare as ts


# In[8]:

import plotly.graph_objs as go


# In[9]:

import dash_table_experiments as dt


# In[17]:

app = dash.Dash(__name__)


# In[ ]:

searchResult = []


# In[14]:

app.layout = html.Div([
        #search function
        html.Label('SEARCH ...'),
        dcc.Input(id = 'search_key_word', type = 'text', value = ''),
        html.Button('+', id = 'add_new_stock_button'),
        dt.DataTable(
            id = 'search_result_table',
            rows = [{}],
            row_selectable = True,
            filterable = False,
            sortable  = False,
            selected_row_indices = []
        ),
        html.Div(id = 'search_result_graph')
    ])


# In[15]:

@app.callback(
Output('search_result_table','rows'),
[Input('search_key_word', 'value')])
def search_stock(search_key_word):
    totalStock = ts.get_stock_basics()
    totalStock['code'] = totalStock.index
    totalStock['search'] = str(totalStock['name']).find(search_key_word)
    searchStock = totalStock.loc[totalStock['search']>-1]
    searchResult = searchStock
    result = searchStock[['code', 'name', 'industry']]
    return result.to_dict('records')


# In[16]:

@app.callback(
Output('search_result_graph', 'children'),
[Input('search_result_table', 'selected_row_indices')])
def show_search_result(selected_row_indices):
    row = selected_row_indices[0]
    searchStockCode = searchResult.code[row]
    return searchStockCode


# In[ ]:

if __name__ == '__main__':
    app.run_server(debug=True)

