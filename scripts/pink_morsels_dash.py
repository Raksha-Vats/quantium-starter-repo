import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os

# Load data
DATA_PATH = "../data/pink_morsel_sales_combined.csv"
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# Group by date and region
grouped = df.groupby(['date', 'region'])['sales'].sum().reset_index()

# Pivot for 'all' view
pivoted = grouped.pivot(index='date', columns='region', values='sales').fillna(0)
pivoted['Total Sales'] = pivoted.sum(axis=1)
pivoted = pivoted.reset_index()

# Hover builder for 'all'
def build_hover_all(row):
    regions = [f"{region}: ${row[region]:,.2f}" for region in ['north', 'south', 'east', 'west']]
    return f"Date: {row['date'].date()}<br>Total Sales: ${row['Total Sales']:,.2f}<br>" + "<br>".join(regions)

pivoted['hover'] = pivoted.apply(build_hover_all, axis=1)

# Initialize Dash
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualizer", style={
        'textAlign': 'center',
        'color': '#EF476F',
        'fontFamily': 'Arial Black',
        'marginBottom': '30px'
    }),

    html.Div([
        html.Label("Select Region:", style={'fontWeight': 'bold', 'fontSize': '18px'}),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '15px', 'fontSize': '16px'},
            inputStyle={'marginRight': '5px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        dcc.Graph(id='sales-graph')
    ], style={'width': '80%', 'margin': 'auto'})
])

# Callback to update chart
@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-selector', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        fig = px.scatter(
            pivoted,
            x='date',
            y='Total Sales',
            hover_data={'hover': True, 'date': False, 'Total Sales': False},
            labels={'date': 'Date', 'Total Sales': 'Sales ($)'},
            title='Total Daily Sales - All Regions'
        )
        fig.update_traces(marker=dict(size=8), hovertemplate="%{customdata[0]}")
    else:
        region_df = grouped[grouped['region'] == selected_region]
        fig = px.scatter(
            region_df,
            x='date',
            y='sales',
            labels={'date': 'Date', 'sales': 'Sales ($)'},
            title=f"Sales in {selected_region.capitalize()} Region"
        )
        fig.update_traces(marker=dict(size=8), hovertemplate="Date: %{x|%Y-%m-%d}<br>Sales: $%{y:,.2f}")

    fig.update_layout(showlegend=False)
    return fig

# Run
if __name__ == '__main__':
    app.run(debug=True)
