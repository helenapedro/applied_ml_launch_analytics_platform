import os
import sys
import dash_bootstrap_components as dbc

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.api_description import eda_rest_api

def create_exploration_page():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    eda_rest_api(),
                )
            ),
        ],
        fluid=True,
        className="mt-5 px-4"
    )
