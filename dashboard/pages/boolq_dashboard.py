import dash
import dash_bootstrap_components as dbc
from dash import html
from dashboard.utils import TITLE
from pathlib import Path

PAGE_TITLE = "boolq_dashboard"

dash.register_page(
    __name__, 
    name=PAGE_TITLE, 
    title=f"{PAGE_TITLE} | {TITLE}", 
    order=2
)

htmpath = Path(__file__).resolve().parents[1] / "graphs" / "boolq_dashboard.html"

with open(htmpath, "r", encoding="utf-8") as f:
    html_content = f.read()

def layout():
    return [
        html.H1("BoolQ"),
        html.Iframe(
            srcDoc=html_content,
            style={"width": "100%", "height": "800px", "border": "none"}
        )
    ]
