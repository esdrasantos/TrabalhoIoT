# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:48:33 2020

@author: Esdra Santos
"""
# modulos utilizados 
import paho.mqtt.client as mqtt 
import json
import serial
import time
import threading

## @var_precipChuva
#  variavel global que armazena o valor da precipitacao de chuva em mm para o dia em questao
precipChuva = 0

## funcao que temporiza o running do codigo 
def printit():
    ## define de quanto em quanto tempo o codigo ira rodar
    threading.Timer(600, printit).start() # Run o código a cada 10min (600s)
    
    ## @var_razao
    #  razao utilizada para transcrever as tensoes digitais de 8 bits (0 - 255) em niveis porcentuais de 0 a 100%
    razao = 100/(2**8) 
   
    ## funcao que organiza as informacoes numa string com formatacao json e a publica num topico mqtt especifico.
    #
    #  @param data informacoes dos sensores: umidade e luminosidade
    #  @param precipChuva informacao da precipitacao de chuva no dia 
    def escreve_msg(data, precipChuva):
      
        try:
            ## variavel que converte json-string em um dict (dicionario python)
            informacao = json.loads(data)
            ## variavel que armazena o valor relativo a etiqueta 'umidade'
            valor_umidade  = int(informacao['umidade'])
            ## manipulacao do valor da umidade para o enquadramento em niveis porcentuais
            valor_umidade *= razao
            ## como a resposta do sensor eh inversamente proporcional a tensao digital, altera-se para obter um valor proporcional 
            valor_luminosidade = int(informacao['luminosidade'])
            ## manipulacao do valor da luminosidade para o enquadramento em niveis porcentuais
            valor_luminosidade *= razao
            ## idem a variave anterior para obtencao de proporcionalidade
            valor_luminosidade = 100 - valor_luminosidade
            
            ## Analise em intervalos dos valores obtidos no sensoriamento para tomada de decisao 
            if(int(valor_umidade) < 50 and float(precipChuva)== 0):
                not_umidade = "É necessário regar a planta" 
            elif(float(precipChuva) > 0):
                not_umidade = "Hoje ira chover, nao e necessario regar a planta"
            else:
                not_umidade = "Planta regada"
            
            if(valor_luminosidade > 78):
                not_lum = "Exposicao solar muito intensa"
                
            elif(30 <= valor_luminosidade <= 78):
                not_lum = "A luminosidade esta adequada"
            else: 
                not_lum = "Pouco luminosidade"
            
            ## @var_msg 
            #  constitui um dicionario com as informacoes relevantes ao sensoriamento e as decisoes 
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
                  ]
                
            ## armazena a conversao do dicionario em json-string
            json_file = json.dumps(msg)
            
            ## exibe uma mensagem no console
            #  @param topico1 topico mqtt para publicacao da mensagem
            #  @param json_file mensagem com os valores as strings de decisao
            print("\nmensagem enviada para o topico " + topico1 + ':\n' + json_file)
            
            ## publica a mensagem no topico mqtt
            client.publish(topico1, payload=json_file, qos=1, retain=False)
            
        except:
            ## exibe uma mensagem de erro no console
            print("Nao foi possivel compor a msg e nem publica-la...")
    
    ## classe filha para o tratamento e configuração de objetos serial       
    class ConexaoSerial(serial.Serial): #classe filha da classe serial
        
        ## metodo que configura a porta serial
        #  @param self relativo ao proprio objeto instanceado na classe filha ConexaoSerial
        def conectar(self):
            try:
                ## atributo de velocidade de comunicacao em bits/s
                self.baudrate = 9600
                ## atributo que identifica a porta serial relativa a conexao
                self.port = 'COM5'
                ## atributo que determina o tempo maximo em ms a se esperar por dados seriais
                self.timeout = 1
            except:
                ## mensagem de erro para conexao nao efetuada
                print("Nao foi possivel se conectar a porta " + str(self.port))
                
        ## metodo que requisita uma informacao e a retorna se ela for recebida
        #  @param self relativo ao proprio objeto instanceado na classe filha ConexaoSerial
        #  @return     bytes recebidos pela serial 
        def requisitarInfo(self):
            try:
                ## metodo de abertura da porta serial relativa ao objeto para comunicacao
                self.open()
                ## metodo que escreve no buffer serial um determinado caractere ou string
                self.write(b'r')
                ## @var_info   
                #  armazena os bytes recebidos pela serial
                #  o metodo readline le uma linha inteira recebida ate o caractere '\n'
                info = self.readline()
                ## a porta serial e fechada terminadas as operacoes 
                self.close()
                ## retorna os bytes recebidos pela serial
                return info
            except:
                ## exibe uma mensagem de erro caso nao seja possivel requisitar a mensagem ou ler o buffer da serial
                print("Nao foi possivel requisitar a informacao da serial...")
        
    ## funcao que trata o evento de mensagem recebida no tópico assinado pelo cliente mqtt
    #
    #  @param client   objeto pertencente a classe mqtt
    #  @param userdata 
    #  @param message  mensagem recebida num dos topicos assinado
    def on_message(client, userdata, message):
        
        ## exibe, no console, a mensagem recebida
        print("\nmensagem recebida do topico",message.topic)
        ## a conversao da mensagem de bytes para string e necessaria para a visualizao utilizando a funcao print()
        print(str(message.payload,'utf-8'))
        ## verifica se a mensagem advem do topico de interesse 
        if(message.topic == topico2):
            try:  
                ## obj recebe o objeto do tipo lista de dicionarios que contem informacoes da previsao do tempo
                obj = json.loads(message.payload)  
                ## o objeto de indice 2 na lista eh o dicionario que contem a informacao da previsao de chuva
                chuvaDict = obj[2]   
                global precipChuva
                ## armazena-se a quantidade de chuva em mm na variável global para manipulação futura
                precipChuva = chuvaDict['value']
                
            except:
                ## exibe uma mensagem de erro caso algum dos processos anteriores for mal-sucedido
                print("Impossivel extrair informacao da precipitacao de chuva")
       
    ## funcao que implementa a rotina do evento de conexao, exibindo o return code e subscrevendo o cliente aos topicos de interesse
    #
    #  @param client   objeto pertencente a classe mqtt
    #  @param userdata 
    #  @param flags    
    #  @param rc       return code, indica se a conexao foi bem sucedida
    def on_connect(client, userdata, flags, rc):
        ## exibe uma mensagem sobre a conexao ao broker mqtt
        print("Conectado ao Broker " + broker + " Resultado de conexao: " + str(rc))
        ## exibe uma mensagem de inscricao
        print("subscrevendo ao topico ", topico2)
        ## inscreve o cliente em um topico especifico do broker
        #  @param topico2 topico da previsao do tempo
        client.subscribe(topico2)
        
    ## Configuracao do cliente mqtt
    ## endereço do broker
    broker = "mqtt.tago.io"      
    ## porta para testes de comunicacao com protocolo mqtt          
    porta = 1883       
    ## tempo em segundos para o envio de uma requisicao ping para manutencao da conexao                   
    keepAlive = 60                        
    ## topicos para publicar e subscrever
    topico1    = "tago/data/regador"
    topico2    = "tago/data/previsao"
    ## configura token para o cliente mqtt
    #  @var_mqtt_username nome de identificao para o cliente (nao obrigatorio)
    #  @var_mqtt_password token para postagem de informacoes exclusivas a um dispositivo no tago.io em um topico 'publico'
    mqtt_username = "esdra"
    mqtt_password = "e35c4944-06a4-46f1-be9d-243af76bd4a0"
    ## instancia um cliente (objeto pertencente a classe mqtt)
    print("\ncriando nova instancia mqtt")
    client = mqtt.Client()
    ## atribui ao cliente username e password atraves do metodo username_pw_set()
    print("Configurando o cliente")
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    ## inicio de loop
    client.loop_start() 
    ## conecta o cliente ao broker
    print("Configurando conexao ", broker)
    client.connect(broker,porta,keepAlive)
    ## associa o callback do evento de conexao ao broker a funcao implementada no codigo
    client.on_connect = on_connect
    ## associa o callback do evento de mensagem recebida a funcao implementada no codigo
    client.on_message = on_message
    ## determina um tempo para o encerramento da conexao
    time.sleep(5) 
    ## encerra a conexao
    client.loop_stop() 

    ## configuracao serial do bluetooth
    ## instancia o bluetooth como um objeto da classe ConexaoSerial: serial.Serial
    bluetooth = ConexaoSerial()
    ## chama o metodo responsavel pela configuracao dos paramentros da comunicacao serial para ao bluetooth
    bluetooth.conectar()
    ## envia requisicao ao microprocessador (via BT) e armazena os bytes de resposta 
    infosensores = bluetooth.requisitarInfo()
    ## exibe as informacoes recebidas por bluetooth
    print("\nInformacao da serial\n" + str(infosensores, 'utf-8'))
    ## chama a funcao que encapsula os dados obtidos em conjunto com as decisoes tomadas a partir deles e envia ao tago.io
    escreve_msg(infosensores, precipChuva)
    
 ## chama a funcao temporizadora   
printit()



