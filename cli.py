import typer
from services.zOrders import getOrdersAll, getOrderItems, getOrder
import debugpy
# Habilita la depuración en el puerto 5679
debugpy.listen(('0.0.0.0', 5678))


app = typer.Typer()

@app.command()
def orders(id: int = 0,
           all: bool = True,
           items: bool = False
           ):
    """Cargar lista pedidos, pedidos o items de un pedido """
    response=[]
    
    if(items):
        getOrderItems(id)
    
    if(all):
        response = getOrdersAll(id)
    else:
         response = getOrder(id)
    
    print(response) 


if __name__ == "__main__":
    app()