import aiogram
import asyncio
from aiogram import Bot,Dispatcher

import handlers.command_handlers
from service.service_data import SaveLoadData as sld



async def main() -> None:

    bot = Bot(sld.get_token())

    dp = Dispatcher()

    dp.include_routers(handlers.command_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())