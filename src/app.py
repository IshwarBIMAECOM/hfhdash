from dash import Dash, dcc, Output, Input, ctx, html, State, MATCH
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib as pa
import plotly.express as px
import json



tab_1 = html.Div([dbc.Card(dbc.CardBody([html.P("This data analysis project visulises metrics relevant to the yearly energy output of solar PV array of capacities varying from 3kW to 6kW and further, metrics relevant to assessing the financial feasibility of the array when first cost is subsidised by 25, 50 and 75 percent."),html.P("This was a part of a larger report presented to project stakeholders, elaborating on ways to achieve project goals of affordability and high performance design. The report pertained to the delivery of 20-30 affordable housing units - a part of a larger masterplan for a 17 acre industrial park focused on community development.The site is listed as a place of national importance in the National Registry of Historic places, maintained by the National Parks Service.")]),  className= "card border-light"), dbc.Card([
    dbc.CardHeader(
        html.H5("Model inputs")), 
    dbc.CardBody([html.P([html.Span("Solar azimuth", className= "text-primary")," is the horizontal angle with respect to north, of the Sun's position, measured in a clockwise direction"],className="text-muted"), html.P([html.Span("Solar altitude angle", className="text-primary")," is measured between an imaginary line between the observer and the sun and the horizontal plane the observer is standing on."], className="text-muted"),html.P([html.Span("Tilt", className="text-primary"), " is the angle of inclination of the solar panel with respect to the horizontal plane."], className="text-muted"), html.P([html.Span("Array power", className="text-primary")," is the maximum amount of electricity the system can produce in 1 hour under standard testing conditions."],className="text-muted")
                         ])])])


array_0= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "2.94.npy", allow_pickle = True)
array_1= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "3.45.npy", allow_pickle=True)
array_2= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "3.9.npy", allow_pickle=True)
array_3= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "4.56.npy", allow_pickle=True)
array_4= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "5.24.npy", allow_pickle=True)
array_5= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "6.03.npy", allow_pickle=True)
    
array_list = [array_0, array_1, array_2, array_3, array_4, array_5]
    
TLCC_value_50 = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"TLCC.npy", allow_pickle=True)
LCOE_value_50 = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"LCOE.npy",allow_pickle=True)
TLCC_value_25 = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"TLCC_25.npy", allow_pickle=True)
LCOE_value_25 = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"LCOE_25.npy", allow_pickle=True)
TLCC_value_75 = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"TLCC_75.npy", allow_pickle=True)
LCOE_value_75 = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"LCOE_75.npy", allow_pickle=True)
    
TLCC_list = [TLCC_value_25, TLCC_value_50, TLCC_value_75]
LCOE_list = [LCOE_value_25, LCOE_value_50, LCOE_value_75]
    
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX,dbc.icons.FONT_AWESOME])
server = app.server
marks ={
    0 : "2.94 kW",
    1 : "3.45 kW",
    2 : "3.9 kW",
    3 : "4.56 kW",
    4 : "5.24 kW",
    5 : "6.03 kW"
}
marks_2 = {
    0 : "25%",
    1 : "50%",
    2 : "75%"
}
app.layout= dbc.Container(
    [dbc.Row([dbc.Col([dbc.Button(html.I(className="fa-sharp fa-solid fa-envelope-open-text fa-3x d-flex align-self-center ms-4"), className="btn btn-light d-flex flex-fill m-0 gap-0", id="offcanvas_button"), dbc.Offcanvas(tab_1, is_open=False, id="offcanvas", title="Project info")], className="d-flex m-0",lg=1), dbc.Col(html.H1(["SOLAR PV ANALYSIS FOR", html.Q("BEHIND THE GATE")], style={"padding":"2rem 2rem", "text-align":"center", "backgroundColor": "#F5F5F5", "margin":"0px"}), lg=11, className="m-0")]
    ,className="g-0 m-0"),
    dbc.Row(dbc.Col([html.Div([], id="multi"),html.Div(dbc.Button("add scenario", id="options", n_clicks=0, className = " btn btn-light w-100 d-flex justify-content-center" ), className="gap-0 mt-2 ms-auto w-75 d-flex justify-content-end ")])),
    ],
fluid=True)

@app.callback(
    Output("offcanvas", "is_open"),
    Input("offcanvas_button", "n_clicks"),
    State("offcanvas","is_open")
)
def trigger_offcanvas(n_clicks,is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output({"type":"graf", "index":MATCH}, "figure"),
    Input({"type":"power_input_3", "index":MATCH}, "value")
)
def updategraf(arg):
    colorlist = ["PinkyL", "Peach", "OryeL", "Redor", "BurgyL", "Burg"]
    array = [array_0, array_1, array_2, array_3, array_4, array_5]
    y_label = [y for y in range(10,61)] 
    figure = px.imshow(np.around(array[arg],2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"), y=y_label, color_continuous_scale=colorlist[arg])
    return figure

@app.callback(
    Output("multi", "children"),
    Input("options", "n_clicks"),
    State("multi", "children")
)
def gen_new_layout(arg, div_children):
    graf = dbc.Spinner(children =[dcc.Graph(id={"type":"graf", "index":arg}, figure={})], type="grow", size= "lg")
    array_size_3 = dcc.Slider(0, 5, 1, marks=marks, value=0, id={"type":"power_input_3", "index":arg}, included=False)
    tilt_input_3 = dbc.InputGroup([dbc.InputGroupText("Input desired Tilt"), dbc.Input(id={"type":"tilt_input_3", "index":arg}, placeholder = f"min 10 max 60", type = "number", min = 10, max=60, value = 30)])
    azimuth_input_3 = dbc.InputGroup([dbc.InputGroupText("Input desired azimuth"), dbc.Input(id = {"type":"azimuth_input_3", "index":arg}, placeholder = f"min 0 max 360", value = 180)])
    label_array_size_3=dbc.Label("Choose array power", html_for={"type":"power_input_3", "index":arg})
    level_of_subsidy_3 = dcc.Slider(0,2,1, value=0, marks = marks_2, id={"type":"subsidy_input_3", "index":arg})
    label_level_of_subsidy_3=dbc.Label("Choose first cost subsidy", html_for={"type":"subsidy_input_3", "index":arg})
    card_1 = dbc.Card([dbc.CardHeader([html.H4("TLCC", className="d-inline"),html.Small("($)", className="d-inline justify-content-end")]), dbc.CardBody(html.H1(children="",id={"type":"TLCC_txt","index":arg})),dbc.CardFooter("Lifetime costs discounted to yr 0")])
    card_2 = dbc.Card([dbc.CardHeader([html.H4("Energy gen/yr", className="d-inline"), html.Small("(kWh)", className="d-inline justify-content-end")]), dbc.CardBody(html.H1(children="", id={"type":"EN_txt", "index":arg})),dbc.CardFooter("Energy produced by array in 1 year")])
    card_3 = dbc.Card([dbc.CardHeader([html.H4("LCOE", className="d-inline"),html.Small("($/kWh.)", className="d-inline- justify-content-end")]), dbc.CardBody(html.H1(children="", id={"type":"LCOE_txt","index":arg})),dbc.CardFooter("Unit cost of energy gen over 30yrs")])
    card_4 = dbc.Card(
        dbc.ListGroup(
            [dbc.ListGroupItem(
                html.Div(
                    [html.P(children="Tilt", className="bg-secondary bg-opacity-50 w-25 d-lg-inline-flex"), html.H4(children="", id={"type":"Tilt","index":arg}, className="w-25 text-lg-center d-lg-inline-flex"), html.Small("click on graph to gen value ", className="w-50 text-lg-end d-lg-inline-flex text-muted")]
                )
            ),dbc.ListGroupItem(
                html.Div(
                    [html.P(children = "Azimuth", className="bg-secondary bg-opacity-50 w-25 d-lg-inline-flex"), html.H4(children="", id={"type":"Azimuth","index":arg},className= "w-25 text-lg-center d-lg-inline-flex"), html.Small("click on graph to gen value ", className="w-50 text-lg-end d-lg-inline-flex text-muted")]
                ))
            ]))
    
    
    new_child = dbc.Row([dbc.Col([html.Br(),html.H4(f"Scenario {str(arg)} inputs", className="d-flex justify-content-center"),html.Br(), html.Br(), html.Br(), html.Br(), card_4, html.Br(), html.Br(), label_array_size_3, array_size_3, html.Br(), label_level_of_subsidy_3, level_of_subsidy_3, html.Br()], width=3, lg=3, style={"background-color":"#f9f9f9"}), dbc.Col([html.Br(), html.H4(f"Scenario {str(arg)}", className="d-flex justify-content-center"), graf, dbc.CardGroup([card_1, card_2,card_3]), html.Br()], width=9, lg=9)])
    div_children.append(new_child)
    
    return div_children


@app.callback(
    
    Output({"type":"EN_txt", "index":MATCH}, "children"),
    Output({"type":"TLCC_txt","index":MATCH}, "children"),
    Output({"type":"LCOE_txt","index":MATCH}, "children"),
    Output({"type":"Tilt","index":MATCH}, "children"),
    Output({"type":"Azimuth","index":MATCH}, "children"),
    Input({"type":"graf", "index":MATCH}, "clickData"),
    Input({"type":"power_input_3", "index":MATCH},"value"),
    Input({"type":"subsidy_input_3", "index":MATCH},"value")
)
def update_stats(arg1,arg2,arg3):

      
    for i in range (0,6):
        for j in range(0,3):
            
            if arg2 == i and arg3==j: 
                coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
                coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
                coords_x_card = str(json.dumps(arg1["points"][0]["x"], indent=2))
                coords_y_card = str(json.dumps(arg1["points"][0]["y"], indent=2))
                array = array_list[i]
                coords_z_str = np.around(array.T[coords_x,coords_y],2)
                TLCC_Inter = TLCC_list[j]
                TLCC_value = np.around(TLCC_Inter[i,:,:],2)
                TLCC_test = TLCC_value.T[coords_x,coords_y]
                LCOE_Inter = LCOE_list[j]
                LCOE_value = np.around(LCOE_Inter[i,:,:],2)
                LCOE_test = LCOE_value.T[coords_x,coords_y]
                
          
    return coords_z_str, TLCC_test, LCOE_test, coords_y_card, coords_x_card

    
if __name__=='__main__':
    app.run_server(debug=True)