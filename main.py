from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
import time

app = Flask(__name__)

# ⚙️ Configuration des clés API Binance
API_KEY = os.getenv("BINANCE_API_KEY", "TA_CLE_API")
API_SECRET = os.getenv("BINANCE_SECRET_KEY", "TON_SECRET")
SECRET_TOKEN = "TON TOKEN SECRET"  # 🔐 Sécurité webhook

client = Client(API_KEY, API_SECRET, testnet=True)  # Utilise le testnet de Binance Futures

# ✅ ROUTE webhook correcte : /webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("🔔 Message reçu :", data)

    # 🔐 Vérification de la clé secrète
    if data.get("secret") != SECRET_TOKEN:
        print("❌ Clé secrète invalide !")
        return jsonify({"status": "error", "message": "Clé secrète invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get('type', 'MARKET').upper()
        action = data.get("action", "").upper()

        reduce_only = any(x in action for x in ['TP', 'SL', 'EXIT'])

        # 🧠 Création de l’ordre
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
        print("🚫 Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("❗ Erreur générale :", e)
        return jsonify({"status": "error", "message": str(e)})

# 🟢 Lancement du serveur Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
