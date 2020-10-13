# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:48:33 2020

@author: Esdra Santos
"""
# Bibliotecas
import paho.mqtt.client as mqtt
import json
import serial
import time

def escreve_msg(data):
      
        informacao = json.loads(data)
        print(informacao)
        print(type(informacao))
        print(informacao["umidade"])
        

class ConexaoSerial(serial.Serial): #classe filha da classe serial
    
    def conectar(self):
  #     obj  =  serial.Serial() nao se inicializa pela classe pai e sim pela filha
        try:
            self.baudrate = 9600
            self.port = 'COM5'
            self.timeout = 1
        except:
            print("Nao foi possivel se conectar a porta " + str(self.port))
        
    def requisitarInfo(self):
        try:
            self.open()
            self.write(b'r')
            info = self.readline()
            info = str(info, 'utf-8')
            print(info)
            self.close()
            return info
        except:
            print("Nao foi possivel requisitar a informacao da serial...")
    

    
# Tratamento do evento de mensagem recebida no tópico assinado pelo cliente mqtt
def on_message(client, userdata, message):
    print("mensagem recebida do topico",message.topic)
    print(json.loads(message.payload))
    
# Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
def on_connect(client, userdata, flags, rc):
    print("Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
    print("subscrevendo ao topico ", topico2)
    client.subscribe(topico2)

 
# Definindo os objetos
broker = "mqtt.tago.io"                # Endereço do broker
porta = 1883                           # Porta do broker
keepAlive = 60                         # Tempo em segundos para o envio de uma requisicao ping
# Topicos para publicar e subscrever
topico1    = "tago/data/regador"
topico2    = "tago/data/previsao"
    
mqtt_username = "esdra"
mqtt_password = "e35c4944-06a4-46f1-be9d-243af76bd4a0"


print("criando nova instancia")
client = mqtt.Client()
print("Configurando o cliente")
client.username_pw_set(username=mqtt_username, password=mqtt_password)

client.loop_start() 

print("Conectando ao broker ", broker)
client.connect(broker,porta,keepAlive)

client.on_connect = on_connect
client.on_message = on_message

time.sleep(5) 
client.loop_stop() 

bluetooth = ConexaoSerial()
bluetooth.conectar()
infosensores = bluetooth.requisitarInfo()
print(type(infosensores))
                 
escreve_msg(infosensores)





