from handlers.shedule_handlers import *
from aiogram.types.bot_command import BotCommand
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Начало ввода данных, для рассчета отпуска"),
    ]
    await bot.set_my_commands(commands)

async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    shedule_bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(shedule_bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handler_shedule(dp)

    # Установка команд бота
    await set_commands(shedule_bot)

    # Запуск поллинга
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())