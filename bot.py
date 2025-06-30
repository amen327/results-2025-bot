
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# تحميل الملفات
df_sabahi = pd.read_excel("Copy of تربية انكليزي اولى صباحي(1).xlsx")
df_masai = pd.read_excel("Copy of تربية انكليزي اولى مسائي(1).xlsx")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! الرجاء إدخال كود الطالب الخاص بك فقط:")

async def search_by_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code_input = update.message.text.strip()

    result_sabahi = df_sabahi[df_sabahi["كود الطالب"].astype(str) == code_input]
    result_masai = df_masai[df_masai["كود الطالب"].astype(str) == code_input]

    if not result_sabahi.empty:
        row = result_sabahi.iloc[0]
        response = f"📚 الدراسة: صباحي\n👤 الاسم: {row['اسم الطالب']}\n🆔 كود الطالب: {row['كود الطالب']}"
        await update.message.reply_text(response)
    elif not result_masai.empty:
        row = result_masai.iloc[0]
        response = f"🌙 الدراسة: مسائي\n👤 الاسم: {row['اسم الطالب']}\n🆔 كود الطالب: {row['كود الطالب']}"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ الكود غير موجود. تأكد من إدخاله بشكل صحيح.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل كود الطالب فقط للحصول على بياناتك.")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7923983055:AAEc9j_hGp1Qq_3ehoaVSPXP2LKNBlk9oMw").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_by_code))

    print("البوت يعمل الآن...")
    app.run_polling()
