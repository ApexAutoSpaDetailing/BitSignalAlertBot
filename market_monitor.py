
import os
import requests

# Telegram credentials stored securely in GitHub Secrets
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )

    response.raise_for_status()
    result = response.json()

    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")

    print("Telegram message sent successfully!")

if __name__ == "__main__":
    send_telegram(
        "🚀 BitSignal Market Monitor is online!\n\n"
        "📊 Bitcoin (BTC)\n"
        "📈 Nvidia (NVDA)\n"
        "🍔 DoorDash (DASH)\n\n"
        "Telegram connection test successful."
    )
