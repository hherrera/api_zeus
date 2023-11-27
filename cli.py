import typer
from services.zOrders import getOrdersAll, getOrderItems, getOrder
app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def orders(consecutive: int = 0,
           all: bool = True,
             items: bool = False
           ):
    """Cargar pedido o items de una pedido """
    response=[]
    
    if(items):
        getOrderItems(consecutive)
    
    if(all):
        response = getOrdersAll(consecutive)
    else:
         response = getOrder(consecutive)
    
    print(response) 


if __name__ == "__main__":
    app()