# Rede de Sensores de Presença Distribuídos #

## Dashboard, API e Admin da rede de sensores ##

Projeto Django para a operação server-side

## Rotas Principais ##
- /dashboard: visualização em gráficos e widgets dos dados
- /api: interface para entrada de dados pelos sensores e geração dos gráficos para o dashboard
- /admin: painel de administração de usuários e modelos

## Modelos ##

### Space ###
Representa uma partição qualquer do espaço (uma sala ou um auditório, por exemplo), delimitado por sensores de entrada e saída em todos os acessos.

Todas as visualizações do dashboard são baseadas nos Spaces.

### Sensor ###
Entidade de monitoramento de entradas e saídas em um Space.

Cada Sensor está associado unicamente à um Space.

### Movement ###

Os sensores emitem Movements, que representam as detecções de entradas e saídas de um espaço físico.

#### Campos para criação: ####
- sensor: Obrigatório. A ID do sensor que detectou o movimento.
- occurence_date: Obrigatório. Data e hora da detecção do movimento no formato "YYYY-MM-DDTHH:MM:SS"
- direction: Obrigatório. 'IN' ou 'OUT', dependendo do sentido da movimentação
- value: Opcional, padrão igual a 1. A quantidade integrada de detecções.

## Gerador de Gráficos ##

Endpoint dos Spaces para geração de gráficos.

- /api/spaces/<ID DO SPACE>/chart?chartType=<TIPO DO GRÁFICO>

### Tipos e campos de request ###

#### Acumulado (accumulative) ####

Histórico de pessoas dentro do espaço no final de cada hora.

- startDate: data no formato DD/MM/YYYY - obrigatório
- endDate: data no formato DD/MM/YYYY - obrigatório
- groupMode: agrupamento de tempo [S, min, H, D, W, M, Y] - opcional, padrão para 'H'

#### Entradas e Saídas (movements) ####

Fluxo positivo e negativo de pessoas dentro do espaço dentro do período.

- startDate: data no formato DD/MM/YYYY - obrigatório
- endDate: data no formato DD/MM/YYYY - obrigatório
- groupMode: agrupamento de tempo [S, min, H, D, W, M, Y] - opcional, padrão para 'H'

#### Ocupação atual (inside) ####

Número atual de pessoas dentro do espaço.

- Sem campos

## Autenticação na API ##

A API usa autenticação HTTP básica, passando usuário e senha pelo cabeçalho "Authentication". [Exemplo para ESP8166](https://github.com/esp8266/Arduino/blob/master/libraries/ESP8266WebServer/examples/HttpBasicAuth/HttpBasicAuth.ino).

## Fake Sensor ##

Ferramenta para geração de dados por sensor virtual.

Requer a biblioteca requests.
