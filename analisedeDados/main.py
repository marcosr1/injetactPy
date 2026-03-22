from database import load_data
from analysis import analysis
import matplotlib.pyplot as plt
import os

def plot_vendas_por_dia(vendas_por_dia):
    plt.figure()
    vendas_por_dia.plot()
    plt.title("Vendas por Dia")
    plt.xlabel("Data")
    plt.ylabel("Valor")
    
    os.makedirs("graficos", exist_ok=True)
    plt.savefig("graficos/vendas_por_dia.png")
    plt.close

def plot_produtos(produtos):

    plt.figure()
    produtos.head(10).plot(kind='bar')

    plt.title("Top Produtos Mais Vendidos")
    plt.xlabel("Produto")
    plt.ylabel("Quantidade")

    os.makedirs("graficos", exist_ok=True)
    plt.savefig("graficos/produtos.png")
    plt.close()

def main():
    print("Carregando Dados")
    df = load_data()
    
    print("Analisando")
    results = analysis(df)
    
    print("Gerando Graficos...")
    if 'vendas_por_dia' in results:
        plot_vendas_por_dia(results['vendas_por_dia'])
    if 'produtos' in results:
        plot_produtos(results['produtos']) 
        
    print("Total de vendas: ", results.get('totaldeVendas'))
    
    print("Outliers encontrados: ")
    print(results.get('outliers'))
    
if __name__ == "__main__":
    main()
    