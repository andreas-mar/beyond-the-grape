import dash_core_components as dcc
import dash_html_components as html
import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from joblib import load
import dash_core_components as dcc
import pandas as pd


def numeric_form_group(name, label, upper_text_width, upper_width, starting_value, min=0, max=1000000, step=10):
    return (dbc.FormGroup(
        [
            dbc.Label(label, html_for=name, width=upper_text_width, style={'font-size': "85%", 'text-align':'left', 'overflow': 'hidden', 'white-space': 'nowrap','color':'darkslategrey'}),
            dbc.Col(
                dbc.Input(
                    type="number", id=name, placeholder=name, value=starting_value, min=min, max=max, step=step,
                    style={'height': '20px', 'width': '80px'}
                ),
                width=upper_width,
            ),
        ],
        row=True,
    ))


def init_regression(server):
    options = ['year', 'ratings_count', 'labels_count',
               'reviews_count', 'is_natural', 'winery_ratings_count',
               'winery_ratings_average', 'winery_labels_count', 'winery_wines_count',
               'users_count', 'regions_count', 'wines_count', 'wineries_count',
               'median_price', 'bold', 'tannic', 'sweet', 'oaky', 'black fruit',
               'red fruit', 'earthy', 'spices', 'ageing', 'yeasty', 'dried fruit',
               'citrus', 'tree fruit', 'vegetal', 'floral', 'tropical', 'beef', 'lamb',
               'veal', 'poultry', 'pork', 'shellfish', 'vegetarian', 'game',
               'spicy-food', 'types'] #Mangler total flavors

    dict_options = ['year', 'ratings_count', 'labels_count',
               'reviews_count', 'is_natural', 'winery_ratings_count',
               'winery_ratings_average', 'winery_labels_count', 'winery_wines_count',
               'users_count', 'regions_count', 'wines_count', 'wineries_count',
               'median_price', 'bold', 'tannic', 'sweet', 'oaky', 'black fruit',
               'red fruit', 'earthy', 'spices', 'ageing', 'yeasty', 'dried fruit',
               'citrus', 'tree fruit', 'vegetal', 'floral', 'types',  'foods'] #Mangler total flavors

    TASTES = ['tropical', 'beef', 'lamb',
       'veal', 'poultry', 'pork', 'shellfish', 'vegetarian', 'game',
       'spicy-food']

    UPPER_WIDTH = 1
    UPPER_TEXT_WIDTH = 6
    SUBSECTION_WIDTHS = '13%'

    predictor_app = Dash(
        server=server,
        title='Beyond The Grape Predictor',
        update_title=None,
        routes_pathname_prefix='/predict/',
        external_stylesheets=[dbc.themes.BOOTSTRAP, 'styles.css'],
        external_scripts=[dbc.themes.BOOTSTRAP, 'styles.css']
    )

    pipeline = load("app/static/models/xbg_wine_model.joblib")

    foods = dbc.FormGroup(
        [
            dbc.Label("Foods", html_for="food-checklist-row", width=2),
            dbc.Col(
                dcc.Checklist(options=[{'label': 'Beef', 'value': 'beef'},
                                       {'label': 'Chicken', 'value': 'chicken'},
                                       {'label': 'Pork', 'value': 'pork'},
                                       {'label': 'Lamb', 'value': 'lamb'},
                                       {'label': 'Veal', 'value': 'veal'},
                                       {'label': 'Poultry', 'value': 'poultry'},
                                       {'label': 'Shellfish', 'value': 'shellfish'},
                                       {'label': 'Vegetarian', 'value': 'vegetarian'},
                                       {'label': 'Game', 'value': 'game'},
                                       {'label': 'Spicy food', 'value': 'spicy-food'},
                                       {'label': 'Tropical', 'value': 'tropical'}], value=['beef', 'chicken', 'pork'],
                              id='food-checklist-row',
                              labelStyle={'display': 'inline-block', 'margin': '5px'}),
                width=7,
            ),
        ],
        row=True,
    )

    types = dbc.FormGroup(
        [
            dbc.Label("Wine type", html_for="types", width=2),
            dbc.Col(
                dcc.RadioItems(options=[{'label': 'Red', 'value': 'red'},
                                        {'label': 'White', 'value': 'white'}, ], value='red', id='types',
                               labelStyle={'display': 'inline-block', 'margin': '5px'}),
                width=7,
            ),
        ],
        row=True,
    )

    # ---------------------------------------------------- Mapping ----------------------------------------------------

    predictor_app.layout = html.Div([html.Section([html.Div([html.H1('Beyond The Grape rating predictor', className='mx-auto my-0 text-uppercase', style={'text-align': 'center', 'color':'darkslategrey'})], style={'margin':'3%'}),
                                         html.Div([

                                             # ---------------------------------------------------- Section 1 ----------------------------------------------------
                                             dbc.Form([foods,
                                                       types]),
                                             html.Div([
                                                 dbc.Form(
                                                     [numeric_form_group('year', 'Year', UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         2002, 1960, 2020, 1),
                                                      numeric_form_group('median_price', 'Price',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         550, 50, 6000, 50),
                                                      numeric_form_group('ratings_count', '# Ratings',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         2000, 0, step=100),
                                                      numeric_form_group('labels_count', '# Labels',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         20, 1, step=1),
                                                      numeric_form_group('reviews_count', '# Reviews',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         1000, 0, step=50)], style={'float': 'left', 'margin':'1%', 'width' : SUBSECTION_WIDTHS}),

                                                 # ---------------------------------------------------- Section 2 ----------------------------------------------------

                                                 dbc.Form([numeric_form_group('tannic', 'Tannic', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              30, 0, 100, 1),
                                                           numeric_form_group('sweet', 'Sweet', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              30, 0, 100, 1),
                                                           numeric_form_group('bold', 'Bold', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              30, 0, 100, 1),
                                                           numeric_form_group('black fruit', 'Black Fruit',
                                                                              UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2, 0, 1, 0.1),
                                                           numeric_form_group('red fruit', 'Red Fruit',
                                                                              UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2, 0, 1, 0.1), ], style={'float': 'left', 'margin':'1%', 'width' : SUBSECTION_WIDTHS}),
                                                 # ---------------------------------------------------- Section 3 ----------------------------------------------------

                                                 dbc.Form([
                                                     numeric_form_group('earthy', 'Earthy', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2, 0, 1, 0.1),
                                                     numeric_form_group('is_natural', 'Is Natural', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0, 0, 1, 1),
                                                     numeric_form_group('winery_ratings_count', '# Winery Ratings',
                                                                        UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                        1000, 0, step=100),
                                                     numeric_form_group('winery_ratings_average',
                                                                        'winery_ratings_average',
                                                                        UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                        4, 0, 5, 0.1),
                                                     numeric_form_group('winery_labels_count', '# winery Labels',
                                                                        UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        20, 0 , 10000, 10), ], style={'float': 'left', 'margin':'1%', 'width' : SUBSECTION_WIDTHS}),
                                                 # ---------------------------------------------------- Section 4 ----------------------------------------------------

                                                 dbc.Form(
                                                     [numeric_form_group('winery_wines_count', '#Winery Wines',
                                                                         UPPER_TEXT_WIDTH,
                                                                         UPPER_WIDTH,
                                                                         20, 0 , 10000, 10),
                                                      numeric_form_group('users_count', '# Users', UPPER_TEXT_WIDTH,
                                                                         UPPER_WIDTH,
                                                                         600, 0 , step= 100),
                                                      numeric_form_group('regions_count', '# Regions',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                        7, 0, step=1),
                                                      numeric_form_group('wines_count', 'Wines count', UPPER_TEXT_WIDTH,
                                                                         UPPER_WIDTH,
                                                                         40, 0, step=10),
                                                      numeric_form_group('wineries_count', 'Wineries count',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         80, 0, step=10)], style={'float': 'left', 'margin':'1%', 'width' : SUBSECTION_WIDTHS}),
                                                 # ---------------------------------------------------- Section 5 ----------------------------------------------------
                                                 dbc.Form([
                                                     numeric_form_group('oaky', 'Oaky', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2, 0, 1, 0.1),
                                                     numeric_form_group('spices', 'Spices', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2, 0, 1, 0.1),
                                                     numeric_form_group('ageing', 'Ageing', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2, 0, 1, 0.1),
                                                     numeric_form_group('yeasty', 'Yeasty', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2, 0, 1, 0.1),
                                                     numeric_form_group('dried fruit', 'Dried Fruit', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2, 0, 1, 0.1)], style={'float': 'left', 'margin':'1%', 'width' : SUBSECTION_WIDTHS}),
                                                 # ---------------------------------------------------- Section 6 ----------------------------------------------------
                                                 dbc.Form([numeric_form_group('citrus', 'Citrus', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2, 0, 1, 0.1),
                                                           numeric_form_group('tree fruit', 'Tree Fruit',
                                                                              UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2, 0, 1, 0.1),
                                                           numeric_form_group('vegetal', 'Vegetal', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2, 0, 1, 0.1),
                                                           numeric_form_group('floral', 'Floral', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2, 0, 1, 0.1)], style={'text-align': 'left', 'margin':'1%', 'width' : SUBSECTION_WIDTHS}), ], style={'display':'flex', 'justify-content':'center'}),

                                         ], style={'text-align': 'center'}),
                                         html.Div([html.P('')], style={'margin': '5%'}),
                                        ]
                                        ), html.H2('        '),
                                     html.H2(id="output_pred", className="predictions_container", style={'text-align': 'center', 'margin' : '150px', 'color':'darkslategrey'}),
                                     ], style={'background-image' : 'url("assets/background.jpg")', 'height' : '100vh', 'background-size':'cover'})

    #Init callback of input fields
    @predictor_app.callback(
        dash.dependencies.Output('output_pred', 'children'),
        [#dash.dependencies.Input('submit_button', 'n_clicks'),
         dash.dependencies.Input('year', 'value'),
         dash.dependencies.Input('ratings_count', 'value'),
         dash.dependencies.Input('labels_count', 'value'),
         dash.dependencies.Input('reviews_count', 'value'),
         dash.dependencies.Input('is_natural', 'value'),
         dash.dependencies.Input('winery_ratings_count', 'value'),
         dash.dependencies.Input('winery_ratings_average', 'value'),
         dash.dependencies.Input('winery_labels_count', 'value'),
         dash.dependencies.Input('winery_wines_count', 'value'),
         dash.dependencies.Input('users_count', 'value'),
         dash.dependencies.Input('regions_count', 'value'),
         dash.dependencies.Input('wines_count', 'value'),
         dash.dependencies.Input('wineries_count', 'value'),
         dash.dependencies.Input('median_price', 'value'),
         dash.dependencies.Input('bold', 'value'),
         dash.dependencies.Input('tannic', 'value'),
         dash.dependencies.Input('sweet', 'value'),
         dash.dependencies.Input('oaky', 'value'),
         dash.dependencies.Input('black fruit', 'value'),
         dash.dependencies.Input('red fruit', 'value'),
         dash.dependencies.Input('earthy', 'value'),
         dash.dependencies.Input('spices', 'value'),
         dash.dependencies.Input('ageing', 'value'),
         dash.dependencies.Input('yeasty', 'value'),
         dash.dependencies.Input('dried fruit', 'value'),
         dash.dependencies.Input('citrus', 'value'),
         dash.dependencies.Input('tree fruit', 'value'),
         dash.dependencies.Input('vegetal', 'value'),
         dash.dependencies.Input('floral', 'value'),
         dash.dependencies.Input('types', 'value'),
         dash.dependencies.Input('food-checklist-row', 'value'), ])
    def calculate_rating(*args):
        #Establish dataframe input
        d = pd.DataFrame()
        for o, i in zip(dict_options, args):
            d[o] = [i]

        for taste in TASTES:
            d[taste] = 1 if taste in list(d['foods'][0]) else 0

        d['types'] = 1 if 'red' in list(d['types'][0]) else 0
        del d['foods']

        #Ordring columns to fit XGB model
        d = d [['year', 'ratings_count', 'labels_count', 'reviews_count', 'is_natural',
       'winery_ratings_count', 'winery_ratings_average', 'winery_labels_count',
       'winery_wines_count', 'users_count', 'regions_count', 'wines_count',
       'wineries_count', 'median_price', 'bold', 'tannic', 'sweet', 'oaky',
       'black fruit', 'red fruit', 'earthy', 'spices', 'ageing', 'yeasty',
       'dried fruit', 'citrus', 'tree fruit', 'vegetal', 'floral', 'tropical',
       'beef', 'lamb', 'veal', 'poultry', 'pork', 'shellfish', 'vegetarian',
       'game', 'spicy-food', 'types']]

        print(d) #Used for decomposition and debugging
        predictions = pipeline.predict(d)[0]
        return 'Predicted rating {}'.format(round(float(predictions),1))

    return predictor_app.server
