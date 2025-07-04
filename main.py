from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

app = Flask(__name__)

# ⚙️ Clés API Binance (réelles)
BINANCE_API_KEY = os.getenv("G5CE2xVrFMtmki3fRCCschkBktF6BBB5Ya75SVflGRSQquwzdbCSLGd9XpHkPIvu")
BINANCE_SECRET_KEY = os.getenv("i9X1xxYoKBqgs1TZQsZYHc3Q621TIUHuXHkNBMOkuXa2E0RgWjTJoZHLISujMiAl")
SECRET_TOKEN = "LA ILAH ILLA ALLAH"

# ✅ Connexion à Binance Futures (mode réel)
client = Client(API_KEY, API_SECRET)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Message reçu :", data)

    # 🔐 Vérifie le token secret
    if data.get("secret") != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Clé secrète invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get('type', 'MARKET').upper()
        action = data.get("action", "").upper()

        # 📦 Préparer la commande
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty,
            reduceOnly=True if 'TP' in action or 'SL' in action or 'EXIT' in action else False
        )

        print("Ordre envoyé :", response)
        return jsonify({"status": "success", "order": response})

    except BinanceAPIException as e:
        print("Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("Erreur interne :", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
