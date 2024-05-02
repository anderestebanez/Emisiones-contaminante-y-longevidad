# Grupo de trabajo Longevidad **Col·legi d´Actuaris de Catalunya**

En el repositorio se ha incluido todo los códigos y análisis realizados para el grupo de trabajo de Longevidad del **Col·legi d´Actuaris de Catalunya**:

* **Definición de métricas** para valorar la capacidad de segmetación por edades de un factor

    Siendo la edad el factor más importante para predecir la probabilidad de fallecer, se generan nuevas métricas que miden la capacidad segmentadora de un factor por edad. 

    Las métricas generadas se pueden agrupar en:

    * Weighted Average Difference (WAD): Son métricas que mide, para un subconjunto de los datos, la diferencia entre la tasa de fallecimiento media por edad del subconjunto respecto al total. Esto permite identificar que factor y que corte de dicho factor genera el subconjunto más diferente a la media. 
    * Mejora en el Square Error por edad: Suma la mejora lograda de la varianza por edad. 

    Resultado, permite valorar de forma masiva cualquier factor numérico y compararlo entre sí. 

    Los códigos están recogidos en el fichero **scr/wad_utils.py** que tiene las siguiente funciones: 
    * Una función por cada métrica creada: wad, wad_estable, wad_relacion y life_squared_error
    * La función para aplicar las métricas a través de un DataFrame: get_best_wad_q
    * Las funciones para hacer _plot_ con el resultado: plot_wad y plot_multiple_wad. 

* **Analisis emisiones contaminante en la longevidad**

    El objetivo es analizar si existe correlación entre las tasas de fallecimiento y la longevidad con las emisiones contaminantes producidas en los diferentes complejos contaminantes de España. 

    Para ello se calcula para cada ciudad de más de 50k habitantes de España las emisiones al aire generadas por los complejos contaminantes que están a 10,20 y 30km a la redonda. 

    Códigos:
    * factores/importDatosPRTR.ipynb: Importa los datos de complejos y emisiones generadas históricas y calcula para cada complejo una serie de factores con la suma, máximo y media histórica de emisiones para cada uno de los elementos contaminantes.
    * resultados/union_kpis_fact.ipynb: Identifica para cada municipio los complejos a 10, 20 o 30km de distancia y les suma los importes calculados en el paso anterior.


* **Cálculo de RME** por causa de fallecimiento y CCAA.
    Se calcula el RME, esto es, los fallecimientos observados entre los estimados en cada CCAA por causa de fallecimiento y año. Para calcular los fallecidos estimados se aplica la tasa de fallecimiento estatal por causa de fallecimiento.

    Como resultado del análisis podemos simplificar la información disponible en el INE quitandole el factor edad y sexo, o solo la edad, facilitando el análisis espacial y temporal de las tasas de fallecimiento por causas.

    Este análisis se basa en el [Atlas Nacional de Mortalidad en España (ANDEES)](https://medea3.shinyapps.io/atlas_nacional/), que fue desarrollado por el grupo de investigación Bayensians de la Fundación FISABIO y la Dirección General de Salud Pública de la Generalitat Valenciana.

    Código:
    * otros/RME_x_Provincia.ipynb

*Rep. GIT: https://github.com/anderestebanez/Analisis_longevidad*


### **Próximos pasos**

* Agregar las emisiones anuales una vez que tenemos las instalaciones cruzadas con los municipios.
* Analisis de la evolución histórica de las emisiones, para identificar el impacto de los cambios de criterios a la hora de informar.
* Usar como variable target las qx por tramos de edad, y ver si las curvas varían según el nivel de emisiones a su alrededor. **CHECK**
* Generar una métrica para medir la capacidad de la variables explicativa de cambiar la curva de Qx. **CHECK**
* Generar nuevas variables explicativas relacionadas con el clima y medio ambiente. Por ejemplo las variables agroclimáticas: https://www.mapa.gob.es/es/agricultura/temas/sistema-de-informacion-geografica-de-datos-agrarios/informacion_agroclimatica.aspx
