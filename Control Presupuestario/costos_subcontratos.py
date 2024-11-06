# Bloque 1: Importacion de bibliotecas----------------------------------------------------------------------------------
import pandas as pd
import numpy as np

# Bloque 2 : Configuración de parametros -----------------------------------------------------------------------------------
dia = '16'
mes = '01'
agno = '2024'
date = dia+mes+agno
date_excel=str(dia+"_"+mes+"_"+agno)
print("Fecha de ejecución: ",dia,"-",mes,"-",agno)
ruta_salida = './Costos_SubContratos/Salidas'
ruta_salida_consolidado_costos = './Consolidado_Costos'
ruta_bases = './Costos_SubContratos/Bases'
name_eepp_mensual = str(ruta_salida+"/Estados de pago al "+date_excel+'.xlsx')
name_consolidado_subcontrato = ruta_salida+"/Historial_pago_subcontratos.xlsx"
name_pactado = ruta_salida+"/Pactado_Subcontratos.xlsx"
name_contratistas = ruta_salida+"/maeSubcontratistas.xlsx"
name_costos_reales = str(ruta_salida_consolidado_costos+'/Costos_subcontratos.xlsx')


# Bloque 3: Importación de archivos (bases-planillas)-----------------------------------------------------------------
subcontratos = pd.read_excel(ruta_bases+'/SubContratos'+date+'.xlsx')
subcontratos_actividades = pd.read_excel(ruta_bases+'/SubContratosActividades'+date+'.xlsx')
cabecera_estado_pago = pd.read_excel(ruta_bases+'/SubContratosCabeceraEstadoPago'+date+'.xlsx')
detalle_estado_pago = pd.read_excel(ruta_bases+'/SubContratosDetalleEstadoPago'+date+'.xlsx')
maeproveedor = pd.read_excel(ruta_bases+'/maeProveedor'+date+'.xlsx')

# ----------------------------------------------------------------------------------------------------------------------
print(" INFO DE DETALLE" , detalle_estado_pago.shape)

# Bloque 4: Subsettings delos archivos importados----------------------------------------------------------------

# Subsetting de subcontratos_actividades Original
subcontratos_actividades = subcontratos_actividades[['IdOrden','IdActividad','Descripcion','Cantidad','PrecioLocal', 'CentroCosto']]
# Subsetting de Cabercera Estados de Pago Original
cabecera_estado_pago = cabecera_estado_pago[['IdOrden','IdEstado', 'Fecha', 'PorcentajeImpuesto']]
# Subsetting de subcontratos Original
subcontratos = subcontratos[['IdOrden', 'TituloOrden','PorcentajeRetencion','CodigoEmpresa','SubContratista','NumeroPresupuesto']]
# Subsetting de mae proveedor para dejar solo los ruts con los nombres
maeproveedor = maeproveedor[['prvRut','prvRazonSocial']]

# Bloque 5: Creación de nuevos ID---------------------------------------------------------------------------------------
subcontratos_actividades['orden_actividad'] = subcontratos_actividades['IdOrden'].astype(str)+subcontratos_actividades['IdActividad'].astype(str)
cabecera_estado_pago['orden_estado'] = cabecera_estado_pago['IdOrden'].astype(str)+cabecera_estado_pago['IdEstado'].astype(str)
detalle_estado_pago['orden_actividad'] = detalle_estado_pago['IdOrden'].astype(str)+detalle_estado_pago['IdActividad'].astype(str)
# Bloque 6: Merge [Detalle estado pago X Subcontratos Actividades]-------------------------------------------------------------------
detalle_estado_pago = detalle_estado_pago.merge(subcontratos_actividades, on='orden_actividad')

# ----------------------------------------------------------------------------------------------------------------------
print(" Nuevas columnas de Detalle Estado Pago", detalle_estado_pago.columns)
print(" INFO DE DETALLE" , detalle_estado_pago.shape)
print("-----")
# Bloque 7: Creación de nuevo ID para proximos Merges-------------------------------------------------------
detalle_estado_pago['orden_estado'] = detalle_estado_pago['IdOrden_x'].astype(str)+detalle_estado_pago['IdEstado'].astype(str)
# ----------------------------------------------------------------------------------------------------------------------
print("Columnas del nuevo Detalle estado Pago", detalle_estado_pago.columns)
# Bloque 8: Nuevos Merges entre bases-------------------------------------------------------------------------
detalle_estado_pago = detalle_estado_pago.merge(cabecera_estado_pago, on='orden_estado')
# ----------------------------------------------------------------------------------------------------------------------
print(" INFO DE DETALLE" , detalle_estado_pago.shape)
print("Columnas del nuevo Detalle estado Pago", detalle_estado_pago.columns)
# ----------------------------------------------------------------------------------------------------------------------
detalle_estado_pago = detalle_estado_pago.merge(subcontratos, on='IdOrden')
# ----------------------------------------------------------------------------------------------------------------------
print("Columnas del nuevo Detalle estado Pago", detalle_estado_pago.columns)
print(" INFO DE DETALLE" , detalle_estado_pago.shape)
print(" INFO DE DETALLE COLUMNAS")
print(detalle_estado_pago.columns)
# ----------------------------------------------------------------------------------------------------------------------
detalle_estado_pago = detalle_estado_pago.merge(maeproveedor, left_on='SubContratista', right_on='prvRut', how='left')
# ----------------------------------------------------------------------------------------------------------------------
print("Columnas del nuevo Detalle estado Pago", detalle_estado_pago.columns)
# Bloque 9: Nuevo Subsettings de la base final: Detalle Estado Pago--------------------------------------------------------------------------
detalle_estado_pago = detalle_estado_pago[['orden_estado','IdOrden_x','IdActividad_x','Descripcion','IdEstado_x','recCodigo','Cantidad_x',
                                           'CantidadPeriodo','PrecioLocal','Fecha','PorcentajeImpuesto','CentroCosto',
                                           'CodigoEmpresa','SubContratista', 'prvRazonSocial','NumeroPresupuesto','PorcentajeRetencion','TituloOrden']]
# ----------------------------------------------------------------------------------------------------------------------
print(" INFO DE DETALLE" , detalle_estado_pago.shape)
# Bloque 10: Creación de nuevas columnas con los Valores Monetarios de los EEPP------------------------------------------------------------
detalle_estado_pago ['Valor EEPP'] = detalle_estado_pago['CantidadPeriodo'].astype(float)*detalle_estado_pago['PrecioLocal'].astype(int)
detalle_estado_pago['Retencion'] = detalle_estado_pago ['Valor EEPP'].astype(int)*(detalle_estado_pago['PorcentajeRetencion'].astype(int)/100)
detalle_estado_pago['Total Neto'] = detalle_estado_pago ['Valor EEPP']-detalle_estado_pago['Retencion']
detalle_estado_pago ['Impuesto'] = detalle_estado_pago['Total Neto']*(detalle_estado_pago['PorcentajeImpuesto'].astype(int)/100)
detalle_estado_pago ['Liquido EEPP'] = detalle_estado_pago['Total Neto']+detalle_estado_pago['Impuesto']
detalle_estado_pago ['emp_cc'] = detalle_estado_pago['CodigoEmpresa'].astype(str)+detalle_estado_pago['CentroCosto'].astype(str)
# mov_cab_det['emp_cc'] = mov_cab_det['Id_Empresa'].astype(str)+mov_cab_det['Id_UAplica2'].astype(str) # Centro de costos
detalle_estado_pago['Fecha'] = pd.to_datetime(detalle_estado_pago['Fecha'],format='%d%m%Y' )
# ----------------------------------------------------------------------------------------------------------------------
print("Columnas del nuevo Detalle estado Pago", detalle_estado_pago.columns)
# Bloque 11: Merger de[Subcontrato Actividades X SubContratos-----------------------------------------------------------------
subcontratos_actividades =  subcontratos_actividades.merge(subcontratos, on='IdOrden')
subcontratos_actividades =  subcontratos_actividades.merge(maeproveedor, left_on='SubContratista', right_on='prvRut', how='left')
# Bloque 12: Creación de nuevas columnas en Subcontrato Actividades-------------------------------------------------------------------
subcontratos_actividades['Total Pactado'] = subcontratos_actividades['Cantidad'].astype(float)*subcontratos_actividades['PrecioLocal'].astype(int)
subcontratos_actividades ['emp_cc'] = subcontratos_actividades['CodigoEmpresa'].astype(str)+subcontratos_actividades['CentroCosto'].astype(str)
# Bloque 13: Creación de nuevo DF con los datos de los proveedores---------------------------------------------------------------
maeSubcontratistas_inicial = subcontratos_actividades[['prvRut','prvRazonSocial']]
maeSubcontratistas = maeSubcontratistas_inicial.drop_duplicates(subset=['prvRut'])
# Bloque 14: Agrupación de las actividades por N° de Orden----------------------------------------------------------------------------------
pactado_subcontratos = subcontratos_actividades.groupby('IdOrden').agg({
    'NumeroPresupuesto': 'first',
    'prvRut': 'first',
    'emp_cc': 'first',
    'Total Pactado': 'sum'
}).reset_index()

# Bloque 15: Exportación de los DF finales para los reportes DE PWBI -----------------------------------------------------------------------------------------------------------
pactado_subcontratos.to_excel(name_pactado,  index=False,sheet_name='pactado_subcontratos')
maeSubcontratistas.to_excel(name_contratistas,  index=False,sheet_name='maeSubcontratistas')
detalle_estado_pago.to_excel(name_eepp_mensual,  index=False,sheet_name='detalle_estado_pago')
detalle_estado_pago.to_excel(name_consolidado_subcontrato,  index=False,sheet_name='detalle_estado_pago')
detalle_estado_pago.to_excel(name_costos_reales,  index=False,sheet_name='detalle_estado_pago')