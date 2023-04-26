import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 8000))

data = {'command': 'set_param', 'freq': 3000000000, 'ampl': -10}
json_data = json.dumps(data)
sock.send(json_data.encode('utf-8'))

response = sock.recv(4096)
response = json.loads(response.decode('utf-8'))
print(response)

sock.close()
