from typing import List
from helpers.db_supabase import supabase
from helpers.utils import check_url_existence

def insertPhotos(photos: dict):
    """Insert/update, debe incluir al key (id) """
    try:
        data, count = supabase.table('photos').insert(photos).execute()
        return data[1]
    except Exception as e:
        print(f"Error al insertar fotos en la tabla 'photos': {e}")
        return None

def insertPhotosInflows(inflow_id: int, photos: dict, action: str):
    try:
        result = insertPhotos(photos)

        if result is not None:
            print(result)
            inflows_photos = {
                "photo_id": result[0]['id'],
                "inflow_id": inflow_id,
                "action": action.upper()
            }

            print(inflows_photos)
            """Insert photos_inflows """
            data, count = supabase.table('photos_inflows').insert(inflows_photos).execute()

            return data[1]
        else:
            print("Error al obtener el resultado de insertPhotos.")
            return None
    except Exception as e:
        print(f"Error al insertar fotos en la tabla 'photos_inflows': {e}")
        return None

def uploadPhotoInflow(inflow_id:int, image_bytes):
 pass

def uploadPhoto(file_name,image_bytes):
   
    try:
        # Decodificar la cadena base64 a bytes
        
        path_file = f"photos/{file_name}"
        # Subir la imagen a Supabase Storage
        supabase.storage.from_("uploads").upload(path_file, image_bytes,file_options={"content-type": "image/jpg"}) 
        
        image_url = supabase.storage.from_("uploads").get_public_url(path_file)

        if  check_url_existence(image_url):
                print(f"Imagen subida exitosamente a {image_url}")
                return image_url
        else:
                print(f"Error al subir la imagen ")
                return None
    except Exception as e:
        print(f"Error al procesar y subir la imagen: {e}")
        return None

if __name__ == "__main__":
    pass
  