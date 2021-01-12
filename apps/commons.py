import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from app import app

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Sleep", href="/apps/sleep", external_link=True,)),
        dbc.NavItem(dbc.NavLink("Stress", href="/apps/stress", external_link=True,)),
        dbc.NavItem(dbc.NavLink("Steps", href="/apps/steps", external_link=True)),

    ],
    brand="Health dashboard",
    brand_href="apps/sleep",
    color="#52057b",
    dark="true"
)

