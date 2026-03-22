from sqlalchemy import create_engine
import pandas as pd
from config import DB_URL, TABLE_NAME

def load_data():
    engine = create_engine(DB_URL)
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, engine)
    return df   