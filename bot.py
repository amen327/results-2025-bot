import logging
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد سجل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تحميل ملفات البيانات
sabahi_df = pd.read_excel("sabahi.xlsx")
masai_df = pd.read_excel("masai.xlsx")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! الرجاء إدخال كود الطالب الخاص بك.")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = str(update.message.text).strip()

    # البحث في الملفين
    result = None

    if 'كود الطالب' in sabahi_df.columns:
        result = sabahi_df[sabahi_df['كود الطالب'].astype(str) == code]

    if result is None or result.empty:
        if 'كود الطالب' in masai_df.columns:
            result = masai_df[masai_df['كود الطالب'].astype(str) == code]

    if result is not None and not result.empty:
        row = result.iloc[0]
        name = row['اسم الطالب']
        student_id = row.get('ID', 'غير متوفر')
        password = row.get('كلمة المرور', 'غير متوفر')

        msg = f"👤 الاسم: {name}\n🆔 المعرف: {student_id}\n🔐 كلمة المرور: {password}"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ لم يتم العثور على كود الطالب. تأكد من صحته وحاول مرة أخرى.")

if __name__ == '__main__':
    import os

    TOKEN = os.getenv("BOT_TOKEN")  # تأكد أن Render يحتوي على متغير BOT_TOKEN

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    print("Bot is running...")
    app.run_polling()
