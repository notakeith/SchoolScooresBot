from data.config import VERSION

message_password = """🤧 Если после этого сообщения вам ничего не пришло - значит вы допустили где-то ошибку\n
🫣 Введите снова логин, а затем пароль, *в разных сообщениях*"""

message_exclusive = """⏳ Мы посвятили множество часов и усилий разработке данного бота. Наша главная цель - обеспечить ваш комфорт и удовлетворение.\n
🪙 Чтобы поддержать и дальнейшее улучшение нашего бота, мы ввели символическую плату. Она позволит обеспечить непрерывное развитие бота, чтобы он оставался надежным и полезным инструментом для вас. \n
😁 Мы рады предоставить Вам 0 недель пробного периода. Это даст Вам возможность ознакомиться с возможностями и преимуществами нашего бота, прежде чем принять решение о подписке.\n
💫 Узнать подробнее о подписке /profile"""

message_unauth_force = """🚧 Ваш пароль был изменен.\n
В связи с этим вы были принудительно выведены из системы. \n
Чтобы продолжить пользоваться сервисом, пожалуйста, войдите в учетную запись заново"""

message_unauth = """🚧 Вы вышли из учетной записи.\n
Для повторного входа напишите /login"""


def message_start(name: str) -> str:
    return f'''👋 Добро пожаловать {name}!\n
Здесь можно узнать домашнее задание и оценки из sh-open.ris61edu.ru
Для начало работы мне нужен логин и пароль от вышеуказанного сайта.\n
🚧 Продолжая пользоваться ботом, вы соглашаетесь с нашим [пользовательским соглашением](example.com). 
Обычное дело, без него мы не имеем права обрабатывать ваши данные'''


def message_start2(name: str) -> str:
    return f'''👋 Добро пожаловать {name}!\n
Здесь можно узнать домашнее задание и оценки из sh-open.ris61edu.ru\n
🌚 Но ты и так уже все знаешь\n
🚧 Кстати, напомню! Продолжая пользоваться ботом, вы соглашаетесь с нашим [пользовательским соглашением](example.com). 
Обычное дело, без него мы не имеем права обрабатывать ваши данные'''


def message_sub() -> str:
    return f'''Вам нужно подписаться на наш новостной канал, чтобы продолжить работу бота.'''

def message_settings(name: str, notification_state: bool) -> str:
    if notification_state:
        line1 = "🍎 Уведомления об оценках: выключены"
    else:
        line1 = "🍏 Уведомления об оценках: включены"
    # TODO: уведомление о конце подписки за 5, 2, 1 день
    return f'''⚙ {name}.\n
🙂 Здесь вы можете включить и выключить уведомления, написать в поддержку или выйти из аккаунта!\n
{line1}\n
Версия: {VERSION}'''


def message_auth_success(child: str, school: str) -> str:
    return f'''Привязан аккаунт:\n
🎓 {child}
🏫 Школа: {school}'''

def get_support_message(count: int, maxcount: int) -> str:
    return f"""✉️ Количество ваших обращений: {count}\n
🚧 Нашли недочет, ошибку, что-то не получилось или хотите передать пожелание автору? — Используйте команду /support с текстом, который хотите передать. На данный момент для отправки файлов используйте онлайн сервисы - imgur, dropmefiles и подобное. А сюда вставляйте ссылку. \n
📡 Количество доступных обращений: {maxcount - count}"""
