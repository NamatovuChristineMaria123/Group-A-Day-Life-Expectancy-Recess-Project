# Import necessary libraries
import dash
from dash import dcc, html  # Dash components for layout and interactivity
from dash.dependencies import Input, Output  # For connecting inputs and outputs in callbacks
import pandas as pd  # Used for loading and manipulating data
import plotly.express as px  # Simplified interface for creating charts
import plotly.figure_factory as ff  # For more complex visualizations like annotated heatmaps

# Load the cleaned and engineered dataset
df = pd.read_csv("Life_Expectancy_Engineered.csv")

# Clean up column names and important fields
df.columns = df.columns.str.strip()  # Remove extra spaces from column names
df['Country'] = df['Country'].astype(str).str.strip()  # Ensure 'Country' values are clean
df['Status'] = df['Status'].astype(str).str.strip()  # Clean 'Status' values

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Life Expectancy Dashboard"

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Group A Life Expectancy Interactive Dashboard", style={'textAlign': 'center'}),

    # Define the tab navigation system
    dcc.Tabs(id='tabs', value='tab-scatter', children=[
        dcc.Tab(label='Scatter Plot', value='tab-scatter'),
        dcc.Tab(label='Trend Line', value='tab-line'),
        dcc.Tab(label='Boxplot', value='tab-box'),
        dcc.Tab(label='Correlation Heatmap', value='tab-heatmap'),
        dcc.Tab(label='Global Map', value='tab-map'),
        dcc.Tab(label='Histogram', value='tab-histogram'),
        dcc.Tab(label='Summary & Download', value='tab-summary'),
    ]),

    # The content for each tab will be rendered here
    html.Div(id='tabs-content')
])

# Callback to update content based on selected tab
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-scatter':
        # Scatter Plot tab layout
        return html.Div([
            html.Label("Select Country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
                value=sorted(df['Country'].unique())[0]
            ),
            html.Label("Select X-Axis Variable:"),
          dcc.Dropdown(
    id='xaxis-dropdown',
    options=[
        {'label': col, 'value': col} 
        for col in df.select_dtypes(include=['float64', 'int64']).columns if col != 'Life expectancy'
    ],
    value='GDP'
),

            dcc.Graph(id='scatter-plot')
        ])

    elif tab == 'tab-line':
        # Trend Line tab layout
        return html.Div([
            html.Label("Select Countries:"),
            dcc.Dropdown(
                id='country-line',
                options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
                value=[sorted(df['Country'].unique())[0]],
                multi=True
            ),
            dcc.Graph(id='line-plot')
        ])

    elif tab == 'tab-box':
        # Boxplot tab layout
        return html.Div([
            html.Label("Show Outliers:"),
            dcc.RadioItems(
                id='outlier-toggle',
                options=[
                    {'label': 'Show', 'value': 'show'},
                    {'label': 'Hide', 'value': 'hide'}
                ],
                value='show',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
            dcc.Graph(id='boxplot-graph')
        ])

    elif tab == 'tab-heatmap':
        # Correlation heatmap layout
        corr = df.select_dtypes(include=['float64', 'int64']).corr()
        fig = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.index),
            colorscale='Viridis',
            zmin=-1, zmax=1,
            showscale=True
        )
        fig.update_layout(title="Correlation Heatmap")
        return html.Div([dcc.Graph(figure=fig)])

    elif tab == 'tab-map':
        # Global map layout
        latest_year = df['Year'].max()
        map_df = df[df['Year'] == latest_year].copy()
        map_df['Country'] = map_df['Country'].str.strip()

        fig = px.choropleth(
            map_df,
            locations="Country",
            locationmode='country names',
            color="Life expectancy",
            hover_name="Country",
            hover_data={
                "Life expectancy": True,
                "GDP": True,
                "Schooling": True,
                "Income composition of resources": True,
                "Health_Wealth_Index": True
            },
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"Global Life Expectancy — Year {latest_year}"
        )

        fig.update_geos(
            showcountries=True,
            showcoastlines=True,
            projection_type="natural earth"
        )

        return html.Div([dcc.Graph(figure=fig)])

    elif tab == 'tab-histogram':
        # Histogram layout
        return html.Div([
            html.Label("Select Variable:"),
            dcc.Dropdown(
                id='histogram-variable',
                options=[{'label': col, 'value': col} for col in [
                    'Life expectancy',
                    'GDP',
                    'Schooling',
                    'Income composition of resources',
                    'Total_Mortality',
                    'Health_Wealth_Index'
                ]],
                value='Life expectancy'
            ),
            html.Label("Filter by Status:"),
            dcc.RadioItems(
                id='status-filter',
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'Developed', 'value': 'Developed'},
                    {'label': 'Developing', 'value': 'Developing'}
                ],
                value='All',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
            dcc.Graph(id='histogram-graph')
        ])

    elif tab == 'tab-summary':
        # Summary and dataset download layout
        return html.Div([
            html.H3("Key Insights"),
            html.P("""
                This dashboard helps identify key socio-economic and health factors influencing life expectancy across countries.
                It supports predictive modeling and data-driven decision-making for health, education, and economic policies.
                The visualizations assist policymakers and researchers in spotting trends and disparities across the world.
            """),
            html.H3("Download Full Dataset"),
            html.Button("Download CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
        ])

# Callback for the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('country-dropdown', 'value'),
    Input('xaxis-dropdown', 'value')
)
def update_scatter(selected_country, xaxis_col):
    filtered_df = df[df['Country'] == selected_country]
    if filtered_df.empty:
        # Return a placeholder chart if no data is available
        fig = px.scatter(x=[1, 2], y=[1, 2], title="No Data Available")
    else:
        # Create scatter plot for selected country and variable
        fig = px.scatter(
            filtered_df,
            x=xaxis_col,
            y='Life expectancy',
            size='Population',
            color='Year',
            hover_name='Year',
            title=f'Life Expectancy vs {xaxis_col} for {selected_country}'
        )
    return fig

# Callback for the trend line
@app.callback(
    Output('line-plot', 'figure'),
    Input('country-line', 'value')
)
def update_line(selected_countries):
    if isinstance(selected_countries, str):
        selected_countries = [selected_countries]
    filtered_df = df[df['Country'].isin(selected_countries)]
    if filtered_df.empty:
        fig = px.line(x=[1, 2], y=[1, 2], title="No Data Available")
    else:
        fig = px.line(
            filtered_df,
            x='Year',
            y='Life expectancy',
            color='Country',
            title=f'Life Expectancy Trends: {", ".join(selected_countries)}'
        )
    return fig

# Callback for the boxplot
@app.callback(
    Output('boxplot-graph', 'figure'),
    Input('outlier-toggle', 'value')
)
def update_boxplot(show_outliers):
    boxmode = 'all' if show_outliers == 'show' else False
    fig = px.box(
        df,
        x='Status',
        y='Life expectancy',
        points=boxmode,
        color='Status',
        title="Life Expectancy by Country Status"
    )
    return fig

# Callback for the histogram
@app.callback(
    Output('histogram-graph', 'figure'),
    Input('histogram-variable', 'value'),
    Input('status-filter', 'value')
)
def update_histogram(selected_var, selected_status):
    filtered_df = df.copy()
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    fig = px.histogram(
        filtered_df,
        x=selected_var,
        nbins=40,
        color='Status',
        marginal='box',
        title=f"Distribution of {selected_var} ({selected_status})"
    )
    fig.update_layout(bargap=0.1)
    return fig

# Callback for downloading the CSV file
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    return dcc.send_data_frame(df.to_csv, "life_expectancy_cleaned.csv")

# Run the app on localhost
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)
