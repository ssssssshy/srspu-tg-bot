from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.database.request as rq


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет!👋'
                        '\n'
                        '\nЯ – твой помощник по расписанию ЮРГПУ(НПИ)!'
                        '\n'
                        '\nСо мной ты можешь быстро узнать актуальное расписание занятий,'
                        'чтобы всегда быть в курсе, куда и когда тебе нужно идти.'
                        '\n'
                        '\n🕒Если возникнут вопросы, я всегда на связи. Удачи в учебе! 📚',
                        reply_markup=kb.main
)

@router.message(F.text == 'Расписание')
async def raspisanie(message: Message):
    await message.answer('Выберите Свое направление', reply_markup= await kb.directions())

@router.callback_query(F.data.startswith('direction_'))
async def direction(callback: CallbackQuery):
    direction_id = callback.data.split('_')[1]
    await callback.answer('Вы выбрали направление')
    await callback.message.answer('Выберите неделю', reply_markup=await kb.weeks(direction_id))

@router.callback_query(F.data.startswith('week_'))
async def week(callback: CallbackQuery):
    week_id = callback.data.split('_')[1]
    await callback.answer('Вы выбрали неделю')
    await callback.message.answer('Выберите день недели', reply_markup=await kb.days(week_id))

@router.callback_query(F.data.startswith('day_'))
async def day(callback: CallbackQuery):
    await callback.answer('Вы выбрали день')
    subject_category = callback.data.split('_')[1]
    
    # Получаем список всех предметов по категории
    subjects_data = await rq.get_subjects_by_category(subject_category)
    
    if subjects_data:
        # Создаем строку с расписанием для всех предметов, выводя их в обратном порядке
        schedule_text = "Расписание:\n"
        for subject in reversed(subjects_data):
            schedule_text += (
                f"Предмет: {subject.name}\n"
                f"Время: {subject.time}\n"
                f"Преподаватель: {subject.teacher_name}\n"
                f"Аудитория: {subject.office}{subject.coprus}\n\n"
            )
        
        # Редактируем сообщение, заменяя старое расписание новым
        await callback.message.edit_text(schedule_text)
    else:
        # Если предметов нет, обновляем сообщение с уведомлением
        await callback.message.edit_text("Нет предметов для выбранного дня.")



   
   
    


