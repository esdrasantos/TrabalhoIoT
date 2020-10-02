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
    threading.Timer(60.0, printit).start() # Run o código a cada 1h (3600 s)
      
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
                          'value'   :  precip
                      }
                  ]
        json_file = json.dumps(previsao)
        cliente.publish(topico1, payload=json_file, qos=1, retain=True) # Publica os dados no broker com retenção
    
    # Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    def on_connect_esdra(client, userdata, flags, rc):
    
        print("[STATUS] Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
      
        
    # Rotina que trata o evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    def on_connect_carlos(client, userdata, flags, rc):
    
        print("[STATUS] Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
    
    def on_connect_murilo(client, userdata, flags, rc):
      
         print("[STATUS] Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
        
    def configura_cliente(cliente,id):
        
        cliente.loop_start()
        
        print("Conectando ao broker...")
        cliente.connect(broker,porta)
         
        if id == 1:
            cliente.on_connect = on_connect_esdra
        if id == 2:
            cliente.on_connect = on_connect_carlos
        
        envia_relatorio(cliente)
        
        time.sleep(5) 
        cliente.loop_stop() 
     
    # Definindo os objetos
    broker = "mqtt.tago.io"                # Endereço do broker
    porta = 1883                           # Porta sem segurança para testes
    #keepAlive = 60                         # Tempo em segundos para o envio de uma requisicao ping
    # Topicos para publicar os dados no tago.io
    topico1    = "tago/data/previsao"
    
    print("Criando nova instancia")
    esdra= mqtt.Client()
    esdra.username_pw_set('',"e35c4944-06a4-46f1-be9d-243af76bd4a0")
    print("Configurando o cliente")
    configura_cliente(esdra,1)
    
    print("Criando nova instancia")
    carlos= mqtt.Client()
    carlos.username_pw_set('','7f1d7f85-761e-4b98-92b4-7bab3f528b82')
    print("Configurando o cliente")
    configura_cliente(carlos,2)
    
    print("Criando nova instancia")
    murilo= mqtt.Client()
    murilo.username_pw_set('','fd30154d-4923-457c-8e19-d2c10d9ff7cf')
    print("Configurando o cliente")
    configura_cliente(murilo,3)

printit() # Chama a função que a periodiza o código para carregar conforme o tempo determinado