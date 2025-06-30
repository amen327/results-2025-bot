
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# تحميل الملفات
df_sabahi = pd.read_excel("صباحي اول كودات.xlsx")
df_masai = pd.read_excel("مسائي اول كودات.xlsx")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك! الرجاء إدخال اسمك الرباعي كما هو تمامًا:")

async def search_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()

    result_sabahi = df_sabahi[df_sabahi["اسم الطالب"] == name]
    result_masai = df_masai[df_masai["اسم الطالب"] == name]

    if not result_sabahi.empty:
        row = result_sabahi.iloc[0]
        await update.message.reply_text(
            f"📚 الدراسة: صباحي
🆔 المعرف: {row['ID']}
🔐 كلمة المرور: {row['كلمة المرور']}"
        )
    elif not result_masai.empty:
        row = result_masai.iloc[0]
        await update.message.reply_text(
            f"🌙 الدراسة: مسائي
🆔 المعرف: {row['ID']}
🔐 كلمة المرور: {row['كلمة المرور']}"
        )
    else:
        await update.message.reply_text("❌ لم يتم العثور على الاسم. تأكد من كتابة الاسم الرباعي بشكل صحيح.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل اسمك الرباعي فقط للحصول على المعرف وكلمة المرور.")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7923983055:AAEc9j_hGp1Qq_3ehoaVSPXP2LKNBlk9oMw").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_student))

    print("البوت يعمل الآن...")
    app.run_polling()
