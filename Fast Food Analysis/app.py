import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, dcc, html, Input, Output ,State
import dash_bootstrap_components as dbc
from datetime import date as dt, timedelta
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import dash
from dash import dash_table
from collections import OrderedDict
import time
import os
from flask_caching import Cache
from collections import Counter
from itertools import combinations
from flask import send_from_directory

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'
                        ,'/assets/style.css']

app = Dash(__name__, external_stylesheets=external_stylesheets ,meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
@app.server.route('/assests/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'assests')
    return send_from_directory(static_folder, path)
cache = Cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
})
app.config.suppress_callback_exceptions = True

timeout = 20


                         #Data Wrangling for Kip Food 1
raw_df_kipfood1=pd.read_csv("path_to_csv")
raw_df_kipfood1.pop(raw_df_kipfood1.columns[0])
raw_df_kipfood1.rename(columns= {"Nr Bon" :"Nr"} , inplace=True)
raw_df_kipfood1.rename(columns={"Tip Plata" :"Pay"} ,inplace=True)
raw_df_kipfood1.rename(columns={"Denumire": "Name"}, inplace=True)
raw_df_kipfood1.rename(columns={"Pret":"Price"},inplace=True)
raw_df_kipfood1.rename(columns={"Cantitate":"Quantity"},inplace=True)
raw_df_kipfood1.rename(columns={"Valoare":"Value"},inplace=True)
products=raw_df_kipfood1['Name'].unique()
raw_df_kipfood1.rename(columns={"Data":"Date"},inplace=True)
raw_df_kipfood1['Date']=pd.to_datetime(raw_df_kipfood1['Date'] ,dayfirst=True)
raw_df_kipfood1['Day']=raw_df_kipfood1['Date'].dt.day
raw_df_kipfood1['Month']=raw_df_kipfood1['Date'].dt.month
raw_df_kipfood1['Year']=raw_df_kipfood1['Date'].dt.year
raw_df_kipfood1['Ora'] = pd.to_datetime(raw_df_kipfood1['Ora'])
raw_df_kipfood1['Hour']=raw_df_kipfood1['Ora'].dt.hour
raw_df_kipfood1['Minute']=raw_df_kipfood1['Ora'].dt.minute
raw_df_kipfood1.drop(['Ora'], axis=1 , inplace=True)
raw_df_kipfood1['Luna']=raw_df_kipfood1['Date'].dt.month_name()


cafea=['CEAI','ESPRESSO', 'IRISH CAPPUCCINO', 'ESPRESSO MARE' ,'LATTE MACCHIATO','CAPPUCCINO MARE ','CAPPUCCINO MIC', 'CAFEA CU LAPTE','LAPTE CONDENSAT ' ,'ESPRESSO MARE']
bauturi=['FRESH DE SEZON' , 'FANTA' , 'KINLEY' , 'COCA COLA' ,'ZMEURA SUC ', 'CAISE NECTAR' , 'AFIN SUC ' , '250 MORCOV MERE  PORTOCALE', 'ARONIA NECTAR ', '500 MORCOV MERE PORTOCALA ', '250 MIX 9 FRUCTE ','250 SFECLA MORCOV PORTOCALA ','500 SFECLA MORCOV PORTOCALA ', '500 PORTOCALE ','PIERSICI NECTAR ','250 RODIE STRUGURI PORTOCALA ',
 '500 RODIE STRUGURI PORTOCALA ' , 'COACAZ NEGRU NECTAR' ,'Lipton',  '250 PORTOCALE' , 'BURN','500 SFECLA MORCOV PORTOCALA',
 'FUZE PEACH' , 'SCHWEPPES MANDARIN' , 'FUZE LEMON', 'SCHWEPPES BITTERLEMON','FUZE FOREST ','FANTA STRUGURI',
 'MONSTER ENERGY' , '500 MIX 9 FRUCTE ' , 'COKE ZERO' , 'FUZE CIRESE SOC' , 'SCHWEPPES RODIE ' , 'APA PLATA ' ,'APA CARBOGAZOASA' ,'FANTA GRAPEFRUIT', 'CAPPY PULPY ',
 'SCHWEPPES PINK ', 'FANTA MYSTERY' , 'NESTEA MANGO' ,  'NESTEA FOREST' , 'LIPTON ' , 'PEPSI  MIRINDA 7UP' , 'PRIGAT','SCHWEPPES POMEGRANATE',
 'APA CARPATICA CARBOGAZOASA', 'APA CARPATICA PLATA' , 'SPRITE' ,'SANA','Prigat','Pepsi ','Aqua Carpatica 0.5L','ACTIVIA','AYRAN']
grill=[' VEGAN SNITZEL  ', 'CEAFA GRILL','KIPPY STRIPS ' ,'ARIPIOARE BBQ' ,'PULPE PUI BBQ', 'SNITZEL PUI' ,'ARIPIOARE PICANTE ', 'MITITEI' , 'PIEPT PORC BBQ', 'COASTE BBQ' ,'POMANA PORCULUI',
 'FRIGARUI DE PUI', 'CARNATI DE PORC' , 'CIOLAN ROTISAT ' , 'PUI ROTISAT ', 'PULPE PUI DEZOSATE ' ,  'PULPE CURCAN ROTISAT ', 'JAMBON ROTISAT',
 'PIEPT DE PORC ROTISAT' ,' SATAY (FRIGARUI DE PORC )',
 'ARIPI CURCAN ROTISATE ' ,'CIOCANELE DE RATA' , 'MUSCHIULET DE PUI' ,'PIEPT DE PUI LA GRATAR', 'FRIPTURA BRASOVEANA']
pizza=['PIZZA NAPOLI','PIZZA KIP ', 'PIZZA CINQUE  TERRE', 'FELIE PIZZA','CHICKEN PIZZA ' ]
sandwich=['CORDON BLEU SANDWICH','SANDWICH ROMA ', 'SANDWICH VIENA', 'SANDWICH PARIS', 'SANDWICH BONN', 'SANDWICH SATURN','FALAFEL SANDWICH', 'CARNIVORE SANDWICH' ]
burger=['BURGER PUI','AMERICAN BURGER', 'KIP BURGER ','L.A. BURGER', 'KRISPY BURGER', 'VEGGIE BURGER ', 'SUPER BURGER', 'BIG BURGER ','TURKEY  BURGER ']
meniu=['MENIU KENTUCKY' , 'MENIU BRASOV', 'MENIU VIENEZ ','Meniu Hamsii', 'MENIU PRAGA ',  'MENIU 4 MICI ','MENIU ARIPIOARE BBQ' ]
speciale=['MAZARE CU PUI', 'SPAGHETE BOLOGNESE' ,'CHILI CON CARNE', 'TOCANITA CU PIPOTE' 'JUMARI DE PESTE '
 'SARAMURA DE MACROU CU MAMALIGA', 'OREZ ARABESC CU PUI' 'FISH N CHIPS ','TOCHITURA ARDELENEASCA ', 'FASOLE CU CIOLAN       ', 'PASTRAV PRAJIT' ,'HAMSII 2',
 'GULAS DE VITA ' , 'OREZ CU PUI ', 'VARZA A LA  CLUJ' ,'PIURE CU CEAFA ','PARJOALE MOLDOVENESTI',
 'PAPRICAS CU MAMALIGUTA','FISH KIP','OREZ ARABESC CU PUI','FISH N CHIPS ', 'TOCANITA CU PIPOTE' ,'JUMARI DE PESTE ',
 'SARAMURA DE MACROU CU MAMALIGA' ]
patiserie=['CROISSANT UNT ', 'BOUGATZA', 'STRUDEL MERE' , 'PLACINTA CU MERE SI SCORTISOARA' ,'PLACINTA CU BRANZA SARATA ',
 'PLACINTA CU B DULCE, MERE SI STAFIDE' ,'PLACINTA DOVLEAC' , 'PLACINTA CU VANILIE']
lipie=['TACO KIP ' , 'CHEESE PITA', 'GYROS PITA' ,'FASII DE PORC','PLE?CAVI?A', 'BURITTO' ,'EFES KEBAB','Shaorma Kip']
garnitura=['INELE DE CEAPA ','CHIFLA PANINI ' ,'CARTOFI GRATINATI CU SMANTANA ' , 'CROCHETE DE CARTOFI ' , 'CARTOFI PAI ' ,'MURATURI', 'CARTOFI CHIPSURI', 'SOS IBIZA ',
                            'SOS MEXICO',   'SOS  CORFU','SOS MIAMI', 'SOS ISTANBUL' ,'SOS TZATZIKI', 'SALATA SANTORINI','SALATA PALERMO','CARTOFI WEDGES ']

hot_dog=['KIP DOG', 'CHICAGO DOG', 'DOUBLE DOG', 'BRATWURST', 'MEGA DOG' ]

values=['Bauturi','Grill','Pizza','Burger','Hot-Dog','Sandwich','Lipie','Meniuri', 'Garnitura','Cafea','Patiserie','Produse Speciale']

conditions1=[
    (raw_df_kipfood1['Name'].isin(bauturi)),
    (raw_df_kipfood1['Name'].isin(grill)),
    (raw_df_kipfood1['Name'].isin(pizza)),
    (raw_df_kipfood1['Name'].isin(burger)),
    (raw_df_kipfood1['Name'].isin(hot_dog)),
    (raw_df_kipfood1['Name'].isin(sandwich)),
    (raw_df_kipfood1['Name'].isin(lipie)),
    (raw_df_kipfood1['Name'].isin(meniu)),
    (raw_df_kipfood1['Name'].isin(garnitura)),
    (raw_df_kipfood1['Name'].isin(cafea)),
    (raw_df_kipfood1['Name'].isin(patiserie)),
    (raw_df_kipfood1['Name'].isin(speciale)),
]

raw_df_kipfood1['Day of Week']=raw_df_kipfood1['Date'].dt.dayofweek
day_conditions=[
    (raw_df_kipfood1['Day of Week']==0),
    (raw_df_kipfood1['Day of Week']==1),
    (raw_df_kipfood1['Day of Week']==2),
    (raw_df_kipfood1['Day of Week']==3),
    (raw_df_kipfood1['Day of Week']==4),
    (raw_df_kipfood1['Day of Week']==5),
    (raw_df_kipfood1['Day of Week']==6),
]
day_values=['Luni', 'Marti','Miercuri','Joi','Vineri','Sambata','Duminica']
month_values=['January','February','March','April','May','June','July','August','September','October','November','December']
month2_values=['October','November','December','January','February','March']
raw_df_kipfood1['Day of Week']=np.select(day_conditions,day_values)
raw_df_kipfood1['Category']=np.select(conditions1,values)

                        #Data Cleaning for Kip Food 2
raw_df_kipfood2=pd.read_csv("path_to_csv")
raw_df_kipfood2.pop(raw_df_kipfood2.columns[0])
raw_df_kipfood2.rename(columns= {"Nr Bon" :"Nr"} , inplace=True)
raw_df_kipfood2.rename(columns={"Tip Plata" :"Pay"} ,inplace=True)
raw_df_kipfood2.rename(columns={"Denumire": "Name"}, inplace=True)
raw_df_kipfood2.rename(columns={"Pret":"Price"},inplace=True)
raw_df_kipfood2.rename(columns={"Cantitate":"Quantity"},inplace=True)
raw_df_kipfood2.rename(columns={"Valoare":"Value"},inplace=True)
products=raw_df_kipfood2['Name'].unique()
raw_df_kipfood2['Data']=pd.to_datetime(raw_df_kipfood2['Data'],dayfirst=True)
raw_df_kipfood2.rename(columns={"Data":"Date"},inplace=True)
raw_df_kipfood2['Day']=raw_df_kipfood2['Date'].dt.day
raw_df_kipfood2['Month']=raw_df_kipfood2['Date'].dt.month
raw_df_kipfood2['Year']=raw_df_kipfood2['Date'].dt.year
raw_df_kipfood2['Ora'] = pd.to_datetime(raw_df_kipfood2['Ora'])
raw_df_kipfood2['Hour']=raw_df_kipfood2['Ora'].dt.hour
raw_df_kipfood2['Minute']=raw_df_kipfood2['Ora'].dt.minute
raw_df_kipfood2.drop(['Ora'], axis=1 , inplace=True)
raw_df_kipfood2['Luna']=raw_df_kipfood2['Date'].dt.month_name()
conditions2=[
    (raw_df_kipfood2['Name'].isin(bauturi)),
    (raw_df_kipfood2['Name'].isin(grill)),
    (raw_df_kipfood2['Name'].isin(pizza)),
    (raw_df_kipfood2['Name'].isin(burger)),
    (raw_df_kipfood2['Name'].isin(hot_dog)),
    (raw_df_kipfood2['Name'].isin(sandwich)),
    (raw_df_kipfood2['Name'].isin(lipie)),
    (raw_df_kipfood2['Name'].isin(meniu)),
    (raw_df_kipfood2['Name'].isin(garnitura)),
    (raw_df_kipfood2['Name'].isin(cafea)),
    (raw_df_kipfood2['Name'].isin(patiserie)),
    (raw_df_kipfood2['Name'].isin(speciale)),
]
raw_df_kipfood2['Day of Week']=raw_df_kipfood2['Date'].dt.dayofweek
day_conditions=[
    (raw_df_kipfood2['Day of Week']==0),
    (raw_df_kipfood2['Day of Week']==1),
    (raw_df_kipfood2['Day of Week']==2),
    (raw_df_kipfood2['Day of Week']==3),
    (raw_df_kipfood2['Day of Week']==4),
    (raw_df_kipfood2['Day of Week']==5),
    (raw_df_kipfood2['Day of Week']==6),
]
raw_df_kipfood2['Day of Week']=np.select(day_conditions,day_values)
raw_df_kipfood2['Category']=np.select(conditions2,values)
valoare_bon1=raw_df_kipfood1.groupby('Nr')['Value'].sum().reset_index()
valoare_bon2=raw_df_kipfood2.groupby('Nr')['Value'].sum().reset_index()
both=[raw_df_kipfood1,raw_df_kipfood2]
ambele_raw_df=pd.concat(both)
app =Dash(external_stylesheets=[dbc.themes.DARKLY])

                                #App Layout
app.layout= html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/assets/style.css'
    ),
    html.Meta(
        content='width=device-width, initial-scale=1.0',
        name='viewport'),
                                    #Title
    html.H1("Statistica Kip Food" , style={"textAlign":"center" ,"font-size":"4em" ,"color":"#00e6e6"}),
                                    #Choose the fast-food dropdown
    html.Div(children=[
    dcc.Dropdown(options=[
       {'label': 'Kip Food 1', 'value': 'kipfood1'},
       {'label': 'Kip Food 2', 'value': 'kipfood2'},
       {'label': 'Ambele', 'value': 'ambele'},
   ],
   value='kipfood1' ,clearable=False,searchable=False, id='dropdown' )
    ], className='dropdown_div'),
                                #Choose the date
    html.Div(children=[
    dcc.DatePickerRange(
    id='datepickerrange',
    min_date_allowed=dt(2020,8,7),
    max_date_allowed=dt(2023,3,15),
    end_date=dt(2023,3,15),
    start_date=dt(2020,8,7),
    number_of_months_shown=3
    )
    ],className='datepicker') ,
                            #Choose the type of pay
    html.Div(children=[
    dbc.Checklist(
     options=[
       {'label': 'Numerar', 'value': 'Numerar'},
       {'label': 'Card', 'value': 'Card'},
   ],
   labelStyle={"margin-right":"20px"},
   id='checkid',
   value=['ambele'],
   inline=True
    )
    ],className='checklist'),
                                #Select different periods
    html.Div(children=[
        dcc.Dropdown(
        id = 'timeframe_dropdown',
        multi = False,
        options = [
            {'label': 'Toata perioada', 'value': 'toata'},
            {'label': 'Ultima zi', 'value': 'zi'},
            {'label': 'Ultimele 7 zile', 'value': '7zile'},
            {'label':'Ultima luna' , 'value':'luna'},
            {'label':'Ultimele 3 luni','value':'3luni'},
            {'label':'Ultimele 6 luni','value':'6luni'},
            {'label':'Ultimul an' , 'value':'an'},
            {'label':'Ultimii 2 ani' , 'value':'2ani'}
        ],
        value='toata',
        clearable=False,
        searchable=False,
    )],className='dropdownperiod'),
                                #Select Day/Hour/Month
    html.Div(children=[
    dbc.RadioItems(
        options=[
                {"label": "Ora", "value": "ora"},
                {"label": "Zi", "value": "zi"},
                {"label": "Luna", "value": "luna"},
            ],
            value='ora',
            id="radioitems",
            inline=True
    )
    ],className="radiobuttons"),
    html.Div(children=[
    html.H3(id='toty')
    ],className='total'),
                        #Line-Chart Graph
    html.Div(children=[
    dcc.Graph(id='linechart')
    ],className='line_chart'),
                        #Pie-Chart Graph
    html.Div(children=[
    dcc.Graph(id='pie-chart')
    ],className='pie_chart'),
                        #Top 5 Table
    html.Div(id='top5table',
    #children=[
    #dash_table.DataTable(
    #id='top5table',
    #data=df.to_dict('records'),
    #columns=[{'id': c, 'name': c} for c in df.columns],
    #editable=True,
    #style_cell={
    #'width':'200px',
    #'height':'50px',
    #'color':'rgb(37, 224, 37)',
    #'background-color':'black',
    #'text-align':'center'
    #}]
    className='top5class'),
                    #Clear Button
    #html.Div(children=[
    #html.Button(id='clear')
    #],className='butonclear'),
                    #Product Info
    #html.Div(children=[
    #html.H1("Sold: 100"),
    #html.Br(),
    #html.H1('Value:100')
    #],className='infoproduct'),
                    #Bar Chart
    #html.Div(children=[
    #dcc.Graph(id='bar_chart')
    #],className='barchartclass'),
                    #Stardust Chart
    html.Div(children=[
    dcc.Graph(id='stardustgraph')
    ],className='stardust'),
                    #Slider for Combinations
    html.Div(children=[
    dcc.Slider(2,5,1,
               value=2,
               id='slider')
    ],className='sliderclass'),
                    #Combinations Table
    html.Div(id='combinationsid', className='combinationsclass')

    ])

                    #Callback for selecting a certain period
@app.callback(
    [Output('datepickerrange', 'start_date'), # This updates the field start_date in the DatePicker
    Output('datepickerrange', 'end_date')], # This updates the field end_date in the DatePicker
    [Input('timeframe_dropdown', 'value')],
)
def updateDataPicker(dropdown_value):
    if dropdown_value == 'toata':
        return dt(2020,8,7),dt(2023,3,15)
    elif dropdown_value == 'zi':
        return dt(2023,3,15) ,dt(2023,3,15)
    elif dropdown_value =='7zile':
        return dt(2023,3,15) - timedelta(7), dt(2023,3,15)
    elif dropdown_value=='luna':
        return dt(2023,3,15) - relativedelta(months=1),dt(2023,3,15)
    elif dropdown_value=='3luni':
        return dt(2023,3,15) -relativedelta(months=3) ,dt(2023,3,15)
    elif dropdown_value=='6luni':
        return dt(2023,3,15) -relativedelta(months=6),dt(2023,3,15)
    elif dropdown_value=='an':
        return dt(2023,3,15) - relativedelta(months=12) ,dt(2023,3,15)
    elif dropdown_value=='2ani':
        return dt(2023,3,15)-relativedelta(months=24) , dt(2023,3,15)


                    #Main Callback
@cache.memoize(timeout=timeout)
@app.callback(
    [Output(component_id='linechart',component_property='figure'),
     Output(component_id='pie-chart' , component_property='figure'),
     Output(component_id='top5table' , component_property='children'),],
    [Input(component_id='dropdown' ,component_property='value'),
     Input(component_id='datepickerrange',component_property='start_date'),
     Input(component_id='datepickerrange',component_property='end_date'),
     Input(component_id='checkid',component_property='value'),
     Input(component_id='radioitems' ,component_property='value')]

)

def get_graph(fastfood,start_date,end_date,pay,tip):
                #Kip Food 1
    if fastfood=='kipfood1':
        df=raw_df_kipfood1
                #Calculating dates
        start_date=pd.to_datetime(start_date)
        end_date=pd.to_datetime(end_date)
        df=df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        days=(end_date-start_date)/np.timedelta64(1,'D')
        weeks=(end_date-start_date)/np.timedelta64(1,'W')
        months=(end_date-start_date)/np.timedelta64(1,'M')
                #Filtering the DataFrame
        if pay==['ambele', 'Card']:
            df=df[df['Pay']=='Card ']
        elif pay==['ambele', 'Numerar']:
            df=df[df['Pay']=='Numerar ']
        if tip=='ora':
                                #Line_Chart
             zi_venit=df.groupby('Date')['Value'].sum().reset_index()
             val_bon=df.groupby(['Nr','Date'])['Value'].sum().reset_index()
             val_bon=val_bon.groupby('Date')['Value'].mean().reset_index()
             zi_venit['Bon']=val_bon['Value']
             line_chart=px.line(zi_venit , x='Date', y='Value' , title='Venit pe zi',hover_data=['Bon'])
             line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
             line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
             line_chart.update_xaxes(showgrid=False)
             line_chart.update_yaxes(showgrid=False)
             line_chart.update_xaxes(title_font_color="aqua" )
             line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                                #Pie_Chart
             hour_value=df.groupby('Hour')['Value'].sum().reset_index()
             clients_hour=df.groupby('Hour')['Nr'].nunique().reset_index()
             clients_hour['Nr']=clients_hour['Nr']/float(days)
             clients_hour['Value']=hour_value['Value']/float(days)
             pie_chart=px.pie(clients_hour,names='Hour' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
             pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
             pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe ora')
             pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
                                #Top 5 Table
             top5_df=pd.DataFrame()
             top5final_dict={}
             top5_list=list()
             top5_filter=df.groupby('Hour')['Name'].value_counts().reset_index(name='Cumparate')
             for i in range(8,20):
                    #top55=top5[top5['Hour']==i][0:5]F
                top5_df=top5_df.append(top5_filter[top5_filter['Hour']==i][0:5])
             for i in range(8,20):
                top5_per=list(top5_df[top5_df['Hour']==i]['Name'])
                top5_list.append(top5_per)
             for i in range(0,12):
                top5final_dict[i+8]=top5_list[i]
             top5df_final=pd.DataFrame(top5final_dict)
             top5_df.reset_index(inplace=True)
             top5full=list(top5_df['Cumparate'])
             top5seg=list(list(top5full[g:g+5])for g in range(0,60,5))
             top5toty=list()
             for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,12))
                top5toty.append(top5trans)
             table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(range(8,20),range(0,12))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
                                #Sunburst Chart
             sunburst_chart=px.sunburst(df, path=['Category', 'Name'], values='Value')



        if tip=='zi':
                            #Line_Chart
            luna_venit=df.groupby(['Year','Month'])['Value'].sum().reset_index()
            luna_venit['Date']=luna_venit['Year'].astype(str)+'-'+luna_venit['Month'].astype(str)
            line_chart=px.line(luna_venit , x='Date', y='Value' , title='Venit pe luna')
            line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
            line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
            line_chart.update_xaxes(showgrid=False)
            line_chart.update_yaxes(showgrid=False)
            line_chart.update_xaxes(title_font_color="aqua" )
            line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                            #Pie Chart
            day_value=df.groupby('Day of Week')['Value'].sum().reset_index()
            clients_day=df.groupby('Day of Week')['Nr'].nunique().reset_index()
            clients_day['Nr']=clients_day['Nr']/float(weeks)
            clients_day['Value']=day_value['Value']/float(weeks)
            pie_chart=px.pie(clients_day,names='Day of Week' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
            pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
            pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe zi')
            pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
                        # Top 5 Table
            top5_df=pd.DataFrame()
            top5final_dict={}
            top5_list=list()
            top5_filter=df.groupby('Day of Week')['Name'].value_counts().reset_index(name='Cumparate')
            for i in day_values:
                top5_df=top5_df.append(top5_filter[top5_filter['Day of Week']==i][0:5])
            for i in day_values:
                top5_per=list(top5_df[top5_df['Day of Week']==i]['Name'])
                top5_list.append(top5_per)
            for i ,j in zip(day_values,range(0,7)):
                top5final_dict[i]=top5_list[j]
            top5df_final=pd.DataFrame(top5final_dict)
            top5full=list(top5_df['Cumparate'])
            top5seg=list(list(top5full[g:g+5])for g in range(0,45,5))
            top5toty=list()
            for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,7))
                top5toty.append(top5trans)
            table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(day_values,range(0,7))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })


        if tip=='luna':
                            #Line_Chart
            an_venit=df.groupby('Year')['Value'].sum().reset_index()
            line_chart=px.line(an_venit , x='Year', y='Value' , title='Venit pe an')
            line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
            line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
            line_chart.update_xaxes(showgrid=False)
            line_chart.update_yaxes(showgrid=False)
            line_chart.update_xaxes(title_font_color="aqua" )
            line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                            #Pie_Chart
            month_value=df.groupby('Luna')['Value'].sum().reset_index()
            clients_month=df.groupby('Luna')['Nr'].nunique().reset_index()
            clients_month['Nr']=clients_month['Nr']
            clients_month['Value']=month_value['Value']
            pie_chart=px.pie(clients_month,names='Luna' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
            pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
            pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe luna')
            pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
                            #Top 5 Table
            top5_df=pd.DataFrame()
            top5final_dict={}
            top5_list=list()
            top5_filter=df.groupby('Luna')['Name'].value_counts().reset_index(name='Cumparate')
            for i in month_values:
                top5_df=top5_df.append(top5_filter[top5_filter['Luna']==i][0:5])
            for i in month_values:
                top5_per=list(top5_df[top5_df['Luna']==i]['Name'])
                top5_list.append(top5_per)
            for i ,j in zip(month_values,range(0,12)):
                top5final_dict[i]=top5_list[j]
            top5df_final=pd.DataFrame(top5final_dict)
            top5full=list(top5_df['Cumparate'])
            top5seg=list(list(top5full[g:g+5])for g in range(0,60,5))
            top5toty=list()
            for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,12))
                top5toty.append(top5trans)
            table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(month_values,range(0,12))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })


                #Kip Food 2
    elif fastfood=='kipfood2':
        df=raw_df_kipfood2
                    #Calculating dates
        start_date=pd.to_datetime(start_date)
        end_date=pd.to_datetime(end_date)
        opend=pd.to_datetime(dt(2022,10,22))
        if (start_date<opend):
            diff=(opend-start_date)/np.timedelta64(1,'D')
            diffw=(opend-start_date)/np.timedelta64(1,'W')
            diffm=(opend-start_date)/np.timedelta64(1,'M')
        else:
            diff=0
            diffw=0
            diffm=0
        days=(end_date-start_date)/np.timedelta64(1,'D')-diff
        weeks=(end_date-start_date)/np.timedelta64(1,'W')-diffw
        months=(end_date-start_date)/np.timedelta64(1,'M')-diffm
                        #Filtering the DataFrame
        df=df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if pay==['ambele', 'Card']:
            df=df[df['Pay']=='Card ']
        elif pay==['ambele', 'Numerar']:
            df=df[df['Pay']=='Numerar ']
        if tip=='ora':
                            #Line_Chart
             zi_venit=df.groupby('Date')['Value'].sum().reset_index()
             val_bon=df.groupby(['Nr','Date'])['Value'].sum().reset_index()
             val_bon=val_bon.groupby('Date')['Value'].mean().reset_index()
             zi_venit['Bon']=val_bon['Value']
             line_chart=px.line(zi_venit , x='Date', y='Value' , title='Venit pe zi' ,hover_data=['Bon'])
             line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
             line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
             line_chart.update_xaxes(showgrid=False)
             line_chart.update_yaxes(showgrid=False)
             line_chart.update_xaxes(title_font_color="aqua" )
             line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                            #Pie_Chart
             hour_value=df.groupby('Hour')['Value'].sum().reset_index()
             clients_hour=df.groupby('Hour')['Nr'].nunique().reset_index()
             clients_hour['Nr']=clients_hour['Nr']/float(days)
             clients_hour['Value']=hour_value['Value']/float(days)
             pie_chart=px.pie(clients_hour,names='Hour' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
             pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
             pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe ora')
             pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
                               #Top 5 Table
             top5_df=pd.DataFrame()
             top5final_dict={}
             top5_list=list()
             top5_filter=df.groupby('Hour')['Name'].value_counts().reset_index(name='Cumparate')
             for i in range(8,20):
                    #top55=top5[top5['Hour']==i][0:5]F
                top5_df=top5_df.append(top5_filter[top5_filter['Hour']==i][0:5])
             for i in range(8,20):
                top5_per=list(top5_df[top5_df['Hour']==i]['Name'])
                top5_list.append(top5_per)
             for i in range(0,12):
                top5final_dict[i+8]=top5_list[i]
             top5df_final=pd.DataFrame(top5final_dict)
             top5_df.reset_index(inplace=True)
             top5full=list(top5_df['Cumparate'])
             top5seg=list(list(top5full[g:g+5])for g in range(0,60,5))
             top5toty=list()
             for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,12))
                top5toty.append(top5trans)
             table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(range(8,20),range(0,12))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
        if tip=='zi':
                            #Line_Chart
            luna_venit=df.groupby(['Year','Month'])['Value'].sum().reset_index()
            luna_venit['Date']=luna_venit['Year'].astype(str)+'-'+luna_venit['Month'].astype(str)
            line_chart=px.line(luna_venit , x='Date', y='Value' , title='Venit pe luna')
            line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
            line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
            line_chart.update_xaxes(showgrid=False)
            line_chart.update_yaxes(showgrid=False)
            line_chart.update_xaxes(title_font_color="aqua" )
            line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                            #Pie_Chart
            day_value=df.groupby('Day of Week')['Value'].sum().reset_index()
            clients_day=df.groupby('Day of Week')['Nr'].nunique().reset_index()
            clients_day['Nr']=clients_day['Nr']/float(weeks)
            clients_day['Value']=day_value['Value']/float(weeks)
            pie_chart=px.pie(clients_day,names='Day of Week' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
            pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
            pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe zi')
            pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
             #Top 5 Table
            top5_df=pd.DataFrame()
            top5final_dict={}
            top5_list=list()
            top5_filter=df.groupby('Day of Week')['Name'].value_counts().reset_index(name='Cumparate')
            for i in day_values:
                top5_df=top5_df.append(top5_filter[top5_filter['Day of Week']==i][0:5])
            for i in day_values:
                top5_per=list(top5_df[top5_df['Day of Week']==i]['Name'])
                top5_list.append(top5_per)
            for i ,j in zip(day_values,range(0,7)):
                top5final_dict[i]=top5_list[j]
            top5df_final=pd.DataFrame(top5final_dict)
            top5full=list(top5_df['Cumparate'])
            top5seg=list(list(top5full[g:g+5])for g in range(0,45,5))
            top5toty=list()
            for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,7))
                top5toty.append(top5trans)
            table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(day_values,range(0,7))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
        if tip=='luna':
                        #Line_Chart
            an_venit=df.groupby('Year')['Value'].sum().reset_index()
            line_chart=px.line(an_venit , x='Year', y='Value' , title='Venit pe an')
            line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
            line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
            line_chart.update_xaxes(showgrid=False)
            line_chart.update_yaxes(showgrid=False)
            line_chart.update_xaxes(title_font_color="aqua" )
            line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                        #Pie_Chart
            month_value=df.groupby('Luna')['Value'].sum().reset_index()
            clients_month=df.groupby('Luna')['Nr'].nunique().reset_index()
            clients_month['Nr']=clients_month['Nr']
            clients_month['Value']=month_value['Value']
            pie_chart=px.pie(clients_month,names='Luna' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
            pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
            pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe luna')
            pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
            #Top 5 Table
            top5_df=pd.DataFrame()
            top5final_dict={}
            top5_list=list()
            top5_filter=df.groupby('Luna')['Name'].value_counts().reset_index(name='Cumparate')
            for i in month2_values:
                top5_df=top5_df.append(top5_filter[top5_filter['Luna']==i][0:5])
            for i in month2_values:
                top5_per=list(top5_df[top5_df['Luna']==i]['Name'])
                top5_list.append(top5_per)
            for i ,j in zip(month2_values,range(0,6)):
                top5final_dict[i]=top5_list[j]
            top5df_final=pd.DataFrame(top5final_dict)
            top5full=list(top5_df['Cumparate'])
            top5seg=list(list(top5full[g:g+5])for g in range(0,30,5))
            top5toty=list()
            for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,6))
                top5toty.append(top5trans)
            table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(month2_values,range(0,6))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })


                    #Both Fast Foods
    else:
        df=ambele_raw_df
                    #Calculating dates
        start_date=pd.to_datetime(start_date)
        end_date=pd.to_datetime(end_date)
        days=(end_date-start_date)/np.timedelta64(1,'D')
        weeks=(end_date-start_date)/np.timedelta64(1,'W')
        months=(end_date-start_date)/np.timedelta64(1,'M')
                    #Filtering the DataFrame
        df=df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if pay==['ambele', 'Card']:
            df=df[df['Pay']=='Card ']
        elif pay==['ambele', 'Numerar']:
            df=df[df['Pay']=='Numerar ']
        if tip=='ora':
                        #Line_Chart
             zi_venit=df.groupby('Date')['Value'].sum().reset_index()
             val_bon=df.groupby(['Nr','Date'])['Value'].sum().reset_index()
             val_bon=val_bon.groupby('Date')['Value'].mean().reset_index()
             zi_venit['Bon']=val_bon['Value']
             line_chart=px.line(zi_venit , x='Date', y='Value' , title='Venit pe zi',hover_data=['Bon'] )
             line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
             line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
             line_chart.update_xaxes(showgrid=False)
             line_chart.update_yaxes(showgrid=False)
             line_chart.update_xaxes(title_font_color="aqua" )
             line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                        #Pie_Chart
             hour_value=df.groupby('Hour')['Value'].sum().reset_index()
             clients_hour=df.groupby('Hour')['Nr'].nunique().reset_index()
             clients_hour['Nr']=clients_hour['Nr']
             clients_hour['Value']=hour_value['Value']/float(days)
             pie_chart=px.pie(clients_hour,names='Hour' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
             pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
             pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe ora')
             pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
                               #Top 5 Table
             top5_df=pd.DataFrame()
             top5final_dict={}
             top5_list=list()
             top5_filter=df.groupby('Hour')['Name'].value_counts().reset_index(name='Cumparate')
             for i in range(8,20):
                    #top55=top5[top5['Hour']==i][0:5]F
                top5_df=top5_df.append(top5_filter[top5_filter['Hour']==i][0:5])
             for i in range(8,20):
                top5_per=list(top5_df[top5_df['Hour']==i]['Name'])
                top5_list.append(top5_per)
             for i in range(0,12):
                top5final_dict[i+8]=top5_list[i]
             top5df_final=pd.DataFrame(top5final_dict)
             top5_df.reset_index(inplace=True)
             top5full=list(top5_df['Cumparate'])
             top5seg=list(list(top5full[g:g+5])for g in range(0,60,5))
             top5toty=list()
             for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,12))
                top5toty.append(top5trans)
             table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(range(8,20),range(0,12))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })

        if tip=='zi':
                        #Line_Chart
            luna_venit=df.groupby(['Year','Month'])['Value'].sum().reset_index()
            luna_venit['Date']=luna_venit['Year'].astype(str)+'-'+luna_venit['Month'].astype(str)
            line_chart=px.line(luna_venit , x='Date', y='Value' , title='Venit pe luna')
            line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
            line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
            line_chart.update_xaxes(showgrid=False)
            line_chart.update_yaxes(showgrid=False)
            line_chart.update_xaxes(title_font_color="aqua" )
            line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                        #Pie_Chart
            day_value=df.groupby('Day of Week')['Value'].sum().reset_index()
            clients_day=df.groupby('Day of Week')['Nr'].nunique().reset_index()
            clients_day['Nr']=clients_day['Nr']/float(weeks)
            clients_day['Value']=day_value['Value']/float(weeks)
            pie_chart=px.pie(clients_day,names='Day of Week' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
            pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
            pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe zi')
            pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
                        #Top 5 Table
            top5_df=pd.DataFrame()
            top5final_dict={}
            top5_list=list()
            top5_filter=df.groupby('Day of Week')['Name'].value_counts().reset_index(name='Cumparate')
            for i in day_values:
                top5_df=top5_df.append(top5_filter[top5_filter['Day of Week']==i][0:5])
            for i in day_values:
                top5_per=list(top5_df[top5_df['Day of Week']==i]['Name'])
                top5_list.append(top5_per)
            for i ,j in zip(day_values,range(0,7)):
                top5final_dict[i]=top5_list[j]
            top5df_final=pd.DataFrame(top5final_dict)
            top5full=list(top5_df['Cumparate'])
            top5seg=list(list(top5full[g:g+5])for g in range(0,45,5))
            top5toty=list()
            for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,7))
                top5toty.append(top5trans)
            table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(day_values,range(0,7))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
        if tip=='luna':
                        #Line_Chart
            an_venit=df.groupby('Year')['Value'].sum().reset_index()
            line_chart=px.line(an_venit , x='Year', y='Value' , title='Venit pe an')
            line_chart.update_traces(line_color='rgb(37, 224, 37)', line_width=2 )
            line_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=20),bgcolor="black" ,font_color='aqua') ,font_color="rgb(37, 224, 37)" , title_font_color="aqua",plot_bgcolor='black',
                                paper_bgcolor='black' ,font=dict(size=18), xaxis=dict(tickfont=dict(color="#1f77b4")))
            line_chart.update_xaxes(showgrid=False)
            line_chart.update_yaxes(showgrid=False)
            line_chart.update_xaxes(title_font_color="aqua" )
            line_chart.update_coloraxes(colorbar_tickcolor='aqua')
                        #Pie_Chart
            month_value=df.groupby('Luna')['Value'].sum().reset_index()
            clients_month=df.groupby('Luna')['Nr'].nunique().reset_index()
            clients_month['Nr']=clients_month['Nr']
            clients_month['Value']=month_value['Value']
            pie_chart=px.pie(clients_month,names='Luna' , values='Nr', hover_data=['Value'] ,color_discrete_sequence=px.colors.sequential.Viridis)
            pie_chart.update_traces(textinfo='label+percent',textposition='auto', textfont_size=13.55 ,textfont_color='white')
            pie_chart.update_layout(title=dict(x=0.35,y=0.95,font=dict(family="Arial",color='rgb(37, 224, 37)')),title_font_size=24,paper_bgcolor='black',autosize=False
                                     ,width=700,height=450 , title_text='Procentajul clientilor pe luna')
            pie_chart.update_layout(hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'))
            #Top 5 Table
            top5_df=pd.DataFrame()
            top5final_dict={}
            top5_list=list()
            top5_filter=df.groupby('Luna')['Name'].value_counts().reset_index(name='Cumparate')
            for i in month_values:
                top5_df=top5_df.append(top5_filter[top5_filter['Luna']==i][0:5])
            for i in month_values:
                top5_per=list(top5_df[top5_df['Luna']==i]['Name'])
                top5_list.append(top5_per)
            for i ,j in zip(month_values,range(0,12)):
                top5final_dict[i]=top5_list[j]
            top5df_final=pd.DataFrame(top5final_dict)
            top5full=list(top5_df['Cumparate'])
            top5seg=list(list(top5full[g:g+5])for g in range(0,60,5))
            top5toty=list()
            for j in range(0,5):
                top5trans=list(top5seg[i][j] for i in range(0,12))
                top5toty.append(top5trans)
            table=dash_table.DataTable(
                data=top5df_final.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in top5df_final.columns],
                tooltip_data=[
                {
                 i : {'value': str(row[j]), 'type': 'text'}
                 for i,j in zip(month_values,range(0,12))
                }for row in top5toty
                ],
                css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: black; font-family: monospace; color: aqua'
                }],
                editable=True,
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })

    return [line_chart ,pie_chart , [table]]

@app.callback(
        [Output(component_id='stardustgraph' , component_property='figure'),
         Output(component_id='combinationsid',component_property='children'),
         Output(component_id='toty',component_property='children')],
        [Input(component_id='dropdown' , component_property='value'),
         Input(component_id='checkid', component_property='value'),
         Input(component_id='datepickerrange',component_property='start_date'),
         Input(component_id='datepickerrange',component_property='end_date'),
         Input(component_id='slider',component_property='value')]
)

def last2charts(fastfood,pay,start_date,end_date,comb):
    if fastfood=='kipfood1':
                        #Sunburst_Chart
        df=raw_df_kipfood1
        start_date=pd.to_datetime(start_date)
        end_date=pd.to_datetime(end_date)
        df=df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if pay==['ambele', 'Card']:
            df=df[df['Pay']=='Card ']
        elif pay==['ambele', 'Numerar']:
            df=df[df['Pay']=='Numerar ']
        sunburst_chart=px.sunburst(df, path=['Category','Name'], values='Value',color_discrete_sequence=px.colors.sequential.Rainbow,title='Venitul pe categorii/subcategorii')
        sunburst_chart.update_layout(paper_bgcolor='black',autosize=False,height=500,width=900,hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'),title_font_color='rgb(37, 224, 37)' ,title_font_size=20)
        sunburst_chart.update_traces(textfont=dict(family=['Arial','Courier New'],size=16 , color='white'))
                        #Combinations Table
        combination=Counter([
        t for _, d in df.groupby('Nr')['Name']
        for t in combinations(d, comb)
    ]).most_common(6)
        comb_trans=list()
        comb_dict={}
        comb_val=list()
        for i,k in zip(range (0,comb),range(0,comb)):
            comb_list=list()
            for j in range(0,6):
                comb_list.append(combination[j][0][k])
            comb_trans.append(comb_list)
        for l in range(0,6):
            comb_val.append(combination[l][1])
        for i in range(0,comb):
            comb_dict[i]=comb_trans[i]
        comb_dict['Vandute:']=comb_val
        comb_df=pd.DataFrame(comb_dict)
        table=dash_table.DataTable(
                data=comb_df.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in comb_df.columns],
                editable=True,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
        venit=df['Value'].sum()
        text="Total: {:,.0f} RON".format(venit )
    elif fastfood=='kipfood2':
                       #Sunburst_Chart
        df=raw_df_kipfood2
        start_date=pd.to_datetime(start_date)
        end_date=pd.to_datetime(end_date)
        df=df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if pay==['ambele', 'Card']:
            df=df[df['Pay']=='Card ']
        elif pay==['ambele', 'Numerar']:
            df=df[df['Pay']=='Numerar ']
        text="Total: {} RON".format("%.0f" % df['Value'].sum())
        sunburst_chart=px.sunburst(df, path=['Category','Name'], values='Value',color_discrete_sequence=px.colors.sequential.Rainbow,title='Venitul pe categorii/subcategorii')
        sunburst_chart.update_layout(paper_bgcolor='black',autosize=False,height=500,width=900,hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'),title_font_color='rgb(37, 224, 37)' ,title_font_size=20)
        sunburst_chart.update_traces(textfont=dict(family=['Arial','Courier New'],size=16 , color='white'))
        #Combinations Table
        combination=Counter([
        t for _, d in df.groupby('Nr')['Name']
        for t in combinations(d, comb)
    ]).most_common(6)
        comb_trans=list()
        comb_dict={}
        comb_val=list()
        for i,k in zip(range (0,comb),range(0,comb)):
            comb_list=list()
            for j in range(0,6):
                comb_list.append(combination[j][0][k])
            comb_trans.append(comb_list)
        for l in range(0,6):
            comb_val.append(combination[l][1])
        for i in range(0,comb):
            comb_dict[i]=comb_trans[i]
        comb_dict['Vandute:']=comb_val
        comb_df=pd.DataFrame(comb_dict)
        table=dash_table.DataTable(
                data=comb_df.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in comb_df.columns],
                editable=True,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
        venit=df['Value'].sum()
        text="Total: {:,.0f} RON".format(venit )
    else:
                        #Sunburst Chart
        df=ambele_raw_df
        start_date=pd.to_datetime(start_date)
        end_date=pd.to_datetime(end_date)
        df=df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if pay==['ambele', 'Card']:
            df=df[df['Pay']=='Card ']
        elif pay==['ambele', 'Numerar']:
            df=df[df['Pay']=='Numerar ']
        text="Total: {} RON".format("%.0f" % df['Value'].sum())
        sunburst_chart=px.sunburst(df, path=['Category','Name'], values='Value',color_discrete_sequence=px.colors.sequential.Rainbow,title='Venitul pe categorii/subcategorii')
        sunburst_chart.update_layout(paper_bgcolor='black',autosize=False,height=500,width=900,hoverlabel=dict(font=dict(family='sans-serif', size=16),bgcolor="black" ,font_color='aqua'),title_font_color='rgb(37, 224, 37)' ,title_font_size=20)
        sunburst_chart.update_traces(textfont=dict(family=['Arial','Courier New'],size=16 , color='white'))
        #Combinations Table
        combination=Counter([
        t for _, d in df.groupby('Nr')['Name']
        for t in combinations(d, comb)
    ]).most_common(6)
        comb_trans=list()
        comb_dict={}
        comb_val=list()
        for i,k in zip(range (0,comb),range(0,comb)):
            comb_list=list()
            for j in range(0,6):
                comb_list.append(combination[j][0][k])
            comb_trans.append(comb_list)
        for l in range(0,6):
            comb_val.append(combination[l][1])
        for i in range(0,comb):
            comb_dict[i]=comb_trans[i]
        comb_dict['Vandute:']=comb_val
        comb_df=pd.DataFrame(comb_dict)
        table=dash_table.DataTable(
                data=comb_df.to_dict('records'),
                columns=[{'id': str(c), 'name': str(c)} for c in comb_df.columns],
                editable=True,
                style_cell={
                'width':'100px',
                'height':'50px',
                'color':'rgb(37, 224, 37)',
                'background-color':'black',
                'text-align':'center'
                })
        venit=df['Value'].sum()
        text="Total: {:,.0f} RON".format(venit )


    return [sunburst_chart , [table] , text]

app.run_server(debug=False)







