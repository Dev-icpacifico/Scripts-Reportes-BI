import pandas as pd
import numpy as np

ruta_salida = './Presupuestos/Salidas'
ruta_bases = './Presupuestos/Bases'
name_centros_costos = str(ruta_salida+'/Centros_de_costos.xlsx')
name_detalle_ppto = ruta_salida+"/Detalle_PPTO.xlsx"



# Importaciones de datos desde las planillas (Tablas) de la base de datos
clases_cc = pd.read_excel(ruta_bases+'/clases_x_cc.xlsx')
clases_x_cc = pd.read_excel(ruta_bases+'/clases_x_cc.xlsx')
ccxedificio = pd.read_excel(ruta_bases+'/ccxedificios.xlsx')
mae_centrocosto = pd.read_excel(ruta_bases+'/maeCentroCosto.xlsx')
preactividades = pd.read_excel(ruta_bases+'/PreActividades.xlsx')
presupuestos = pd.read_excel(ruta_bases+'/Presupuestos.xlsx')
presupuesto_actividades = pd.read_excel(ruta_bases+'/PresupuestoActividad.xlsx')
presupuesto_actividad_recurso = pd.read_excel(ruta_bases+'/PresupuestoActividadRecurso.xlsx')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("-----------------------------Carga de datos exitosa----------------------------")

mae_centrocosto['ctoEmpresa'] = mae_centrocosto['ctoEmpresa'].astype(str)  # Cambio de tipo tipo de dato
mae_centrocosto = mae_centrocosto.drop(mae_centrocosto[mae_centrocosto['ctoEmpresa'] != '104'].index)
# Creación de nueva columna en el maestro de centro de costos (cod empresa + cod cc)
mae_centrocosto['emp_cc'] = mae_centrocosto['ctoEmpresa'].astype(str) + mae_centrocosto['ctoCodigo'].astype(str)
# Selección de columnas necesarias del maestro centro de costos
mae_centrocosto = mae_centrocosto[['ctoEmpresa', 'ctoCodigo', 'ctoDescripcion', 'emp_cc']]
mae_centrocosto = pd.merge(mae_centrocosto, clases_x_cc, left_on='emp_cc', right_on='cod_cc', how='left')
print(mae_centrocosto.columns)
mae_centrocosto = mae_centrocosto[['ctoEmpresa','ctoCodigo','ctoDescripcion','emp_cc', 'cod_clase_cc']]
print(mae_centrocosto.columns)
# Impresiones para revisar el maestro de centros de costos
print("-----------------------------Refac del Maestro de Centro de Costos----------------------------")
print(mae_centrocosto.shape)  # Filas y columnas
print(mae_centrocosto.columns)  # Columnas
print(mae_centrocosto.info(verbose=True))  # Tipos de datos
print(mae_centrocosto.head)  # Muestra de las 1eras 5 filas
mae_centrocosto = pd.merge(mae_centrocosto, ccxedificio, left_on='emp_cc', right_on='emp_cc', how='left')
print("-------------------------------------------------------------------------------------------------------")
print(mae_centrocosto.shape)  # Filas y columnas
print(mae_centrocosto.columns)  # Columnas
print(mae_centrocosto.info(verbose=True))  # Tipos de datos
print(mae_centrocosto.head)  # Muestra de las 1eras 5 filas
# Exportación del DataFrame con los centros de costos

mae_centrocosto['emp_cc_short'] = mae_centrocosto['emp_cc'].str[:8]
mae_centrocosto = mae_centrocosto.drop(mae_centrocosto[
                (mae_centrocosto['emp_cc_short'] != '10410301')& # DV1
                (mae_centrocosto['emp_cc_short'] != '10410302')& # DV2
                (mae_centrocosto['emp_cc_short'] != '10410303')& # DV3
                (mae_centrocosto['emp_cc_short'] != '10430101')].index) # CASA 27
mae_centrocosto.to_excel(name_centros_costos, index=False, sheet_name='Centros_de_Costos')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

presupuesto_actividad_recurso = presupuesto_actividad_recurso.drop(
    presupuesto_actividad_recurso[(presupuesto_actividad_recurso['CodigoPresupuesto'] != 'ZZZZZZ039') & (
            presupuesto_actividad_recurso[
                'CodigoPresupuesto'] != 'ZZZZZZ050') & (
                                    presupuesto_actividad_recurso[
                                        'CodigoPresupuesto'] != 'ZZZZZZ049') & (
            presupuesto_actividad_recurso[
                'CodigoPresupuesto'] != 'ZZZZZZ057')].index)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

presupuesto_actividades = presupuesto_actividades.drop(
    presupuesto_actividades[(presupuesto_actividades['CodigoPresupuestoPpto'] != 'ZZZZZZ039') & (
            presupuesto_actividades[
                'CodigoPresupuestoPpto'] != 'ZZZZZZ050') & (
                                    presupuesto_actividades[
                                        'CodigoPresupuestoPpto'] != 'ZZZZZZ049') & (
            presupuesto_actividades[
                'CodigoPresupuestoPpto'] != 'ZZZZZZ057')].index)


# Merge de presupuesto con presupuesto actividades
"""
Este merge se realiza para obtener el cod de la empresa a la que está asociado el detalle del presupuesto
por actividades, centros de costos y valores presupuestados
"""
pre_act_pre = pd.merge(presupuestos, presupuesto_actividades, left_on='CodigoPresupuesto',
                       right_on='CodigoPresupuestoPpto', how='inner', suffixes=('_pre', '_pre_act'))
# CodigoPresupuestoPpto
# Verificación del merge con los métodos Shape y Columns
print('Merge entre presupuesto con presupuesto actividad')
print(pre_act_pre.shape)
print(pre_act_pre.columns)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Selección de columnas para el Data Frame de presupuesto actividades
pre_act_pre = pre_act_pre[['CodigoPresupuesto', 'CodigoActividadPpto', 'DescripcionPpto', 'PrecioUnitarioPpto',
                           'CantidadActividadPpto', 'CentroCosto', 'CodigoArea', 'Empresa']]
# Creación de nuevas columnas id para hacer merge con el Maestro de centro de costos
pre_act_pre['emp_cc'] = pre_act_pre['Empresa'].astype(str) + pre_act_pre['CentroCosto'].astype(str)
"""Exportación preliminar el DataFrame del presupuesto
El argumento index=False evita escribir el índice del DataFrame en el archivo Excel
Se puede comentar, ya que solo es para verificación de datos"""
# pre_act_pre.to_excel('pre_act_pre.xlsx', index=False)

# Merge del DataFrame del detalle del presupuesto con el maestro de centros de costos
print("COLUMNAS DE MAE CENTROCOSTOS")
print(mae_centrocosto.shape)
print(mae_centrocosto.columns)

print("=====================================")
print("COLUMNAS DE PRESUPUESTO ACTIVIDAD")
print(pre_act_pre.shape)
print(pre_act_pre.columns)

pre_act_pre = pre_act_pre.merge(mae_centrocosto, on='emp_cc', suffixes=('_pre', '_cc'))
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", pre_act_pre.shape)
# Cambio de nombres de las columnas:
pre_act_pre = pre_act_pre.rename(columns={'CentroCosto': 'CodCentroCosto'})
pre_act_pre = pre_act_pre.rename(columns={'ctoDescripcion': 'CentroCosto'})

# Creación de nuva columna con el total de presupuesto
pre_act_pre['total_ppttoo'] = pre_act_pre['PrecioUnitarioPpto'].astype(float) * pre_act_pre[
    'CantidadActividadPpto'].astype(float)

"""Exportación preliminar el DataFrame del presupuesto
El argumento index=False evita escribir el índice del DataFrame en el archivo Excel
Se puede comentar, ya que solo es para verificación de datos"""
# pre_act_pre.to_excel('pre_act_pre_2.xlsx', index=False)

"""Merge del nuevo DataFrame del presupuesto con la planilla de clases de centros de costos. 
El Dataframe con las clases de centros de costos fue creado de manera manual según la información entregada
en el control presupuestario de Raúl Briceño """
pre_act_pre = pre_act_pre.merge(clases_cc, left_on='CentroCosto', right_on='cod_cc', how='left',
                                suffixes=('_pre', '_cc'))
print("&&&&&&&&&&&&&&&&&&&&&&&&", pre_act_pre.shape)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
# Filtro de datos para un presupuesto especifico:
Si se quiere filtrar los datos para un presupuesto especifico se debe usar la siguiente linea de codigo:
# pre_act_pre = pre_act_pre.drop(pre_act_pre[pre_act_pre['CodigoPresupuesto']!='ZZZZZZ039'].index)
# pre_act_pre = pre_act_pre.drop(pre_act_pre[(pre_act_pre['CodigoPresupuesto'] != 'ZZZZZZ039') & (pre_act_pre['CodigoPresupuesto'] != 'ZZZZZZ050')].index)
En la linea se debe utilizar el codigo del presupuesto que se quiere para eliminar todos los demás registros
que no corresponden
"""
pre_act_pre = pre_act_pre.drop(pre_act_pre[(pre_act_pre['CodigoPresupuesto'] != 'ZZZZZZ039') & (
        pre_act_pre['CodigoPresupuesto'] != 'ZZZZZZ050') & (
                                                   pre_act_pre['CodigoPresupuesto'] != 'ZZZZZZ049') & (
            presupuesto_actividades[
                'CodigoPresupuestoPpto'] != 'ZZZZZZ057')].index)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""Exportación del DataFrame con los datos del presupuesto
El argumento index=False evita escribir el índice del DataFrame en el archivo Excel
Se puede comentar, ya que solo es para verificación de datos"""
print(pre_act_pre.columns)

pre_act_pre = pre_act_pre[['CodigoPresupuesto', 'CodigoActividadPpto', 'DescripcionPpto',
       'PrecioUnitarioPpto', 'CantidadActividadPpto', 'CodCentroCosto',
       'CodigoArea', 'Empresa', 'emp_cc', 'ctoEmpresa', 'ctoCodigo',
       'CentroCosto', 'cod_clase_cc_pre', 'Edificio', 'total_ppttoo']]



presupuesto_actividad_recurso ['new_id'] =  presupuesto_actividad_recurso['CodigoPresupuesto']+presupuesto_actividad_recurso['CodigoActividad']
pre_act_pre['new_id'] = pre_act_pre['CodigoPresupuesto'] + pre_act_pre['CodigoActividadPpto']

pre_act_pre = pd.merge(pre_act_pre, presupuesto_actividad_recurso, left_on='new_id',
                       right_on='new_id', how='left')
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
pre_act_pre['CantidadRecursoActividad'] = pre_act_pre['CantidadRecursoActividad'].astype(float)
pre_act_pre['PrecioRecurso'] = pre_act_pre['PrecioRecurso'].astype(float)
pre_act_pre['total_actividad'] = pre_act_pre['CantidadRecursoActividad']*pre_act_pre['PrecioRecurso']*pre_act_pre['CantidadActividadPpto']
pre_act_pre = pre_act_pre.rename(columns={'CodigoPresupuesto_x': 'CodigoPresupuesto'})

pre_act_pre = pre_act_pre[['CodigoPresupuesto', 'CodigoActividadPpto', 'DescripcionPpto',
       'PrecioUnitarioPpto', 'CantidadActividadPpto', 'CodCentroCosto',
       'CodigoArea', 'Empresa', 'emp_cc', 'ctoEmpresa', 'ctoCodigo',
       'CentroCosto','Edificio', 'total_ppttoo','CodigoRecurso',
       'CantidadRecursoActividad', 'Factor', 'Rendimiento', 'PrecioRecurso',
       'DescripcionRecurso', 'clase', 'CantidadProy', 'PrecioProy',
       'total_actividad']]

print(pre_act_pre.columns)
pre_act_pre.to_excel(name_detalle_ppto, index=False, sheet_name='Presupuesto Base')