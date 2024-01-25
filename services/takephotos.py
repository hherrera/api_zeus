from services.cameras import Camera
from crud.cameras import fecthCamerabyId
from crud.photos import uploadPhoto,insertPhotosInflows

import datetime

def takephoto(cam : Camera, inflow_id:int, action : str):
    result = None
    
         
    frame = cam.frame()
    if frame is not None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # Crear un nombre de archivo con el timestamp
            file_name = f"frame_{timestamp}.jpg"
            url_image = uploadPhoto(file_name, frame)
            if url_image is not None:
                if insertPhotosInflows(inflow_id=inflow_id,photos={"url":url_image},action=action)  is not None:
                    return url_image

