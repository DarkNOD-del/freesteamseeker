from datetime import datetime



def get_date():
    now = datetime.utcnow()

    month_names = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря'
    }

    day_names = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }

    return now.strftime("{day}, %d {month} %Y в %H:%M по UTC".format(month = month_names[now.month], day = day_names[now.weekday()]))



def update_readme(post_title, post_banner):
    try:
        content = f"""

# FREE STEAM SEEKER

Бот, который отслеживает игры с раздач и отправляет в твой Telegram!

## ⚡️ Актуальные данные

Последнее обновление: `{get_date()}`  
Последняя сохраненная игра: `{post_title}` 

<img width="100%" src='{post_banner}' alt='{post_title}'/>

## 🔗 Сайты-доноры

[![Logo](https://img.shields.io/badge/Free%20Steam-darkblue?style=for-the-badge&logo=steam&logoColor=white)](https://freesteam.ru/) 

![Logo](https://img.shields.io/badge/В%20будущем%20будет%20больше...-darkgreen?style=for-the-badge)

## ⚙️ Переменные окружения

Чтобы запустить этот проект, вам нужно будет добавить следующие переменные окружения в ваш .env файл.

`BOT_TOKEN` - идентификатор вашего бота в Telegram

`CHAT_ID` - идентификатор чата, куда отправлять сообщения

`SAVED_ID_PATH` - путь до файла с последним сохраненным постом (по умолчанию saved_id.txt)

## 🚀 Авторы

Сделано с 🐍 от [![GitHub](https://img.shields.io/badge/GitHub-DarkNOD-red)](https://github.com/DarkNOD-del)"""

        with open("README.md", "w", encoding = "utf-8") as file:
            file.write(content)

        return True

    except:
        return False



if __name__ == "__main__":
    pass
