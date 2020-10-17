# Flower Monitor 🌼 (Trabalho de IoT 2020)
##  Integrantes: Carlos Souza, Esdra A. dos Santos, Gabriela Bley Rodrigues e Murilo Schuck.
### Curso de Eletrônica da F.E.T Liberato Salzano Vieira da Cunha, Turma: 4411

#### Proposta: 
Quantificar os parâmetros de umidade do solo e a luminosidade em uma planta, indicando, através da informação coletada pelos sensores e da precipitação de chuva no dia em questão, se é necessário regar a planta e/ou retirá-la do sol quando a exposição for excessiva. 

#### Recursos e equipamentos: 
O sensoriamente será feito através de um higrômetro e um LDR. O sinais serão pré-processados por um Microcontrolador ARM e as informações
serão transmitidas pela serial utilizando o módulo Bluetooth HC-05.

#### Implementação:
Cada cliente possui um código implementado em Python que recebe as informações do sensoriamento através do bluetooth, analisando a informação de preciptação de chuva recebida do "servidor" - que simula uma "mini estação metereológica" - por protocolo MQTT no tópico tago/data/previsao do broker mqtt.tago.io. De acordo com os dados recebidos, o código encapsula, em formato json, as informações obtidas do sensoriamento e determina a notificação a ser exibida na dashboard para cada caso: Necessidade ou não de regar a planta, luminosidade escassa, adequada ou excessiva. As dashboards, por sua vez, concentram e exibem todas as informações: temperatura máxima/mínima, precipitação de chuva ☔, umidade do solo, luminosidade ☀️ e notificações a respeito da condição da planta. 

HIGRÔMETRO:
<img src="https://ae01.alicdn.com/kf/HTB1r0P4JVXXXXb8XpXXq6xXFXXXj/225565846/HTB1r0P4JVXXXXb8XpXXq6xXFXXXj.jpg" width="200" height="200" /> 
LDR:
<img src="https://sc01.alicdn.com/kf/HTB1Da3pKFXXXXXRapXXq6xXFXXXP.jpg_350x350.jpg" width="200" height="200" />
HC-05:
<img src="https://cdn.awsli.com.br/600x700/921/921725/produto/38307342/2c043a596e.jpg" width="200" height="200" />


 :shipit: 




