# Arquitetura do Projeto

Este documento descreve a arquitetura do projeto de automação de suporte N2 para a Ingresse.

## Visão geral

O projeto é composto por quatro scripts principais localizados no diretório `scripts/` e um conjunto de dados de exemplo em `data/`. A intenção é fornecer ferramentas que auxiliem analistas de suporte na investigação de incidentes, consulta a pedidos e monitoramento de serviços críticos.

## Componentes

### 1. healthcheck_services.sh
Um script em shell que realiza chamadas HTTP para endpoints de healthcheck dos serviços críticos (checkout, emissão de ingressos e notificações) e grava um log com o status HTTP retornado. Útil para verificar rapidamente a disponibilidade da plataforma em dias de pico.

### 2. ticket_status_cli.py
Aplicação de linha de comando em Python que consulta o banco de dados de pedidos (`sample_orders.db`) para recuperar informações sobre o status do pedido, pagamento e entrega do ingresso. Ideal para consultas rápidas de chamados escalados pelo SAC.

### 3. log_error_report.py
Script Python que lê o arquivo de log (`sample_logs.log`) e gera um resumo de erros por tipo e serviço. Esse relatório pode ser exportado como métrica para ferramentas de monitoramento como Datadog e Grafana.

### 4. peak_event_monitor.py
Ferramenta de monitoramento em Python que analisa métricas de utilização e desempenho a partir de um CSV (`sample_metrics.csv`). O script emite alertas no console quando a taxa de erro ou a latência ultrapassam limites pré-definidos, ajudando no acompanhamento de picos de venda ou eventos ao vivo.

## Dados de exemplo

- `sample_orders.db`: banco SQLite com tabelas `orders` e `tickets` contendo alguns registros fictícios.
- `sample_logs.log`: arquivo de log simulando entradas de erros de diferentes serviços.
- `sample_metrics.csv`: métricas de requests, taxa de erro e latência para diferentes serviços ao longo do tempo.

Esses dados servem apenas para demonstração e podem ser substituídos por fontes reais em produção.

## Fluxo de utilização

1. **Healthcheck dos serviços**: execute `scripts/healthcheck_services.sh` para verificar a disponibilidade dos serviços.
2. **Consulta de pedidos**: utilize `scripts/ticket_status_cli.py <order_id>` para obter detalhes de um pedido.
3. **Relatório de erros**: após um evento, execute `scripts/log_error_report.py` para identificar os tipos de erro mais recorrentes.
4. **Monitoramento de pico**: durante um pico, rode `scripts/peak_event_monitor.py` para monitorar taxas de erro e latência e receber alertas.

Esta arquitetura modular permite que cada componente seja evoluído de forma independente e integrado a ferramentas de monitoramento e automação existentes.
