import logging
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعدادات تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تحميل الملفات مرة واحدة
df_sabah = pd.read_excel("صباحي اول كودات.xlsx")
df_sabah["الدراسة"] = "صباحي"

df_masa = pd.read_excel("مسائي اول كودات.xlsx")
df_masa["الدراسة"] = "مسائي"

# دمج الملفات
df_all = pd.concat([df_sabah, df_masa], ignore_index=True)

# تأكد من أن العمود الأول اسمه "ID"
df_all.columns = [col.strip().lower() for col in df_all.columns]  # تحويل إلى lowercase
df_all.rename(columns={"id": "id", "كلمة المرور": "password", "اسم الطالب": "name"}, inplace=True)

# المعالج الأساسي للرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    
    if not user_input.isdigit():
        await update.message.reply_text("❌ الرجاء إدخال كود الطالب فقط (أرقام فقط).")
        return

    code = int(user_input)
    row = df_all[df_all['id'] == code]

    if row.empty:
        await update.message.reply_text("لم يتم العثور على الطالب بهذا الكود ❗")
    else:
        name = row.iloc[0]["name"]
        password = row.iloc[0]["password"]
        study_type = row.iloc[0]["الدراسة"]
        reply = f"👤 الاسم: {name}\n🔐 كلمة المرور: {password}\n📚 الدراسة: {study_type}"
        await update.message.reply_text(reply)

# إعداد البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك، أرسل كود الطالب فقط للحصول على المعلومات 📩")

if __name__ == '__main__':
    application = ApplicationBuilder().token("7923983055:AAEc9j_hGp1Qq_3ehoaVSPXP2LKNBlk9oMw").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()
