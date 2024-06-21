from services.zQuotations import getRptSalesFormat
from reports.render_report import render_template_to_pdf,render_template_to_pdf_gotenberg


def rpt_quotation_format(consecutive:int,output_file:str)->str:
  ## cargar datos
  data = getRptSalesFormat(consecutive,23)
  ## validar datos
  if data is None or len(data) == 0:
    return None
  ## procesar datos
   
  ## retornar datos
  return render_template_to_pdf(template_name='RptCotizacionDeCliente.html', data=data, output_filename=output_file)

