import pandas as pd

report_builder = pd.read_excel("./Salidas/ReporteBuilder.xlsx")
datos_builder = report_builder[['rut trabajador', 'Fecha', 'EMPRESA', 'TIEMPO']]
# Obtener el primer día del mes para cada fecha
df_reducido = datos_builder.groupby(['rut trabajador', pd.Grouper(key='Fecha', freq='M')])['TIEMPO'].sum().reset_index()
# Renombrar la columna resultante
df_reducido = df_reducido.rename(columns={'TIEMPO': 'Horas totales'})
# Convertir la fecha al primer día de cada mes
df_reducido['Fecha'] = df_reducido['Fecha'].dt.to_period('M').dt.to_timestamp()
# Ahora df_reducido contiene las horas totales trabajadas por cada trabajador en cada mes
# Puedes imprimir el DataFrame resultante
print(df_reducido)
df_reducido['new_id'] = df_reducido['rut trabajador'].astype(str)+df_reducido['Fecha'].astype(str)


# Guardar el DataFrame en un archivo Excel
df_reducido.to_excel('./Bases/Builder.xlsx', index=False, sheet_name='Reporte Horas')
