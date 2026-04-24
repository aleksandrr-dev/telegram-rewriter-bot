import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    'English': 'EN', 'Russian': 'RU', 'Spanish': 'ES', 'French': 'FR',
    'German': 'DE', 'Italian': 'IT', 'Portuguese': 'PT', 'Dutch': 'NL',
    'Polish': 'PL', 'Japanese': 'JA', 'Chinese': 'ZH-CN', 'Korean': 'KO',
    'Arabic': 'AR', 'Turkish': 'TR', 'Swedish': 'SV', 'Norwegian': 'NO',
    'Danish': 'DA', 'Finnish': 'FI', 'Belarusian': 'BE', 'Czech': 'CS',
    'Vietnamese': 'VI', 'Thai': 'TH', 'Hindi': 'HI', 'Persian': 'FA',
    'Latin': 'LA', 'Old English': 'EN-X-OLD', 'Ancient Greek': 'EL',
    'Biblical Hebrew': 'HE', 'Aramaic': 'ARQ', 'Koine Greek': 'GRC',
    'Church Slavonic': 'CU', 'Old Russian': 'RU-X-OLD', 'Sanskrit': 'SA',
    'Old Norse': 'NON', 'Sumerian': 'SGM', 'Proto-Indo-European': 'PIE',
    'Scythian': 'SCY', 'Ossetian': 'OS', 'Elvish (Sindarin)': 'SD',
}

STYLES = ['Formal', 'Casual', 'Funny', 'Aggressive', 'Poetic']
LANGUAGES_PER_PAGE = 5
LANG_LIST = list(SUPPORTED_LANGUAGES.keys())

def get_language_keyboard(page=0):
    keyboard = []
    start = page * LANGUAGES_PER_PAGE
    end = start + LANGUAGES_PER_PAGE
    page_langs = LANG_LIST[start:end]
    for lang in page_langs:
        keyboard.append([InlineKeyboardButton(lang, callback_data=f'lang_{lang}')])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton('⬅️ Back', callback_data=f'page_{page-1}'))
    if end < len(LANG_LIST):
        nav.append(InlineKeyboardButton('Next ➡️', callback_data=f'page_{page+1}'))
    if nav:
        keyboard.append(nav)
    keyboard.append([InlineKeyboardButton('🔍 Search / Поиск', callback_data='search_lang')])
    return InlineKeyboardMarkup(keyboard)

def get_mode_keyboard():
    keyboard = [
        [InlineKeyboardButton('🌍 Translate / Перевести', callback_data='mode_translate')],
        [InlineKeyboardButton('✏️ Rewrite / Переписать', callback_data='mode_rewrite')],
        [InlineKeyboardButton('🔄 Translate + Rewrite / Перевести + Переписать', callback_data='mode_both')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_style_keyboard():
    keyboard = [[InlineKeyboardButton(style, callback_data=f'style_{style}')] for style in STYLES]
    keyboard.append([InlineKeyboardButton('🏠 Main Menu / Главное меню', callback_data='home')])
    return InlineKeyboardMarkup(keyboard)

async def translate_text(text, target_lang, style=None):
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=config.GROQ_API_KEY)
    if style:
        prompt = f"You are a professional translator. First translate the following text into {target_lang} language, then rewrite it in a {style} style. Your entire response must be written in {target_lang} only. Return only the final result with no explanations:\n\n{text}"
    else:
        prompt = f"You are a professional translator. Translate the following text into {target_lang} language. Your response must be written entirely in {target_lang}. Return only the translated text with no explanations:\n\n{text}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def rewrite_text(text, style):
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=config.GROQ_API_KEY)
    prompt = f"Rewrite the following text in a {style} style. Keep the same language. Return only the rewritten text:\n\n{text}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Welcome! / Добро пожаловать!\n\nChoose a mode / Выберите режим:",
        reply_markup=get_mode_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('mode_'):
        context.user_data['mode'] = data.split('_')[1]
        if data == 'mode_rewrite':
            await query.edit_message_text("Choose a style / Выберите стиль:", reply_markup=get_style_keyboard())
        else:
            await query.edit_message_text("Choose target language / Выберите язык:", reply_markup=get_language_keyboard())

    elif data == 'search_lang':
        context.user_data['searching_language'] = True
        await query.edit_message_text("Type a language name / Введите название языка:")

    elif data.startswith('page_'):
        page = int(data.split('_')[1])
        await query.edit_message_reply_markup(reply_markup=get_language_keyboard(page))

    elif data.startswith('lang_'):
        lang = data.split('_', 1)[1]
        context.user_data['target_lang'] = lang
        context.user_data['searching_language'] = False
        mode = context.user_data.get('mode')
        if mode == 'both':
            await query.edit_message_text("Choose a style / Выберите стиль:", reply_markup=get_style_keyboard())
        else:
            await query.edit_message_text("Send me the text / Отправьте текст:")

    elif data.startswith('style_'):
        style = data.split('_', 1)[1]
        context.user_data['style'] = style
        mode = context.user_data.get('mode')
        if mode == 'rewrite':
            await query.edit_message_text("Send me the text / Отправьте текст:")
        elif mode == 'both' and context.user_data.get('target_lang'):
            await query.edit_message_text("Send me the text / Отправьте текст:")
        else:
            await query.edit_message_text("Choose target language / Выберите язык:", reply_markup=get_language_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if context.user_data.get('searching_language'):
        search_term = text.lower()
        matches = [lang for lang in LANG_LIST if search_term in lang.lower()]
        if matches:
            keyboard = [[InlineKeyboardButton(lang, callback_data=f'lang_{lang}')] for lang in matches]
            keyboard.append([InlineKeyboardButton('🔍 Search again / Искать снова', callback_data='search_lang')])
            await update.message.reply_text("Results / Результаты:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_text("No results / Нет результатов. Try again / Попробуйте снова.")
        context.user_data['searching_language'] = False
        return

    mode = context.user_data.get('mode')
    if not mode:
        await update.message.reply_text("Please use /start to begin. / Используйте /start для начала.")
        return

    target_lang = context.user_data.get('target_lang')
    style = context.user_data.get('style')

    await update.message.reply_text("Processing... / Обрабатываю... ⏳")

    try:
        if mode == 'translate':
            result = await translate_text(text, target_lang)
        elif mode == 'rewrite':
            result = await rewrite_text(text, style)
        elif mode == 'both':
            result = await translate_text(text, target_lang, style)

        await update.message.reply_text(f"✅ Result / Результат:\n\n{result}", reply_markup=get_mode_keyboard())
        context.user_data.clear()
        context.user_data['mode'] = mode

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again. / Произошла ошибка. Попробуйте снова.")

def main():
    application = Application.builder().token(config.BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
