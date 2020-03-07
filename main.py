import dash
import dash_design_kit as ddk
import dash_core_components as dcc
from dash.dependencies import Output,Input
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import requests

r = requests.get("https://financialmodelingprep.com/api/v3/symbol/available-cryptocurrencies")
symbols = [{"label": i["name"], "value": i["symbol"]} for i in r.json()]
time = [{"label":"1 min","value":"1min"},
        {"label":"5 min","value":"5min"},
        {"label":"15 min","value":"15min"},
        {"label":"30 min","value":"30min"},
        {"label":"1 hour","value":"1hour"}]
app = dash.Dash()

app.layout = ddk.App(show_editor=True,children=[ddk.ControlCard(width=50,children=[ddk.ControlItem(children=[dcc.Dropdown(id="dd1",options=symbols,value="BTCUSD")])]),
                               ddk.ControlCard(width=25,children=[ddk.ControlItem(children=[dcc.Dropdown(id="dd2",options=time,value="15min")
                                                                                            ])]),
                               ddk.ControlCard(width=25,children=[ddk.ControlItem(children=[dcc.Input(id="Input_Value", value=5)])]),
                               ddk.Card(children=[ddk.Graph(id="graph")])





])

@app.callback(Output("graph","figure"),[Input("dd1","value"),Input("dd2","value"),Input("Input_Value","value")])
def update_graph(dd1,dd2,Input_Value):
    r = requests.get("https://financialmodelingprep.com/api/v3/historical-chart/%s/%s" %(dd2,dd1))
    df = pd.DataFrame.from_dict(r.json())
    df["date"] = pd.to_datetime(df["date"])
    df["SMA"] = df["close"].rolling(int(Input_Value)).mean()
    data = [go.Scatter(x=df["date"], y=df['close'],name="Price"),go.Scatter(x=df["date"], y=df['SMA'],name="SMA %s" %(Input_Value))]
    return {"data": data,"layout": go.Layout(xaxis={
        'showgrid': False
    },
        yaxis={
            'showgrid': False
        })
            }



app.run_server(debug=True,port=8000)