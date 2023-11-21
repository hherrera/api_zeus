
class Camera:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def stream(self):
        import cv2
        import io
        import base64

        # Conectarse a la cámara
        camera = cv2.VideoCapture(f"rtsp://{self.username}:{self.password}@{self.ip}")

        # Iniciar la transmisión
        while True:
            # Capturar un cuadro
            ret, frame = camera.read()

            # Codificar el cuadro en base64
            encoded_frame = cv2.imencode('.jpg', frame)[1].tostring()
            encoded_frame = base64.b64encode(encoded_frame)

            # Enviar el cuadro
            yield encoded_frame

        # Cerrar la cámara
        camera.release()

    def frame(self):
        import cv2
        import io
        import base64

        # Conectarse a la cámara
        camera = cv2.VideoCapture(f"rtsp://{self.username}:{self.password}@{self.ip}")

        # Capturar un cuadro
        ret, frame = camera.read()

        # Codificar el cuadro en base64
        encoded_frame = cv2.imencode('.jpg', frame)[1].tostring()
        encoded_frame = base64.b64encode(encoded_frame)

        # Devolver bytes
        return encoded_frame
        # devolver cuadro
        #return FileResponse(io.BytesIO(encoded_frame), media_type="image/jpeg")

