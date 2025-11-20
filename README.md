# Despiezador IA

Herramienta para analizar planos de carpintería y despiece de muebles usando modelos de OpenAI. Incluye agentes para instructor de modelación, analista de piezas y supervisor, además de una interfaz gráfica en progreso.

## Requisitos

- Python 3.11+
- Tesseract OCR instalado y accesible (en Windows la ruta usada por defecto es `C:\Program Files\Tesseract-OCR\tesseract.exe`).
- Dependencias del proyecto:
  ```bash
  pip install -r requirements.txt
  ```
- Credenciales de OpenAI en las variables de entorno estándar (`OPENAI_API_KEY`, etc.).

## Estructura del proyecto

> Carpetas `output/` e `input/` no se listan a pedido del usuario.

```
.
|-- assets
|   |-- icons
|   |   |-- AI_icon.svg
|   |   |-- all_star_logo.svg
|   |   |-- analista.svg
|   |   |-- analista_piezas.svg
|   |   |-- diagram_bar.svg
|   |   |-- dolar_icon.svg
|   |   |-- Dropdown.svg
|   |   |-- images.svg
|   |   |-- instructor.svg
|   |   |-- openAI.svg
|   |   |-- pdf_file.svg
|   |   |-- refresh.svg
|   |   |-- supervisor.svg
|   |   \-- upload.svg
|   \-- file_ids.json
|-- src
|   |-- agents
|   |   |-- ai_client.py
|   |   |-- base_agent.py
|   |   |-- sg_analista_piezas.py
|   |   |-- sg_instructor_modelacion.py
+   |   \-- sg_supervisor_piezas.py
|   |-- analista_piezas
|   |   \-- cli.py
|   |-- config
|   |   |-- prompts.py
|   |   |-- resources_rc.py
|   |   \-- settings.py
|   |-- instructor_modelacion
|   |   |-- analyzers
|   |   |   |-- image_analyzer.py
|   |   |   |-- ocr_reader.py
|   |   |   \-- pdf_analyzer.py
|   |   |-- cli.py
|   |   |-- reporter.py
|   |   \-- summarizer.py
|   |-- supervisor_piezas
|   |   \-- cli.py
|   |-- tests
|   |   |-- combobox.py
|   |   |-- combobox_css.py
|   |   |-- test_image_pdf.py
|   |   \-- test_ocr_reader.py
|   |-- ui
|   |   |-- components
|   |   |   |-- chat_area.py
|   |   |   |-- chat_topbar.py
|   |   |   |-- fileitem_widget.py
|   |   |   |-- info_card.py
|   |   |   |-- message_bubble.py
|   |   |   |-- model_combobox.py
|   |   |   \-- sidebar.py
|   |   |-- controllers
|   |   |   |-- furniture_controller.py
|   |   |   \-- sg_model_controller.py
|   |   |-- styles
|   |   |   |-- resources.qrc
|   |   |   \-- style.qss
|   |   |-- windows
|   |   |   \-- main_window.py
|   |   \-- app.py
|   |-- utils
|   |   |-- keywords.py
|   |   |-- paths.py
|   |   |-- scanner.py
|   |   \-- types.py
|   \-- main.py
\-- requirements.txt
```

## Uso rápido (CLI)

1) Coloca los planos en `input/<NombreMueble>/`.
2) Ajusta `NOMBRE_MUEBLE` en `src/main.py`.
3) Ejecuta:
```bash
python -m src.main
```
Esto dispara al instructor, luego al analista y opcionalmente al supervisor de piezas. Los resultados se guardan en `output/<NombreMueble>/`.

## Interfaz gráfica (estado actual)

- Ubicada en `src/ui`. La ventana principal (`ui/windows/main_window.py`) y componentes (sidebar, chat, combo de modelo) están en construcción y aún no cubren todo el flujo de análisis.
- Los estilos se definen en `src/ui/styles/style.qss` y los íconos en `assets/icons/`.

## Notas técnicas

- `agents/ai_client.py` centraliza llamadas a OpenAI y manejo de IDs de archivos (registrados en `assets/file_ids.json`).
- OCR: `instructor_modelacion/analyzers/ocr_reader.py` usa Tesseract; verifica la ruta en `pytesseract.pytesseract.tesseract_cmd`.
- Conversión de PDF a imagen y metadatos: `instructor_modelacion/analyzers/pdf_analyzer.py` (usa PyMuPDF y OpenCV).
- Escaneo de entradas: `utils/scanner.py`.

## Próximos pasos sugeridos

- Completar el flujo del supervisor en `main.py` (actualmente comentado).
- Finalizar la UI y conectar controladores con los agentes.
- Añadir pruebas automáticas para la capa UI/CLI y manejo de errores en OCR/archivo.
