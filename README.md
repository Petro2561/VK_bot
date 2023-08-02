# VK_bot
Бот-каталог для Кондитерского магазина

## Использованные технологии
SQLAlchemy, SQLite, VKbottle, Docker

## Как развернуть бота
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

### Как все устроено

Ввиду маленького размера проекта и отсутсвия дальнейших планов по масштабированию проекта использована база SQLite, а фотографии хранятся в папке media.
В качестве ORM использована SQLAlchemy.

Использована библиотека Vkbottle такб как относительно популярна и имеет понятную документацию на русском языке. Также в библиотеке реализована Машина Состояний.

Основаная логика когда реализована в файле bot.py. В файле находятся 4 хендела: стартовый и три хендлера для состояний.
Реализована кнопка назад.  
Сообщения для каждого состояния подгружаются из JSON файла scenario.json.  
В файле config хранятся глобальные переменные.  
В папке utils хранятся клавиатуры. 




