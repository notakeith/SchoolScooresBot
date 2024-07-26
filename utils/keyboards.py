from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_auth = InlineKeyboardButton('🚪 Войти', callback_data='login')
inline_kb_auth = InlineKeyboardMarkup().add(inline_btn_auth)

inline_btn_sub1month = InlineKeyboardButton('1️⃣ 1 месяц', callback_data='sub1month')
inline_btn_sub3month = InlineKeyboardButton('3️⃣ 3 месяца', callback_data='sub3month')
inline_btn_sub1year = InlineKeyboardButton('9️⃣ 9 месяцев', callback_data='sub1year')
inline_kb_payment = InlineKeyboardMarkup(resize_keyboard=False,one_time_keyboard = True)
inline_kb_payment.add(inline_btn_sub1month)
inline_kb_payment.add(inline_btn_sub3month)
inline_kb_payment.add(inline_btn_sub1year)


inline_btn_sub = InlineKeyboardButton("🔗 Подписаться", url="telegrammbot_name")
inline_btn_checksub = InlineKeyboardButton("✅ Проверить", callback_data="checkSub")
inline_kb_sub = InlineKeyboardMarkup(resize_keyboard=False,one_time_keyboard = True)
inline_kb_sub.add(inline_btn_sub)
inline_kb_sub.add(inline_btn_checksub)



async def get_inline_btn_quit(notification_state:bool):
    if notification_state: inline_btn_notification = InlineKeyboardButton('🍎 Выключить уведомления', callback_data='notificationON')
    else: inline_btn_notification = InlineKeyboardButton('🍏 Включить уведомления', callback_data='notificationOFF')
    inline_btn_support = InlineKeyboardButton('📨 Написать в поддержку', callback_data='support')
    inline_btn_quit = InlineKeyboardButton('🚪 Выйти', callback_data='quit')
    inline_kb_settings = (InlineKeyboardMarkup(resize_keyboard=True))
    inline_kb_settings.row_width=1
    inline_kb_settings.add(inline_btn_notification,inline_btn_support,inline_btn_quit)
    return inline_kb_settings