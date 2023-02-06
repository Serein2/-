
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_cytoscape as cyto
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output
import warnings
warnings.filterwarnings("ignore")
import sys
import os
import pathlib
import json

import utils.utils as utils, utils.config as config

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
"""
fig
"""

conn = utils.getconnect()
values = ("长沙", '湘潭', '株洲', '北京', '上海')
type = 'pollution'
result, cursor = utils.get_cityinfo(conn,  values, type)
df = utils.getdataFrameBytime(result, cursor)


fig1 = px.line(df, df.index, 'so2', color="city", line_group="city", hover_name="city",
        line_shape="spline", render_mode="svg",template='plotly_white')
fig2 = px.scatter(df, df.index, 'so2', color='city')
fig2.update_layout(showlegend=False)
fig2.update_traces(marker_size=5)

layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=400,
    width=1000
)
fig = go.Figure(data=fig1.data + fig2.data,layout=layout)

fig.update_layout(
    margin=dict(l=200, t=20, b=20),  # 上下左右的边距大小
)

"""
navbar
"""
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                "Article",
                href="https://medium.com/plotly/exploring-and-investigating-network-relationships-with-plotlys-dash-and-dash-cytoscape-ec625ef63c59?source=friends_link&sk=e70d7561578c54f35681dfba3a132dd5",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Source Code",
                href="https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-cytoscape-lda",
            )
        ),
    ],
    brand="Plotly dash-cytoscape demo - CORD-19 LDA analysis output",
    brand_href="#",
    color="dark",
    dark=True,
)

"""
body_layout
"""
body_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            f"""
                -----
                ##### Data:
                -----
                For this demonstration, papers from the CORD-19 dataset* were categorised into
                 topics using
                [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) analysis.

                Each topic is shown in different color on the citation map, as shown on the right.
                """
                        )
                    ],
                    sm=12,
                    md=4,
                ),
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                -----
                ##### Topics:
                -----
                """
                        ),
                        html.Div(
                            "abc",
                            style={
                                "fontSize": 11,
                                "height": "100px",
                                "overflow": "auto",
                            },
                        ),
                    ],
                    sm=12,
                    md=8,
                ),
            ]
        ),
        ])

journal_ser = {'a': 'b'}
app.layout = html.Div([navbar,
    body_layout,
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='example-graph',
                    figure=fig)
            ),
            dbc.Col(
                html.Div("你好")
            )
        ]
    )

    ]
)



if __name__ == "__main__":
    app.run_server(debug=True)
