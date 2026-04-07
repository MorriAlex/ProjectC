import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd

# Загрузка данных
df_raw = pd.read_csv('PP12_ISP23_dashboard.csv', parse_dates=['date'])
df_raw['month'] = df_raw['date'].dt.strftime('%Y-%m')
df_raw['year'] = df_raw['date'].dt.year
df_raw['day'] = df_raw['date'].dt.day

# Создание приложения с тёмной темой
app = dash.Dash(__name__)
app.title = "Дашборд продаж"

# Кастомные стили для тёмной темы
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Стили для тёмной темы
dark_theme = {
    'backgroundColor': '#1e1e1e',
    'textColor': '#e0e0e0',
    'cardBg': '#2d2d2d',
    'borderColor': '#404040',
    'hoverBg': '#3d3d3d',
    'accentColor': '#00b4d8',
    'accentHover': '#0096c7',
    'dangerColor': '#ef476f',
    'successColor': '#06d6a0',
    'warningColor': '#ffd166'
}

# Layout с обновлённым дизайном
app.layout = html.Div([
    # Шапка с градиентом
    html.Div([
        html.H1("📊 Дашборд анализа продаж", style={
            'textAlign': 'center', 
            'margin': '0',
            'color': dark_theme['textColor'],
            'fontSize': '32px',
            'fontWeight': '600',
            'background': f'linear-gradient(135deg, {dark_theme["accentColor"]} 0%, {dark_theme["successColor"]} 100%)',
            '-webkit-background-clip': 'text',
            '-webkit-text-fill-color': 'transparent',
            'background-clip': 'text'
        }),
        html.P("Интерактивная аналитика продаж и прибыли", style={
            'textAlign': 'center', 
            'color': '#aaa',
            'margin': '10px 0 0 0',
            'fontSize': '14px'
        })
    ], style={
        'padding': '30px',
        'background': dark_theme['cardBg'],
        'borderRadius': '10px',
        'marginBottom': '25px',
        'borderBottom': f'3px solid {dark_theme["accentColor"]}'
    }),

    # Блок фильтров
    html.Div([
        html.Div([
            html.Label("📁 Категории:", style={'color': dark_theme['textColor'], 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': cat, 'value': cat} for cat in df_raw['category'].unique()],
                multi=True,
                placeholder="Выберите категории",
                style={'backgroundColor': dark_theme['cardBg'], 'color': dark_theme['textColor']},
                className='dark-dropdown'
            )
        ], style={'flex': '1', 'margin': '10px', 'minWidth': '200px'}),
        
        html.Div([
            html.Label("📍 Регионы:", style={'color': dark_theme['textColor'], 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': reg, 'value': reg} for reg in df_raw['region'].unique()],
                multi=True,
                placeholder="Выберите регионы",
                className='dark-dropdown'
            )
        ], style={'flex': '1', 'margin': '10px', 'minWidth': '200px'}),
        
        html.Div([
            html.Label("📅 Диапазон дат:", style={'color': dark_theme['textColor'], 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df_raw['date'].min(),
                end_date=df_raw['date'].max(),
                display_format='YYYY-MM-DD',
                style={'backgroundColor': dark_theme['cardBg']},
                className='dark-datepicker'
            )
        ], style={'flex': '1', 'margin': '10px', 'minWidth': '250px'}),
        
        html.Div([
            html.Button("🔄 Обновить данные", id="refresh-button", n_clicks=0, style={
                'margin': '28px 10px 0 10px',
                'padding': '10px 24px',
                'background': f'linear-gradient(135deg, {dark_theme["accentColor"]} 0%, {dark_theme["successColor"]} 100%)',
                'color': 'white',
                'border': 'none',
                'borderRadius': '8px',
                'fontSize': '14px',
                'fontWeight': '500',
                'cursor': 'pointer',
                'transition': 'transform 0.2s, box-shadow 0.2s'
            })
        ])
    ], style={
        'display': 'flex', 
        'flexWrap': 'wrap',
        'marginBottom': '30px',
        'padding': '20px',
        'background': dark_theme['cardBg'],
        'borderRadius': '12px',
        'gap': '10px'
    }),

    # KPI карточки
    html.Div([
        html.Div([
            html.Div("💰", style={'fontSize': '32px', 'marginBottom': '10px'}),
            html.H5("Общая выручка", style={'margin': '0', 'color': '#aaa', 'fontSize': '14px'}),
            html.H2(id="total-sales", style={'margin': '10px 0 0 0', 'color': dark_theme['successColor'], 'fontSize': '28px'})
        ], style={
            'flex': '1',
            'background': dark_theme['cardBg'],
            'borderRadius': '12px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'border': f'1px solid {dark_theme["borderColor"]}',
            'transition': 'transform 0.2s',
            'cursor': 'pointer'
        }, className='kpi-card'),
        
        html.Div([
            html.Div("📈", style={'fontSize': '32px', 'marginBottom': '10px'}),
            html.H5("Общая прибыль", style={'margin': '0', 'color': '#aaa', 'fontSize': '14px'}),
            html.H2(id="total-profit", style={'margin': '10px 0 0 0', 'color': dark_theme['accentColor'], 'fontSize': '28px'})
        ], style={
            'flex': '1',
            'background': dark_theme['cardBg'],
            'borderRadius': '12px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'border': f'1px solid {dark_theme["borderColor"]}'
        }, className='kpi-card'),
        
        html.Div([
            html.Div("📊", style={'fontSize': '32px', 'marginBottom': '10px'}),
            html.H5("Средняя рентабельность", style={'margin': '0', 'color': '#aaa', 'fontSize': '14px'}),
            html.H2(id="avg-margin", style={'margin': '10px 0 0 0', 'color': dark_theme['warningColor'], 'fontSize': '28px'})
        ], style={
            'flex': '1',
            'background': dark_theme['cardBg'],
            'borderRadius': '12px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'border': f'1px solid {dark_theme["borderColor"]}'
        }, className='kpi-card'),
        
        html.Div([
            html.Div("🔄", style={'fontSize': '32px', 'marginBottom': '10px'}),
            html.H5("Количество транзакций", style={'margin': '0', 'color': '#aaa', 'fontSize': '14px'}),
            html.H2(id="transaction-count", style={'margin': '10px 0 0 0', 'color': dark_theme['dangerColor'], 'fontSize': '28px'})
        ], style={
            'flex': '1',
            'background': dark_theme['cardBg'],
            'borderRadius': '12px',
            'padding': '20px',
            'margin': '10px',
            'textAlign': 'center',
            'border': f'1px solid {dark_theme["borderColor"]}'
        }, className='kpi-card')
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '30px'}),

    # Графики
    html.Div([
        html.Div(dcc.Graph(id="line-chart", config={'displayModeBar': False}), 
                style={'width': '49%', 'display': 'inline-block', 'background': dark_theme['cardBg'], 
                       'borderRadius': '12px', 'padding': '15px', 'margin': '0 1% 20px 0'}),
        html.Div(dcc.Graph(id="bar-chart", config={'displayModeBar': False}), 
                style={'width': '49%', 'display': 'inline-block', 'background': dark_theme['cardBg'], 
                       'borderRadius': '12px', 'padding': '15px', 'margin': '0 0 20px 1%'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Div(dcc.Graph(id="pie-chart", config={'displayModeBar': False}), 
                style={'width': '49%', 'display': 'inline-block', 'background': dark_theme['cardBg'], 
                       'borderRadius': '12px', 'padding': '15px', 'margin': '0 1% 0 0'}),
        html.Div([
            html.Div("💡 Ключевые инсайты", style={
                'fontSize': '20px', 
                'fontWeight': '600', 
                'marginBottom': '15px',
                'color': dark_theme['accentColor'],
                'borderBottom': f'2px solid {dark_theme["accentColor"]}',
                'paddingBottom': '10px'
            }),
            html.Div(id="insights-text", style={'color': dark_theme['textColor'], 'lineHeight': '1.6'})
        ], style={
            'width': '49%', 
            'display': 'inline-block', 
            'verticalAlign': 'top', 
            'background': dark_theme['cardBg'],
            'borderRadius': '12px', 
            'padding': '20px',
            'marginLeft': '1%',
            'minHeight': '400px'
        })
    ], style={'marginBottom': '30px'}),

    # Таблица
    html.Div([
        html.H4("📋 Детальные данные", style={
            'color': dark_theme['textColor'], 
            'marginBottom': '15px',
            'fontSize': '18px'
        }),
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": col, "id": col} for col in ['date', 'category', 'sales', 'profit', 'region']],
            page_size=15,
            style_table={'overflowX': 'auto', 'backgroundColor': dark_theme['cardBg']},
            style_header={
                'backgroundColor': dark_theme['borderColor'],
                'color': dark_theme['textColor'],
                'fontWeight': 'bold',
                'border': f'1px solid {dark_theme["borderColor"]}'
            },
            style_cell={
                'textAlign': 'left', 
                'backgroundColor': dark_theme['cardBg'],
                'color': dark_theme['textColor'],
                'border': f'1px solid {dark_theme["borderColor"]}',
                'padding': '10px'
            },
            style_data={
                'color': dark_theme['textColor'],
                'backgroundColor': dark_theme['cardBg']
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#252525'
                }
            ],
            sort_action='native',
            filter_action='native'
        )
    ], style={
        'padding': '20px',
        'background': dark_theme['cardBg'],
        'borderRadius': '12px',
        'marginTop': '20px'
    })
], style={
    'padding': '30px', 
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'backgroundColor': dark_theme['backgroundColor'],
    'minHeight': '100vh'
})

# Кастомный CSS для тёмной темы
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #1e1e1e;
                margin: 0;
                padding: 0;
            }
            .dark-dropdown .Select-control {
                background-color: #2d2d2d !important;
                border-color: #404040 !important;
                color: #e0e0e0 !important;
            }
            .dark-dropdown .Select-menu-outer {
                background-color: #2d2d2d !important;
                border-color: #404040 !important;
            }
            .dark-dropdown .Select-option {
                background-color: #2d2d2d !important;
                color: #e0e0e0 !important;
            }
            .dark-dropdown .Select-option.is-focused {
                background-color: #3d3d3d !important;
            }
            .dark-dropdown .Select-value-label {
                color: #e0e0e0 !important;
            }
            .dark-datepicker input {
                background-color: #2d2d2d !important;
                color: #e0e0e0 !important;
                border-color: #404040 !important;
            }
            .kpi-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            }
            .Select-placeholder {
                color: #888 !important;
            }
            .Select-clear-zone {
                color: #888 !important;
            }
            .Select-arrow-zone {
                color: #888 !important;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,180,216,0.3);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback
@callback(
    [Output('total-sales', 'children'),
     Output('total-profit', 'children'),
     Output('avg-margin', 'children'),
     Output('transaction-count', 'children'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('data-table', 'data'),
     Output('insights-text', 'children')],
    [Input('category-filter', 'value'),
     Input('region-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('refresh-button', 'n_clicks')]
)
def update_dashboard(categories, regions, start_date, end_date, n_clicks):
    if n_clicks > 0:
        df = pd.read_csv('PP12_ISP23_dashboard.csv', parse_dates=['date'])
    else:
        df = df_raw.copy()
    
    if categories:
        df = df[df['category'].isin(categories)]
    if regions:
        df = df[df['region'].isin(regions)]
    if start_date and end_date:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if df.empty:
        empty_fig = px.line(title="Нет данных")
        empty_fig.update_layout(template='plotly_dark', paper_bgcolor='#2d2d2d', plot_bgcolor='#2d2d2d')
        return (
            "0 руб.", "0 руб.", "0%", "0",
            empty_fig, empty_fig, empty_fig,
            [],
            html.P("Нет данных для выбранных фильтров", style={'color': '#aaa', 'textAlign': 'center'})
        )
    
    total_sales = df['sales'].sum()
    total_profit = df['profit'].sum()
    avg_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0
    transaction_count = len(df)
    
    # Графики с тёмной темой
    line_fig = px.line(df, x='date', y=['sales', 'profit'],
                       title='Динамика продаж и прибыли',
                       labels={'value': 'Сумма (руб.)', 'variable': 'Показатель'})
    line_fig.update_layout(template='plotly_dark', paper_bgcolor='#2d2d2d', plot_bgcolor='#2d2d2d',
                           font_color='#e0e0e0', title_font_color='#00b4d8')
    line_fig.update_traces(line=dict(width=3))
    
    bar_data = df.groupby('category', as_index=False)['sales'].sum()
    bar_fig = px.bar(bar_data, x='category', y='sales',
                     title='Продажи по категориям',
                     labels={'sales': 'Выручка (руб.)', 'category': 'Категория'},
                     color='sales', color_continuous_scale='Tealgrn')
    bar_fig.update_layout(template='plotly_dark', paper_bgcolor='#2d2d2d', plot_bgcolor='#2d2d2d',
                          font_color='#e0e0e0', title_font_color='#00b4d8')
    
    pie_data = df.groupby('region', as_index=False)['sales'].sum()
    pie_fig = px.pie(pie_data, values='sales', names='region',
                     title='Доля продаж по регионам',
                     color_discrete_sequence=px.colors.sequential.Tealgrn_r)
    pie_fig.update_layout(template='plotly_dark', paper_bgcolor='#2d2d2d', plot_bgcolor='#2d2d2d',
                          font_color='#e0e0e0', title_font_color='#00b4d8')
    
    table_data = df[['date', 'category', 'sales', 'profit', 'region']].to_dict('records')
    
    max_sale_row = df.loc[df['sales'].idxmax()] if not df.empty else None
    max_profit_row = df.loc[df['profit'].idxmax()] if not df.empty else None
    best_region = df.groupby('region')['profit'].sum().idxmax() if not df.empty else None
    best_category = df.groupby('category')['profit'].sum().idxmax() if not df.empty else None
    
    insights = []
    if max_sale_row is not None:
        insights.append(html.Li([
            html.Span("🏆 ", style={'color': '#ffd166'}),
            f"Максимальная продажа: {max_sale_row['sales']:,.0f} руб. ",
            html.Small(f"({max_sale_row['date'].strftime('%Y-%m-%d')})", style={'color': '#aaa'})
        ], style={'marginBottom': '10px'}))
    if max_profit_row is not None:
        insights.append(html.Li([
            html.Span("💰 ", style={'color': '#06d6a0'}),
            f"Максимальная прибыль: {max_profit_row['profit']:,.0f} руб. ",
            html.Small(f"({max_profit_row['date'].strftime('%Y-%m-%d')})", style={'color': '#aaa'})
        ], style={'marginBottom': '10px'}))
    if best_region:
        insights.append(html.Li([
            html.Span("📍 ", style={'color': '#00b4d8'}),
            f"Самый прибыльный регион: {best_region}"
        ], style={'marginBottom': '10px'}))
    if best_category:
        insights.append(html.Li([
            html.Span("📁 ", style={'color': '#ef476f'}),
            f"Самая прибыльная категория: {best_category}"
        ], style={'marginBottom': '10px'}))
    
    insights_text = html.Ul(insights, style={'listStyleType': 'none', 'paddingLeft': '0'}) if insights else html.P("Нет данных для аналитики", style={'color': '#aaa', 'textAlign': 'center'})
    
    return (
        f"{total_sales:,.0f} ₽",
        f"{total_profit:,.0f} ₽",
        f"{avg_margin:.1f}%",
        f"{transaction_count}",
        line_fig,
        bar_fig,
        pie_fig,
        table_data,
        insights_text
    )

if __name__ == '__main__':
    port = 8050
    print(f"🌙 Дашборд запущен. Откройте в браузере: http://127.0.0.1:{port}")
    app.run(debug=True, port=port)