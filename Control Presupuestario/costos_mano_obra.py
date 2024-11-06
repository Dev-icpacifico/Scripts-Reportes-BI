# ------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
from unidecode import unidecode
# ------------------------------------------------------------------------------------------
mes = '03'
agno = '2024'

ruta_salida = './Costos_Mano_Obra/Salidas/Remuneraciones_' + mes + agno + '.xlsx'
ruta_salida_consolidado_costos = './Consolidado_Costos'
ruta_consolidado = './Costos_Mano_Obra/Salidas/Consolidado_Remuneraciones.xlsx'
ruta_bases = './Costos_Mano_Obra/Bases'
name_costos_reales = str(ruta_salida_consolidado_costos+'/Costos_Mano_Obra.xlsx')

# ------------------------------------------------------------------------------------------

consolidado_remuneraciones = pd.read_excel(ruta_consolidado)
libro_rem = pd.read_excel(ruta_bases+"/Libro Remuneraciones " + mes + "-" + agno + ".xlsx")
cargos = pd.read_excel(ruta_bases+"/Cargos por area.xlsx")
datos_demograficos = pd.read_excel(ruta_bases+"/Datos Demograficos.xlsx")
cc_ppto = pd.read_excel(ruta_bases+"/ccyppto.xlsx")

# ------------------------------------------------------------------------------------------

# Cambiar los nombres de las columnas a minúsculas
libro_rem.columns = libro_rem.columns.str.lower()
# Eliminar los acentos de los nombres de las columnas y reemplazar espacios por guiones bajos
libro_rem.columns = [unidecode(col).replace(' ', '_') for col in libro_rem.columns]
# ----------------------------------------------------------------------------------------------------
print("##########################")
libro_rem = libro_rem.rename(columns={'empleado_-_nombre_completo': 'trabajador'})
print(libro_rem.columns)
libro_rem = libro_rem.merge(cargos, on='cargo', suffixes=('_x', '_y'))
libro_rem = libro_rem.rename(columns={'nombre_area': 'proyecto'})
libro_rem['bono_de_produccion'] = libro_rem['bono_de_produccion'] + libro_rem['bono_produccion_/d']
libro_rem['bono_extra'] = libro_rem['bono_extra'] + libro_rem['bono_extra_/d']
libro_rem['bono_incentivo'] = libro_rem['bono_incentivo'] + libro_rem['bono_incentivo_/d']
libro_rem['bono_responsabilidad'] = libro_rem['bono_responsabilidad'] + libro_rem['bono_responsabilidad_/d']
libro_rem['horas_extras_festivas'] = libro_rem['horas_extras_festivas'] + libro_rem['horas_extras_festivas_/d']
libro_rem['horas_extras_50%'] = libro_rem['horas_extras_50%'] + libro_rem['hora_extra_/d']

libro_rem = libro_rem[
    ['fecha_inicio', 'rut', 'trabajador', 'cargo', 'tipo', 'area', 'proyecto', 'fecha_ingreso_compania',
     'dias_trabajados', 'sueldo_base', 'colacion', 'bono_de_produccion','bono_extra',
     'bono_incentivo', 'bono_responsabilidad', 'horas_extras_festivas','horas_extras_50%',
     'indemnizacion_legal_anos_de_servicio','indemnizacion_por_vacaciones', 'indemnizacion_sustitutiva_previo_aviso',
     'movilizacion', 'total_haberes', 'anticipo', 'sueldo_liquido', 'sis', 'mutual_empleador',
     'seguro_cesantia_empleador']]
# Convertir los valores de la columna 'Nombre' a formato con la inicial en mayúscula
libro_rem['cargo'] = libro_rem['cargo'].str.title()
print("##########################")
print(libro_rem.columns)
print("##########################")

libro_rem['costo_empresa'] = libro_rem['total_haberes'] + libro_rem['sis'] + libro_rem['mutual_empleador'] + libro_rem[
    'seguro_cesantia_empleador']
libro_rem['new_id'] = libro_rem['tipo'].astype(str) + libro_rem['proyecto'].astype(str)
libro_rem =  libro_rem.merge(cc_ppto, on='new_id')

libro_rem.drop(columns=['new_id'], inplace=True)


libro_rem = libro_rem.merge(datos_demograficos, on='rut',suffixes=('_x','_y'))
libro_rem.to_excel(ruta_salida, index=False, sheet_name='Remuneraciones' + mes + agno)

consolidado_remuneraciones = pd.concat([consolidado_remuneraciones, libro_rem], axis=0)
consolidado_remuneraciones.to_excel(ruta_consolidado, index=False, sheet_name='Consolidado')
consolidado_remuneraciones.to_excel(name_costos_reales, index=False, sheet_name='Consolidado')