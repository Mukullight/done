import json
import pandas as pd  # Included for completeness, though not used here


def get_number_of_records(file_path: str) -> int:
    """
    Get the number of records in the dataset by loading the summary JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['total_records']

def total_benchmarks(file_path: str) -> int:
    """
    Get the total number of benchmarks in the dataset by loading the summary JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return len(data['benchmarks'])

def total_capabilities(file_path: str) -> int:
    """
    Get the total number of capabilities in the dataset by loading the summary JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return len(data['capabilities'])




def number_of_countries(df: pd.DataFrame) -> int:
    """Get the number of countries in the dataset."""
    return len(unique_countries(df))


def number_of_restaurants(df: pd.DataFrame) -> int:
    """Get the number of restaurants in the dataset."""
    return len(df.index)


def top_cuisine(df: pd.DataFrame) -> int:
    """Get the top cuisine in the dataset."""
    data = df["Cuisine"].value_counts().index
    if len(data) == 0:
        return "-"
    return data[0]


def number_of_cities(df: pd.DataFrame) -> int:
    """Get the number of cities in the dataset."""
    return len(df[df["City"].notna()]["City"].unique())

def unique_countries(df: pd.DataFrame) -> pd.Series:
    """Get unique countries from the dataset."""
    return df[df["Country"].notna()]["Country"].unique()