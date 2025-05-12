import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def cargar_datos(archivo="DATA.xlsx", columna='datos'):
    """Carga los datos desde el archivo Excel"""
    df = pd.read_excel(archivo)
    return df[columna]

def mostrar_estadisticas_basicas(data):
    """Muestra las estadísticas básicas de los datos"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de datos", f"{len(data):,}")
        st.metric("Mínimo", f"{data.min():,.2f}")
        st.metric("Máximo", f"{data.max():,.2f}")
    
    with col2:
        st.metric("Media", f"{data.mean():,.2f}")
        st.metric("Mediana", f"{data.median():,.2f}")
        st.metric("Desviación estándar", f"{data.std():,.2f}")
    
    with col3:
        st.metric("Coeficiente de variación", f"{(data.std() / data.mean() * 100):,.2f}%")
        st.metric("Rango", f"{data.max() - data.min():,.2f}")
        st.metric("Moda", f"{data.mode().iloc[0]:,.2f}")

def crear_histograma_interactivo(data, intervalo):
    """Crea un histograma interactivo con Plotly"""
    # Calcular intervalos
    min_val = data.min()
    max_val = data.max()
    min_rounded = (min_val // intervalo) * intervalo
    max_rounded = ((max_val // intervalo) + 1) * intervalo
    bins = np.arange(min_rounded, max_rounded + intervalo, intervalo)
    
    # Calcular histograma
    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Calcular sumas por intervalo
    suma_total = data.sum()
    sumas_por_intervalo = []
    for i in range(len(bin_edges)-1):
        suma_intervalo = data[(data >= bin_edges[i]) & (data < bin_edges[i+1])].sum()
        sumas_por_intervalo.append(suma_intervalo)
    
    # Crear DataFrame para el gráfico
    df_hist = pd.DataFrame({
        'Rango': [f"{bin_edges[i]:,.0f} - {bin_edges[i+1]:,.0f}" for i in range(len(hist))],
        'Frecuencia': hist,
        'Suma_Importes': sumas_por_intervalo,
        'Porcentaje_Frecuencia': [(h/len(data))*100 for h in hist],
        'Porcentaje_Importes': [(s/suma_total)*100 for s in sumas_por_intervalo]
    })
    
    # Crear gráfico con Plotly
    fig = go.Figure()
    
    # Agregar barras
    fig.add_trace(go.Bar(
        x=df_hist['Rango'],
        y=df_hist['Frecuencia'],
        text=df_hist['Frecuencia'].apply(lambda x: f"{x:,}"),
        textposition='auto',
        name='Frecuencia',
        hovertemplate="<b>%{x}</b><br>" +
                     "Frecuencia: %{y:,}<br>" +
                     "Suma Importes: $" + df_hist['Suma_Importes'].apply(lambda x: f"{x:,.2f}") + "<br>" +
                     "Porcentaje Frecuencia: " + df_hist['Porcentaje_Frecuencia'].apply(lambda x: f"{x:.1f}%") + "<br>" +
                     "Porcentaje Importes: " + df_hist['Porcentaje_Importes'].apply(lambda x: f"{x:.1f}%") +
                     "<extra></extra>"
    ))
    
    # Configurar layout
    fig.update_layout(
        title=f"Distribución de Datos por Intervalos de {intervalo:,}",
        xaxis_title="Rango de Valores",
        yaxis_title="Frecuencia",
        showlegend=False,
        hovermode='x unified',
        template='plotly_white'
    )
    
    # Rotar etiquetas del eje x
    fig.update_xaxes(tickangle=45)
    
    return fig, df_hist

def main():
    st.set_page_config(page_title="Análisis de Datos", layout="wide")
    
    st.title("📊 Análisis de Distribución de Datos")
    
    try:
        # Cargar datos
        data = cargar_datos()
        
        # Sidebar para controles
        st.sidebar.header("Configuración")
        intervalo = st.sidebar.selectbox(
            "Selecciona el tamaño del intervalo:",
            [50000, 100000, 200000, 500000],
            format_func=lambda x: f"{x:,}"
        )
        
        # Mostrar estadísticas básicas
        st.header("Estadísticas Básicas")
        mostrar_estadisticas_basicas(data)
        
        # Crear y mostrar histograma interactivo
        st.header("Histograma Interactivo")
        fig, df_hist = crear_histograma_interactivo(data, intervalo)
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar tabla de datos
        st.header("Tabla de Datos Detallada")
        st.dataframe(
            df_hist.style.format({
                'Frecuencia': '{:,}',
                'Suma_Importes': '${:,.2f}',
                'Porcentaje_Frecuencia': '{:.1f}%',
                'Porcentaje_Importes': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # Agregar descarga de datos
        st.download_button(
            label="📥 Descargar Datos Analizados",
            data=df_hist.to_csv(index=False).encode('utf-8'),
            file_name=f'analisis_intervalo_{intervalo}.csv',
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Asegúrate de que el archivo 'DATA.xlsx' existe y contiene una columna 'datos'")

if __name__ == "__main__":
    main() 