import pdfkit
import requests
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def render_template_to_pdf(template_name: str, data: dict, output_filename: str) -> str:
    """
    Renderiza una plantilla Jinja2 con los datos proporcionados y la convierte a PDF.

    Args:
        template_name (str): Nombre del archivo de la plantilla Jinja2.
        data (dict): Datos a ser insertados en la plantilla.
        output_filename (str): Nombre del archivo PDF de salida.

    Returns:
        str: Nombre del archivo PDF generado.

    Raises:
        TemplateNotFound: Si la plantilla especificada no se encuentra.
        OSError: Si hay un problema con la generación del archivo PDF.
    """
    try:
        # Cargar la plantilla
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)

        # Renderizar la plantilla con los datos
        rendered_html = template.render(data)
        # Definir las opciones de configuración para el PDF
        options = {
            'page-size': 'Letter'  # Tamaño de la hoja Carta
            
        }
        # Convertir el HTML renderizado a PDF
        pdfkit.from_string(rendered_html, output_filename, options=options)

        # Retornar el nombre del archivo PDF generado
        return output_filename
    
    except TemplateNotFound as e:
        print(f"Error: Plantilla '{template_name}' no encontrada.")
        raise e

    except OSError as e:
        print(f"Error: No se pudo generar el archivo PDF '{output_filename}'.")
        raise e
def render_template_to_pdf_gotenberg(template_name: str, data: dict, output_filename: str) -> str:
    """
    Renderiza una plantilla Jinja2 con los datos proporcionados y la convierte a PDF usando Gotenberg.

    Args:
        template_name (str): Nombre del archivo de la plantilla Jinja2.
        data (dict): Datos a ser insertados en la plantilla.
        output_filename (str): Nombre del archivo PDF de salida.

    Returns:
        str: Nombre del archivo PDF generado.

    Raises:
        TemplateNotFound: Si la plantilla especificada no se encuentra.
        OSError: Si hay un problema con la generación del archivo PDF.
    """
    try:
        # Cargar la plantilla
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)

        # Renderizar la plantilla con los datos
        rendered_html = template.render(data)

        # Preparar la solicitud a Gotenberg
        files = {
            'files': ('index.html', rendered_html),
        }
        url = 'http://gotenbertg:3000/forms/chromium/convert/html'

        # Enviar la solicitud a Gotenberg
        response = requests.post(url, files=files)

        if response.status_code == 200:
            # Guardar el archivo PDF
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            return output_filename
        else:
            raise OSError(f"Error: No se pudo generar el archivo PDF '{output_filename}' con Gotenberg. Status code: {response.status_code}")

    except TemplateNotFound as e:
        print(f"Error: Plantilla '{template_name}' no encontrada.")
        raise e

    except OSError as e:
        print(f"Error: No se pudo generar el archivo PDF '{output_filename}'.")
        raise e