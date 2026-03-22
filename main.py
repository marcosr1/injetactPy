import psycopg2
import random
import uuid
from faker import Faker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

agora = datetime.now()

fake = Faker('pt_BR')

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

status_list = ["PENDING", "PREPARING", "READY", "DELIVERED", "CANCELLED"]
payment_methods = ["PIX", "CREDIT_CARD", "DEBIT_CARD", "CASH"]


cursor.execute('SELECT id, nome, preco FROM produtos')
produtos = cursor.fetchall()


produtos_dict = {
    str(p[0]): {
        "nome": p[1],
        "preco": p[2]
    }
    for p in produtos
}

def gerar_status(payment, total):
    if payment == "PIX":
        probs = [0.1, 0.2, 0.2, 0.45, 0.05]
    else:
        probs = [0.15, 0.25, 0.25, 0.3, 0.05]

    if total > 120:
        probs[-1] += 0.1

    return random.choices(status_list, probs)[0]

def gerar_json_pedido():
    itens = []

    for _ in range(random.randint(1, 4)):
        produto = random.choice(produtos)

        itens.append({
            "produtoId": str(produto[0]),
            "quantidade": random.randint(1, 3)
        })

    return {
        "nomeCliente": fake.name(),
        "numeroCliente": fake.phone_number(),
        "observacao": random.choice(["Sem cebola", "Sem sal", None]),
        "paymentMethod": random.choice(payment_methods),
        "items": itens
    }

quantidade = 10
batch_size = 100

for i in range(quantidade):

    pedido_json = gerar_json_pedido()

    order_id = str(uuid.uuid4())
    total_pedido = 0
    itens_db = []

    for item in pedido_json["items"]:
        produto_id = item["produtoId"]
        quantidade_item = item["quantidade"]

        produto = produtos_dict.get(produto_id)

        if not produto:
            continue  

        nome_prod = produto["nome"]
        preco = produto["preco"]

        subtotal = preco * quantidade_item
        total_pedido += subtotal

        itens_db.append((
            str(uuid.uuid4()),
            order_id,
            nome_prod,
            preco,
            quantidade_item,
            subtotal
        ))

    if not itens_db:
        continue

    status = gerar_status(pedido_json["paymentMethod"], total_pedido)


    cursor.execute("""
        INSERT INTO orders
        ("id", "nomeCliente", "numeroCliente", "observacao", "status", "total", "paymentMethod", "createdAt", "updatedAt")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        order_id,
        pedido_json["nomeCliente"],
        pedido_json["numeroCliente"],
        pedido_json["observacao"],
        status,
        total_pedido,
        pedido_json["paymentMethod"],
        agora,
        agora
    ))


    cursor.executemany("""
        INSERT INTO "orderItems"
        ("id", "orderId", "nomeProduto", "precoUnitario", "quantidade", "subtotal", "createdAt", "updatedAt")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, [
        item + (agora, agora) for item in itens_db
    ])

    if i % batch_size == 0:
        conn.commit()
        print(f"{i} pedidos processados...")

conn.commit()
cursor.close()
conn.close()

print("Simulação estilo API concluída 🚀")