import sys
import os
import pytest
from dash import dcc, html

# Add path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.pink_morsels_dash import app, update_graph

def test_header_present():
    layout = app.layout
    header = layout.children[0]
    assert isinstance(header, html.H1)
    assert header.id == "header"
    assert "Pink Morsel Sales Visualizer" in header.children
    print("✅ The header is present.")

def test_graph_present():
    layout = app.layout
    graph_div = layout.children[2]
    graph = graph_div.children[0]
    assert isinstance(graph, dcc.Graph)
    assert graph.id == "sales-graph"
    print("✅ The visualisation is present.")

def test_region_picker_present():
    layout = app.layout
    radio_div = layout.children[1]
    radio = radio_div.children[1]
    assert isinstance(radio, dcc.RadioItems)
    assert radio.id == "region-selector"
    expected_options = ['all', 'north', 'east', 'south', 'west']
    actual_values = [opt['value'] for opt in radio.options]
    for val in expected_options:
        assert val in actual_values
    print("✅ The region picker is present.")

def test_update_graph_all():
    fig = update_graph("all")
    assert fig.data is not None
    assert fig.layout.title.text == "Total Daily Sales - All Regions"

def test_update_graph_north():
    fig = update_graph("north")
    assert fig.data is not None
    assert fig.layout.title.text == "Sales in North Region"
