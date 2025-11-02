import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def load_benchmark_data(data_dir):
    """Load all CSV files from the benchmark directory."""
    dataframes = {}
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            path = os.path.join(data_dir, file)
            df = pd.read_csv(path)
            dataframes[file.replace('.csv', '')] = df
    return dataframes

def plot_training_time(df):
    """Plot training time comparison."""
    fig = px.bar(df, x='model', y='training_time',
                 title='Training Time by Model',
                 labels={'training_time': 'Training Time (seconds)',
                        'model': 'Model'})
    fig.update_traces(textposition='outside')
    return fig

def plot_memory_usage(df):
    """Plot memory usage comparison."""
    fig = px.bar(df, x='model', y='memory_usage',
                 title='Memory Usage by Model',
                 labels={'memory_usage': 'Memory Usage (MB)',
                        'model': 'Model'})
    fig.update_traces(textposition='outside')
    return fig

def plot_accuracy_comparison(df):
    """Plot accuracy metrics comparison."""
    fig = px.scatter(df, x='model', y=['accuracy', 'precision', 'recall', 'f1_score'],
                    title='Model Performance Metrics',
                    labels={'value': 'Score', 'model': 'Model',
                           'variable': 'Metric'})
    return fig

def create_benchmark_visualizations(data_dir):
    """Create all benchmark visualizations."""
    # Load data
    data = load_benchmark_data(data_dir)
    
    # Create plots for each dataset
    plots = {}
    for dataset_name, df in data.items():
        plots[dataset_name] = {
            'training_time': plot_training_time(df),
            'memory_usage': plot_memory_usage(df),
            'performance_metrics': plot_accuracy_comparison(df)
        }
    
    return plots

# Usage
if __name__ == "__main__":
    data_dir = "/home/mukullight/Music/hackealt/data/epoch_benchmark_data"
    plots = create_benchmark_visualizations(data_dir)
    
    # Save or display plots as needed
    for dataset, dataset_plots in plots.items():
        for plot_name, fig in dataset_plots.items():
            fig.write_html(f"{dataset}_{plot_name}.html")
