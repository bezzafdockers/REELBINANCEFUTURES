from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

app = Flask(__name__)

# ✅ Clés API pour Binance Futures Testnet
API_KEY = os.getenv("BINANCE_API_KEY", "TA_CLE_API_ICI")
API_SECRET = os.getenv("BINANCE_SECRET_KEY", "TON_SECRET_ICI")

# ✅ Ton token secret sacré
SECRET_TOKEN = "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"

# ✅ Connexion à Binance Testnet
client = Client(API_KEY, API_SECRET, testnet=True)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Reçu:", data)

    # 🔐 Vérifie le token secret
    if data.get("secret") != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Token secret invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get("type", "MARKET").upper()
        reduce_only = any(k in data['action'] for k in ["TP", "SL", "Exit"])

        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty,
            reduceOnly=reduce_only
        )

        print("✅ Ordre exécuté:", response)
        return jsonify({"status": "success", "order": response})

    except BinanceAPIException as e:
        print("❌ Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("❌ Erreur système :", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
