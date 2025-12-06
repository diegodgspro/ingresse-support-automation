# Runbooks

Este documento descreve como utilizar cada script do projeto de automação de suporte N2.

## healthcheck_services.sh

**Objetivo:** Verificar rapidamente se os serviços críticos da plataforma de ingressos estão respondendo.

**Como executar:**
```bash
bash scripts/healthcheck_services.sh
```
O script irá percorrer os endpoints de healthcheck definidos e registrar o resultado em `data/healthchecks.log`. Uma saída típica no terminal será:

```
[2025-12-05 20:00:01] Iniciando healthcheck dos serviços...
[2025-12-05 20:00:01] Checkout API - https://api.ingresse.local/health/checkout - HTTP 200 - OK
...
```

## ticket_status_cli.py

**Objetivo:** Consultar detalhes de um pedido de ingresso, incluindo status do pagamento e da entrega do ticket.

**Como executar:**
```bash
python3 scripts/ticket_status_cli.py <order_id>
```

Exemplo de saída:

```
=== RESUMO DO PEDIDO ===
ID do pedido      : 1
E-mail do cliente : cliente@example.com
Status do pedido  : COMPLETED
Status pagamento  : PAID
Código do ticket  : ABC123
Status entrega    : DELIVERED

=== SUGESTÃO DE AÇÃO ===
- Pedido OK. Validar se o cliente está usando o e-mail correto ou app da plataforma.
```

## log_error_report.py

**Objetivo:** Gerar um resumo dos erros registrados em log por tipo e serviço, auxiliando na identificação de problemas recorrentes.

**Como executar:**
```bash
python3 scripts/log_error_report.py
```

O script lerá `data/sample_logs.log` e imprimirá no console a contagem de erros por tipo e por serviço. Esse resumo pode ser utilizado para alimentar dashboards em ferramentas de monitoramento.

## peak_event_monitor.py

**Objetivo:** Monitorar métricas de desempenho e utilização durante um pico de vendas ou evento ao vivo.

**Como executar:**
```bash
python3 scripts/peak_event_monitor.py
```

O script analisará `data/sample_metrics.csv` e emitirá alertas quando a taxa de erro for superior a 5% ou a latência ultrapassar 1000 ms. A lógica de monitoramento pode ser adaptada para ler métricas de APIs ou sistemas de filas em tempo real.

---

Adapte esses runbooks conforme necessário para o ambiente de produção e integre com sistemas de monitoramento (Datadog, Grafana) e processos de suporte existentes.
