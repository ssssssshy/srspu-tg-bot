from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.request import get_directions,get_direction_week, get_week_day


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Расписание')],
],
                           resize_keyboard=True,
                           input_field_placeholder='выбери пункт в меню.')

async def directions():
    all_directions = await get_directions()
    keyboard = InlineKeyboardBuilder()
    for direction in all_directions:
        keyboard.add(InlineKeyboardButton(text=direction.code, callback_data=f'direction_{direction.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to main'))
    return keyboard.adjust(2).as_markup()

async def weeks(direction_id):
    all_weeks = await get_direction_week(direction_id)
    keyboard = InlineKeyboardBuilder()
    for week in all_weeks:
        keyboard.add(InlineKeyboardButton(text=week.name, callback_data=f'week_{week.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to main'))
    return keyboard.adjust(2).as_markup()

async def days(week_id):
    all_days = await get_week_day(week_id)
    keyboard = InlineKeyboardBuilder()
    for day in all_days:
        keyboard.add(InlineKeyboardButton(text=day.name, callback_data=f'day_{day.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to main'))
    return keyboard.adjust(2).as_markup()

