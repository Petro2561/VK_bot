import json

from config import CatalogStates, bot_api
from utils.keyboard import KEYBOARD_1, KEYBOARD_3, get_keyboard
from models import Session, Item
from vkbottle import CtxStorage, PhotoMessageUploader, TemplateElement, template_gen
from vkbottle.bot import Bot, Message


with open("scenario.json", "r", encoding="utf-8") as f:
    scenarios = json.load(f)

bot = Bot(api=bot_api)
photo_uploader = PhotoMessageUploader(bot.api)
ctx_storage = CtxStorage()
session = Session()


@bot.on.message(lev="/start")
async def start_handler(message: Message):
    """Стартовый хэндлер"""
    start_scenario = scenarios[0]["start"]
    await message.answer(start_scenario["message"], keyboard=KEYBOARD_1.get_json())
    await bot.state_dispenser.set(message.peer_id, state=CatalogStates.SECTION)


@bot.on.message(state=CatalogStates.SECTION)
async def menu_handler(message: Message):
    """Хэндлер выбора товара"""
    start_scenario = scenarios[1]["section"]
    category = message.text
    ctx_storage.set("message", message)
    keyboard = get_keyboard(category)
    await message.answer(f"Вы находитесь в категории {category}")
    await message.answer(start_scenario["message"], keyboard=keyboard.get_json())
    await bot.state_dispenser.set(message.peer_id, state=CatalogStates.CHOOSE)


@bot.on.message(state=CatalogStates.CHOOSE)
async def choose_handler(message: Message):
    """Вспомогательный хэдлер, отсюда мы либо возвращаемся к выбору товара, либо идем в хендлер товара"""
    choose_scenario = scenarios[2]["choose"]
    if message.text == "Назад":
        await message.answer(choose_scenario["message"], keyboard=KEYBOARD_1.get_json())
        await bot.state_dispenser.set(message.peer_id, state=CatalogStates.SECTION)
    else:
        await bot.state_dispenser.set(message.peer_id, state=CatalogStates.ITEM)
        await item_handler(message)


@bot.on.message(state=CatalogStates.ITEM)
async def item_handler(message: Message):
    """Хендлер товара"""
    item_scenario = scenarios[3]["item"]
    if message.text == "Назад":
        message = ctx_storage.get("message")
        await menu_handler(message)
    else:
        item_name = message.text
        item = session.query(Item).filter(Item.name == item_name).first()
        photo = await photo_uploader.upload(
            file_source=item.photo_path, peer_id=message.peer_id
        )
        carousel = template_gen(
            TemplateElement(
                title=item_name, description=item.description, buttons=KEYBOARD_3
            )
        )
        await message.answer(
            item_scenario["message"], template=carousel, attachment=photo
        )


if __name__ == "__main__":
    bot.run_forever()
