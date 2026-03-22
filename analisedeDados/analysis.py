import pandas as pd

def analysis(df): 
    results = {}
    
    if 'createdAt' in df.columns:
        df['createdAt'] = pd.to_datetime(df['createdAt'])
        
    results['resumo'] = df.describe()
    
    if ('total') in df.columns:
        results['totaldeVendas'] = df['total'].sum()
        
    if ('createdAt') in df.columns and 'total' in df.columns:
        vendas_por_dia = df.groupby(df['createdAt'].dt.date)['total'].sum()
        results['vendas_por_dia'] = vendas_por_dia
        
    if 'total' in df.columns:
        media = df['total'].mean()
        desvio = df['total'].std()
        outliers = df[df['total'] > media + 2 * desvio]
        results['outliers'] = outliers
        
    return results