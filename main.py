from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

app = Flask(__name__)

# 🔐 Configuration API Binance
API_KEY = os.getenv("BINANCE_API_KEY", "TA_CLE_API")
API_SECRET = os.getenv("BINANCE_SECRET_KEY", "TON_SECRET")
SECRET_TOKEN = "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"

client = Client(API_KEY, API_SECRET, testnet=True)  # Pour Binance Futures Testnet

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("✅ Données reçues :", data)

    # 🔒 Vérification du secret
    if data.get("secret") != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "⛔ Clé secrète invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get('type', 'MARKET').upper()

        reduce = 'TP' in data['action'] or 'SL' in data['action'] or 'Exit' in data['action']

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty,
            reduceOnly=reduce
        )

        print("🚀 Ordre exécuté :", order)
        return jsonify({"status": "success", "order": order})

    except BinanceAPIException as e:
        print("❌ Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("❌ Erreur générale :", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
