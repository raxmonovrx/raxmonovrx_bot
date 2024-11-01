from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os

# Admin ID va token o'rnating
ADMIN_ID = 123456789  # Telegram ID raqamingizni shu yerga yozing
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway yoki Render'da Tokenni o‘rnatamiz

# Botning boshlang‘ich komandasi
def start(update, context):
    update.message.reply_text("Salom! Qaysi loyiha kodini olmoqchisiz?")

# Zip fayllarni yuklash funksiyasi
def upload_zip(update, context):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        file = update.message.document
        if file.mime_type == 'application/zip':
            file_id = file.file_id
            new_file = context.bot.get_file(file_id)
            new_file.download(f"{file.file_name}")
            update.message.reply_text(f"{file.file_name} muvaffaqiyatli yuklandi.")
        else:
            update.message.reply_text("Faqat zip fayllarni yuklashingiz mumkin.")
    else:
        update.message.reply_text("Kechirasiz, bu amal faqat admin uchun mavjud.")

# Foydalanuvchi loyihani olish uchun tugma bosganda
def project_buttons(update, context):
    keyboard = [[InlineKeyboardButton("Source Code", callback_data='project_code')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Loyiha kodini olish uchun tugmani bosing:", reply_markup=reply_markup)

# Callback funksiya: tugma bosilganda zip faylni yuboradi
def button(update, context):
    query = update.callback_query
    query.answer()

    # Botdan oxirgi yuklangan zip faylni olish uchun
    project_file = max([f for f in os.listdir() if f.endswith('.zip')], key=os.path.getctime, default=None)
    if project_file:
        with open(project_file, 'rb') as f:
            query.message.reply_document(f)
    else:
        query.message.reply_text("Hozircha yuklangan zip fayl mavjud emas.")

# Asosiy botni ishga tushirish
def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("project", project_buttons))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # Zip fayllarni yuklashni qo'llab-quvvatlash uchun MessageHandler
    updater.dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/zip"), upload_zip))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
