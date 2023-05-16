import socket
import json
import matplotlib.pyplot as plt

HOST = "127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 8000))
data = {'command': 'set_param_agilent', 'freq': 3000000000, 'ampl': -10}
json_data = json.dumps(data)
sock.send(json_data.encode('utf-8'))

response = sock.recv(4096)
response = json.loads(response.decode('utf-8'))
print(response)

sock.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 8000))
data = {'command': 'set_param_belan', 'freq': 3000000000, 'span_bw': 2000000, 'radio_bw' : 30000, 'video_bw' : 1000, 'razv': False }
json_data = json.dumps(data)
sock.send(json_data.encode('utf-8'))

response = sock.recv(4096)
response = json.loads(response.decode('utf-8'))
print(response)

sock.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 8000))

data = {'command': 'read_data'}
json_data = json.dumps(data)
sock.send(json_data.encode('utf-8'))

response = sock.recv(16384)
response = json.loads(response.decode('utf-8'))
sock.close()
y = response['y']
x = response['x']
print(y[0:4])
plt.plot(x,y)
plt.show()

