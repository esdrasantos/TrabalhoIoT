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

    threading.Timer(14400, printit).start() # Run o código a cada 1h (3600 s)

    def PrevisaoDoTempo(cidade):    
        
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
        
        return(temperaturamax,temperatura,precip)

    def envia_relatorio(cliente, cidade):   
        (temperaturamax, temperaturamin, precip) = PrevisaoDoTempo(cidade)
        
        previsao = [
                      {
                      'variable': 'temperaturamin',
                      'value'   :  temperaturamin
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
    def on_connect(client, userdata, flags, rc):

        print("Cliente conectado; resultado de conexao: " + str(rc))
  
    def configura_cliente(cliente, id, cidade):

        cliente.loop_start()
        
        print("Conectando o cliente " + str(id) + " ao broker " + str(broker))
        cliente.connect(broker,porta)
        cliente.on_connect = on_connect
        
        envia_relatorio(cliente, cidade)
        
        time.sleep(5) 
        cliente.loop_stop() 

    # Definindo os objetos
    broker = "mqtt.tago.io"                 # Endereço do broker
    porta = 1883                            # Porta sem segurança para testes
    #keepAlive = 60                         # Tempo em segundos para o envio de uma requisicao ping
    # Topicos para publicar os dados no tago.io
    topico1    = "tago/data/previsao"
    
    print("Criando nova instancia")
    esdra = mqtt.Client()
    esdra.username_pw_set('',"e35c4944-06a4-46f1-be9d-243af76bd4a0")
    print("Configurando o cliente")
    configura_cliente(esdra, 1, "Novo Hamburgo")
    
    print("\nCriando nova instancia")
    carlos= mqtt.Client()
    carlos.username_pw_set('',"a41ac0bf-dd9a-4852-82b0-9ab0cd6acacc")
    print("Configurando o cliente")
    configura_cliente(carlos, 2, "Sapucaia do Sul")
    
    print("\nCriando nova instancia")
    murilo= mqtt.Client()
    murilo.username_pw_set('',"126127bf-b15b-4054-abf0-4f0a6f17e828")
    print("Configurando o cliente")
    configura_cliente(murilo, 3, "Sapucaia do Sul")

printit() # Chama a função que a periodiza o código para carregar conforme o tempo determinado