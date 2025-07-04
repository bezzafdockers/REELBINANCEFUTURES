from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

app = Flask(__name__)

# 🔐 Clés d'API
API_KEY = os.getenv("BINANCE_API_KEY", "TA_CLE_API")
API_SECRET = os.getenv("BINANCE_SECRET_KEY", "TON_SECRET")
SECRET_TOKEN = "AiDa#1960AlGeR@+=nAdIa"

# 🔄 Initialisation client Binance Futures Testnet
client = Client(API_KEY, API_SECRET)
client.FUTURES_URL = 'https://testnet.binancefuture.com'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("🔔 Données reçues :", data)

    if data.get("secret") != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Clé secrète invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get('type', 'MARKET').upper()
        reduce_only = 'TP' in data['action'] or 'SL' in data['action'] or 'Exit' in data['action']

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty,
            reduceOnly=reduce_only
        )

        print("✅ Ordre envoyé :", response)
        return jsonify({"status": "success", "order": response})

    except BinanceAPIException as e:
        print("❌ Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("⚠️ Erreur inconnue :", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
