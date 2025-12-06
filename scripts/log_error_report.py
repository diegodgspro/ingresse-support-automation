#!/usr/bin/env python3
from collections import Counter
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_logs.log"

def parse_logs():
    errors_by_type = Counter()
    errors_by_service = Counter()

    if not LOG_PATH.exists():
        print(f"[ERRO] Arquivo de log não encontrado em {LOG_PATH}")
        return errors_by_type, errors_by_service

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            # Exemplo de formato:
            # 2025-12-05T20:00:01Z | service=checkout | level=ERROR | type=PAYMENT_GATEWAY_TIMEOUT | msg=...
            parts = line.strip().split("|")
            if len(parts) < 4:
                continue

            service_part = parts[1].strip()
            type_part = parts[3].strip()

            service = service_part.split("=")[1]
            error_type = type_part.split("=")[1]

            errors_by_type[error_type] += 1
            errors_by_service[service] += 1

    return errors_by_type, errors_by_service

def main():
    errors_by_type, errors_by_service = parse_logs()

    print("=== RELATÓRIO DE ERROS POR TIPO ===")
    for error_type, count in errors_by_type.most_common():
        print(f"{error_type}: {count}")

    print("\n=== RELATÓRIO DE ERROS POR SERVIÇO ===")
    for service, count in errors_by_service.most_common():
        print(f"{service}: {count}")

    print("\nSugestão de uso:")
    print("- Exportar este resumo como métrica para Datadog/Grafana (ex: erros por tipo/serviço).")
    print("- Usar no debrief pós-evento para priorizar correções.")

if __name__ == "__main__":
    main()
