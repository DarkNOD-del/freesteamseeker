import os
import time
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup


CHAT_ID       = os.getenv('CHAT_ID')
BOT_TOKEN     = os.getenv('BOT_TOKEN')
SAVED_ID_PATH = os.getenv('SAVED_ID_PATH') if len(os.getenv('SAVED_ID_PATH')) > 1 else "saved_id.txt"
TARGET_URI = "https://freesteam.ru/"



def get_saved_id():
    saved_id = "0"

    if not os.path.exists(SAVED_ID_PATH):
        with open(SAVED_ID_PATH, "w", encoding = 'utf-8') as f:
            f.write(saved_id)
        
        return saved_id

    with open(SAVED_ID_PATH, "r", encoding = 'utf-8') as f:
        saved_id = f.read()
    
    return saved_id.strip()



def set_save_id(new_id):
    with open(SAVED_ID_PATH, "w", encoding = 'utf-8') as f:
        f.write(new_id)



def collect_data():
    response = requests.get(url= TARGET_URI)

    if response.status_code != 200:
        print(f"[ERROR] Не удалось получить данные с {TARGET_URI} (STATUS CODE: {response.status_code})")
        return
    
    soup = BeautifulSoup(response.text, "lxml")

    blog_grid = soup.find("div", id = "blog-grid")

    if not blog_grid:
        print("[ERROR] Не удалось получить данные из таблицы (TABLE NOT FOUND)")
        return
    
    saved_id = get_saved_id()
    
    post_boxes = blog_grid.find_all("div", class_ = "post-box")

    new_posts = []

    for post_box in post_boxes:
        try:
            id = post_box.find("article").get("id").strip()
        except:
            continue

        try:
            title = post_box.find("h2", class_ = "entry-title").text.strip()
        except:
            title = "Нет данных"

        try:
            content = post_box.find("div", class_ = "entry-content").text.replace(". ", ".\n").strip()
        except:
            content = ""

        try:
            post_link = post_box.find("a", class_ = "thumb-link").get("href")
        except:
            post_link = TARGET_URI
        
        try:
            banner_link = post_box.find("img", class_ = "attachment-banner-small-image").get("data-src")
        except:
            banner_link = open("data/no-photo.jpg", 'rb')

        try:
            entry_cats = post_box.find("span", class_ = "entry-cats").find_all("a")
            platform = entry_cats[0].text.strip()
            status = entry_cats[1].text.strip()
        except:
            platform = "Нет данных"
            status = "Нет данных"

        try:
            posted_on = post_box.find("div", class_ = "posted-on").text.split("Опубликовано")[1].strip()
        except:
            posted_on = "Нет данных"

        if saved_id == id:
            break

        new_posts.append({
            "id" : id,
            "title" : title,
            "content" : content,
            "platform" : platform,
            "status" : status,
            "posted_on" : posted_on,
            "post_link" : post_link,
            "banner_link" : banner_link
        })

    if len(new_posts) <= 0:
        print("[FOUND] Новых постов не обнаружено")
        return
    
    new_posts.reverse()
    
    print(f"[FOUND] Найдено новых постов: {len(new_posts)}")

    bot = telebot.TeleBot(BOT_TOKEN)
    
    for i, new_post in enumerate(new_posts):
        try:
            caption = f"*{new_post['title'].upper()}*\nСтатус: `{new_post['status']}`\nПлатформа: `{new_post['platform']}`\nОпубликовано: `{new_post['posted_on']}`"
            
            keyboard = types.InlineKeyboardMarkup(row_width = 1)
            keyboard.add(types.InlineKeyboardButton("Перейти", url = new_post['post_link']))

            bot.send_photo(CHAT_ID, new_post['banner_link'], caption, reply_markup = keyboard, parse_mode = "Markdown")
            
            set_save_id(new_post['id'])

            print(f"   [{i + 1}/{len(new_posts)}] Отправлено в канал: {new_post['title']}")
        except:
            print(f"   [{i + 1}/{len(new_posts)}] Не удалось отправить пост")

        time.sleep(0.5)

    

def main():   
    os.system("clear")
    print("[START] Работа началась")
    collect_data()
    print("[END]   Работа окончена")



if __name__ == "__main__":
    main()
