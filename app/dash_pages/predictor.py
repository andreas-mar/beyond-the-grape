import dash_core_components as dcc
import dash_html_components as html
import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from joblib import load
import dash_core_components as dcc
import pandas as pd


def numeric_form_group(name, label, upper_text_width, upper_width, starting_value):
    return (dbc.FormGroup(
        [
            dbc.Label(label, html_for=name, width=upper_text_width, style={'font-size': "85%", 'text-align':'left'}),
            dbc.Col(
                dbc.Input(
                    type="number", id=name, placeholder=starting_value, value=starting_value,
                    style={'height': '25px', 'width': '100px'}
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

    UPPER_WIDTH = 2
    UPPER_TEXT_WIDTH = 5

    predictor_app = Dash(
        server=server,
        title='Wine rating predictor',
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

    predictor_app.layout = html.Section([html.H1('Wine buddy predictor', style={'margin': '2%', 'color': 'green', 'text-align': 'center'}),
                                         html.Div([

                                             # ---------------------------------------------------- Section 1 ----------------------------------------------------
                                             dbc.Form([foods,
                                                       types]),
                                             html.Div([
                                                 dbc.Form(
                                                     [numeric_form_group('year', 'year', UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         2),
                                                      numeric_form_group('median_price', 'median_price',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         1),
                                                      numeric_form_group('ratings_count', 'ratings_count',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         1),
                                                      numeric_form_group('labels_count', 'labels_count',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         1),
                                                      numeric_form_group('reviews_count', 'reviews_count',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         1)], style={'float': 'left', 'margin':'1%'}),

                                                 # ---------------------------------------------------- Section 2 ----------------------------------------------------

                                                 dbc.Form([numeric_form_group('tannic', 'Tannic', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.22),
                                                           numeric_form_group('sweet', 'sweet', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.03),
                                                           numeric_form_group('oaky', 'oaky', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              1.2),
                                                           numeric_form_group('black fruit', 'black fruit',
                                                                              UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              1.2),
                                                           numeric_form_group('red fruit', 'red fruit',
                                                                              UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              1.2), ], style={'float': 'left', 'margin':'1%'}),
                                                 # ---------------------------------------------------- Section 3 ----------------------------------------------------

                                                 dbc.Form([
                                                     numeric_form_group('earthy', 'earthy', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2),
                                                     numeric_form_group('is_natural', 'is_natural', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2),
                                                     numeric_form_group('winery_ratings_count', 'winery_ratings_count',
                                                                        UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                        0.2),
                                                     numeric_form_group('winery_ratings_average',
                                                                        'winery_ratings_average',
                                                                        UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                        0.2),
                                                     numeric_form_group('winery_labels_count', 'winery_labels_count',
                                                                        UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2), ], style={'float': 'left', 'margin':'1%'}),
                                                 # ---------------------------------------------------- Section 4 ----------------------------------------------------

                                                 dbc.Form(
                                                     [numeric_form_group('winery_wines_count', 'winery_wines_count',
                                                                         UPPER_TEXT_WIDTH,
                                                                         UPPER_WIDTH,
                                                                         0.2),
                                                      numeric_form_group('users_count', 'users_count', UPPER_TEXT_WIDTH,
                                                                         UPPER_WIDTH,
                                                                         0.2),
                                                      numeric_form_group('regions_count', 'regions_count',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         0.2),
                                                      numeric_form_group('wines_count', 'wines_count', UPPER_TEXT_WIDTH,
                                                                         UPPER_WIDTH,
                                                                         0.2),
                                                      numeric_form_group('wineries_count', 'wineries_count',
                                                                         UPPER_TEXT_WIDTH, UPPER_WIDTH,
                                                                         0.2)], style={'float': 'left', 'margin':'1%'}),
                                                 # ---------------------------------------------------- Section 5 ----------------------------------------------------
                                                 dbc.Form([
                                                     numeric_form_group('bold', 'bold', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.29),
                                                     numeric_form_group('spices', 'spices', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.2),
                                                     numeric_form_group('ageing', 'ageing', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.32),
                                                     numeric_form_group('yeasty', 'yeasty', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.8),
                                                     numeric_form_group('dried fruit', 'dried fruit', UPPER_TEXT_WIDTH,
                                                                        UPPER_WIDTH,
                                                                        0.14)], style={'float': 'left', 'margin':'1%'}),
                                                 # ---------------------------------------------------- Section 6 ----------------------------------------------------
                                                 dbc.Form([numeric_form_group('citrus', 'citrus', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.2),
                                                           numeric_form_group('tree fruit', 'tree fruit',
                                                                              UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.4),
                                                           numeric_form_group('vegetal', 'vegetal', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.23),
                                                           numeric_form_group('floral', 'floral', UPPER_TEXT_WIDTH,
                                                                              UPPER_WIDTH,
                                                                              0.4)], style={'text-align': 'left', 'margin':'1%'}), ]),

                                         ], style={'text-align': 'center'}),
                                         html.Div([dbc.Button("Analyze", color="success", className="mr-1",
                                                                  id='submit_button'),
                                                       dbc.Button("Randomize!", color="danger", className="mr-1",
                                                                  id='randomize_button')], style={'margin': '5%'}),
                                        html.Div(id="output_pred", className="predictions_container")],
                                        style={'background-image' : 'url("app/static/assets/img/bg-masthead.jpg")'}
                                        )

    @predictor_app.callback(
        dash.dependencies.Output('output_pred', 'children'),
        [dash.dependencies.Input('submit_button', 'n_clicks'),
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
    def calculate_rating(n_clicks, *args):
        d = pd.DataFrame()
        for o, i in zip(dict_options, args):
            d[o] = [i]

        for taste in TASTES:
            d[taste] = 1 if taste in list(d['foods'][0]) else 0

        d['types'] = 1 if 'red' in list(d['types'][0]) else 0
        del d['foods']
        d = d [['year', 'ratings_count', 'labels_count', 'reviews_count', 'is_natural',
       'winery_ratings_count', 'winery_ratings_average', 'winery_labels_count',
       'winery_wines_count', 'users_count', 'regions_count', 'wines_count',
       'wineries_count', 'median_price', 'bold', 'tannic', 'sweet', 'oaky',
       'black fruit', 'red fruit', 'earthy', 'spices', 'ageing', 'yeasty',
       'dried fruit', 'citrus', 'tree fruit', 'vegetal', 'floral', 'tropical',
       'beef', 'lamb', 'veal', 'poultry', 'pork', 'shellfish', 'vegetarian',
       'game', 'spicy-food', 'types']]
        #d = d.to_numpy()
        print(d)
        #print(d.shape)
        predictions = pipeline.predict(d)
        return 'Predicted rating is {} {}. Result is {}'.format(n_clicks, d, predictions)

    return predictor_app.server
