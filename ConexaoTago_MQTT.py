# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:48:33 2020

@author: Esdra Santos
"""
# Bibliotecas
import paho.mqtt.client as mqtt
import json
import serial

def escreve_msg(valor_umidade,valor_luminosidade):
    msg = [
            {
                'variable': 'umidade',
                'value'   :  valor_umidade
            },
            {
                'variable': 'luminosidade',
                'value'   :  valor_luminosidade
            }
          ]
  
    print(msg)
    json_file = json.dumps(msg)
    client.publish(topico1, payload=json_file, qos=1, retain=False)
    
# Tratamento do evento de mensagem recebida no tópico assinado pelo cliente mqtt
def on_message(client, userdata, message):
    print("mensagem recebida do topico",message.topic)

# Método que exibe o registro da comunicacao por protocolo mqtt no terminal
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
def on_connect(client, userdata, flags, rc):

    print("[STATUS] Conectado ao Broker" + broker + " Resultado de conexao: " + str(rc))
    print("subscrevendo ao topico", topico1)
    client.subscribe(topico1)
    escreve_msg(25,15000)
 
# Definindo os objetos
broker = "mqtt.tago.io"          # Endereço do broker
porta = 1883                           # Porta do broker
keepAlive = 60                         # Tempo em segundos para o envio de uma requisicao ping
# Topicos para publicar e subscrever
topico1    = "tago/data/regador"

mqtt_username = "token"
mqtt_password = "7f1d7f85-761e-4b98-92b4-7bab3f528b82"

print("criando nova instancia")
client = mqtt.Client()
print("Configurando o cliente")
client.username_pw_set(mqtt_username, password=mqtt_password)
print("Conectando ao broker...")
client.connect(broker,porta,keepAlive)

client.on_connect = on_connect
client.on_message = on_message
client.on_log     = on_log



client.loop_forever() # Estabelece uma comunicacao continua entre o cliente e o broker




