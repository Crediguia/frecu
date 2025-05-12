import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def cargar_datos(archivo="DATA.xlsx", columna='datos'):
    """Carga los datos desde el archivo Excel"""
    df = pd.read_excel(archivo)
    return df[columna]

def mostrar_estadisticas_basicas(data):
    """Muestra las estadísticas básicas de los datos"""
    print("\n=== ESTADÍSTICAS BÁSICAS ===")
    print(f"Total de datos: {len(data):,}")
    print(f"Mínimo: {data.min():,.2f}")
    print(f"Máximo: {data.max():,.2f}")
    print(f"Media: {data.mean():,.2f}")
    print(f"Mediana: {data.median():,.2f}")
    print(f"Desviación estándar: {data.std():,.2f}")
    print(f"Coeficiente de variación: {(data.std() / data.mean() * 100):,.2f}%")

def crear_histograma_50k(data):
    """Crea un histograma con intervalos de 50,000 y análisis de porcentajes por suma de importes"""
    # Calcular intervalos
    min_val = data.min()
    max_val = data.max()
    min_rounded = (min_val // 50000) * 50000
    max_rounded = ((max_val // 50000) + 1) * 50000
    bins_50k = np.arange(min_rounded, max_rounded + 50000, 50000)
    
    # Crear histograma
    plt.figure(figsize=(15, 8))  # Aumentado el ancho para mejor visualización
    hist, bin_edges = np.histogram(data, bins=bins_50k)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Calcular suma total y sumas por intervalo
    suma_total = data.sum()
    sumas_por_intervalo = []
    for i in range(len(bin_edges)-1):
        suma_intervalo = data[(data >= bin_edges[i]) & (data < bin_edges[i+1])].sum()
        sumas_por_intervalo.append(suma_intervalo)
    
    # Graficar barras verticales
    plt.bar(bin_centers, hist, width=40000,  # Ajustado el ancho de las barras
            color='skyblue', edgecolor='black', alpha=0.7)
    
    # Añadir etiquetas
    for i, v in enumerate(hist):
        if v > 0:  # Solo mostrar etiquetas para barras con datos
            plt.text(bin_centers[i], v, f"{v:,}", 
                    ha='center', va='bottom')
    
    # Configurar gráfico
    plt.title("Distribución de Datos por Intervalos de 50,000", fontsize=14)
    plt.xlabel("Rango de Valores", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.xticks(bins_50k, rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Mostrar frecuencias y análisis de importes
    print("\n=== ANÁLISIS POR INTERVALO DE 50,000 ===")
    print(f"Suma total de importes: {suma_total:,.2f}")
    print("\nDesglose por intervalo:")
    print("-" * 100)  # Aumentado el ancho de la línea
    print(f"{'Rango':<35} {'Frecuencia':<15} {'Suma Importes':<25} {'% del Total':<15}")
    print("-" * 100)
    
    for i in range(len(hist)):
        if hist[i] > 0:  # Solo mostrar intervalos con datos
            porcentaje_frecuencia = (hist[i] / len(data)) * 100
            porcentaje_importe = (sumas_por_intervalo[i] / suma_total) * 100
            print(f"{bin_edges[i]:,.0f} - {bin_edges[i+1]:,.0f}: {hist[i]:,} datos ({porcentaje_frecuencia:.1f}%) | "
                  f"{sumas_por_intervalo[i]:,.2f} ({porcentaje_importe:.1f}%)")
    
    plt.show()

def main():
    # Cargar datos
    try:
        data = cargar_datos()
        
        # Mostrar estadísticas
        mostrar_estadisticas_basicas(data)
        
        # Crear histograma
        crear_histograma_50k(data)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Asegúrate de que el archivo 'DATA.xlsx' existe y contiene una columna 'datos'")

if __name__ == "__main__":
    main()
