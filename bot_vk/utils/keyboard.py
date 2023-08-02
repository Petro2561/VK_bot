from models import Item, Section, Session
from vkbottle import Keyboard, Text

session = Session()

def get_keyboard(category: str) -> Keyboard:
    keyboard_2 = Keyboard(one_time=True)
    section = session.query(Section).filter(Section.name == category).first()
    items = session.query(Item).filter(Item.section_id == section.id).all()
    for item in items:
        keyboard_2.add(Text(item.name))
    keyboard_2.add(Text("Назад"))
    return keyboard_2


KEYBOARD_1 = Keyboard(one_time=True)
for section in session.query(Section).all():
    KEYBOARD_1.add(Text(section.name))


KEYBOARD_3 = Keyboard(one_time=True).add(Text(("Назад")))
