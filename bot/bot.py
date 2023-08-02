import os
from vkbottle import BaseStateGroup
from vkbottle.bot import Bot, Message
from utils.models import Session, Item
from vkbottle import CtxStorage
from vkbottle import TemplateElement, template_gen
from vkbottle import PhotoMessageUploader
from utils.keyboard import get_keyboard, KEYBOARD_1, KEYBOARD_3
from dotenv import load_dotenv
import yaml


# # Загрузка сценариев из YAML-файла
# def load_scenarios():
#     with open('scenario.yaml', 'r', encoding='utf-8') as f:
#         return yaml.safe_load(f)


# scenarios = load_scenarios()
# print(scenarios)

load_dotenv()
bot = Bot(os.getenv("VK_TOKEN"))
photo_uploader = PhotoMessageUploader(bot.api)
session = Session()
ctx_storage = CtxStorage()


class CatalogStates(BaseStateGroup):
    CHOOSE = "Выбор_категории"
    SECTION = "Категория"
    ITEM = "Товар"


@bot.on.message(lev='/start')
async def start_handler(message: Message):
    """Стартовый хэндлер"""
    await message.answer("Привет, я Бот-каталог кондитерской", keyboard=KEYBOARD_1.get_json())
    await bot.state_dispenser.set(message.peer_id, state=CatalogStates.SECTION)


@bot.on.message(state=CatalogStates.SECTION)
async def menu_handler(message: Message):
    """Хэндлер выбора товара"""
    category = message.text
    ctx_storage.set("message", message)
    ctx_storage.set("category", category)
    keyboard = get_keyboard(category)
    await message.answer(f"Вы находитесь в категории {category}")
    await message.answer(f"Выберите товар или вернитесь назад", keyboard=keyboard.get_json())
    await bot.state_dispenser.set(message.peer_id, state=CatalogStates.CHOOSE)


@bot.on.message(state=CatalogStates.CHOOSE)
async def choose_handler(message: Message):
    """Вспомогательный хэдлер, отсюда мы либо возвращаемся к выбору товара, либо идем в хендлер товара"""
    if message.text == 'Назад':
        await message.answer("Вы вернулись на главную", keyboard=KEYBOARD_1.get_json())
        await bot.state_dispenser.set(message.peer_id, state=CatalogStates.SECTION)
    else:
        await bot.state_dispenser.set(message.peer_id, state=CatalogStates.ITEM)
        await item_handler(message)


@bot.on.message(state=CatalogStates.ITEM)
async def item_handler(message: Message):
    """Хендлер товара"""
    if message.text == 'Назад':
        message = ctx_storage.get("message")
        await menu_handler(message)
    else:
        item_name = message.text
        item = session.query(Item).filter(Item.name == item_name).first()
        photo = await photo_uploader.upload(
            file_source=item.photo_path, peer_id=message.peer_id
        )
        carousel = template_gen(TemplateElement(title=item_name, description=item.description, buttons=KEYBOARD_3))
        await message.answer("Вот ваш товар", template=carousel, attachment=photo)


if __name__ == "__main__":
   bot.run_forever()
