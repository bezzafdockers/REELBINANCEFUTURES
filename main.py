from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
import time

app = Flask(__name__)

# ⚙️ Config API Binance
API_KEY = os.getenv("BINANCE_API_KEY", "TA_CLE_API")
API_SECRET = os.getenv("BINANCE_SECRET_KEY", "TON_SECRET")
SECRET_TOKEN = "AiDa#1960AlGeR@+=nAdIa"

client = Client(API_KEY, API_SECRET, testnet=True)  # ⬅️ testnet=True pour Binance Futures Testnet

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Message reçu :", data)

    # 🔐 Vérification du secret
    if data.get("secret") != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Clé secrète invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get('type', 'MARKET').upper()

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty,
            reduceOnly=True if 'TP' in data['action'] or 'SL' in data['action'] or 'Exit' in data['action'] else False
        )

        print("Ordre envoyé :", response)
        return jsonify({"status": "success", "order": response})

    except BinanceAPIException as e:
        print("Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("Erreur générique :", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
