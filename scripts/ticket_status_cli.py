#!/usr/bin/env python3
import sqlite3
import argparse
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_orders.db"

def get_order_details(order_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            o.id,
            o.customer_email,
            o.status,
            o.payment_status,
            t.ticket_code,
            t.delivery_status
        FROM orders o
        LEFT JOIN tickets t ON t.order_id = o.id
        WHERE o.id = ?
    """, (order_id,))

    row = cursor.fetchone()
    conn.close()
    return row

def main():
    parser = argparse.ArgumentParser(
        description="Ferramenta de consulta rápida de status de pedido/ticket."
    )
    parser.add_argument("order_id", type=int, help="ID do pedido a ser consultado")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"[ERRO] Banco de dados não encontrado em {DB_PATH}")
        return

    result = get_order_details(args.order_id)

    if not result:
        print(f"[INFO] Nenhum pedido encontrado para ID={args.order_id}")
        return

    (order_id, email, status, payment_status, ticket_code, delivery_status) = result

    print("=== RESUMO DO PEDIDO ===")
    print(f"ID do pedido      : {order_id}")
    print(f"E-mail do cliente : {email}")
    print(f"Status do pedido  : {status}")
    print(f"Status pagamento  : {payment_status}")
    print(f"Código do ticket  : {ticket_code or 'N/A'}")
    print(f"Status entrega    : {delivery_status or 'N/A'}")

    # Orientações automáticas de troubleshooting
    print("\n=== SUGESTÃO DE AÇÃO ===")
    if payment_status == "PAID" and not ticket_code:
        print("- Pagamento confirmado mas ticket não gerado. Verificar serviço de emissão.")
    elif payment_status != "PAID":
        print("- Pagamento ainda não confirmado. Orientar cliente a aguardar/validar com a operadora.")
    elif ticket_code and delivery_status != "DELIVERED":
        print("- Reenviar ingresso por e-mail ou verificar fila de e-mails.")
    else:
        print("- Pedido OK. Validar se o cliente está usando o e-mail correto ou app da plataforma.")

if __name__ == "__main__":
    main()
