import sys
sys.path.append('/home/user-astra/School_for_Life/KPA/Niir_razrb')
# print(sys.path)
from main_work import OOP
import socket
import json

oop = OOP()
oop.connect_agilent()
oop.agilent_on_off("ON")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8000))
sock.listen(5)

while True:
    client, addr = sock.accept()
    print(f"Подключение от {addr[0]}")
    data = json.loads(client.recv(4096).decode('utf-8'))
    command = data['command']
    if command == 'set_param':
        ampl = data['ampl']
        freq = data['freq']
        response = {'success': True}
    else:
        response = {'success': False, 'error': 'Command not found'}

    if addr:
        oop.inst_param_agilent(freq, ampl)
    json_response = json.dumps(response)
    client.send(json_response.encode('utf-8'))
    client.close()

