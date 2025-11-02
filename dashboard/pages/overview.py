import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from pathlib import Path

from dashboard.data.utils import get_number_of_records, total_benchmarks, total_capabilities
from dashboard.decorators import load_df

from dashboard.utils import TITLE

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

category_colors = {
    "coding": "#636EFA",
    "reasoning": "#EF553B",
    "knowledge": "#00CC96",
    "games": "#AB63FA",
    "mathematics": "#FFA15A",
    "agents": "#19D3F3"
}

import json

pth = str(Path(__file__).resolve().parents[2] / "data" / "processed" / "capability_heights.json")
with open(pth) as f:
    data = json.load(f)

capabilities_data = data['all']  # if your JSON has the 'all' key

# === Flattened capabilities data ===
capabilities_data = {k: v for k, v in data['all'].items()}



PAGE_TITLE = "Overview"
dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/", order=0)
file_path = str(Path(__file__).resolve().parents[2] / "data" / "processed" / "data_summary.json")





# === Statistics ===
def calculate_stats(selected_caps):
    if not selected_caps:
        return 0, 0, 0, 0
    improvements, growth_rates, current_scores = [], [], []
    for cap in selected_caps:
        cap_data = capabilities_data[cap]
        scores = list(cap_data['heights'].values())
        years = sorted(cap_data['heights'].keys())
        improvement = scores[-1] - scores[0]
        improvements.append(improvement)
        current_scores.append(scores[-1])
        if len(years) > 1 and scores[0] != 0:
            total_growth = (scores[-1] - scores[0]) / scores[0]
            avg_annual = (total_growth / (len(years) - 1)) * 100
            growth_rates.append(avg_annual)
    avg_improvement = sum(improvements) / len(improvements)
    avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
    return avg_improvement, avg_growth, max(current_scores), min(current_scores)

# === Figure builder ===
def build_figure(selected_caps):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("📈 Timeline Evolution", "📊 Improvement 2019-2025", "⚡ Annual Growth", ""),
        specs=[[{"colspan": 2}, None], [{"type": "bar"}, {"type": "bar"}]],
        row_heights=[0.6, 0.4],
        vertical_spacing=0.12
    )
    
    for name in selected_caps:
        data_cap = capabilities_data[name]
        years = sorted(data_cap["heights"].keys())
        scores = [data_cap["heights"][y] * 100 for y in years]
        color = category_colors.get(data_cap["category"], "#ffffff")
        fig.add_trace(go.Scatter(
            x=years, y=scores, mode="lines+markers", name=name,
            line=dict(color=color, width=3),
            marker=dict(size=10, line=dict(width=2, color='white')),
            hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Score: %{y:.1f}%<extra></extra>"
        ), row=1, col=1)
    
    # Bar 1: improvement
    improvements, names_bar, colors_bar = [], [], []
    for name in selected_caps:
        data_cap = capabilities_data[name]
        years = sorted(data_cap["heights"].keys())
        scores = [data_cap["heights"][y] * 100 for y in years]
        improvements.append(scores[-1] - scores[0])
        names_bar.append(name[:20])
        colors_bar.append(category_colors.get(data_cap["category"], "#ffffff"))
    
    fig.add_trace(go.Bar(
        y=names_bar, x=improvements, orientation='h',
        marker=dict(color=colors_bar, line=dict(color='white', width=1.5)),
        text=[f"+{imp:.1f}%" for imp in improvements],
        textposition='outside',
        showlegend=False
    ), row=2, col=1)
    
    # Bar 2: annual growth
    growths, names_growth, colors_growth = [], [], []
    for name in selected_caps:
        data_cap = capabilities_data[name]
        years = sorted(data_cap["heights"].keys())
        scores = [data_cap["heights"][y] * 100 for y in years]
        if len(years) > 1 and scores[0] != 0:
            avg_growth = ((scores[-1]-scores[0])/(len(years)-1))/scores[0]*100
            growths.append(avg_growth)
            names_growth.append(name[:20])
            colors_growth.append(category_colors.get(data_cap["category"], "#ffffff"))
    
    if growths:
        sorted_growth = sorted(zip(growths, names_growth, colors_growth), reverse=True)
        growths, names_growth, colors_growth = zip(*sorted_growth)
    
    fig.add_trace(go.Bar(
        y=list(names_growth), x=list(growths), orientation='h',
        marker=dict(color=list(colors_growth), line=dict(color='white', width=1.5)),
        text=[f"{g:.1f}%" for g in growths], textposition='outside', showlegend=False
    ), row=2, col=2)
    
    fig.update_layout(
        template="plotly_dark",
        height=900, showlegend=True,
        paper_bgcolor="#0a0a15", plot_bgcolor="#12121e",
        font=dict(family="Arial", size=13, color="white"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig





def layout():
    return [
        html.H3("Overview", className="mb-3"),
        html.P(
            """ A historic overview of the timeline for ai capabilities bottlenecks and breakthroughs. 
            This section provides a brief introduction about the scope of the project
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "-",
                                    id="records",
                                    className="card-title",
                                ),
                                html.H6("Total Records", className="card-subtitle"),
                                
                            ]
                        ),
                        color="#0313a6",
                        
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "-",
                                    id="benchmarks",
                                    className="card-title",
                                ),
                                html.H6("Total Benchmarks", className="card-subtitle"),
                            ]
                        ),
                        color="#0ae6d0",
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("-", id="capabilities", className="card-title"),
                                html.H6("Total Capabilities", className="card-subtitle"),
                            ]
                        ),
                        color="#eae721",
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Row(
                    [dbc.Container([
    dbc.Row(dbc.Col(html.H1("🎯 AI Capability Dashboard", className="text-center mb-4"), width=12)),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("✓ Select Capabilities", class_name="bg-primary text-white"),
                dbc.CardBody(dcc.Checklist(
                    id="capability-checklist",
                    options=[{"label": cap.replace("_", " ").title(), "value": cap} for cap in capabilities_data.keys()],
                    value=["code_generation", "physical_intuition", "scientific_reasoning"],
                    inputStyle={"marginRight": "10px"},
                    labelStyle={"display": "block", "padding": "5px", "cursor": "pointer", "borderRadius": "4px",
                                "marginBottom": "4px", "transition": "all 0.2s"},
                ), style={"maxHeight": "350px", "overflowY": "auto"})
            ], className="mb-4 shadow-sm", style={"borderRadius": "10px"}),
            
            dbc.Card([
                dbc.CardHeader("📊 Statistics", class_name="bg-success text-white"),
                dbc.CardBody(html.Div(id="stats-display", style={"lineHeight": "1.8"}))
            ], className="mb-4 shadow-sm", style={"borderRadius": "10px"}),
            
            dbc.Card([
                dbc.CardHeader("🎨 Categories", class_name="bg-info text-white"),
                dbc.CardBody([
                    html.Div([
                        html.Span("●", style={"color": color, "fontSize": "18px", "marginRight": "8px"}),
                        html.Span(cat.title())
                    ], className="mb-2") for cat, color in category_colors.items()
                ])
            ], className="shadow-sm", style={"borderRadius": "10px"}),
        ], width=3),
        
        dbc.Col(dcc.Graph(id="capability-graph", figure=build_figure(["code_generation", "physical_intuition", "scientific_reasoning"])), width=9)
    ])
], fluid=True, style={"backgroundColor": "#0a0a15", "minHeight": "100vh", "paddingTop": "20px", "paddingBottom": "40px"})

                    ]
                ),
            ],
            class_name="g-3",
        ),
    ]



@callback(
    [
        Output("records", "children"),
        Output("benchmarks", "children"),
        Output("capabilities", "children"),
    ],
    Input("url", "pathname"),  # Trigger on page load
)
@load_df
def update_overview(df: pd.DataFrame, _) -> tuple:
    """Callback to update numbers on the top of homepage."""
    return (
        get_number_of_records(file_path),
        total_benchmarks(file_path),
        total_capabilities(file_path),

    )

@callback(
    [Output("capability-graph", "figure"), Output("stats-display", "children")],
    [Input("capability-checklist", "value")]
)
def update_dashboard(selected_caps):
    fig = build_figure(selected_caps)
    avg_imp, avg_growth, max_score, min_score = calculate_stats(selected_caps)
    stats = [
        html.Div([html.Strong("Active Capabilities: "), html.Span(f"{len(selected_caps)}/{len(capabilities_data)}")]),
        html.Div([html.Strong("Avg Improvement: "), html.Span(f"+{avg_imp:.1f}%")]),
        html.Div([html.Strong("Avg Annual Growth: "), html.Span(f"{avg_growth:.1f}%")]),
        html.Div([html.Strong("Score Range: "), html.Span(f"{min_score:.1f}% - {max_score:.1f}%")])
    ]
    return fig, stats



