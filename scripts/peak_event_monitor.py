#!/usr/bin/env python3
import csv
from pathlib import Path

METRICS_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_metrics.csv"

def check_metrics():
    if not METRICS_PATH.exists():
        print(f"[ERRO] Arquivo de métricas não encontrado em {METRICS_PATH}")
        return

    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = row["timestamp"]
            service = row["service"]
            requests = int(row["requests"])
            error_rate = float(row["error_rate"])
            latency_ms = float(row["latency_ms"])

            alerts = []
            if error_rate > 0.05:
                alerts.append(f"taxa de erro alta ({error_rate*100:.1f}%)")
            if latency_ms > 1000:
                alerts.append(f"latência alta ({latency_ms} ms)")

            if alerts:
                print(f"[ALERTA] {timestamp} - {service}: {', '.join(alerts)}")
            else:
                print(f"[OK] {timestamp} - {service}: dentro dos limites")

def main():
    print("=== Monitor de Pico de Evento ===")
    check_metrics()

if __name__ == "__main__":
    main()
