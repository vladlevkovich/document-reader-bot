from aiogram.fsm.state import State,StatesGroup

class FileStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_question = State()
