import numpy as np
import pandas as pd
from unidecode import unidecode

mes = '09'
agno = '2024'

# ruta_salida = './Salidas/Remuneraciones_' + mes + agno + '.xlsx'
ruta_consolidado = './Salidas/Consolidados/Consolidado_datos_reporte_maranguiz.xlsx'
ruta_vigente = './Salidas/Dotacion_vigente_al_' + mes + '_' + agno + '.xlsx'
ruta_consolidado_vigente = './Salidas/Consolidados/Consolidado_Dotacion_vigente.xlsx'
report_builder = pd.read_excel("./Bases/Builder.xlsx")

consolidado_datos = pd.read_excel(ruta_consolidado)
consolidado_dotacion_vigente = pd.read_excel(ruta_consolidado_vigente)
libro_rem = pd.read_excel("./Bases/" + mes + "-" + agno + ".xlsx")
datos_demograficos = pd.read_excel("./Bases/Datos Demograficos.xlsx")
centros_costos = pd.read_excel("./Bases/Centros_C_rep_rrhh.xlsx")
area_sup = pd.read_excel("./Bases/Areas_supervisores.xlsx")

# print(type(libro_rem))
print(libro_rem.shape)
print(centros_costos.head())
# Cambiar los nombres de las columnas a minúsculas
libro_rem.columns = libro_rem.columns.str.lower()

# Eliminar los acentos de los nombres de las columnas y reemplazar espacios por guiones bajos
libro_rem.columns = [unidecode(col).replace(' ', '_') for col in libro_rem.columns]
libro_rem.columns = [unidecode(col).replace('__', '_') for col in libro_rem.columns]
# print(libro_rem.columns)
libro_rem['empleado_rut'] = libro_rem['empleado_rut'].str.replace('.', '')

libro_rem['haberes_imponibles_bono_de_produccion'] = libro_rem['haberes_imponibles_bono_de_produccion'].astype(int) + \
                                                     libro_rem['haberes_imponibles_bono_produccion_/d'].astype(int)
libro_rem['haberes_imponibles_bono_responsabilidad'] = libro_rem['haberes_imponibles_bono_responsabilidad'].astype(
    int) + libro_rem['haberes_imponibles_bono_responsabilidad_/d'].astype(int)
libro_rem['haberes_imponibles_bono_extra'] = libro_rem['haberes_imponibles_bono_extra'].astype(int) + libro_rem[
    'haberes_imponibles_bono_extra_/d'].astype(int)
libro_rem['haberes_imponibles_horas_extras_festivas'] = libro_rem['haberes_imponibles_horas_extras_festivas'].astype(
    int) + libro_rem['haberes_imponibles_horas_extras_festivas_/d'].astype(int)
libro_rem['haberes_imponibles_horas_extras_50%'] = libro_rem['haberes_imponibles_horas_extras_50%'].astype(int) + \
                                                   libro_rem['haberes_imponibles_hora_extra_/d'].astype(int)
libro_rem['haberes_imponibles_bono_incentivo'] = libro_rem['haberes_imponibles_bono_incentivo'].astype(int) + libro_rem[
    'haberes_imponibles_bono_incentivo_/d'].astype(int)

# Crear una nueva columna 'nueva_columna' basada en la condición de 'fecha_salida' no esté vacío
libro_rem['egreso'] = libro_rem['trabajo_fecha_termino_trabajo'].apply(lambda x: 'Si' if x != '' else '')

libro_rem['costo_empresa_fnqt'] = libro_rem['haberes_no_imponibles_indemnizacion_por_vacaciones'] + libro_rem[
    'haberes_no_imponibles_indemnizacion_sustitutiva_previo_aviso'] + libro_rem[
                                      'haberes_no_imponibles_indemnizacion_voluntaria'] + libro_rem[
                                      'haberes_no_imponibles_indemnizacion_legal_anos_de_servicio']
libro_rem['costo_empresa_haber'] = libro_rem['liquidacion_sueldo_bruto'] - libro_rem['costo_empresa_fnqt']
libro_rem['costo_empresa_mo'] = libro_rem['costo_empresa_haber'] + libro_rem[
    'aportes_patronales_total_aportes_patronales']

# Merge con Centros de Costos
libro_rem = pd.merge(libro_rem, centros_costos, left_on='trabajo_centro_de_costo',
                     right_on='centrocosto', how='inner', suffixes=('_x', '_y'))

print(libro_rem.shape)
# Merge con Datos Demograficos
libro_rem = pd.merge(libro_rem, datos_demograficos, left_on='empleado_rut',
                     right_on='rut', how='left', suffixes=('_x', '_y'))
print(libro_rem.shape)
print(libro_rem.columns)

libro_rem = libro_rem[['periodo', 'empleado_rut',
                       'empleado_nombre_completo', 'trabajo_fecha_ingreso_compania',
                       'trabajo_fecha_termino_trabajo', 'trabajo_razon_de_termino',
                       'trabajo_cargo', 'trabajo_familia_de_cargo', 'trabajo_centro_de_costo',
                       'trabajo_nombre_division', 'trabajo_nombre_area', 'empleado_sexo',
                       'empleado_fecha_de_nacimiento', 'trabajo_nombre_subarea_asignada(o)',
                       'trabajo_nombre_subarea_nivel_1', 'trabajo_nombre_supervisor',
                       'liquidacion_dias_trabajados',
                       'liquidacion_dias_de_ausencias_(aplicadas)',
                       'liquidacion_dias_de_licencias_(aplicadas)',
                       'liquidacion_dias_de_permisos_(aplicadas)',
                       'haberes_imponibles_sueldo_base', 'haberes_imponibles_gratificacion',
                       'haberes_imponibles_bono_de_produccion',
                       'haberes_imponibles_bono_responsabilidad',
                       'haberes_imponibles_bono_permanencia_casa_27',
                       'haberes_imponibles_bono_extra',
                       'haberes_imponibles_bono_turno_extra',
                       'haberes_imponibles_horas_extras_festivas',
                       'haberes_imponibles_bono_turno_festivo',
                       'haberes_imponibles_horas_extras_50%',
                       'haberes_imponibles_dif_mes_anterior',
                       'haberes_imponibles_diferencia_gratificacion',
                       'haberes_imponibles_diferencia_sueldo_imm',
                       'haberes_imponibles_bono_vacaciones',
                       'haberes_imponibles_bono_incentivo',
                       'haberes_no_imponibles_colacion',
                       'haberes_no_imponibles_movilizacion',
                       'haberes_no_imponibles_movilizacion_c27',
                       'haberes_no_imponibles_sala_cuna',
                       'haberes_no_imponibles_asignacion_familiar',
                       'haberes_no_imponibles_asignacion_familiar_retroactiva',
                       'haberes_no_imponibles_asignacion_estudio',
                       'haberes_no_imponibles_indemnizacion_por_vacaciones',
                       'haberes_no_imponibles_indemnizacion_sustitutiva_previo_aviso',
                       'haberes_no_imponibles_indemnizacion_legal_anos_de_servicio',
                       'haberes_no_imponibles_indemnizacion_voluntaria',
                       'liquidacion_sueldo_bruto', 'aportes_patronales_mutual_empleador',
                       'aportes_patronales_seguro_cesantia_empleador',
                       'aportes_patronales_sis', 'aportes_patronales_total_aportes_patronales',
                       'aportes_patronales_trabajo_pesado_empleador', 'egreso',
                       'costo_empresa_fnqt', 'costo_empresa_haber', 'costo_empresa_mo',
                       'centrocosto', 'nombre_centro_costo', 'rut', 'Estado', 'direccion', 'Latitud',
                       'Longitud', 'ciudad', 'region', 'sexo', 'fecha_nacimiento',
                       'nacionalidad', 'estado_civil', 'nivel_escolaridad']]

libro_rem = libro_rem.rename(columns={'trabajo_fecha_ingreso_compania': 'fecha_ingreso_compania'})
libro_rem = libro_rem.rename(columns={'trabajo_fecha_termino_trabajo': 'fecha_termino_trabajo'})
libro_rem = libro_rem.rename(columns={'trabajo_razon_de_termino': 'razon_de_termino'})
libro_rem = libro_rem.rename(columns={'trabajo_cargo': 'cargo'})
libro_rem = libro_rem.rename(columns={'trabajo_familia_de_cargo': 'familia_de_cargo'})
libro_rem = libro_rem.rename(columns={'trabajo_centro_de_costo': 'centro_de_costo'})
libro_rem = libro_rem.rename(columns={'trabajo_nombre_division': 'nombre_division'})
libro_rem = libro_rem.rename(columns={'trabajo_nombre_area': 'nombre_area'})
libro_rem = libro_rem.rename(columns={'trabajo_nombre_subarea_nivel_1': 'nombre_subarea_nivel_1'})
libro_rem = libro_rem.rename(columns={'trabajo_nombre_supervisor': 'nombre_supervisor'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_sueldo_base': 'sueldo_base'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_gratificacion': 'gratificacion'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_de_produccion': 'bono_de_produccion'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_responsabilidad': 'bono_responsabilidad'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_permanencia_casa_27': 'bono_permanencia_casa_27'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_extra': 'bono_extra'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_turno_festivo': 'bono_turno_festivo'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_horas_extras_festivas': 'horas_extras_festivas'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_turno_festivo': 'bono_turno_festivo'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_horas_extras_50%': 'horas_extras_50%'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_dif_mes_anterior': 'dif_mes_anterior'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_diferencia_gratificacion': 'diferencia_gratificacion'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_diferencia_sueldo_imm': 'diferencia_sueldo_imm'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_vacaciones': 'bono_vacaciones'})
libro_rem = libro_rem.rename(columns={'haberes_imponibles_bono_incentivo': 'bono_incentivo'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_colacion': 'colacion'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_movilizacion': 'movilizacion'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_movilizacion_c27': 'movilizacion_c27'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_sala_cuna': 'sala_cuna'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_asignacion_familiar': 'asignacion_familiar'})
libro_rem = libro_rem.rename(
    columns={'haberes_no_imponibles_asignacion_familiar_retroactiva': 'asignacion_familiar_retroactiva'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_asignacion_estudio': 'asignacion_estudio'})
libro_rem = libro_rem.rename(
    columns={'haberes_no_imponibles_indemnizacion_por_vacaciones': 'indemnizacion_por_vacaciones'})
libro_rem = libro_rem.rename(
    columns={'haberes_no_imponibles_indemnizacion_sustitutiva_previo_aviso': 'indemnizacion_sustitutiva_previo_aviso'})
libro_rem = libro_rem.rename(
    columns={'haberes_no_imponibles_indemnizacion_legal_anos_de_servicio': 'indemnizacion_legal_anos_de_servicio'})
libro_rem = libro_rem.rename(columns={'haberes_no_imponibles_indemnizacion_voluntaria': 'indemnizacion_voluntaria'})
libro_rem = libro_rem.rename(columns={'aportes_patronales_mutual_empleador': 'mutual_empleador'})
libro_rem = libro_rem.rename(columns={'aportes_patronales_seguro_cesantia_empleador': 'seguro_cesantia_empleador'})
libro_rem = libro_rem.rename(columns={'aportes_patronales_sis': 'sis'})
libro_rem = libro_rem.rename(columns={'aportes_patronales_total_aportes_patronales': 'total_aportes_patronales'})
libro_rem = libro_rem.rename(columns={'liquidacion_dias_trabajados': 'dias_trabajados'})
libro_rem = libro_rem.rename(columns={'liquidacion_dias_de_ausencias_(aplicadas)': 'dias_de_ausencias_(aplicadas)'})
libro_rem = libro_rem.rename(columns={'liquidacion_dias_de_licencias_(aplicadas)': 'dias_de_licencias_(aplicadas)'})
libro_rem = libro_rem.rename(columns={'liquidacion_dias_de_permisos_(aplicadas)': 'dias_de_permisos_(aplicadas)'})

# Merge con Area Supervisores
libro_rem = pd.merge(libro_rem, area_sup, on='nombre_supervisor', how='left', suffixes=('_x', '_y'))
print(libro_rem.shape)
print(libro_rem.columns)

libro_rem['new_id'] = libro_rem['empleado_rut'].astype(str) + libro_rem['periodo'].astype(str)

datos_builder = report_builder[['new_id', 'Horas totales']]

libro_rem = pd.merge(libro_rem, datos_builder, on='new_id', how='left', suffixes=('_x', '_y'))

dotacion_vigente = libro_rem[libro_rem['fecha_termino_trabajo'].isna()]
consolidado_datos = pd.concat([consolidado_datos, libro_rem], axis=0)
consolidado_datos.to_excel(ruta_consolidado, index=False, sheet_name='Consolidado_mo')
dotacion_vigente.to_excel(ruta_vigente, index=False, sheet_name='Personal Vigente ' + mes + agno)
consolidado_dotacion_vigente = pd.concat([consolidado_dotacion_vigente, dotacion_vigente], axis=0)
consolidado_dotacion_vigente.to_excel(ruta_consolidado_vigente, index=False,
                                      sheet_name='Consolidado_Dotacion_Histórica')
