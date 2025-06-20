import os
from dotenv import load_dotenv
import unicodedata
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 6130272246

# Menú principal
main_menu = ReplyKeyboardMarkup(
    [["1. Información sobre el grupo premium"], ["2. Preguntas frecuentes"]],
    resize_keyboard=True
)

faq_menu = ReplyKeyboardMarkup(
    [["1. Porcentaje de ganancias"], ["2. Plataforma de apuestas"], ["3. Duda de pick"], ["4. Otra pregunta"]],
    resize_keyboard=True
)

# Estado dinámico
dynamic_state = {}

# Función para normalizar texto (elimina acentos y pasa a minúsculas)
def normalizar(texto):
    texto = texto.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    dynamic_state.pop(user_id, None)
    await update.message.reply_text("👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Manejo de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    text_raw = update.message.text.strip()
    text = normalizar(text_raw)

    if user_id in dynamic_state:
        motivo = dynamic_state.pop(user_id)
        mensaje = f"📩 Nueva duda:\nID: {user_id}\nMotivo: {motivo}\nMensaje: {text_raw}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
        await update.message.reply_text("Gracias, un administrador te responderá pronto.")
        return

    # ✅ Opción 1: Información sobre el grupo premium
    if "informacion sobre el grupo premium" in text:
        registro_url = (
            f"https://api.buclecompany.com/widget/form/NzctQhiqWZCkJyHaUtti"
            f"?notrack=true&telegram_id={user_id}"
        )

        await update.message.reply_text(
            "🎯 *Información sobre el grupo premium:*\n\n"
            "✅ Acceso a picks diarios\n"
            "📈 Estrategias con respaldo numérico\n"
            "🤖 Automatización de alertas\n"
            "💬 Comunidad privada en Telegram\n\n"
            "📝 Para acceder, por favor completa este formulario. "
            "Tu información será registrada de forma segura:\n"
            f"{registro_url}",
            parse_mode="Markdown"
        )
        return

    # ✅ Opción 2: Preguntas frecuentes
    elif "preguntas frecuentes" in text:
        await update.message.reply_text("Selecciona una opción:", reply_markup=faq_menu)
        return

    # ✅ Subopciones FAQ
    elif "porcentaje de ganancias" in text:
        await update.message.reply_text("📊 El porcentaje de ganancias mensual es de aproximadamente 85%.")
        return

    elif "plataforma de apuestas" in text:
        await update.message.reply_text("🏟 Usamos principalmente Bet365 y Caliente.mx.")
        return

    elif "duda de pick" in text:
        dynamic_state[user_id] = "Duda sobre pick"
        await update.message.reply_text("📝 Por favor, escribe tu duda sobre algún pick.")
        return

    elif "otra pregunta" in text:
        dynamic_state[user_id] = "Otra pregunta general"
        await update.message.reply_text("🗨️ Por favor, escribe tu pregunta.")
        return

    # ❓ Por defecto
    else:
        await update.message.reply_text("👋 ¿Cómo puedo ayudarte hoy?", reply_markup=main_menu)

# Lanzar el bot
if __name__ == "__main__":
    print("🔄 Iniciando bot en modo polling...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot corriendo correctamente…")
    app.run_polling()