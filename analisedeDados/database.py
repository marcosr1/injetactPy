from sqlalchemy import create_engine
import pandas as pd
from config import DB_URL, TABLE_NAME

def load_data():
    engine = create_engine(DB_URL)
    query = '''
        SELECT 
            o.id,
            o."createdAt",
            o.total,
            oi."nomeProduto",
            oi.quantidade,
            oi."precoUnitario"
        FROM "orders" o
        JOIN "orderItems" oi ON oi."orderId" = o.id
    '''
    df = pd.read_sql(query, engine)
    return df   