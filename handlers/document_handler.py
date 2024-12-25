from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from document_agent.fsm.fsm import FileStates
from document_agent.llm.agent import process_document
from aiogram.filters import Command
from document_agent.kb.kb import keyboard
import re
import os

router = Router()

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

@router.message(Command('read'))
async def start_read(message: Message, state: FSMContext):
    try:
        await message.answer('📄 Надішліть документ (PDF, DOCX або TXT), щоб я міг обробити його.')
        await state.set_state(FileStates.waiting_for_file)
    except Exception as e:
        await message.answer(str(e))

@router.message(FileStates.waiting_for_file, F.document)
async def receive_file(message: Message, state: FSMContext):
    try:
        filename = sanitize_filename(message.document.file_name)
        file_path = f'./files/{filename}'
        await message.bot.download(file=message.document.file_id, destination=file_path)
        await message.answer('📄 Файл успішно прочитано')
        await state.update_data(document_path=file_path)
        await state.set_state(FileStates.waiting_for_question)
    except Exception as e:
        await message.answer(str(e))

@router.message(FileStates.waiting_for_question)
async def receive_question(message: Message, state: FSMContext):
    try:
        query = message.text
        data = await state.get_data()
        if query.lower() == 'stop':
            await state.clear()
            await message.answer('🚫 Робота завершена. Якщо хочете почати заново, введіть /read.', reply_markup=keyboard)
            os.remove(data['document_path'])
            return
        result = process_document(data['document_path'], query)
        await message.answer(result)
        await state.set_state(FileStates.waiting_for_question)
    except Exception as e:
        await message.answer(str(e))
