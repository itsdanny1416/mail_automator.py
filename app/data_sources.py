import pandas as pd 
from sqlalchemy import create_engine
import os

def load_from_excel(path: str, sheet_name: str | int = 0) -> pd.DataFrame:
    """Load data from an Excel file into a DataFrame."""
    return pd.read_excel(path, sheet_name=sheet_name)

def load_from_sql(query: str) -> pd.DataFrame:
    """Load data from a SQL database into a DataFrame."""
    engine = create_engine (os.environ["SQL_URL"])
    return pd.read_sql_query(query, engine)
 