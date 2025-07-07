import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import os

# Load the CSV
data_path = os.path.join("..", "data", "pink_morsel_sales_combined.csv")
df = pd.read_csv(data_path)

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'])

# Group by date and region to sum sales per region
grouped = df.groupby(['date', 'region'])['sales'].sum().reset_index()

# Pivot to get regions as columns (for tooltip info)
pivoted = grouped.pivot(index='date', columns='region', values='sales').fillna(0)

# Add total sales column
pivoted['Total Sales'] = pivoted.sum(axis=1)

# Reset index for plotting
final_df = pivoted.reset_index()

# Melt the regional sales back into a string for hover info
def hover_text(row):
    regions = [f"{region}: ${row[region]:,.2f}" for region in pivoted.columns if region != 'Total Sales']
    return f"Date: {row['date'].date()}<br>Total Sales: ${row['Total Sales']:,.2f}<br>" + "<br>".join(regions)

final_df['hover'] = final_df.apply(hover_text, axis=1)

# Create a scatter plot (no lines)
fig = px.scatter(
    final_df,
    x='date',
    y='Total Sales',
    hover_data={'hover': True, 'date': False, 'Total Sales': False},
    labels={'date': 'Date', 'Total Sales': 'Total Sales ($)'},
)

fig.update_traces(marker=dict(size=8), hovertemplate='%{customdata[0]}')
fig.update_layout(title='Total Daily Sales of Pink Morsels', showlegend=False)

# Create Dash app layout
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center'}),
    dcc.Graph(id='sales-scatter-chart', figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
