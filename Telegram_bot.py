import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram import WebAppInfo
import json

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# التوكن من متغيرات البيئة
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# رابط Web App الخاص بك (سيتم تعيينه بعد النشر)
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://telegram_bot.up.railway.app")

# قاعدة بيانات بسيطة (في الذاكرة)
user_data = {}

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📱 افتح Web App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("ℹ️ معلومات", callback_data="info")],
        [InlineKeyboardButton("📊 إحصائيات", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"مرحباً {user.first_name}! 👋\n\n"
        "هذا بوت متكامل مع Web App\n"
        "اضغط على الزر أدناه لفتح التطبيق:",
        reply_markup=reply_markup
    )

# معالجة Web App data
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    user_id = update.effective_user.id
    
    # حفظ بيانات المستخدم
    user_data[user_id] = data
    
    await update.message.reply_text(
        f"✅ تم استقبال بيانات من Web App:\n"
        f"الاسم: {data.get('name', 'غير معروف')}\n"
        f"البريد: {data.get('email', 'غير معروف')}\n"
        f"📊 يمكنك رؤية البيانات على: {WEB_APP_URL}/user/{user_id}"
    )

# معلومات البوت
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📋 معلومات البوت:\n"
        "✅ يعمل على Railway 24/7\n"
        "✅ مرتبط مع Web App\n"
        "✅ يدعم قاعدة بيانات\n"
        f"🔗 رابط الويب: {WEB_APP_URL}"
    )

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    
    # إضافة Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(CallbackQueryHandler(info, pattern="info"))
    
    logger.info("🤖 البوت يعمل...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
