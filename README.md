# VK_bot
Бот-каталог для Кондитерского магазина

Использованы технологии SQLAlchemy, SQLlite, VKbottle, Docker

Для запуска бота необходимо клонировать репозиторий git clone 

В директории bot_vk создать .env файл и добавить VK_TOKEN

Собрать образ:
```
docker build -t bot .
```

Запустить контейнер:
```
docker run -d --name my-bot bot
```

Готового бота можно найти по ссылке https://vk.com/im?peers=-215578680&sel=-221808421
Для начала работы с ботом нужно ввести сообщение start
