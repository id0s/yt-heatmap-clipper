import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = ""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if "youtube.com" not in text and "youtu.be" not in text:
        await update.message.reply_text("Kirim link YouTube saja.")
        return

    await update.message.reply_text("🎬 Processing video...")

    try:

        # jalankan script run.py
        process = subprocess.Popen(
            ["python", "run.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # otomatis pilih mode
        input_data = "1\nn\n" + text + "\n"

        process.communicate(input=input_data)

        clips_dir = "clips"

        if not os.path.exists(clips_dir):
            await update.message.reply_text("Clip gagal dibuat.")
            return

        files = os.listdir(clips_dir)

        if not files:
            await update.message.reply_text("Tidak ada clip yang dihasilkan.")
            return

        for file in files:
            path = os.path.join(clips_dir, file)

            await update.message.reply_video(video=open(path, "rb"))

            os.remove(path)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot berjalan...")

app.run_polling()
