import aiogram
import asyncio
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram import F

router = Router()

@router.message(Command('start'))
async def start_handler(message: types.Message) -> None:
    pass