import pandas as pd
import numpy as np

ruta_salida = './Costos_Materiales/Salidas'
ruta_salida_consolidado_costos = './Consolidado_Costos'
ruta_bases = './Costos_Materiales/Bases'
ruta_bases_externo = './Presupuestos/Salidas'
name_costos_materiales = str(ruta_salida+'/Costos_Materiales.xlsx')
name_costos_reales = str(ruta_salida_consolidado_costos+'/Costos_Materiales.xlsx')
# name_detalle_ppto = ruta_salida+"/Detalle_PPTO.xlsx"

# Importaciones de datos desde las planillas (Tablas) de la base de datos
bod_movimiento = pd.read_excel(ruta_bases+'/bod_movimiento.xlsx')
bod_movimiento_detalle = pd.read_excel(ruta_bases+'/BodMovimientoDetalle.xlsx')
pre_act_pre = pd.read_excel(ruta_bases_externo+'/Detalle_PPTO.xlsx')
mae_centrocosto = pd.read_excel(ruta_bases_externo+'/Centros_de_costos.xlsx')
recursos = pd.read_excel(ruta_bases+'/maerecursos.xlsx')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
recursos = recursos[['crecCodigo', 'srecCodigo', 'grecCodigo', 'recCodigo', 'recDescripcion', 'recUnidad']]

# ######################################################################################################################

# Eliminación de columnas de Bod movimiento detalle
bod_movimiento_detalle.drop(['LIFO', 'DIGITADO', 'PPP'], axis=1)

# Merge de Bod Movimiento con Bod Movimiento Detalle
# mov_cab_det = bod_movimiento.merge(bod_movimiento_detalle, on='Id_Registro', suffixes=('_cab', '_det'))
salidas_bodega = bod_movimiento_detalle.merge(bod_movimiento, on='Id_Registro')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Verificación del merge con los métodos Shape y Columns
print("Primer merge de bod mov con bod movimiento detalle")
print(salidas_bodega.shape)
print(salidas_bodega.columns)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Creación de nuevas columnas id para hacer merge con el Maestro de centro de costos
salidas_bodega['emp_bod'] = salidas_bodega['Id_Empresa'].astype(str) + salidas_bodega['Id_Unid_Captura'].astype(
    str)  # Bodega
salidas_bodega['emp_un_neg'] = salidas_bodega['Id_Empresa'].astype(str) + salidas_bodega['Id_UAplica1'].astype(
    str)  # Unidad Negocio
salidas_bodega['emp_cc'] = salidas_bodega['Id_Empresa'].astype(str) + salidas_bodega['Id_UAplica2'].astype(
    str)  # Centro de costos
# Creación de nueva columna [total_movimiento] = contien el total en $ del movimiento registrado
salidas_bodega['total_movimiento'] = salidas_bodega['Cantidad'] * salidas_bodega['Precio']
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
Se crea un nuevo DataFrame "Costos Reales" que contendrá el merge entre el detalle de los movimientos de la empresa
con el Maestro de Centro de costos para obtener: Bodegas - Unidades de Negocio - Centros de Costos"""

costos_reales = pd.merge(salidas_bodega, mae_centrocosto, left_on='emp_bod', right_on='emp_cc', how='left')
print("Primer costos_reales de merge de mov_cab_det con maecentrocosto")
print(costos_reales.shape)

costos_reales = pd.merge(costos_reales, mae_centrocosto, left_on='emp_un_neg', right_on='emp_cc', how='left')
print("Segundo costos_reales de merge de mov_cab_det con maecentrocosto")
print(costos_reales.shape)

costos_reales = pd.merge(costos_reales, mae_centrocosto, left_on='emp_cc_x', right_on='emp_cc', how='left',
                         suffixes=('_a', '_b'))
print("Tercero costos_reales de merge de mov_cab_det con maecentrocosto")
print(costos_reales.columns)
print(costos_reales.shape)
print("---------------------")
print(pre_act_pre.columns)
print("anterior registros del preac", pre_act_pre.shape)
# df_sin_duplicados = df.drop_duplicates(subset='id', keep='first')
pre_act_pre = pre_act_pre.drop_duplicates(subset='emp_cc', keep='first')
print("nuevos registros del preac", pre_act_pre.shape)

costos_reales = pd.merge(costos_reales, pre_act_pre, left_on='emp_cc_x', right_on='emp_cc', how='left',
                         suffixes=('_ctr', '_pre2'))
print("1er costos_reales merge de mov_cab_det con pre_act_pre")

print(costos_reales.shape)
print(costos_reales.columns)
print("-------------------------------------")

costos_reales['Id_Empresa'] = costos_reales['Id_Empresa'].astype(str)  # Cambio de tipo tipo de dato
costos_reales = costos_reales.drop(costos_reales[costos_reales['Id_Empresa'] != '104'].index)
costos_reales = costos_reales.drop(costos_reales[costos_reales['OrigenMovimiento'] != 'Sal'].index)

print(costos_reales.shape)

# Cambio de nombre a columnas: Bodegas - Unidades de Negocio - Centros de Costos
costos_reales = costos_reales.rename(columns={'emp_bod': 'cod_bodega'})
costos_reales = costos_reales.rename(columns={'emp_un_neg': 'cod_unidad_negocio'})
costos_reales = costos_reales.rename(columns={'ctoDescripcion_y': 'nom_un_neg'})
costos_reales = costos_reales.rename(columns={'ctoDescripcion': 'centro_costo'})
costos_reales = costos_reales.rename(columns={'nombre_clase_ctr': 'categoria_cc'})
costos_reales = costos_reales.rename(columns={'CodigoPresupuesto': 'CodigoPresupuesto_pre'})

costos_reales = costos_reales.drop(
    costos_reales[(costos_reales['nom_un_neg'] != 'DV ETAPA 1') & (costos_reales['nom_un_neg'] != 'DV ETAPA 2') & (
            costos_reales['nom_un_neg'] != 'CASA ARQ Y SERV INM ') & (
            costos_reales['nom_un_neg'] != 'DV ETAPA 3')].index)

print(costos_reales.columns)

costos_reales = costos_reales[['TipoMov', 'Id_Empresa', 'FechaHoraMov', 'OrigenMovimiento', 'Id_Recurso',
                               'total_movimiento', 'cod_bodega', 'cod_unidad_negocio', 'centro_costo',
                               'CodigoPresupuesto_pre', 'emp_cc_x']]
# Nuevo Merge entre los costos reales y el maestro de recursos
costos_reales = pd.merge(costos_reales, recursos, left_on='Id_Recurso', right_on='recCodigo', how='left',
                         suffixes=('_ctr', '_rec'))

print(costos_reales.shape)
print(costos_reales.columns)
costos_materiales = costos_reales
costos_materiales.to_excel(name_costos_materiales, index=False, sheet_name='Costos_Materiales')
costos_materiales.to_excel(name_costos_reales, index=False, sheet_name='Costos_Materiales')