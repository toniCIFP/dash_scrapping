import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

#parametres
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json

url="https://www.eex.com/en/market-data/natural-gas/futures#%7B%22snippetpicker%22%3A%22292%22%7D"
doc=requests.get(url, timeout=25)
doc.text

browser = webdriver.Chrome()
browser.get('https://www.eex.com/en/market-data/natural-gas/futures#%7B%22snippetpicker%22%3A%22292%22%7D')
# Hem de fer clic a les cookies
elem = browser.find_element(By.CLASS_NAME, 'uo_cookie_btn_type_0')
elem.click()
# Hem de fer clic al month
boton = browser.find_element(By.XPATH , '//*[@id="symbolheader_ngfttf"]/div/div[2]/div[4]')
boton.click()
# Omplim el buscador del dia
buscador = browser.find_element(By.XPATH , '//*[@id="symbolheader_ngfttf"]/div/div[1]/div/input')
buscador.clear()
buscador.send_keys("2023-03-02")
buscador.send_keys(Keys.RETURN)

import time
df = pd.DataFrame(columns=['Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre'])

valores = []
for dia in range(1, 21):
    buscador = browser.find_element(By.XPATH , '//*[@id="symbolheader_ngfttf"]/div/div[1]/div/input')
    buscador.clear()
    buscador.send_keys(f"2023-03-{dia}")
    buscador.send_keys(Keys.RETURN)
    time.sleep(2)
    
    
    valors = []
    filas = buscador.find_elements(By.XPATH, '//*[@id="baseloadwidget_ngfttf"]/table/tbody/tr')

    for fila in filas:
        cuarto_td = fila.find_elements(By.XPATH,"./td[4]")

        if cuarto_td:
            valors.append(cuarto_td[0].text)
        else:
            valors.append(None)
            
    if len(valors) > 0:
        df = df.append(pd.Series(valors, index=df.columns), ignore_index=True)        
    
    time.sleep(3)

df = df.replace(to_replace=r',', value='', regex=True)

df['Marzo'] = df['Marzo'].astype(int)
df['Abril'] = df['Abril'].astype(int)
df['Mayo'] = df['Mayo'].astype(int)
df['Junio'] = df['Junio'].astype(int)
df['Julio'] = df['Julio'].astype(int)
df['Agosto'] = df['Agosto'].astype(int)
df['Septiembre'] = df['Septiembre'].astype(int)
    
    
# Initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

navbar = dbc.Navbar(
    [dbc.NavbarBrand("WEB SCRAPPING NATURAL GAS FEATURES", className="ms-2",style={'textAlign': 'center','height':'80px'})
    ],
    color="info",
    dark=True
)


grafica1=dcc.Graph(id='grafica1', 
                    figure = {'data':[
                            go.Scatter(
                            x=dfdia.index,
                            y=dfdia['demanda'],
                            mode='lines',
                            )],
                    'layout':go.Layout(xaxis = {'title':'Tiempo'},yaxis = {'title':'Demanda Elèctrica [MWh]'},title="Demanda")}
        )



app.layout =  html.Div(children=[navbar,
    dbc.Row([
        dbc.Col(html.Div([grafica1]),width=12)
        ]),
    dbc.Row([
        dbc.Col(html.Div([dbc.Alert("Dissenyat per Toni Amer", color="dark")]),width=12)
    ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)