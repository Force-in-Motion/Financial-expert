import asyncio
from aiogram import Bot,Dispatcher

from handlers import (command_handlers, goals_handlers, insert_data_handlers,
                      data_user_handlers, transactions_handlers, statistic_handlers)
from service.service_data import SaveLoadData as sld



async def main() -> None:

    bot = Bot(sld.get_token())

    dp = Dispatcher()

    dp.include_routers(command_handlers.router,
                       insert_data_handlers.router,
                       goals_handlers.router,
                       data_user_handlers.router,
                       transactions_handlers.router,
                       statistic_handlers.router
                       )

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())