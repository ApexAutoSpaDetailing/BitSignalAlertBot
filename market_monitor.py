
import os
import sys
import requests

# ==========================================
# BitSignal Market Monitor
# Telegram Connection Diagnostic
# ==========================================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


def check_configuration():
    """Check required GitHub secrets."""

    print("Checking BitSignal configuration...")

    if not BOT_TOKEN:
        raise RuntimeError(
            "Missing TELEGRAM_BOT_TOKEN GitHub secret"
        )

    if not CHAT_ID:
        raise RuntimeError(
            "Missing TELEGRAM_CHAT_ID GitHub secret"
        )

    print("Bot token: configured")
    print("Chat ID: configured")


def telegram_request(method, payload=None):
    """Call Telegram API and safely report errors."""

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/{method}"
    )

    try:
        response = requests.post(
            url,
            json=payload or {},
            timeout=20
        )

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError(
                f"Telegram returned HTTP "
                f"{response.status_code} "
                "with an invalid response"
            )

        if not response.ok or not data.get("ok"):
            description = data.get(
                "description", "Unknown Telegram error"
            )

            # Do not print full URLs containing tokens.
            raise RuntimeError(
                f"Telegram HTTP {response.status_code}: "
                f"{description}"
            )

        return data.get("result")

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            "Telegram network request failed: "
            f"{type(exc).__name__}"
        ) from None


def verify_bot():
    """Verify token and identify the Telegram bot."""

    print("Verifying Telegram bot...")

    bot = telegram_request("getMe")

    print(
        "Authenticated bot: @"
        + bot.get("username", "unknown")
    )


def send_telegram(message):
    """Send a message to the configured chat."""

    print("Sending Telegram test notification...")

    telegram_request(
        "sendMessage",
        {
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    print("SUCCESS: Telegram message delivered!")


def main():
    print("=" * 40)
    print("BitSignal Market Monitor")
    print("=" * 40)

    check_configuration()
    verify_bot()

    message = (
        "🚀 BitSignal Market Monitor ONLINE!\n\n"
        "✅ GitHub Actions connected\n"
        "✅ Telegram API authenticated\n\n"
        "📊 Monitoring targets:\n"
        "₿ Bitcoin (BTC)\n"
        "📈 Nvidia (NVDA)\n"
        "🍔 DoorDash (DASH)\n\n"
        "🔔 Telegram delivery test successful.\n\n"
        "Next: Enable automatic market monitoring."
    )

    send_telegram(message)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            "ERROR: "
            + str(error),
            file=sys.stderr
        )
        sys.exit(1)
