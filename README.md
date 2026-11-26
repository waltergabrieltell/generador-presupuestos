# Generador de Presupuestos

El **Generador de Presupuestos** es una aplicación gráfica desarrollada con Python y Tkinter. Permite crear, editar y guardar presupuestos de manera sencilla y eficiente. A continuación, se detalla la utilidad, las funciones principales, la tecnología utilizada y cómo usar la aplicación.

## Utilidad
La aplicación es útil para profesionales que necesitan crear y mantener presupuestos de manera rápida y precisa. Permite agregar, editar y eliminar artículos, y calcular automáticamente el total general del presupuesto. Además, facilita la carga y guardado de presupuestos en archivos de texto.

## Funciones Principales

1. **Agregar Artículo**:
   - Permite añadir nuevos artículos al presupuesto.
   - Campos requeridos: Descripción, Cantidad y Precio unitario.

2. **Editar Artículo**:
   - Permite modificar la información de un artículo seleccionado.
   - Selecciona un ítem de la tabla y realiza los cambios en los campos de entrada.

3. **Eliminar Artículo**:
   - Permite eliminar un artículo seleccionado de la tabla.

4. **Guardar Presupuesto**:
   - Permite guardar el presupuesto actual en un archivo de texto con formato específico.

5. **Cargar Presupuesto**:
   - Permite cargar un presupuesto desde un archivo de texto existente.

## Tecnología Utilizada
- **Python**: Lenguaje de programación principal.
- **Tkinter**: Biblioteca estándar de Python para crear interfaces gráficas.

## Cómo Usar la Aplicación

### Paso 1: Ejecutar la Aplicación
1. Asegúrate de tener Python instalado en tu sistema.
2. Descarga o clona el repositorio.
3. Navega hasta el directorio del proyecto en tu terminal o línea de comandos.
4. Ejecuta el archivo `presupuestos.py`:

   ```sh
   python presupuestos.py
   ```

### Paso 2: Crear un Presupuesto
1. **Ingresar Datos Iniciales**:
   - En la sección superior, ingresa los datos del cliente, la moneda y la fecha del presupuesto.

2. **Agregar Artículos**:
   - Ingresar la descripción, cantidad y precio unitario de cada artículo.
   - Haz clic en el botón "Agregar ítem" para añadir el artículo a la tabla.

### Paso 3: Editar Presupuesto
1. **Seleccionar Artículo**:
   - Haz doble clic en el artículo que deseas editar.

2. **Modificar Datos**:
   - Cambia los valores en los campos de entrada correspondientes.

3. **Guardar Cambios**:
   - Haz clic en el botón "Guardar cambios" para guardar los cambios realizados.

### Paso 4: Eliminar Artículos
1. **Seleccionar Artículo**:
   - Haz clic en el ítem que deseas eliminar.

2. **Eliminar**:
   - Haz clic en el botón "Eliminar seleccionado" para eliminar el artículo de la lista.

### Paso 5: Guardar y Cargar Presupuestos
1. **Guardar Presupuesto**:
   - Haz clic en el botón "Guardar presupuesto" para guardar el presupuesto actual en un archivo de texto.
   - Selecciona una ubicación y nombre de archivo, luego haz clic en "Guardar".

2. **Cargar Presupuesto**:
   - Haz clic en el botón "Cargar presupuesto" para cargar un presupuesto desde un archivo de texto existente.
   - Selecciona el archivo de presupuesto, luego haz clic en "Abrir".

## Ejemplo de Archivo de Presupuesto
El archivo de presupuesto debe tener el siguiente formato:

```
Cliente: Walter
Fecha: 2026-11-26
Moneda: Euros

Descripción	Cantidad	Precio unitario	Subtotal
Hojas lizas	100	0.01	1.00 Euros
Lapiz	20	0.1	2.00 Euros
Cuadernos	5	2.0	10.00 Euros
Libro de Matematicas	1	50.0	50.00 Euros

Total general: 63.00 Euros
```

### Notas Adicionales
- La aplicación no permite agregar subtotales manualmente; estos se calculan automáticamente.
- Asegúrate de que el formato del archivo de presupuesto sea exacto para evitar errores.

