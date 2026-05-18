import telebot
from telebot import types
import random
import os

TOKEN = "8926322049:AAEdbt7L5roSbgo7g2z_SPwBZ1QgeeHt5qU"

bot = telebot.TeleBot(TOKEN)

# ================= FACTS =================

animal_facts = [
    "🦒 Керік күніне тек 30 минут ұйықтайды.",
    "🐙 Сегізаяқтың 3 жүрегі бар.",
    "🐧 Пингвин өмір бойы бір жұппен жүруі мүмкін.",
    "🦁 Арыстанның ақырған дауысы 8 км естіледі.",
    "🐬 Дельфиндер бір-біріне ат қояды.",
    "🦉 Үкі басын 270° бұра алады.",
    "🐘 Піл ешқашан секіруді білмейді.",
    "🐼 Панда күніне 12 сағат тамақ жейді.",
    "🦈 Акула динозаврлардан да бұрын өмір сүрген.",
    "🐢 Тасбақа 150 жыл өмір сүре алады.",
    "🦓 Әр зебраның сызығы ерекше.",
    "🦜 Тотықұс 100+ сөз жаттай алады.",
    "🐊 Крокодил тілін шығара алмайды.",
    "🐸 Бақа терісі арқылы су ішеді.",
    "🐨 Коала күніне 20 сағат ұйықтайды.",
    "🦌 Бұғы өте жылдам жүгіреді.",
    "🐅 Жолбарыстың терісі де жолақты.",
    "🐇 Қоянның тістері өмір бойы өседі.",
    "🦔 Кірпі суда жүзе алады.",
    "🐿 Тиін тамағын ұмытып кетеді."
]

# ================= QUIZ =================

quiz_questions = [
    {
        "question": "🦁 Арыстан қайда өмір сүреді?",
        "options": ["Шөл", "Джунгли", "Саванна"],
        "answer": "Саванна"
    },
    {
        "question": "🐧 Пингвин ұша ала ма?",
        "options": ["Иә", "Жоқ"],
        "answer": "Жоқ"
    },
    {
        "question": "🐘 Ең үлкен құрлық жануары?",
        "options": ["Піл", "Аю", "Кит"],
        "answer": "Піл"
    },
    {
        "question": "🦒 Ең ұзын мойынды жануар?",
        "options": ["Түйе", "Керік", "Бұғы"],
        "answer": "Керік"
    },
    {
        "question": "🐬 Дельфин не?",
        "options": ["Балық", "Сүтқоректі", "Құс"],
        "answer": "Сүтқоректі"
    },
    {
        "question": "🦉 Түнде жақсы көретін құс?",
        "options": ["Бүркіт", "Үкі", "Тауық"],
        "answer": "Үкі"
    },
    {
        "question": "🐢 Ең баяу жануарлардың бірі?",
        "options": ["Қоян", "Тасбақа", "Қасқыр"],
        "answer": "Тасбақа"
    },
    {
        "question": "🦈 Акула не арқылы тыныс алады?",
        "options": ["Өкпе", "Желбезек", "Тері"],
        "answer": "Желбезек"
    },
    {
        "question": "🐨 Коала не жейді?",
        "options": ["Балық", "Эвкалипт", "Ет"],
        "answer": "Эвкалипт"
    },
    {
        "question": "🐼 Панданың сүйікті асы?",
        "options": ["Бамбук", "Ет", "Шөп"],
        "answer": "Бамбук"
    }
]

# ================= IMAGES =================

animal_images = os.listdir("images")


@bot.message_handler(func=lambda message: message.text == "📸 Жануар суреті")
def send_animal_photo(message):
    random_image = random.choice(animal_images)

    image_path = f"images/{random_image}"

    with open(image_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

# ================= SCORE =================

scores = {}

# ================= MENU =================

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🦁 Факт")
    btn2 = types.KeyboardButton("🎯 Quiz")
    btn3 = types.KeyboardButton("📸 Жануар суреті")
    btn4 = types.KeyboardButton("🏆 Ұпайым")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    return markup

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌍 WildPedia Bot-қа қош келдің!\n\nТөменнен таңдап көр 👇",
        reply_markup=main_menu()
    )

# ================= FACT =================

@bot.message_handler(func=lambda m: m.text == "🦁 Факт")
def fact(message):
    bot.send_message(
        message.chat.id,
        random.choice(animal_facts)
    )

# ================= IMAGE =================

@bot.message_handler(func=lambda m: m.text == "📸 Жануар суреті")
def animal_photo(message):
    bot.send_photo(
        message.chat.id,
        random.choice(animal_images),
        caption="📸 Керемет жануар!"
    )

# ================= SCORE =================

@bot.message_handler(func=lambda m: m.text == "🏆 Ұпайым")
def score(message):
    user_id = message.from_user.id

    if user_id not in scores:
        scores[user_id] = 0

    bot.send_message(
        message.chat.id,
        f"🏆 Сенің ұпайың: {scores[user_id]}"
    )

# ================= QUIZ =================

@bot.message_handler(func=lambda m: m.text == "🎯 Quiz")
def quiz(message):

    question_data = random.choice(quiz_questions)

    markup = types.InlineKeyboardMarkup()

    for option in question_data["options"]:
        btn = types.InlineKeyboardButton(
            option,
            callback_data=f"{option}|{question_data['answer']}"
        )
        markup.add(btn)

    bot.send_message(
        message.chat.id,
        question_data["question"],
        reply_markup=markup
    )

# ================= ANSWER =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    selected, correct = call.data.split("|")

    user_id = call.from_user.id

    if user_id not in scores:
        scores[user_id] = 0

    if selected == correct:
        scores[user_id] += 1

        bot.answer_callback_query(
            call.id,
            "✅ Дұрыс!"
        )

        bot.send_message(
            call.message.chat.id,
            f"🔥 Дұрыс жауап!\n🏆 Ұпай: {scores[user_id]}"
        )

    else:
        bot.answer_callback_query(
            call.id,
            "❌ Қате!"
        )

        bot.send_message(
            call.message.chat.id,
            f"😢 Қате!\nДұрыс жауап: {correct}"
        )

# ================= RUN =================

print("🤖 Bot іске қосылды!")

keep_alive()
bot.infinity_polling()