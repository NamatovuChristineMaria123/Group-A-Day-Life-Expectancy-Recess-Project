import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


# 📌 Load and clean dataset

df = pd.read_csv("Life_Expectancy_Engineered.csv")
df.columns = df.columns.str.strip()
df['Country'] = df['Country'].astype(str).str.strip()
df['Status'] = df['Status'].astype(str).str.strip()

print("Countries:", df['Country'].unique())
print("Statuses:", df['Status'].unique())


app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Life Expectancy Dashboard"


#  Layout with tabs

app.layout = html.Div([
    html.H1("🌍 Life Expectancy Interactive Dashboard", style={'textAlign': 'center'}),

    dcc.Tabs(id='tabs', value='tab-scatter', children=[
        dcc.Tab(label='Scatter Plot', value='tab-scatter'),
        dcc.Tab(label='Trend Line', value='tab-line'),
        dcc.Tab(label='Boxplot', value='tab-box'),
        dcc.Tab(label='Correlation Heatmap', value='tab-heatmap'),
        dcc.Tab(label='Global Map', value='tab-map'),
        dcc.Tab(label='Summary & Download', value='tab-summary'),
    ]),

    html.Div(id='tabs-content')
])


# 📌 Content per tab

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-scatter':
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
                    {'label': col, 'value': col} for col in [
                        'GDP',
                        'Schooling',
                        'Income composition of resources',
                        'Total_Mortality',
                        'Health_Wealth_Index'
                    ]
                ],
                value='GDP'
            ),

            dcc.Graph(id='scatter-plot')
        ])

    elif tab == 'tab-line':
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
        fig = px.box(
            df,
            x='Status',
            y='Life expectancy',
            title="Life Expectancy: Developed vs Developing"
        )
        return html.Div([
            dcc.Graph(figure=fig)
        ])

    elif tab == 'tab-heatmap':
        corr = df.select_dtypes(include=['float64', 'int64']).corr()
        fig = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.index),
            colorscale='Viridis'
        )
        fig.update_layout(title="Correlation Heatmap")
        return html.Div([
            dcc.Graph(figure=fig)
        ])

    elif tab == 'tab-map':
        latest_year = df['Year'].max()
        map_df = df[df['Year'] == latest_year]
        fig = px.choropleth(
            map_df,
            locations="Country",
            locationmode='country names',
            color="Life expectancy",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"Global Life Expectancy (Year: {latest_year})"
        )
        return html.Div([
            dcc.Graph(figure=fig)
        ])

    elif tab == 'tab-summary':
        return html.Div([
            html.H3("🔑 Key Insights"),
            html.P("""
                 Higher schooling and income composition strongly correlate with higher life expectancy.
                 Countries with high Adult Mortality and HIV/AIDS rates tend to have lower life expectancy.
                 Developed countries generally have higher life expectancy than developing countries.
                 GDP alone does not guarantee high life expectancy — health and education investments matter too.
            """),
            html.H3("⬇️ Download Full Dataset"),
            html.Button("Download CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
        ])


# 📌 Scatter callback

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('country-dropdown', 'value'),
    Input('xaxis-dropdown', 'value')
)
def update_scatter(selected_country, xaxis_col):
    filtered_df = df[df['Country'] == selected_country]
    if filtered_df.empty:
        fig = px.scatter(x=[1, 2], y=[1, 2], title="⚠️ No Data Available")
    else:
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


# Multi-country line trend callback

@app.callback(
    Output('line-plot', 'figure'),
    Input('country-line', 'value')
)
def update_line(selected_countries):
    if isinstance(selected_countries, str):
        selected_countries = [selected_countries]
    filtered_df = df[df['Country'].isin(selected_countries)]
    if filtered_df.empty:
        fig = px.line(x=[1, 2], y=[1, 2], title="⚠️ No Data Available")
    else:
        fig = px.line(
            filtered_df,
            x='Year',
            y='Life expectancy',
            color='Country',
            title=f'Life Expectancy Trends: {", ".join(selected_countries)}'
        )
    return fig


# 📌 Download CSV callback

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    return dcc.send_data_frame(df.to_csv, "life_expectancy_cleaned.csv")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
