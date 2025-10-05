import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🧠 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /convert 100 usd eur")

# 💱 /convert command
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 3:
            await update.message.reply_text("Usage: /convert <amount> <from> <to>\nExample: /convert 100 usd eur")
            return

        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()

        # use exchangerate.host (free)
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        data = requests.get(url).json()

        converted = data.get("result", None)
        if converted is None:
            await update.message.reply_text("❌ Conversion failed. Check the currencies.")
            return

        # add flags
        flags = {"USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵"}
        from_flag = flags.get(from_currency, "")
        to_flag = flags.get(to_currency, "")

        await update.message.reply_text(
            f"{from_flag} {amount:.2f} {from_currency} = {converted:.2f} {to_flag} {to_currency}"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# 🚀 Main entry
async def main():
    token = os.getenv("BOT_TOKEN")
    app_url = os.getenv("RENDER_EXTERNAL_URL")  # Render auto-sets this
    port = int(os.getenv("PORT", 8443))

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))

    # Remove any old webhook
    await app.bot.delete_webhook()
    # Set new webhook
    await app.bot.set_webhook(f"{app_url}/webhook")

    print(f"🌐 Webhook set to {app_url}/webhook")
    print("🤖 Bot is running via webhook...")

    await app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="/webhook",
    )

if __name__ == "__main__":
    asyncio.run(main())
