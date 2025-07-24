import dash
from dash import dcc, html, Input, Output, dash_table, State, callback_context
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import os

# Generate comprehensive farm data matching React version
def generate_farm_data():
    regions = ['South West', 'South East', 'East Midlands', 'West Midlands', 
               'North West', 'Yorkshire', 'North East', 'East Anglia']
    supplier_tiers = ['Gold', 'Silver', 'Bronze']
    nvz_status = ['NVZ', 'Non-NVZ']
    risk_levels = ['Low', 'Medium', 'High']
    
    farms = []
    for i in range(270):
        farm = {
            'id': f'FARM_{str(i + 1).zfill(3)}',
            'name': f"{np.random.choice(['Green', 'Hill', 'Valley', 'Brook', 'Meadow', 'Field', 'Oak', 'Manor'])} {np.random.choice(['Farm', 'Dairy', 'Estate', 'Holdings'])}",
            'region': np.random.choice(regions),
            'size': np.random.randint(50, 450),
            'herd_size': np.random.randint(80, 380),
            'supplier_tier': np.random.choice(supplier_tiers),
            'nvz_status': np.random.choice(nvz_status),
            'natural_habitat': np.random.randint(5, 30),
            'soil_health': round(3 + np.random.random() * 3, 1),
            'water_efficiency': np.random.randint(70, 95),
            'biodiversity_score': np.random.randint(40, 90),
            'nitrogen_efficiency': np.random.randint(45, 85),
            'phosphorus_efficiency': np.random.randint(50, 85),
            'drought_risk': np.random.choice(risk_levels),
            'flood_risk': np.random.choice(risk_levels),
            'tnfd_compliant': np.random.random() > 0.15,
            'sfi_enrolled': np.random.random() > 0.4,
            'cs_enrolled': np.random.random() > 0.6,
            'overall_score': np.random.randint(50, 90),
            'milk_volume': np.random.randint(500000, 2500000),
            'sustainabilit_premium': np.random.randint(0, 5000) if np.random.random() > 0.3 else 0,
            'last_updated': (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d')
        }
        farms.append(farm)
    
    return pd.DataFrame(farms)

# Initialize the Dash app
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                external_stylesheets=[
                    'https://codepen.io/chriddyp/pen/bWLwgP.css',
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
                ])

# For deployment
server = app.server

# Generate the data
farms_df = generate_farm_data()

# Define the layout with enhanced styling
app.layout = html.Div([
    # Store for selected farm data
    dcc.Store(id='selected-farm-store'),
    
    # Header with gradient
    html.Div([
        html.Div([
            html.Div([
                html.H1("UK Dairy Processor", 
                        style={'color': 'white', 'margin': 0, 'fontSize': '2.5rem'}),
                html.P("Environmental Monitoring Dashboard", 
                       style={'color': '#93c5fd', 'margin': 0, 'fontSize': '1.2rem'})
            ], style={'flex': 1}),
            
            html.Div([
                html.Div([
                    html.Div(className='pulse-dot', style={'width': '10px', 'height': '10px', 
                                  'backgroundColor': '#10b981', 'borderRadius': '50%'}),
                    html.Span("TNFD Compliant", style={'marginLeft': '8px', 'color': 'white'})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginRight': '20px'}),
                
                html.Div([
                    html.Span("270 Supplier Farms", style={'color': '#e0e7ff'})
                ], style={'marginRight': '20px'}),
                
                html.Div([
                    html.Span(f"Last Updated: {datetime.now().strftime('%d/%m/%Y')}", 
                             style={'color': '#e0e7ff'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
    ], style={
        'background': 'linear-gradient(135deg, #1e40af 0%, #059669 100%)',
        'padding': '2rem 3rem',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),
    
    # Main content
    html.Div([
        # Filters Section
        html.Div([
            html.H3("Portfolio Filters", style={'marginBottom': '1.5rem', 'color': '#1f2937'}),
            html.Div([
                html.Div([
                    html.Label("Search Farms", style={'fontWeight': 'bold', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Input(
                        id='search-input',
                        type='text',
                        placeholder='Farm name or ID...',
                        style={'width': '100%', 'padding': '0.5rem', 'borderRadius': '6px', 
                               'border': '1px solid #d1d5db'}
                    )
                ], style={'width': '23%', 'marginRight': '2%'}),
                
                html.Div([
                    html.Label("Region", style={'fontWeight': 'bold', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id='region-dropdown',
                        options=[{'label': 'All Regions', 'value': 'all'}] + 
                                [{'label': r, 'value': r} for r in farms_df['region'].unique()],
                        value='all',
                        style={'width': '100%'}
                    )
                ], style={'width': '23%', 'marginRight': '2%'}),
                
                html.Div([
                    html.Label("Supplier Tier", style={'fontWeight': 'bold', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id='tier-dropdown',
                        options=[{'label': 'All Tiers', 'value': 'all'}] + 
                                [{'label': t, 'value': t} for t in farms_df['supplier_tier'].unique()],
                        value='all',
                        style={'width': '100%'}
                    )
                ], style={'width': '23%', 'marginRight': '2%'}),
                
                html.Div([
                    html.Label("Risk Level", style={'fontWeight': 'bold', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id='risk-dropdown',
                        options=[
                            {'label': 'All Risk Levels', 'value': 'all'},
                            {'label': 'Low', 'value': 'Low'},
                            {'label': 'Medium', 'value': 'Medium'},
                            {'label': 'High', 'value': 'High'}
                        ],
                        value='all',
                        style={'width': '100%'}
                    )
                ], style={'width': '23%'})
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
            
            # Filter summary
            html.Div(id='filter-summary', style={'marginTop': '1rem', 'color': '#6b7280', 'fontSize': '0.9rem'})
        ], style={
            'padding': '2rem',
            'backgroundColor': 'white',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
            'marginBottom': '2rem'
        }),
        
        # Metrics Cards
        html.Div(id='metrics-cards', style={'marginBottom': '2rem'}),
        
        # TNFD Metrics Section
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H4("🌿 Land Metrics", style={'color': '#059669', 'marginBottom': '1rem'}),
                        html.Div(id='land-metrics-content')
                    ], style={
                        'backgroundColor': '#ecfdf5',
                        'padding': '1.5rem',
                        'borderRadius': '12px',
                        'border': '1px solid #86efac'
                    })
                ], style={'width': '32%'}),
                
                html.Div([
                    html.Div([
                        html.H4("💧 Water Metrics", style={'color': '#2563eb', 'marginBottom': '1rem'}),
                        html.Div(id='water-metrics-content')
                    ], style={
                        'backgroundColor': '#eff6ff',
                        'padding': '1.5rem',
                        'borderRadius': '12px',
                        'border': '1px solid #93c5fd'
                    })
                ], style={'width': '32%'}),
                
                html.Div([
                    html.Div([
                        html.H4("🌳 Biodiversity Metrics", style={'color': '#7c3aed', 'marginBottom': '1rem'}),
                        html.Div(id='biodiversity-metrics-content')
                    ], style={
                        'backgroundColor': '#f5f3ff',
                        'padding': '1.5rem',
                        'borderRadius': '12px',
                        'border': '1px solid #c4b5fd'
                    })
                ], style={'width': '32%'})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '2rem'})
        ]),
        
        # Charts Section
        html.Div([
            html.Div([
                html.Div([
                    html.H4("Regional Performance", style={'marginBottom': '1rem'}),
                    dcc.Graph(id='regional-performance-chart')
                ], style={
                    'backgroundColor': 'white',
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
                })
            ], style={'width': '49%'}),
            
            html.Div([
                html.Div([
                    html.H4("Risk Assessment", style={'marginBottom': '1rem'}),
                    dcc.Graph(id='risk-assessment-chart')
                ], style={
                    'backgroundColor': 'white',
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
                })
            ], style={'width': '49%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '2rem'}),
        
        # Additional Charts
        html.Div([
            html.Div([
                html.Div([
                    html.H4("Supplier Tier Distribution", style={'marginBottom': '1rem'}),
                    dcc.Graph(id='tier-distribution-chart')
                ], style={
                    'backgroundColor': 'white',
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
                })
            ], style={'width': '49%'}),
            
            html.Div([
                html.Div([
                    html.H4("Environmental Scheme Enrollment", style={'marginBottom': '1rem'}),
                    dcc.Graph(id='scheme-enrollment-chart')
                ], style={
                    'backgroundColor': 'white',
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
                })
            ], style={'width': '49%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '2rem'}),
        
        # Farm Table
        html.Div([
            html.Div([
                html.H3("Supplier Farm Overview", style={'flex': 1}),
                html.Div([
                    html.Button("Export Data", id='export-btn', 
                               style={'marginRight': '1rem', 'padding': '0.5rem 1rem',
                                     'border': '1px solid #d1d5db', 'borderRadius': '6px',
                                     'backgroundColor': 'white', 'cursor': 'pointer'}),
                    html.Button("Add Farm", id='add-farm-btn',
                               style={'padding': '0.5rem 1rem', 'backgroundColor': '#10b981',
                                     'color': 'white', 'border': 'none', 'borderRadius': '6px',
                                     'cursor': 'pointer'})
                ])
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                     'marginBottom': '1rem'}),
            
            html.Div(id='farm-table-container')
        ], style={
            'backgroundColor': 'white',
            'padding': '2rem',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
        })
    ], style={'padding': '2rem', 'backgroundColor': '#f9fafb'})
])

# Callbacks
@app.callback(
    [Output('metrics-cards', 'children'),
     Output('land-metrics-content', 'children'),
     Output('water-metrics-content', 'children'),
     Output('biodiversity-metrics-content', 'children'),
     Output('regional-performance-chart', 'figure'),
     Output('risk-assessment-chart', 'figure'),
     Output('tier-distribution-chart', 'figure'),
     Output('scheme-enrollment-chart', 'figure'),
     Output('farm-table-container', 'children'),
     Output('filter-summary', 'children')],
    [Input('search-input', 'value'),
     Input('region-dropdown', 'value'),
     Input('tier-dropdown', 'value'),
     Input('risk-dropdown', 'value')]
)
def update_dashboard(search_value, region, tier, risk):
    # Filter data
    filtered_df = farms_df.copy()
    
    if search_value:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_value, case=False) | 
            filtered_df['id'].str.contains(search_value, case=False)
        ]
    
    if region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    if tier != 'all':
        filtered_df = filtered_df[filtered_df['supplier_tier'] == tier]
    
    if risk != 'all':
        filtered_df = filtered_df[
            (filtered_df['drought_risk'] == risk) | (filtered_df['flood_risk'] == risk)
        ]
    
    # Calculate metrics
    total_farms = len(filtered_df)
    tnfd_compliance = (filtered_df['tnfd_compliant'].sum() / total_farms * 100) if total_farms > 0 else 0
    avg_score = filtered_df['overall_score'].mean() if total_farms > 0 else 0
    high_risk = len(filtered_df[(filtered_df['drought_risk'] == 'High') | (filtered_df['flood_risk'] == 'High')])
    high_risk_pct = (high_risk / total_farms * 100) if total_farms > 0 else 0
    
    # Create metric cards
    metrics_cards = html.Div([
        html.Div([
            html.Div(str(total_farms), style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'color': '#1e40af'}),
            html.Div("Total Farms", style={'color': '#6b7280', 'marginTop': '0.5rem'}),
            html.Div("suppliers", style={'fontSize': '0.8rem', 'color': '#9ca3af'})
        ], style={
            'width': '24%',
            'backgroundColor': 'white',
            'padding': '1.5rem',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
            'textAlign': 'center'
        }),
        
        html.Div([
            html.Div(f"{tnfd_compliance:.1f}%", style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'color': '#10b981'}),
            html.Div("TNFD Compliance", style={'color': '#6b7280', 'marginTop': '0.5rem'}),
            html.Div("+12% this quarter", style={'fontSize': '0.8rem', 'color': '#10b981'})
        ], style={
            'width': '24%',
            'backgroundColor': 'white',
            'padding': '1.5rem',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
            'textAlign': 'center'
        }),
        
        html.Div([
            html.Div(f"{avg_score:.0f}/100", style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'color': '#f59e0b'}),
            html.Div("Avg Score", style={'color': '#6b7280', 'marginTop': '0.5rem'}),
            html.Div("+8.1 points", style={'fontSize': '0.8rem', 'color': '#f59e0b'})
        ], style={
            'width': '24%',
            'backgroundColor': 'white',
            'padding': '1.5rem',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
            'textAlign': 'center'
        }),
        
        html.Div([
            html.Div(f"{high_risk_pct:.1f}%", style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'color': '#ef4444'}),
            html.Div("High Risk Farms", style={'color': '#6b7280', 'marginTop': '0.5rem'}),
            html.Div("-3% vs last quarter", style={'fontSize': '0.8rem', 'color': '#10b981'})
        ], style={
            'width': '24%',
            'backgroundColor': 'white',
            'padding': '1.5rem',
            'borderRadius': '12px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
            'textAlign': 'center'
        })
    ], style={'display': 'flex', 'justifyContent': 'space-between'})
    
    # TNFD Metrics
    if total_farms > 0:
        natural_habitat_area = (filtered_df['size'] * filtered_df['natural_habitat'] / 100).sum()
        soil_health_compliance = (filtered_df['soil_health'] >= 4.0).sum() / total_farms * 100
        avg_water_efficiency = filtered_df['water_efficiency'].mean()
        water_compliance = (filtered_df['water_efficiency'] >= 85).sum() / total_farms * 100
        avg_biodiversity = filtered_df['biodiversity_score'].mean()
    else:
        natural_habitat_area = 0
        soil_health_compliance = 0
        avg_water_efficiency = 0
        water_compliance = 0
        avg_biodiversity = 0
    
    land_metrics = html.Div([
        html.Div([
            html.Span("Natural Habitat Coverage", style={'color': '#6b7280'}),
            html.Span(f"{natural_habitat_area:.0f} ha", style={'fontWeight': 'bold', 'color': '#059669'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '0.8rem'}),
        html.Div([
            html.Span("Soil Health Compliance", style={'color': '#6b7280'}),
            html.Span(f"{soil_health_compliance:.1f}%", style={'fontWeight': 'bold', 'color': '#059669'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '0.8rem'}),
        html.Div([
            html.Span("Peatland Exposure", style={'color': '#6b7280'}),
            html.Span(f"{np.random.randint(20, 80)} ha", style={'fontWeight': 'bold', 'color': '#059669'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ])
    
    water_metrics = html.Div([
        html.Div([
            html.Span("Average Efficiency", style={'color': '#6b7280'}),
            html.Span(f"{avg_water_efficiency:.0f}%", style={'fontWeight': 'bold', 'color': '#2563eb'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '0.8rem'}),
        html.Div([
            html.Span("Compliance Rate", style={'color': '#6b7280'}),
            html.Span(f"{water_compliance:.1f}%", style={'fontWeight': 'bold', 'color': '#2563eb'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '0.8rem'}),
        html.Div([
            html.Span("Risk Exposure", style={'color': '#6b7280'}),
            html.Span(f"{high_risk_pct:.1f}%", style={'fontWeight': 'bold', 'color': '#2563eb'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ])
    
    biodiversity_metrics = html.Div([
        html.Div([
            html.Span("Average Score", style={'color': '#6b7280'}),
            html.Span(f"{avg_biodiversity:.0f}/100", style={'fontWeight': 'bold', 'color': '#7c3aed'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '0.8rem'}),
        html.Div([
            html.Span("Species Richness", style={'color': '#6b7280'}),
            html.Span(f"{np.random.randint(20, 35)}", style={'fontWeight': 'bold', 'color': '#7c3aed'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '0.8rem'}),
        html.Div([
            html.Span("Habitat Connectivity", style={'color': '#6b7280'}),
            html.Span(f"{np.random.randint(65, 95)}%", style={'fontWeight': 'bold', 'color': '#7c3aed'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ])
    
    # Regional performance chart
    if total_farms > 0:
        regional_data = filtered_df.groupby('region').agg({
            'id': 'count',
            'overall_score': 'mean',
            'tnfd_compliant': lambda x: (x.sum() / len(x) * 100),
            'milk_volume': 'sum'
        }).reset_index()
        regional_data.columns = ['Region', 'Farms', 'Avg Score', 'TNFD Compliance %', 'Total Volume']
        
        fig1 = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        fig1.add_trace(
            go.Bar(x=regional_data['Region'], y=regional_data['Farms'], 
                   name='Number of Farms', marker_color='#3b82f6'),
            secondary_y=False
        )
        
        fig1.add_trace(
            go.Scatter(x=regional_data['Region'], y=regional_data['Avg Score'], 
                      name='Avg Score', mode='lines+markers', marker_color='#10b981',
                      line=dict(width=3)),
            secondary_y=True
        )
        
        fig1.add_trace(
            go.Scatter(x=regional_data['Region'], y=regional_data['TNFD Compliance %'], 
                      name='TNFD Compliance %', mode='lines+markers', marker_color='#f59e0b',
                      line=dict(width=3)),
            secondary_y=True
        )
        
        fig1.update_xaxes(title_text="Region")
        fig1.update_yaxes(title_text="Number of Farms", secondary_y=False)
        fig1.update_yaxes(title_text="Score / Compliance %", secondary_y=True)
        fig1.update_layout(height=400, hovermode='x unified', plot_bgcolor='white',
                          paper_bgcolor='white', font=dict(size=12))
    else:
        fig1 = go.Figure()
        fig1.update_layout(title="No data available", height=400)
    
    # Risk assessment chart
    if total_farms > 0:
        risk_levels = ['Low', 'Medium', 'High']
        drought_counts = [len(filtered_df[filtered_df['drought_risk'] == r]) for r in risk_levels]
        flood_counts = [len(filtered_df[filtered_df['flood_risk'] == r]) for r in risk_levels]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='Drought Risk', x=risk_levels, y=drought_counts,
                             marker_color='#fbbf24'))
        fig2.add_trace(go.Bar(name='Flood Risk', x=risk_levels, y=flood_counts,
                             marker_color='#60a5fa'))
        fig2.update_layout(barmode='stack', height=400, plot_bgcolor='white',
                          paper_bgcolor='white', font=dict(size=12))
    else:
        fig2 = go.Figure()
        fig2.update_layout(title="No data available", height=400)
    
    # Tier distribution chart
    if total_farms > 0:
        tier_data = filtered_df['supplier_tier'].value_counts()
        colors = {'Gold': '#fbbf24', 'Silver': '#9ca3af', 'Bronze': '#f97316'}
        fig3 = px.pie(values=tier_data.values, names=tier_data.index, 
                     color_discrete_map=colors, hole=0.4)
        fig3.update_layout(height=400, showlegend=True)
    else:
        fig3 = go.Figure()
        fig3.update_layout(title="No data available", height=400)
    
    # Scheme enrollment chart
    if total_farms > 0:
        sfi_enrolled = filtered_df['sfi_enrolled'].sum()
        cs_enrolled = filtered_df['cs_enrolled'].sum()
        both_enrolled = len(filtered_df[filtered_df['sfi_enrolled'] & filtered_df['cs_enrolled']])
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=['SFI Enrolled', 'CS Enrolled', 'Both Schemes'],
            y=[sfi_enrolled, cs_enrolled, both_enrolled],
            marker_color=['#10b981', '#3b82f6', '#7c3aed']
        ))
        fig4.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
                          yaxis_title="Number of Farms")
    else:
        fig4 = go.Figure()
        fig4.update_layout(title="No data available", height=400)
    
    # Farm table
    if total_farms > 0:
        display_df = filtered_df[['name', 'id', 'region', 'supplier_tier', 'size', 
                                'overall_score', 'tnfd_compliant', 'drought_risk', 'flood_risk']].head(50)
        
        # Format TNFD column
        display_df_copy = display_df.copy()
        display_df_copy['tnfd_compliant'] = display_df_copy['tnfd_compliant'].map({True: '✓', False: '✗'})
        
        farm_table = dash_table.DataTable(
            data=display_df_copy.to_dict('records'),
            columns=[
                {'name': 'Farm Name', 'id': 'name'},
                {'name': 'ID', 'id': 'id'},
                {'name': 'Region', 'id': 'region'},
                {'name': 'Tier', 'id': 'supplier_tier'},
                {'name': 'Size (ha)', 'id': 'size'},
                {'name': 'Score', 'id': 'overall_score'},
                {'name': 'TNFD', 'id': 'tnfd_compliant'},
                {'name': 'Drought Risk', 'id': 'drought_risk'},
                {'name': 'Flood Risk', 'id': 'flood_risk'}
            ],
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontFamily': 'Arial, sans-serif'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9fafb'
                },
                {
                    'if': {'column_id': 'supplier_tier', 'filter_query': '{supplier_tier} = Gold'},
                    'backgroundColor': '#fef3c7',
                    'color': '#92400e'
                },
                {
                    'if': {'column_id': 'supplier_tier', 'filter_query': '{supplier_tier} = Silver'},
                    'backgroundColor': '#f3f4f6',
                    'color': '#374151'
                },
                {
                    'if': {'column_id': 'supplier_tier', 'filter_query': '{supplier_tier} = Bronze'},
                    'backgroundColor': '#fed7aa',
                    'color': '#92400e'
                }
            ],
            style_header={
                'backgroundColor': '#f3f4f6',
                'fontWeight': 'bold',
                'borderBottom': '2px solid #e5e7eb'
            },
            page_size=20,
            sort_action="native",
            filter_action="native"
        )
    else:
        farm_table = html.P("No farms match the selected filters", 
                           style={'textAlign': 'center', 'color': '#6b7280', 'padding': '2rem'})
    
    # Filter summary
    filter_summary = html.Div([
        html.Span(f"Showing {total_farms} of {len(farms_df)} farms", style={'marginRight': '2rem'}),
        html.Span([
            html.Span("●", style={'color': '#10b981', 'marginRight': '0.3rem'}),
            f"{filtered_df['tnfd_compliant'].sum() if total_farms > 0 else 0} TNFD Compliant"
        ], style={'marginRight': '2rem'}),
        html.Span([
            html.Span("●", style={'color': '#3b82f6', 'marginRight': '0.3rem'}),
            f"{filtered_df['sfi_enrolled'].sum() if total_farms > 0 else 0} SFI Enrolled"
        ])
    ])
    
    return (metrics_cards, land_metrics, water_metrics, biodiversity_metrics,
            fig1, fig2, fig3, fig4, farm_table, filter_summary)

if __name__ == '__main__':
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port, debug=False)