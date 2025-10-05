import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /convert 100 usd eur")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 3:
            await update.message.reply_text("Usage: /convert <amount> <from> <to>\nExample: /convert 100 usd eur")
            return

        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()

        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        data = requests.get(url).json()

        converted = data.get("result", None)
        if converted is None:
            await update.message.reply_text("❌ Conversion failed. Check the currencies.")
            return

        flags = {"USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵"}
        from_flag = flags.get(from_currency, "")
        to_flag = flags.get(to_currency, "")

        await update.message.reply_text(
            f"{from_flag} {amount:.2f} {from_currency} = {converted:.2f} {to_flag} {to_currency}"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    print("🤖 Bot is running...")
    app.run_polling()
