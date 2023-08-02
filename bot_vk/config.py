import os
from dotenv import load_dotenv
from vkbottle import API
from vkbottle import BaseStateGroup

load_dotenv()

bot_api = API(os.getenv("VK_TOKEN"))

class CatalogStates(BaseStateGroup):
    CHOOSE = "Выбор_категории"
    SECTION = "Категория"
    ITEM = "Товар"
