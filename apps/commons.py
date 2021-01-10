import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Sleep", href="/apps/sleep")),
        dbc.NavItem(dbc.NavLink("Stress", href="/apps/stress")),
        dbc.NavItem(dbc.NavLink("Steps", href="/apps/steps")),

    ],
    brand="Health dashboard",
    brand_href="#",
    color="#52057b",
    dark="true"
)