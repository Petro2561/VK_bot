from models import Session, Section, Item  # предположим, что сессия и модели были импортированы здесь

from sqlalchemy import desc
import json

# Создаем сессию
session = Session()

new_section_1 = Section(name='Торты')
new_section_2 = Section(name='Пироги')
new_section_3 = Section(name='Печенье')
# Добавление секции в сессию и сохранение в базе данных
session.add(new_section_1)
session.add(new_section_2)
session.add(new_section_3)
section_cookies = session.query(Section).filter_by(name='Печенье').first()
section_cakes = session.query(Section).filter_by(name='Торты').first()
section_pies = session.query(Section).filter_by(name='Пироги').first()

items = [
    Item(name='Кукис', description='Вкусное и каллорийное печенье', photo_path='./media/cookies.jpg', section=section_cookies),
    Item(name='Медовое печенье', description='Нежнейшее печенье', photo_path='./media/honey_cookie.jpg', section=section_cookies),
    Item(name='Шоколадный торт', description='Классический торт', photo_path='./media/chocolate_cake.png', section=section_cakes),
    Item(name='Медовик', description='Медовик не нуждается в представлении', photo_path='./media/napoleon.jpg', section=section_cakes),
    Item(name='Осетинский пирог', description='Осетинский пирог это больше чем пирог', photo_path='./media/osetian_pie.jpg', section=section_pies),
    Item(name='Шарлотка', description='Под кружечку молока самое оно', photo_path='./media/sharlotka.jpg', section=section_pies),
]
for item in items:
    session.add(item)
session.commit()

# Извлечение всех объектов Section из базы данных

# Конвертация в JSON и запись в файл
# item_to_update = session.query(Item).filter(Item.name == 'Шоколадный торт').first()

# # Обновляем photo_path
# item_to_update.photo_path = 'media/cookies.jpg'


session.commit()

sections = session.query(Item).all()
for section in sections:
    print(section)

# получаем все записи из таблицы Item, связанные с определенной секцией
# items = session.query(Item).filter(Item.section_id == some_section_id).all()
# for item in items:
#     print(item)