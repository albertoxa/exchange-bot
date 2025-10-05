import requests
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "7987348424:AAH5K-z1fIv7tDlzJJR1RmjtPYaZJHTBsgk"
API_URL = "https://openexchangerates.org/api/latest.json?app_id=15e04396216e4a3d87b6ca2058031608"


# ---------- Helper function ----------
def send_reply(update, text):
    """Safely send a reply in both private and group chats."""
    if update.message:
        update.message.reply_text(text)
    elif update.callback_query:
        update.callback_query.message.reply_text(text)


# ---------- Command handler ----------
def convert(update, context):
    if len(context.args) != 3:
        send_reply(update, "Usage: /convert <amount> <from_currency> <to_currency>\nExample: /convert 100 usd eur")
        return

    try:
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()
    except ValueError:
        send_reply(update, "❌ Invalid amount. Example: /convert 100 usd eur")
        return

    # Fetch currency rates
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        rates = data["rates"]
    except Exception as e:
        send_reply(update, f"⚠️ Error fetching data: {e}")
        return

    # Validate currencies
    if from_currency not in rates or to_currency not in rates:
        send_reply(update, "❌ Invalid currency code. Example: USD, EUR, GBP, JPY")
        return

    # Perform conversion
    usd_amount = amount / rates[from_currency]
    converted = usd_amount * rates[to_currency]
    send_reply(update, f"💱 {amount:.2f} {from_currency} = {converted:.2f} {to_currency}")


# ---------- Main function ----------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("convert", convert))

    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
