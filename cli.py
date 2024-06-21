import typer
from services.zOrders import getOrdersAll, getOrderItems, getOrder
from commands.sync import sync_orders
#import debugpy
# Habilita la depuración en el puerto 5679
#debugpy.listen(('0.0.0.0', 5678))


app = typer.Typer()

@app.command()
def orders(id: int = 0,
           all: bool = False,
           new: bool = False,
           status: bool = False
           ):
    """Cargar lista pedidos, pedidos o items de un pedido """
    response=[]
    
    if(status):
        response = sync_orders(type='Status')
    
    if(all):
        response = sync_orders(type='All')
    
    if(new):
        response = sync_orders(type='New')
    if(id):
        response = sync_orders(type='One',id=id)  
    
    print(response) 




if __name__ == "__main__":
    app()