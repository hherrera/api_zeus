import paramiko
from getpass import getpass

# Configuración del túnel SSH
local_port = 51433
remote_host = "192.168.0.9"
remote_port = 1433
ssh_user = "laclay"
ssh_host = "190.131.227.1"

# Solicitar la contraseña de SSH de manera segura
ssh_password = getpass("Ingrese la contraseña de SSH: ")

# Crear una conexión SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conectar al servidor SSH
    ssh.connect(ssh_host, username=ssh_user, password=ssh_password)

    # Crear un canal para el túnel SSH
    transport = ssh.get_transport()
    tunnel = transport.open_channel('direct-tcpip', (remote_host, remote_port), ('localhost', local_port))

    print(f"Túnel SSH establecido: localhost:{local_port} -> {remote_host}:{remote_port}")

    # Mantener el script en ejecución para mantener el túnel activo
    input("Presione Enter para salir y cerrar el túnel.")

finally:
    # Cerrar la conexión SSH
    ssh.close()
