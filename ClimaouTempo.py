# -*- coding: utf-8 -*-
"""
Created on Sun Sep  19 11:04:00 2020

@author: Carlos Souza
@collaborator: Esdra Santos

"""
## modulos utilizados
import weathercom
import paho.mqtt.client as mqtt
import json
import time
import threading

## funcao que temporiza o running do codigo 
def printit():
    
    ## define de quanto em quanto tempo o codigo ira rodar
    #  running de código a cada  4 horas (14400s)
    threading.Timer(600, printit).start() 
    
    ## funcao de scrapping de informacoes sobre a previsao do tempo
    #
    #  @param cidade localidade da previsao do tempo
    #  @return tupla (temperatura maxima, temperatura minima, precipitacao de chuva)
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
    
    ## funcao que constitui que encapsula as informacoes da previsao do tempo e publica em topico mqtt
    #  
    #  @param cliente objeto da classe mqtt
    #  @param cidade  localidade para requisicao especifica da previsao do tempo para cada cliente
    def envia_relatorio(cliente, cidade):   
        
        ## atribui as variaveis as informacoes retornadas da previsao do tempo
        (temperaturamax, temperaturamin, precip) = PrevisaoDoTempo(cidade)
        ## encapsula as informacoes em um dict 
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
        
        ## @var_json_file
        #  armazena a conversao do dicionario composto anteriormente em json-string
        json_file = json.dumps(previsao)
        
        ## publica a mensagem em um topico determinado
        #  @param topico1 topico referente a previsao do tempo
        #  @param payload mensagem a ser publicada
        #  @param qos     quality of service: determina a garantia da entrega da mensagem 
        #  @param retain  determina se a mensagem sera retida no broker (=True) ou nao (=False)
        cliente.publish(topico1, payload=json_file, qos=1, retain=True) 

    ## funcao que implementa a rotina do evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    #
    #  @param client   objeto pertencente a classe mqtt
    #  @param userdata 
    #  @param flags    
    #  @param rc       return code, indica se a conexao foi bem sucedida
    def on_connect(client, userdata, flags, rc):

        print("Cliente conectado; resultado de conexao: " + str(rc))
    
    ## funcao para configuracao e conexao do cliente 
    #
    # @param cliente objeto mqtt
    # @param id      identificacao do cliente
    # @param cidade  localidade do cliente
    def configura_cliente(cliente, id, cidade):

        cliente.loop_start()
        ## conecta o cliente ao broker
        print("Conectando o cliente " + str(id) + " ao broker " + str(broker))
        cliente.connect(broker,porta)
        ## associa o callback do evento de conexao ao broker a funcao implementada no codigo
        cliente.on_connect = on_connect
        ## chama a funcao quue encasula publica os dados da previsao do tempo 
        envia_relatorio(cliente, cidade)
        ## determina um tempo para o encerramento da conexao
        time.sleep(5) 
        ## encerra a conexao
        cliente.loop_stop() 

    ## Configuracao do cliente mqtt
    ## endereço do broker
    broker = "mqtt.tago.io"                
    ## porta para testes de comunicacao com protocolo mqtt (sem seguranca) 
    porta = 1883                           
    ## Topico para publicacao dos dados no broker do tago.io
    topico1    = "tago/data/previsao"
    
    ## instancia um objeto-cliente pertencente a classe mqtt.Client
    print("Criando nova instancia")
    esdra = mqtt.Client()
    ## atribui o token respectivo ao dispositivo no tago.io ao cliente
    esdra.username_pw_set('',"e35c4944-06a4-46f1-be9d-243af76bd4a0")
    print("Configurando o cliente")
    ## chama a funcao responsavel pela configuracao e conexao do cliente
    configura_cliente(esdra, 1, "Novo Hamburgo")
        
    ## instancia um objeto-cliente pertencente a classe mqtt.Client
    print("\nCriando nova instancia")
    carlos= mqtt.Client()
    ## atribui o token respectivo ao dispositivo no tago.io ao cliente
    carlos.username_pw_set('',"a41ac0bf-dd9a-4852-82b0-9ab0cd6acacc")
    print("Configurando o cliente")
    ## chama a funcao responsavel pela configuracao e conexao do cliente
    configura_cliente(carlos, 2, "Sapucaia do Sul")
    
    ## instancia um objeto-cliente pertencente a classe mqtt.Client
    print("\nCriando nova instancia")
    murilo= mqtt.Client()
    ## atribui o token respectivo ao dispositivo no tago.io ao cliente
    murilo.username_pw_set('',"126127bf-b15b-4054-abf0-4f0a6f17e828")
    ## chama a funcao responsavel pela configuracao e conexao do cliente
    print("Configurando o cliente")
    configura_cliente(murilo, 3, "Sapucaia do Sul")

printit() # Chama a função que a periodiza o código para carregar conforme o tempo determinado