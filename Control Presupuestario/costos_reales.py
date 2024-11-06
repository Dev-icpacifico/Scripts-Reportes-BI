import pandas as pd
import numpy as np

ruta_salida = './Consolidado_Costos'
ruta_bases = './Consolidado_Costos'
name_costos_reales = str(ruta_salida+'/Consolidado_Costos_Reales.xlsx')
# name_detalle_ppto = ruta_salida+"/Detalle_PPTO.xlsx"

# Importaciones de datos desde las planillas (Tablas) de la base de datos
costos_mano_obra = pd.read_excel(ruta_bases+'/Costos_Mano_Obra.xlsx')
costos_subcontratos = pd.read_excel(ruta_bases+'/Costos_subcontratos.xlsx')
costos_materiales = pd.read_excel(ruta_bases+'/Costos_Materiales.xlsx')

# Definir un diccionario de mapeo
mapeo_proyecto = {'ZZZZZZ039': '1041030100000', 'ZZZZZZ050': '1041030200000','ZZZZZZ049': '1043010100000','ZZZZZZ057': '1041030300000'  }

costos_mano_obra = costos_mano_obra[['fecha_inicio','costo_empresa','proyecto','presupuesto','centrocosto','tipo']]
costos_mano_obra = costos_mano_obra.rename(columns={'fecha_inicio': 'fecha'})
costos_mano_obra = costos_mano_obra.rename(columns={'costo_empresa': 'costo(clp)'})
costos_mano_obra = costos_mano_obra.rename(columns={'proyecto': 'unidad_negocio'})
costos_mano_obra = costos_mano_obra.rename(columns={'centrocosto': 'centro_costo'})
costos_mano_obra = costos_mano_obra.rename(columns={'tipo': 'recurso'})
costos_mano_obra['bodega'] = ''
costos_mano_obra['categoria'] = 'Mano de Obra'
costos_mano_obra['unidad_negocio'] = costos_mano_obra['presupuesto'].map(mapeo_proyecto)



costos_subcontratos = costos_subcontratos[['Fecha','Valor EEPP','NumeroPresupuesto','emp_cc','Descripcion']]
costos_subcontratos = costos_subcontratos.rename(columns={'Fecha': 'fecha'})
costos_subcontratos = costos_subcontratos.rename(columns={'Valor EEPP': 'costo(clp)'})
costos_subcontratos = costos_subcontratos.rename(columns={'NumeroPresupuesto': 'presupuesto'})
costos_subcontratos = costos_subcontratos.rename(columns={'emp_cc': 'centro_costo'})
costos_subcontratos = costos_subcontratos.rename(columns={'Descripcion': 'recurso'})
costos_subcontratos['bodega'] = ''
costos_subcontratos['unidad_negocio'] = costos_subcontratos['presupuesto'].map(mapeo_proyecto)
costos_subcontratos['categoria'] = 'Subcontratos'



costos_materiales = costos_materiales[['FechaHoraMov','total_movimiento','cod_bodega','cod_unidad_negocio','CodigoPresupuesto_pre','emp_cc_x', 'crecCodigo', 'recDescripcion']]
costos_materiales = costos_materiales.rename(columns={'FechaHoraMov': 'fecha'})
costos_materiales = costos_materiales.rename(columns={'total_movimiento': 'costo(clp)'})
costos_materiales = costos_materiales.rename(columns={'cod_bodega': 'bodega'})
costos_materiales = costos_materiales.rename(columns={'cod_unidad_negocio': 'unidad_negocio'})
costos_materiales = costos_materiales.rename(columns={'CodigoPresupuesto_pre': 'presupuesto'})
costos_materiales = costos_materiales.rename(columns={'emp_cc_x': 'centro_costo'})
costos_materiales = costos_materiales.rename(columns={'crecCodigo': 'clasificacion'})
costos_materiales = costos_materiales.rename(columns={'recDescripcion': 'recurso'})
costos_maquinaria = costos_materiales

costos_materiales = costos_materiales.drop(costos_materiales[
            (costos_materiales['centro_costo'] == '10410301FGG07') |
            (costos_materiales['centro_costo'] == '1041030200010')|
            (costos_materiales['centro_costo'] == '1041030300005')].index)

costos_materiales['categoria'] = 'Materiales'

costos_maquinaria = costos_maquinaria.drop(costos_maquinaria[
            (costos_maquinaria['centro_costo'] != '10410301FGG07') &
            (costos_maquinaria['centro_costo'] != '1041030200010')&
            (costos_maquinaria['centro_costo'] != '1041030300005')].index)
costos_maquinaria['categoria'] = 'Maquinaria'

print("###############################################################################################################")
print(costos_mano_obra.columns)
print("###############################################################################################################")
print(costos_subcontratos.columns)
print("###############################################################################################################")
print(costos_materiales.columns)

dataframes = [costos_mano_obra, costos_subcontratos, costos_materiales,costos_maquinaria]
# Unir los DataFrames en base al nombre de las columnas
consolidado_costos = pd.concat(dataframes, sort=False)

# Mostrar el DataFrame resultante
print(consolidado_costos.columns)
print(consolidado_costos.shape)
print(consolidado_costos.info)
print("-----------------------------------------------------------------------------------------------------------------")

print("-----------------------------------------------------------------------------------------------------------------")
# consolidado_costos.to_excel('Consolidado_Costos_Reales_pre.xlsx', index=False, sheet_name='Consolidado_Costos')
consolidado_costos = consolidado_costos.drop(consolidado_costos[(consolidado_costos['presupuesto'] == 'ZZZZZZ014') | (
        consolidado_costos['presupuesto'] == 'ZZZZZZ046')].index)
# Mostrar el DataFrame resultante
print(consolidado_costos)
print(consolidado_costos.shape)
print(consolidado_costos.info)
"""
consolidado_costos = consolidado_costos.drop(consolidado_costos[(consolidado_costos['presupuesto'] != 'ZZZZZZ039') & (
        consolidado_costos['presupuesto'] != 'ZZZZZZ050') & (
                                                   consolidado_costos['presupuesto'] != 'ZZZZZZ049') & (
            consolidado_costos[
                'presupuesto'] != 'ZZZZZZ057') & (
            consolidado_costos[
                'presupuesto'] != '')].index)
"""

mapeo_pre = {'10410301':'ZZZZZZ039', '10410302':'ZZZZZZ050','10430101':'ZZZZZZ049','10410303':'ZZZZZZ057'}
consolidado_costos['unidad_negocio'] = consolidado_costos['unidad_negocio'].astype(str)
consolidado_costos['unidad_negocio_short'] = consolidado_costos['unidad_negocio'].str[:8]
consolidado_costos['presupuesto'] = consolidado_costos['unidad_negocio_short'].map(mapeo_pre)

# Mostrar el DataFrame resultante
print(consolidado_costos.columns)
print(consolidado_costos.shape)
print(consolidado_costos.info)

mapeo_clasificacion = {'Mano de Obra':'B', 'Materiales':'C','Subcontratos':'D'}
consolidado_costos['clasificacion_2'] = consolidado_costos['categoria'].map(mapeo_clasificacion)

# Crear la nueva columna 'c' utilizando numpy.where
# consolidado_costos['clasificacion_3'] = np.where(consolidado_costos['clasificacion'] == "NaN", consolidado_costos['clasificacion_2'], consolidado_costos['clasificacion'])
consolidado_costos['clasificacion_3'] = consolidado_costos['clasificacion'].fillna(consolidado_costos['clasificacion_2'])
consolidado_costos = consolidado_costos.drop('clasificacion', axis=1)
consolidado_costos = consolidado_costos.drop('clasificacion_2', axis=1)
consolidado_costos = consolidado_costos.rename(columns={'clasificacion_3': 'clasificacion'})
consolidado_costos.to_excel(name_costos_reales, index=False, sheet_name='Consolidado_Costos')
