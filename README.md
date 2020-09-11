# Regador automático (Trabalho de IoT 2020)
##  Integrantes: Carlos Souza, Esdra A. dos Santos, Gabriela Bley Rodrigues e Murilo Schuck.
### Curso de Eletrônica da F.E.T Liberato Salzano Vieira da Cunha, Turma: 4411

Proposta: Quantificar a umidade do solo de uma planta e indicar quando ela deve ser regada com base na previsão do tempo e a precipitação de chuva.
A planta é regada automaticamente caso não haja possibilidade de chuva no dia da análise ou no dia seguinte. Verifica-se, também, a luminosidade
na planta e notifica caso a disposição de luz solar for excessiva.

Recursos e equipamentos: O sensoriamente será feito através de um higrômetro e um LDR. O sinais serão pré-processados por um Microcontrolador ARM e as informações
serão transmitidas pela serial utilizando o módulo Bluetooth HC-05.

HIGRÔMETRO:
<img src="https://ae01.alicdn.com/kf/HTB1r0P4JVXXXXb8XpXXq6xXFXXXj/225565846/HTB1r0P4JVXXXXb8XpXXq6xXFXXXj.jpg" width="200" height="200" /> 
LDR:
<img src="https://sc01.alicdn.com/kf/HTB1Da3pKFXXXXXRapXXq6xXFXXXP.jpg_350x350.jpg" width="200" height="200" />
HC-05:
<img src="https://cdn.awsli.com.br/600x700/921/921725/produto/38307342/2c043a596e.jpg" width="200" height="200" />

As informações coletadas serão processadas por uma implementação em Python e/ou Nodered com o intuito de as analisar para a tomada de decisões,
organizá-las em formato json e as transmitir por protoco mqtt ao broker mqtt.tago.io, onde a dashboard para exibição dos dados será elaborada.

Também será desenvolvido um leitor de RSS feed para a obtenção de informações a respeito da precipitação de chuva ☔.




