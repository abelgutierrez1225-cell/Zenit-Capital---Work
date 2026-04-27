# Captura de los Instrumentos
## Descripción General

Este script analiza el desempeño del portafolio comparando sus ganancias contra el movimiento del mercado para cada instrumento. El objetivo es medir la captura de mercado, definida como la proporción del movimiento del mercado que fue efectivamente capturada por el portafolio.

El análisis combina información de retornos de mercado, ganancias del portafolio y un cálculo teórico del profit de mercado, permitiendo evaluar la eficiencia del portafolio por instrumento.

## Returns (Esto son los retornos que tuvieron los instrumentos de nuestro portafolio en la semana de 20-03-2026 al 27-03-2026)

Esta sección define los retornos del mercado para cada instrumento durante el periodo analizado.

Se utiliza un diccionario donde cada clave corresponde a un instrumento y su valor representa el retorno porcentual en ese periodo. Estos retornos funcionan como la referencia base del mercado y se utilizan posteriormente para asignar el movimiento de mercado a cada instrumento dentro del análisis.

## Data (De aqui se lee la data utilizada en el codigo y sus variables, el excel "Posicion Optima Futuros 1" estara disponible en el archivo)

En esta sección se carga la información base del portafolio desde un archivo de Excel.

El archivo contiene las variables necesarias para el análisis, incluyendo las ganancias del portafolio y el profit teórico del mercado. Se realiza una normalización de los nombres de columnas eliminando espacios y convirtiéndolos a mayúsculas.

## Clean (Limpieza de datos numéricos provenientes de Excel)

Esta sección se encarga de preparar los datos para el análisis, transformando valores provenientes de Excel a un formato numérico adecuado.

> GANANCIAS = Profit del portafolio (Realized + Unrealized)

Se limpian los valores de la columna de ganancias eliminando separadores de miles y convirtiendo el formato contable de números negativos a formato estándar. Esta variable representa el resultado total del portafolio por instrumento, incluyendo tanto ganancias realizadas como no realizadas.

> MERCADO = Profit teórico del mercado

Se aplica el mismo proceso de limpieza a la columna de mercado. Esta variable representa el profit esperado siguiendo únicamente el movimiento del mercado, sirviendo como punto de comparación para evaluar el desempeño del portafolio.

> CAPTURA = Qué porcentaje del movimiento del mercado capturó el portafolio

La captura se calcula como la relación entre las ganancias del portafolio y el profit del mercado. Esta métrica mide la eficiencia del portafolio en capturar el movimiento del mercado.

> RETURN

Se asigna a cada instrumento su retorno correspondiente mediante un mapeo con el diccionario de retornos definido previamente. Esto permite vincular la información de mercado con los datos del portafolio.

- Filtrado de datos: Se eliminan las filas que no contienen información completa en términos de retorno o captura, asegurando que el análisis se realice únicamente con datos válidos.

- Manejo de divisiones inválidas: Se evita la división por cero recalculando la captura únicamente cuando el valor de mercado es distinto de cero. En caso contrario, se asigna un valor nulo.

- Ordenamiento: Se reorganiza el DataFrame para que los instrumentos sigan el mismo orden definido en el diccionario de retornos. 

## PLOT (Grafica - captura del mercado)

Esta sección genera una visualización que permite comparar el movimiento del mercado con la captura del portafolio para cada instrumento.

> Preparación de datos

Se crea una copia del DataFrame y se definen las variables necesarias para el gráfico:

Movimiento del mercado, PnL ajustado por captura y Colores utilizados.

Se asignan colores según el signo de la captura:
- Verde para captura positiva
- Rojo para captura negativa

> Figura Base

Se construye la figura del gráfico con un tamaño dinámico que depende de la cantidad de instrumentos. También se calcula un rango máximo para escalar adecuadamente los valores.

> Gap Central

Se crea un espacio en el centro del gráfico que separa visualmente los valores positivos y negativos, facilitando la comparación.

Barras de mercado (Retuns de los instrumentos en base al mercado): Se representan los retornos del mercado mediante barras horizontales en color azul claro. Estas barras sirven como referencia base del movimiento del mercado.

Las barras que representan el desempeño del portafolio se dibujan desde el gap central, lo que permite visualizar directamente la captura respecto al movimiento del mercado.

> Nombres de los instrumentos dentro del Gap creado

Los nombres de los instrumentos se colocan en el centro del gráfico, dentro del gap, para mejorar la legibilidad y asociación con sus respectivas barras.

Cuadros de informacion al finalizar las barras (M: representa el return del mercado y C: la captura que tuvimos)

Se agrega información textual al final de cada barra indicando:

- M: retorno del mercado
- C: porcentaje de captura del portafolio

Esto permite una interpretación rápida de los resultados por instrumento.

> Fecha indicando el periodo analizado

Se muestra el rango de fechas correspondiente al periodo analizado, proporcionando contexto temporal al gráfico.

> Leyenda informativa

Se incluye una leyenda que explica el significado de los colores utilizados en el gráfico, diferenciando entre movimiento de mercado y tipos de captura.

