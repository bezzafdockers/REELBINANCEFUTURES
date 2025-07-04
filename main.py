from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

app = Flask(__name__)

# ⚙️ Charge les variables d'environnement (doivent être définies sur Render)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")
SECRET_TOKEN = "LA ILAH ILLA ALLAH"

# ✅ Connexion à Binance Futures réel
client = Client(API_KEY, API_SECRET)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Message reçu :", data)

    # 🔐 Vérification du token secret
    if data.get("secret") != SECRET_TOKEN:
        return jsonify({"status": "error", "message": "Clé secrète invalide"}), 403

    try:
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        qty = float(data['qty'])
        order_type = data.get('type', 'MARKET').upper()
        action = data.get("action", "").upper()

        print(f"📊 Envoi ordre : {side} {qty} {symbol} [{order_type}]")

        # Envoi de l'ordre
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=qty,
            reduceOnly=True if 'TP' in action or 'SL' in action or 'EXIT' in action else False
        )

        print("✅ Ordre envoyé :", response)
        return jsonify({"status": "success", "order": response})

    except BinanceAPIException as e:
        print("⚠️ Erreur Binance :", e)
        return jsonify({"status": "error", "message": str(e)})

    except Exception as e:
        print("🔥 Erreur interne :", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81)
