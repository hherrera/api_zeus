import cv2
import time
import io
import base64

class Camera:
    def __init__(self, url):
        self.url= url
        

    def frame(self):
        try:
            # Conectarse a la cámara

            camera = cv2.VideoCapture(self.url)

            # Capturar un cuadro
            ret, frame = camera.read()
            if not ret or frame is None:
                print("Error al capturar el fotograma desde la cámara.")
                return None

            # Codificar el cuadro en base64
            encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
            #encoded_frame = base64.b64encode(encoded_frame)

            # Devolver bytes
            return encoded_frame

        except Exception as e:
            print(f"Error durante la conexión a la cámara: {e}")
            return None
        finally:
            # Cerrar la cámara
            camera.release()
    
    def record_video(self, output_path='output_video.mp4', duration=10):
        try:
            # Conectarse a la cámara
            camera = cv2.VideoCapture(self.url)

            # Configurar el objeto VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = camera.get(cv2.CAP_PROP_FPS)
            width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Grabar video durante la duración especificada
            start_time = time.time()
            while time.time() - start_time < duration:
                ret, frame = camera.read()
                if not ret or frame is None:
                    print("Error al capturar el fotograma desde la cámara.")
                    break

                # Escribir el fotograma en el archivo de video
                out.write(frame)

            print(f"Video guardado en: {output_path}")

        except Exception as e:
            print(f"Error durante la grabación del video: {e}")
        finally:
            # Cerrar la cámara y el objeto VideoWriter
            camera.release()
            out.release()


if __name__ == "__main__":
    import datetime
    ip = "192.168.2.11"
    user = "admin"
    password = "sistemas2023" 
    # 1av1d4esBella
    cam1 = Camera(f"rtsp://{user}:{password}@{ip}:554/cam/realmonitor?channel=1&subtype=1")

    result = cam1.frame()

    if result is not None:
        print("Fotograma capturado exitosamente.")
         # Obtener el timestamp actual
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Crear un nombre de archivo con el timestamp
        file_name = f"fotograma_{timestamp}.jpg"
        with open(file_name, "wb") as file:
         file.write(result)

    
