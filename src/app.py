from dash import Dash, dcc, Output, Input, ctx, html, State
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib as pa
# from dash_extensions import Download
# from dash_extensions.snippets import send_file
import plotly.express as px
import json
   
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server
card_1 = dbc.Card([dbc.CardHeader(html.H4(["NPV",html.Sup("*")])),dbc.CardBody(html.H1(children="", id="NPV_txt")), dbc.CardFooter("Sum of 30yr costs and benefits")])
card_2 = dbc.Card([dbc.CardHeader(html.H4(["TLCC", html.Sup("**")])), dbc.CardBody(html.H1(children="",id="TLCC_txt")),dbc.CardFooter("Lifetime costs discounted to yr 0")])
card_3 = dbc.Card([dbc.CardHeader(html.H4(["Energy gen/yr"])), dbc.CardBody(html.H1(children="", id="EN_txt")),dbc.CardFooter("Energy produced by array in 1 year")])
card_4 = dbc.Card([dbc.CardHeader(html.H4(["LCOE", html.Sup("+")])), dbc.CardBody(html.H1(children="", id="LCOE_txt")),dbc.CardFooter("Unit cost of energy gen over 30yrs")])
array_1= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "2.94.npy", allow_pickle = True)
array_2= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "3.45.npy", allow_pickle=True)
array_3= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "3.9.npy", allow_pickle=True)
array_4= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "4.56.npy", allow_pickle=True)
array_5= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "5.24.npy", allow_pickle=True)
array_6= np.load(pa.PurePath(pa.Path(__name__)).parent / "data" / "6.03.npy", allow_pickle=True)

app.layout =dbc.Container(
    [dbc.Row(html.H1("50% Subsidy"), style={"padding":"2rem 2rem", "text-align":"center"}),
     dbc.Row([dbc.Col(
        "", width = 6, lg=3, style= {"height" : "100"}),
              dbc.Col(
                        dbc.RadioItems(
                            options = [{"label":"2.94kW", "value":1}, {"label":"3.45kW", "value":2}, {"label":"3.9kW","value":3}, {"label":"4.56kW", "value":4}, {"label":"5.24kW", "value":5}, {"label":"6.03kW", "value":6}], value= 1, id= "Power_Input", inline= True),
              width =6, lg=9, style= {"height" : "100"}
              ),
              dbc.Col("", width =6, lg=1, style= {"height" : "100"})
             ],align = "end", style= {"height" : "25"}),
     dbc.Row(
         dcc.Graph(
             id="graf", figure={}
         )
     ), 
     dbc.Row(
        dbc.CardGroup(
            [card_1, card_2, card_3, card_4,])
     ),
     dbc.Row(
         html.H6(
             [html.Sup("*"),"Net Present Value computed at discount rate of 10% P.A"], className= "text-decoration-underline")
     ), 
     dbc.Row(
         html.H6(
             [html.Sup("*"),"TOTAL LIFECYCLE COST"], className= "text-decoration-underline"
         )
     ),
    dbc.Row(
        html.H6(
            [html.Sup("*"),"LEVELIZED COST OF ENERGY"], className= "text-decoration-underline"
        )
    ),
    dbc.Row(
        dbc.Button("show more", class_name = "btn btn-light", id="description", n_clicks=0)
    ),
    dbc.Row(
        dbc.Fade(
            dbc.Card([dbc.CardBody(
                [html.H5("This data analysis project visulises metrics relevant to the yearly energy output of solar PV array of capacities varying from 3kW to 6kW (whose first cost has been subsidised by 50%) and additional metrics relevant to assessing the financial feasibility of the array. This was a part of a larger report presented to project stakeholders elaborating on ways to achieve project goals of affordability and high performance design. The report pertained to the delivery of 20-30 affordable housing units - a part of a larger masterplan for a 17 acre industrial park focused on community development.The site is listed as a place of national importance in the National Registry of Historic places, maintained by the National Parks Service."),
                 ]
                    )]
                
            ), id="fade-transition", is_in=False, appear=False, style={"transition": "opacity 2000ms ease"},timeout=2000
        )
    ),
    
     
    ]
)

@app.callback(
    Output(component_id= "graf", component_property = "figure"),
    Input(component_id= "Power_Input",component_property = "value")
    )
def update_graph(arg):
    
       
    if arg == 1:
        figure = px.imshow(np.around(array_1,2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"),color_continuous_scale=px.colors.sequential.Pinkyl)
    elif arg == 2:
        figure = px.imshow(np.around(array_2,2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"), color_continuous_scale=px.colors.sequential.Peach)
    elif arg == 3:
        figure = px.imshow(np.around(array_3,2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"), color_continuous_scale=px.colors.sequential.Oryel)
    elif arg == 4:
        figure = px.imshow(np.around(array_4,2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"), color_continuous_scale=px.colors.sequential.Redor)
    elif arg == 5:
        figure = px.imshow(np.around(array_5,2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"), color_continuous_scale=px.colors.sequential.Burgyl)
    elif arg == 6:
        figure = px.imshow(np.around(array_6,2), aspect="auto",origin="lower",labels=dict( x="azimuth",y="altitude", color="kWh"), color_continuous_scale=px.colors.sequential.Burg)
    return figure


@app.callback(
    Output(component_id="EN_txt", component_property= "children"),
    Output(component_id="TLCC_txt", component_property= "children"),
    Output(component_id="LCOE_txt", component_property= "children"),
    Output(component_id="NPV_txt", component_property= "children"),
    [Input(component_id="graf", component_property="clickData"),
    Input(component_id= "Power_Input",component_property = "value")]
    )
def update_all(arg1,arg2):
        
    TLCC_value = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"TLCC.npy", allow_pickle=True)
    LCOE_value =np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"LCOE.npy",allow_pickle=True)
    NPV_value = np.load(pa.PurePath(pa.Path(__name__)).parent / "data" /"NPV.npy", allow_pickle=True)
    
    
    if arg2 == 1:
       
        coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
        coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
        coords_z_str = np.around(array_1.T[coords_x,coords_y],2)
        TLCC_value = np.around(TLCC_value[0,:,:],2)
        TLCC_test = TLCC_value.T[coords_x,coords_y]
        LCOE_value = np.around(LCOE_value[0,:,:],2)
        LCOE_test = LCOE_value.T[coords_x,coords_y]
        NPV_value = np.around(NPV_value[0,:,:],2)
        NPV_test = NPV_value.T[coords_x,coords_y]
        if NPV_test >= 0:
          NPV_out = "POSITIVE NPV"
        else:
          NPV_out = "NEGATIVE NPV"
        
        
    
    
    elif arg2 == 2:
        
        coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
        coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
        coords_z_str = np.around(array_2.T[coords_x,coords_y],2)
        TLCC_value = np.around(TLCC_value[1,:,:],2)
        TLCC_test = TLCC_value.T[coords_x,coords_y]
        LCOE_value = np.around(LCOE_value[1,:,:],2)
        LCOE_test = LCOE_value.T[coords_x,coords_y]
        NPV_value = np.around(NPV_value[1,:,:],2)
        NPV_test = NPV_value.T[coords_x,coords_y]
        if NPV_test >= 0:
          NPV_out = "POSITIVE NPV"
        else:
          NPV_out = "NEGATIVE NPV"
    

    elif arg2 == 3:
        coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
        coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
        coords_z_str = np.around(array_3.T[coords_x,coords_y],2)
        TLCC_value = np.around(TLCC_value[2,:,:],2)
        TLCC_test = TLCC_value.T[coords_x,coords_y]
        LCOE_value = np.around(LCOE_value[2,:,:],2)
        LCOE_test = LCOE_value.T[coords_x,coords_y]
        NPV_value = np.around(NPV_value[2,:,:],2)
        NPV_test = NPV_value.T[coords_x,coords_y]
        if NPV_test >= 0:
          NPV_out = "POSITIVE NPV"
        else:
          NPV_out = "NEGATIVE NPV"
        
    

    elif arg2 == 4:
        
        coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
        coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
        coords_z_str = np.around(array_4.T[coords_x,coords_y],2)
        TLCC_value = np.around(TLCC_value[3,:,:],2)
        TLCC_test = TLCC_value.T[coords_x,coords_y]
        LCOE_value = np.around(LCOE_value[3,:,:],2)
        LCOE_test = LCOE_value.T[coords_x,coords_y]
        NPV_value = np.around(NPV_value[3,:,:],2)
        NPV_test = NPV_value.T[coords_x,coords_y]
        if NPV_test >= 0:
          NPV_out = "POSITIVE NPV"
        else:
          NPV_out = "NEGATIVE NPV"
     
           
    

    elif arg2 == 5:
        
        coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
        coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
        coords_z_str = np.around(array_5.T[coords_x,coords_y],2)
        TLCC_value = np.around(TLCC_value[4,:,:],2)
        TLCC_test = TLCC_value.T[coords_x,coords_y]
        LCOE_value = np.around(LCOE_value[4,:,:],2)
        LCOE_test = LCOE_value.T[coords_x,coords_y]
        NPV_value = np.around(NPV_value[4,:,:],2)
        NPV_test = NPV_value.T[coords_x,coords_y]
        if NPV_test >= 0:
          NPV_out = "POSITIVE NPV"
        else:
          NPV_out = "NEGATIVE NPV"        
        
    

    elif arg2 == 6:
        
        coords_x = int(json.dumps(arg1["points"][0]["x"], indent=2))
        coords_y = int(json.dumps(arg1["points"][0]["y"], indent=2))
        coords_z_str = np.around(array_6.T[coords_x,coords_y],2)
        TLCC_value = np.around(TLCC_value[5,:,:],2)
        TLCC_test = TLCC_value.T[coords_x,coords_y]
        LCOE_value = np.around(LCOE_value[5,:,:],2)
        LCOE_test = LCOE_value.T[coords_x,coords_y]
        NPV_value = np.around(NPV_value[5,:,:],2)
        NPV_test = NPV_value.T[coords_x,coords_y]
        if NPV_test >= 0:
          NPV_out = "POSITIVE NPV"
        else:
          NPV_out = "NEGATIVE NPV"

        
    return coords_z_str, TLCC_test, LCOE_test, NPV_out



@app.callback(
    Output("fade-transition", "is_in"),
    Input("description", "n_clicks"),
    State("fade-transition", "is_in"),
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in






if __name__=='__main__':
    app.run_server(debug=True)

    # https://github.com/facultyai/dash-bootstrap-components/issues/286
    