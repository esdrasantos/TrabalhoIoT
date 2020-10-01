# -*- coding: utf-8 -*-
"""
Created on Sun Sep  19 11:04:00 2020

@author: Carlos Souza
@collaborator: Esdra Santos

"""

import weathercom
import paho.mqtt.client as mqtt
import json
import time
import threading

def printit():
    threading.Timer(3600.0, printit).start() # Run o código a cada 1h (3600 s)
      
    cidade="Novo Hamburgo"
    weatherDetails = weathercom.getCityWeatherDetails(city=cidade, queryType="daily-data")
    print(f'Cidade: {weatherDetails[weatherDetails.find("city")+8:weatherDetails.find("longitude")-4]}')
    temperatura=weatherDetails[weatherDetails.find("temperature")+14:weatherDetails.find("temperatureMax")-3]
    print(f'Temperatura: {temperatura}ºC')
    temperaturamax=weatherDetails[weatherDetails.find("temperatureMax")+25:weatherDetails.find("uvIndex")-3]
    print(f'Temperatura máxima desde as 7 da manhã: {temperaturamax}ºC')
    sensacao=weatherDetails[weatherDetails.find("feelsLike")+12:weatherDetails.find("gust")-3]
    print(f'Sensação térmica: {sensacao}ºC')
    umidade=weatherDetails[weatherDetails.find("humidity")+11:weatherDetails.find("icon")-3]
    print(f'Umidade relativa do ar: {umidade}%')
    precip=weatherDetails[weatherDetails.find("precip24")+15:weatherDetails.find("snowD")-3]
    print(f'Precipitação do dia: {precip}mm')
    vento=weatherDetails[weatherDetails.find("windSpeed")+11:weatherDetails.find("windDir")-3]
    print(f'Velocidade do vento: {vento}km/h')
    
    print('\nConexão por protocolo MQTT')
    def envia_relatorio(cliente):
        previsao = [
                      {
                          'variable': 'temperaturamin',
                          'value'   :  temperatura
                      },
                      {
                          'variable': 'temperaturamax',
                          'value'   :  temperaturamax
                      },
                      {
                          'variable': 'chuva',
                          'value'   :  10
                      }
                  ]
        json_file = json.dumps(previsao)
        cliente.publish(topico1, payload=json_file, qos=1, retain=True) # Publica os dados no broker com retenção
    

    # Método que exibe o registro da comunicacao por protocolo mqtt no terminal
    def on_log_esdra(esdra, userdata, level, buf):
        print("log: ",buf)
    
    # Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    def on_connect_esdra(esdra, userdata, flags, rc):
    
        print("[STATUS] Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
        print("subscrevendo ao topico", topico1)
        
     # Método que exibe o registro da comunicacao por protocolo mqtt no terminal
    def on_log_carlos(esdra, userdata, level, buf):
        print("log: ",buf)
    
    # Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    def on_connect_carlos(esdra, userdata, flags, rc):
    
        print("[STATUS] Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
        print("subscrevendo ao topico", topico1)
     
    # Definindo os objetos
    broker = "mqtt.tago.io"                # Endereço do broker
    porta = 1883                           # Porta sem segurança para testes
    #keepAlive = 60                         # Tempo em segundos para o envio de uma requisicao ping
    # Topicos para publicar os dados no tago.io
    topico1    = "tago/data/previsao"
    
    esdra_username = "" # Nome do cliente 
    esdra_password = "e35c4944-06a4-46f1-be9d-243af76bd4a0" #token do dispositivo/cliente
    print("Criando nova instancia")
    esdra= mqtt.Client()
    print("Configurando o cliente")
    esdra.username_pw_set(esdra_username, password=esdra_password)
    
    esdra.loop_start()
    
    print("Conectando ao broker...")
    esdra.connect(broker,porta)
    esdra.on_connect = on_connect_esdra
    esdra.on_log     = on_log_esdra
    envia_relatorio(esdra)
    
    time.sleep(4) 
    esdra.loop_stop() 
    
    carlos_username = "" # Nome do cliente 
    carlos_password = "7f1d7f85-761e-4b98-92b4-7bab3f528b82" #token do dispositivo/cliente
    print("Criando nova instancia")
    carlos= mqtt.Client()
    print("Configurando o cliente")
    
    carlos.username_pw_set(carlos_username, password=carlos_password)
    
    carlos.loop_start()
    
    print("Conectando ao broker...")
    carlos.connect(broker,porta)
    carlos.on_connect = on_connect_carlos
    carlos.on_log     = on_log_carlos
    envia_relatorio(carlos)
    
    time.sleep(4) 
    carlos.loop_stop() 
    
    
    
printit() # Chama a função que a periodiza o código para carregar conforme o tempo determinado