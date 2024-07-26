from aiogram import types


async def set_default_commands(dp) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('scores', 'Посмотреть оценки'),
            types.BotCommand('notification', 'Включить/Выключить уведомления'),
            types.BotCommand('profile', 'Открыть пользователя'),
            types.BotCommand('settings', 'Настройки'),
        ]
    )
