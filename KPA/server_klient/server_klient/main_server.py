import sys
import socket
import json
import logging

sys.path.append('/home/user-astra/School_for_Life/KPA/Niir_razrb')
from main_work import OOP


class Server(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 8000))
        self.sock.listen(5)
        self.oop = OOP()
        self.oop.connect_belan()
        self.oop.connect_agilent()
        self.oop.agilent_on_off("ON")
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(filename)s:%(funcName)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )

        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(file_handler)

    def handle_client(self, client, addr):
        self.logger.info(f"Подключение от {addr}")
        self.logger.info(f"Вот такой клинет {client}")
        data = json.loads(client.recv(4096).decode('utf-8'))
        command = data['command']
        if command == "set_param_agilent":
            self.log(command, data)
            self.set_param_agilent(data, client)
        elif command == "set_param_belan":
            self.log(command, data)
            self.set_param_belan(data, client)
        elif command == "read_data":
            self.log(command, data)
            self.read_data(data, client)
        else:
            message = " Command not found"

            self.send_error(message, client)


    def set_param_agilent(self, data, client):
        ampl = data['ampl']
        freq = data['freq']
        self.oop.inst_param_agilent(freq, ampl)
        response = {'success': True}
        self.send_response(response, client)

    def set_param_belan(self, data,client):
        cent_freq = data['freq']
        span_bw = data['span_bw']
        radio_bw = data['radio_bw']
        video_bw = data['video_bw']
        razv = data['razv']
        self.oop.inst_param(cent_freq, span_bw, radio_bw, video_bw, razv)
        response = {'success': True}
        self.send_response(response, client)

    def read_data(self, data, client):
        result = self.oop.read_data()
        if result:
            y, x, freq, ampl = result
            y_json = y
            x_json = x.tolist()
            response = {'y': y_json, 'x': x_json, 'freq': freq, 'ampl': ampl}
            with open('response.json', 'w') as f:
                json.dump(response, f)
            self.send_response(response, client)
        else:
            message = "Ошибка чтения"
            self.send_error(message, client)

    def send_error(self, message, client):
        self.logger.info(f"Ошибка {message}")
        response = {'success': False, 'error': message}
        json_response = json.dumps(response)
        client.send(json_response.encode('utf-8'))
        client.close()

    def send_response(self, response, client):
        self.logger.info("Выполнено")
        json_response = json.dumps(response)
        client.send(json_response.encode('utf-8'))
        client.close()

    def log(self, command, data):
        self.logger.info(f"Полученная команда {command}")
        self.logger.info(f"Полученные параметры {data}")


s = Server()
s.sock.listen()
while True:
    client, addr = s.sock.accept()
    s.handle_client(client, addr)
