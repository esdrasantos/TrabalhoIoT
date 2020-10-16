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
import threading

global precipChuva 

def printit():
    threading.Timer(600, printit).start() # Run o código a cada 1h (3600 s)
    razao = 100/(2**8) 
    def escreve_msg(data, precipChuva):
          
        try: 
            informacao = json.loads(data)
            
            valor_umidade  = int(informacao['umidade'])
            valor_umidade *= razao
            valor_umidade  = 100 - valor_umidade
            valor_luminosidade = int(informacao['luminosidade'])
            valor_luminosidade *= razao
            valor_luminosidade = 100 - valor_luminosidade
            
            if(int(valor_umidade) < 50 and int(precipChuva)== 0):
                not_umidade = "É necessário regar a planta" 
            elif(float(precipChuva) > 0):
                not_umidade = "Hoje ira chover, nao e necessario regar a planta"
            else:
                not_umidade = "Planta regada"
            
            if(valor_luminosidade > 78):
                not_lum = "Exposicao solar muito intensa"
                
            elif(30 < valor_luminosidade <= 78):
                not_lum = "A luminosidade esta adequada"
            else: 
                not_lum = "Pouco luminosidade"
            
                
            msg = [
                    {
                        'variable': 'umidade',
                        'value'   :  valor_umidade
                    },
                    {
                        'variable': 'luminosidade',
                        'value'   :  valor_luminosidade  
                    },
                    {
                        'variable': 'notifUmidade',
                        'value'   :  not_umidade
                    },
                    {
                        'variable': 'notifLuminosidade',
                        'value'   : not_lum
                    },
                    {
                        'variable': 'botao',
                        'value'   : 1
                    }
                  ]
                
            
            json_file = json.dumps(msg)
            print("\nmensagem enviada para o topico " + topico1 + ':\n' + json_file)
            client.publish(topico1, payload=json_file, qos=1, retain=False)
            
        except:
            print("Nao foi possivel compor a msg e nem publica-la...")
           
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
                #info = str(info, 'utf-8')
                self.close()
                return info
            except:
                print("Nao foi possivel requisitar a informacao da serial...")
    
        
    # Tratamento do evento de mensagem recebida no tópico assinado pelo cliente mqtt
    def on_message(client, userdata, message):
        
        print("\nmensagem recebida do topico",message.topic)
        print(str(message.payload,'utf-8')) # message.payload pertence a classe bytes, converte-se para string 
        if(message.topic == topico2):
            try:  
                obj = json.loads(message.payload)  # os bytes que constituem a estrtura de dados em formato json são convertidos numa lista de dicionários
                chuvaDict = obj[2]                 # o objeto de indice 2 na lista é o dicionário que contem a informação da previsão de chuva
                global precipChuva 
                precipChuva = chuvaDict['value']   # armazena-se a quantidade de chuva em mm na variável global para manipulação futura
    
            except:
                print("Impossivel extrair informacao da precipitacao de chuva")
       
    # Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    def on_connect(client, userdata, flags, rc):
        print("Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
        print("subscrevendo ao topico ", topico2)
        client.subscribe(topico2)
        client.subscribe(topico3)
     
    # Definindo os objetos
    
    
    broker = "mqtt.tago.io"                # Endereço do broker
    porta = 1883                           # Porta do broker
    keepAlive = 60                         # Tempo em segundos para o envio de uma requisicao ping
    # Topicos para publicar e subscrever
    topico1    = "tago/data/regador"
    topico2    = "tago/data/previsao"
    topico3    = "tago/data/realtime"
        
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
    print("\nInformacao da serial\n" + str(infosensores, 'utf-8'))
    
    escreve_msg(infosensores, precipChuva)

printit()





