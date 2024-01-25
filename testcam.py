
from services.takephotos import takephoto
from crud.cameras import fecthCamerabyDoorId


#takephoto(1, 8, "INGRESO")

data = fecthCamerabyDoorId(2)

print(data)
