from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import random
from random import choice

import requests
import os
import asyncio
import time

from pyowm import OWM
from pyowm.utils.config import get_default_config

from bs4 import BeautifulSoup
from config import TOKEN,DEVELOPER,API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
owm = OWM(API_KEY)

letters = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Щ", "Э", "Ю", "Я"]

# Check have user admin in group
async def is_admin_group(chat_id, user_id):
    try:
        result = await bot.get_chat_member(chat_id, user_id)
        if "administrator" in result["status"] or "creator" in result["status"]:
            return True
        return False
    except Exception as e:
        pass
        
# Check game in chat
def is_game_in_chat(chat_id):
    try:
        with open("chats/" + str(chat_id) + "/" + "info.txt") as game:
            game.close()
        return True
    except Exception as e:
        return False

# Check dirs 
def verification_dirs_chat(chat_id):
    try:
        path = os.path.join(os.getcwd() + "/chats", str(chat_id))
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "crosses")
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "associations")
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "mafia")
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "hand")
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "charade")
        if not os.path.exists(path):
            os.mkdir(path)

    except Exception as e:
        pass

# Remove dirs
def remove_dirs_chat(chat_id):
    try:
        path = os.path.join(os.getcwd() + "/chats", str(chat_id))

        if os.path.exists(path):

            path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "crosses")
            if os.path.exists(path):
                files = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/crosses")
                if files:
                    for temp in files:
                        os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/crosses/" + temp)
                os.rmdir(os.getcwd() + "/chats/" + str(chat_id) + "/crosses")

            path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "associations")
            if os.path.exists(path):
                files = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/associations")
                if files:
                    for temp in files:
                        os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/associations/" + temp)
                os.rmdir(os.getcwd() + "/chats/" + str(chat_id) + "/associations")

            path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "mafia")
            if os.path.exists(path):
                files = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")
                if files:
                    for temp in files:
                        os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp)
                os.rmdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")

            path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "hand")
            if os.path.exists(path):
                files = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/hand")
                if files:
                    for temp in files:
                        os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/hand/" + temp)
                os.rmdir(os.getcwd() + "/chats/" + str(chat_id) + "/hand")

            path = os.path.join(os.getcwd() + "/chats/" + str(chat_id), "charade")
            if os.path.exists(path):
                files = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/charade")
                if files:
                    for temp in files:
                        os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/charade/" + temp)
                os.rmdir(os.getcwd() + "/chats/" + str(chat_id) + "/charade")

            files = os.listdir(os.getcwd() + "/chats/" + str(chat_id))
            if files:
                for temp in files:
                    os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/" + temp)

            return os.rmdir(os.getcwd() + "/chats/" + str(chat_id))

    except Exception as e:
        pass

# Type: new member
@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_members_delete(message):
    try:
        if await is_admin_group(message.chat.id, message.bot.id):
            await bot.delete_message(message.chat.id, message.message_id)
            
        if message.new_chat_members[0].id == bot.id:
            verification_dirs_chat(message.chat.id)
            buttons  = [types.InlineKeyboardButton(text='Игры 📌', callback_data="Игры"),types.InlineKeyboardButton(text='Помощь ◀', callback_data="Помощь")] 
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            return await message.answer("🍍 Приветствую Вас, господа!\nМеня зовут - *Ананасыч*\nЯ многофункциональный бот\n\nС моей помощью можно:\n💾 Играть в различные игры\n👮 Следить за порядком\n🔔 Администрировать чат\n\n_для полного функционала рекомендую выдать мне права администратора_", parse_mode="Markdown", reply_markup=keyboard)
        return await message.answer("🍍[%s](tg://user?id=%d), *добро пожаловать в %s*" % (message.new_chat_members[0].first_name, message.new_chat_members[0].id,message.chat.full_name), parse_mode="Markdown")
    except Exception as e:
        pass

# Type: left member
@dp.message_handler(content_types=["left_chat_member"])
async def new_chat_members_delete(message):
    try:
        if message.left_chat_member.id == bot.id:
            return remove_dirs_chat(message.chat.id)

        if await is_admin_group(message.chat.id, message.bot.id):
            await bot.delete_message(message.chat.id, message.message_id)

        await message.answer("🍍 [%s](tg://user?id=%d) покинул(-а) *%s*" % (message.left_chat_member.first_name, message.left_chat_member.id,message.chat.full_name), parse_mode="Markdown")
        
        if not os.path.isfile(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt"):
            return True

        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt") as game:
            record = game.read()

        if "MAFIA" in record:
            await leave_from_mafia(message.chat.id, message.from_user.id)
            
        if "ASSOCIATIONS" in record:
            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations/" + temp) as player:
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations/" + temp)
    except Exception as e:
        pass

# Command: start
@dp.message_handler(commands=['start', 'help', 'welcome'])
async def start_command(message: types.Message):
    try:
        buttons  = [types.InlineKeyboardButton(text='Игры 📌', callback_data="Игры"),types.InlineKeyboardButton(text='Помощь ◀', callback_data="Помощь")] 
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        return await message.answer("Приветствую - я Ананасыч 🍍\nМногоспособный бот для веселья!", reply_markup=keyboard)
    except Exception as e:
        pass

# Bag command
@dp.message_handler(commands=['bag'])
async def mute_command(message: types.Message):
    try:
        text = message.text.split(" ")
        if len(text) < 2:
            return await message.reply("🍍 *Нет текста сообщения*\n\nИспользуйте: /bag [Текст]", parse_mode="Markdown")
            
        await message.reply("🍍 Сообщение было отправлено!")
        text = message.text.replace(text[0], "")
        message = "⚠ *Сообщение о баге*\n\nОтправитель: [%s](tg://user?id=%d)\nЧат ID: %d\nUser ID: %d\n\nСообщение:\n%s" % (message.from_user.first_name,message.from_user.id,message.chat.id,message.from_user.id,text)
        await bot.send_message(DEVELOPER, message, parse_mode="Markdown")
    except Exception as e:
        pass 

# Admins commands
# Command: mute
@dp.message_handler(commands=['mute'])
async def mute_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await message.answer("🍍 Нужно использовать только в чатах!")

        if not message.reply_to_message:
            return await message.reply("🍍 Команда должна быть использована на ответное сообщение!")

        if not await is_admin_group(message.chat.id, message.bot.id):
            return await bot.send_message(message.chat.id, "🍍 Для полного функционала бота, рекомендуется выдать Администратора.")

        if message.reply_to_message.from_user.id == message.bot.id:
            return await message.reply("🍍 Невозможно использовать команду...")

        if not await is_admin_group(message.chat.id, message.from_user.id):
            return await bot.delete_message(message.chat.id, message.message_id)

        if await is_admin_group(message.chat.id, message.reply_to_message.from_user.id):
            return await message.reply("🍍 [%s](tg://user?id=%d) является *Администратором*" % (message.reply_to_message.from_user.first_name,message.reply_to_message.from_user.id), parse_mode="Markdown")

        await message.answer("🍍 [%s](tg://user?id=%d) *не сможет писать в чат 30 минут*" % (message.reply_to_message.from_user.first_name,message.reply_to_message.from_user.id), parse_mode="Markdown")
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,until_date=int(time.time()) + 60*30,can_send_messages=False)
    except Exception as e:
        pass

# Command: Kick
@dp.message_handler(commands=['kick'])
async def kick_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await message.answer("🍍 Нужно использовать только в чатах!")

        if not message.reply_to_message:
            return await message.reply("🍍 Команда должна быть использована на ответное сообщение!")

        if not await is_admin_group(message.chat.id, message.bot.id):
            return await bot.send_message(message.chat.id, "🍍 Для полного функционала бота, рекомендуется выдать Администратора.")

        if message.reply_to_message.from_user.id == message.bot.id:
            return await message.reply("🍍 Невозможно использовать команду...")

        if not await is_admin_group(message.chat.id, message.from_user.id):
            return await bot.delete_message(message.chat.id, message.message_id)

        if await is_admin_group(message.chat.id, message.reply_to_message.from_user.id):
            return await message.reply("🍍 [%s](tg://user?id=%d) является *Администратором*" % (message.reply_to_message.from_user.first_name,message.reply_to_message.from_user.id), parse_mode="Markdown")

        await bot.delete_message(message.chat.id, message.message_id)
        await message.answer("🍍 [%s](tg://user?id=%d) *кикнул(-а)* [%s](tg://user?id=%d)" % (message.from_user.first_name,message.from_user.id,message.reply_to_message.from_user.first_name,message.reply_to_message.from_user.id), parse_mode="Markdown")
        await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    except Exception as e:
        pass 

# Games
# Command: Fanta
@dp.message_handler(commands=['fanta'])
async def fanta_command(message: types.Message):
    try:

        buttons  = [types.InlineKeyboardButton(text='Дальше', callback_data="Дальше")] 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)

        with open("info/fanta_message.txt", encoding="utf8") as fanta:
            mission = fanta.read().replace("\\n", "\n").split("|")

        select_mission = random.randint(0,len(mission)) - 1
        await message.reply("🍍 %s" % mission[select_mission], parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        pass

# Command: hand
@dp.message_handler(commands=['hand'])
async def hand_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await bot.send_message(message.from_user.id, "🍍 Эту игру можно запустить только в группе)")

        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            return await bot.delete_message(message.chat.id, message.message_id)

        verification_dirs_chat(message.chat.id)

        buttons  = [types.InlineKeyboardButton(text='Принять 👍', callback_data="Рука")] 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)

        return await message.reply("🍍 [%s](tg://user?id=%d) кидает вызов в камень-ножницы-бумага" % (message.from_user.first_name,message.from_user.id), parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        pass 

# Command: coinflip
@dp.message_handler(commands=['coinflip'])
async def coinflip_command(message: types.Message):
    try:
        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            await bot.delete_message(message.chat.id, message.message_id)

        coin = ["Орёл", "Решка"]
        return await message.reply("🍍 [%s](tg://user?id=%d) подбросил монету\n*Выпало: 🪙 %s*" % (message.from_user.first_name,message.from_user.id, choice(coin)), parse_mode="Markdown")        
    except Exception as e:
        pass

# Command: crosses
@dp.message_handler(commands=['crosses'])
async def crosses_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await bot.send_message(message.from_user.id, "🍍 Эту игру можно запустить только в группе)")

        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            await bot.delete_message(message.chat.id, message.message_id)

        buttons  = [types.InlineKeyboardButton(text='Присоединиться ⚔', callback_data="Крестики-нолики")] 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)

        verification_dirs_chat(message.chat.id)

        return await message.reply("🍍 [%s](tg://user?id=%d) хочет поиграть в крестики-нолики" % (message.from_user.first_name,message.from_user.id), parse_mode="Markdown", reply_markup=keyboard)        
    except Exception as e:
        pass

# Help function crosses
def progress_to_win_crosses(check_pos):
    if check_pos[0] != 0 and check_pos[0] == check_pos[1] and check_pos[1] == check_pos[2]:
        return check_pos[0]
    elif check_pos[3] != 0 and check_pos[3] == check_pos[4] and check_pos[4] == check_pos[5]:
        return check_pos[3]
    elif check_pos[6] != 0 and check_pos[6] == check_pos[7] and check_pos[7] == check_pos[8]:
        return check_pos[6]
    elif check_pos[0] != 0 and check_pos[0] == check_pos[3] and check_pos[3] == check_pos[6]:
        return check_pos[0]
    elif check_pos[1] != 0 and check_pos[1] == check_pos[4] and check_pos[4] == check_pos[7]:
        return check_pos[1]
    elif check_pos[2] != 0 and check_pos[2] == check_pos[5] and check_pos[5] == check_pos[8]:
        return check_pos[2]
    elif check_pos[0] != 0 and check_pos[0] == check_pos[4] and check_pos[4] == check_pos[8]:
        return check_pos[0]
    elif check_pos[2] != 0 and check_pos[2] == check_pos[4] and check_pos[4] == check_pos[6]:
        return check_pos[2]
    elif check_pos[0] != 0 and check_pos[1] != 0 and check_pos[2] != 0 and check_pos[3] != 0 and check_pos[4] != 0 and check_pos[5] != 0 and check_pos[6] != 0 and check_pos[7] != 0 and check_pos[8] != 0:
        return 4
    return False

# Command: cities
@dp.message_handler(commands=['cities'])
async def crosses_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await bot.send_message(message.from_user.id, "🍍 Эту игру можно запустить только в группе)")

        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            await bot.delete_message(message.chat.id, message.message_id)

        if not await is_admin_group(message.chat.id, bot.id):
            return await message.reply("🍍 Для запуска данной игры мне нужны права Администратора.")

        verification_dirs_chat(message.chat.id)
        first_letter = choice(letters)

        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt", "+w") as game:
            game.write("CITIES|%s|0|0" % first_letter)

        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/cities.txt", "+w") as city:
            city.close()

        await bot.delete_message(message.chat.id, message.message_id)

        step = await message.answer("🍍 *Города*\nИгра города запущена!\n\n📌 Бот пишет букву на которую нужно написать город\nСледующий ход будет на последнию букву города\nСоответственно игрок пропустит следующий ход\n\nНапишите город на букву: *%s*" % first_letter, parse_mode="Markdown")        
        await asyncio.sleep(60)
        if os.path.isfile(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt"):
            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt") as game:
                record = game.read().split("|")

            if record[2] == "0":
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt")
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/cities.txt")
                return await bot.delete_message(message.chat.id, step.message_id)
    except Exception as e:
        pass   

# Command: charade
@dp.message_handler(commands=['charade'])
async def mafia_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await bot.send_message(message.from_user.id, "🍍 Эту игру можно запустить только в группе)")

        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            return await bot.delete_message(message.chat.id, message.message_id)

        if not await is_admin_group(message.chat.id, bot.id):
            return await message.reply("🍍 Для запуска данной игры мне нужны права Администратора.")

        buttons = [types.InlineKeyboardButton(text='Присоединиться', callback_data="Шарада")] 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)

        verification_dirs_chat(message.chat.id)

        await bot.delete_message(message.chat.id, message.message_id)
        step_first_message = await message.answer("🍍 *Шарада*\n\nИдёт набор участников", parse_mode="Markdown", reply_markup=keyboard)
        message.message_id = step_first_message.message_id
        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt", "+w") as game:
            game.write("CHARADE|REGISTER|%d" % message.message_id)

        await asyncio.sleep(60)
        players = os.listdir(os.getcwd() + "/chats/" + str(message.chat.id) + "/charade")
        await bot.delete_message(message.chat.id, message.message_id)
        if not players or len(players) < 1:
            for temp in players:
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/charade/" + temp)

            os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt")
            return await message.answer("🍍 *Шарада*\nНедостаточно игроков!", parse_mode="Markdown")

        index = choice(players)
        index = int(index.replace(".txt", ""))
        info = await bot.get_chat_member(message.chat.id, index)

        step_second = await message.answer("🍍 *Шарада*\nИгра начинается!\n\nСлово должен придумать: [%s](tg://user?id=%d)\n⌛ Время: 20 секунд" % (info.user.first_name, index), parse_mode="Markdown")
        step_third = await bot.send_message(index, "🍍 *Шарада*\nПридумайте слово и напишите его мне", parse_mode="Markdown")

        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt", "+w") as game:
            game.write("CHARADE|NEED_WORD|%d|%d" % (index, message.message_id))

        await asyncio.sleep(20)
        if os.path.isfile(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt"):
            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt") as game:
                info = game.read().split("|")

            if info[0] == "CHARADE" and info[1] == "NEED_WORD":
                await bot.delete_message(message.chat.id, step_second.message_id)
                await bot.delete_message(index, step_third.message_id)
                await bot.send_message(message.chat.id,"🍍 *Шарада*\nИгра закончена!\n\nСлово небыло придумано..", parse_mode="Markdown")
                players = os.listdir(os.getcwd() + "/chats/" + str(message.chat.id) + "/charade")
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt")
                for temp in players:
                    os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/charade/" + temp)
                    os.remove(os.getcwd() + "/users/" + temp)
            
    except Exception as e:
        pass   

# Command: mafia
@dp.message_handler(commands=['mafia'])
async def mafia_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await bot.send_message(message.from_user.id, "🍍 Эту игру можно запустить только в группе)")

        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            return await bot.delete_message(message.chat.id, message.message_id)

        if not await is_admin_group(message.chat.id, bot.id):
            return await message.reply("🍍 Для запуска данной игры мне нужны права Администратора.")

        buttons = [types.InlineKeyboardButton(text='Присоединиться 🤵', callback_data="Мафия")] 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)

        verification_dirs_chat(message.chat.id)

        await bot.delete_message(message.chat.id, message.message_id)
        step_first_message = await message.answer("🍍 *Мафия*\n\nИдёт набор участников", parse_mode="Markdown", reply_markup=keyboard)
        message.message_id = step_first_message.message_id

        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt", "+w") as game:
            game.write("MAFIA|REGISTER|%d" % message.message_id)

        await asyncio.sleep(60)
        step_second_message = await message.reply("🍍 *Мафия*\nИдёт набор участников\n⌛ Осталось: *60 секунд*", parse_mode="Markdown")

        await asyncio.sleep(30)
        step_third_message = await message.reply("🍍 *Мафия*\nИдёт набор участников\n⌛ Осталось: *30 секунд*", parse_mode="Markdown")

        await asyncio.sleep(30)

        await bot.delete_message(message.chat.id, step_first_message.message_id)
        await bot.delete_message(message.chat.id, step_second_message.message_id)
        await bot.delete_message(message.chat.id, step_third_message.message_id)

        players = os.listdir(os.getcwd() + "/chats/" + str(message.chat.id) + "/mafia")
        if len(players) < 3:
            os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt")
            for temp in players:
                os.remove(os.getcwd() + "/users/" + temp)
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/mafia/" + temp)
                return await bot.edit_message_text(chat_id=message.chat.id, message_id=step_first_message.message_id, text="🍍 *Мафия*\n\nНедостаточно игроков для начала игры.", parse_mode="Markdown",reply_markup=None)

        count_mafia = 0
        count_police = 0
        count_medic = 0
        count_whore = 0

        if len(players) >= 3 and len(players) <= 5:
            count_mafia = 1

        elif len(players) > 5 and len(players) <= 6:
            count_mafia = 1
            count_police = 1

        elif len(players) > 6 and len(players) <= 8:
            count_mafia = 1
            count_police = 1
            count_medic = 1

        elif len(players) > 8 and len(players) <= 10:
            count_mafia = 2
            count_police = 1
            count_medic = 1
            count_whore = 1

        else:
            count_mafia = 3
            count_police = 1
            count_medic = 1
            count_whore = 1

        mafia_players = []
        police_players = []
        medic_players = []
        whore_players = []

        len_range = count_mafia + count_police + count_medic + count_whore
        for i in range(len_range):
            player = choice(players)
            if count_mafia != 0:
                if player not in mafia_players:
                    count_mafia -= 1
                    players.remove(player)
                    mafia_players.append(player)

                    continue
            elif count_police != 0:
                if player not in police_players:
                    count_police -= 1
                    players.remove(player)
                    police_players.append(player)

                    continue
            elif count_medic != 0:
                if player not in medic_players:
                    count_medic -= 1
                    players.remove(player)
                    medic_players.append(player)

                    continue
            elif count_whore != 0:
                if player not in whore_players:
                    count_whore -= 1
                    players.remove(player)
                    whore_players.append(player)

                    continue

        dirs = os.listdir(os.getcwd() + "/chats/" + str(message.chat.id) + "/mafia")

        for temp in dirs:
            index = int(temp.replace(".txt", ""))
            if temp in mafia_players:
                await game_give_role(message.chat.id, index, 0)
                continue

            elif temp in police_players:
                await game_give_role(message.chat.id, index, 1)
                continue

            elif temp in medic_players:
                await game_give_role(message.chat.id, index, 2)
                continue

            elif temp in whore_players:
                await game_give_role(message.chat.id, index, 3)
                continue

            else:
                await game_give_role(message.chat.id, index, 4)

        step_final_message = await message.answer("🍍 *Мафия*\n\nИгра началась!", parse_mode="Markdown")
        await set_mafia_mode(message.chat.id, 1, "Night", message.message_id, True)
    except Exception as e:
        pass

# Help functions
async def game_give_role(chat_id, user_id, role):
    try:
        roles = ["🤵 Ваша роль: *Мафия*\nВаша задача: Устраняйте людей для победы!", 
        "👮‍♂️ Ваша роль: *Коммисар*\nВаша задача: Раскрывать личности людей",
        "👨‍⚕️ Ваша роль: *Медик*\nВаша задача: Спасать чужие жизни", 
        "🤷 Ваша роль: *Снежана*\nВаша задача: Мешайте другим игрокам выполнять действия", 
        "🙎‍♂️ Ваша роль: *Мирный*"]

        info = await bot.get_chat_member(chat_id, user_id)
        with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + str(user_id) + ".txt", "+w") as player:
            player.write("%d|1|0|%s" % (role, info.user.first_name))

        return await bot.send_message(user_id, roles[role], parse_mode="Markdown")
    except Exception as e:
        pass

async def set_mafia_mode(chat_id, day, mode, message, start=False):
    try:
        if not os.path.isfile(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt"):
            return True

        with open(os.getcwd() + "/chats/" + str(chat_id) + "/info.txt", "+w") as game:
            game.write("MAFIA|%s|%d|%d" %(mode,day,message))

        if mode == "Night":
            players = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")
            for temp in players:

                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp) as player:
                    info = player.read().split("|")

                if int(info[1]) != 1:
                    continue

                if int(info[0]) != 4:
                    # Variables
                    live_players = players
                    live_players.remove(temp)
                    buttons = []
                    #
                    for item in live_players:
                        with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + item) as player:
                            records = player.read().split("|")

                        if int(records[1]) != 1:
                            continue
                    
                        callback_text = "%d_%d_%s_%d_%d" % (chat_id, day, mode, message, int(item.replace(".txt", "")))
                        buttons.append(types.InlineKeyboardButton(text=records[3], callback_data=callback_text))
                        keyboard = types.InlineKeyboardMarkup(row_width=1)
                        keyboard.add(*buttons)

                    if int(info[0]) == 0:
                        await bot.send_message(int(temp.replace(".txt", "")), "🤵 Кого убить этой ночью?", reply_markup=keyboard)
                    elif int(info[0]) == 1:
                        await bot.send_message(int(temp.replace(".txt", "")), "👮‍♂️ Кого будем проверять?", reply_markup=keyboard)
                    elif int(info[0]) == 2:
                        await bot.send_message(int(temp.replace(".txt", "")), "👨‍⚕️ Кого будем лечить?", reply_markup=keyboard)
                    elif int(info[0]) == 3: 
                        await bot.send_message(int(temp.replace(".txt", "")), "🤷 К кому сегодня сходим?", reply_markup=keyboard)  
                    continue
                    
            image_night = open(os.getcwd() + "/info/night.jpg", "rb")
            await bot.send_photo(chat_id=chat_id, photo=image_night, caption="🍍 *Мафия*\n*Наступает ночь..*\n\nЖители города расходятся по своим домам, и ложаться спать\nМафия начинает делать свои дела..", parse_mode="Markdown")
            await asyncio.sleep(60)
            await set_mafia_mode(chat_id, day + 1, "Day", message)
        elif mode == "Day":
            game_message = "🍍 *Мафия*\n*Наступает утро*\n\nЖителя города встают со своих мягких кроватей.."
            players = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")
            # Variables
            users_id = []
            number_users = []
            role_users = []

            whoore_choose = 0
            medic_help = 0

            for temp in players:
                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp) as player:
                    info = player.read().split("|")

                if int(info[1]) != 1:
                    continue

                users_id.append(int(temp.replace(".txt", "")))
                number_users.append(int(info[2]))
                role_users.append(int(info[0]))

                if int(info[0]) == 3:
                    whoore_choose = int(info[3])
                elif int(info[0]) == 2:
                    medic_help = int(info[3])

                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp, "+w") as player:
                    player.write("%s|%s|0|%s" % (info[0], info[1], info[3]))

            killed = 0
            max_count = 0
            count = 0
            for i in range(len(players)):

                if users_id[i] == whoore_choose and role_users[i] == 2:
                    medic_help = 0
                    continue

                if users_id[i] == whoore_choose:
                    continue

                if role_users[i] != 0:
                    continue

                killed = number_users[i]
                for a in range(len(players)):
                    if users_id[a] == whoore_choose:
                        continue

                    if role_users[a] != 0:
                        continue
                    
                    if killed == number_users[a]:
                        count += 1
                if count > max_count:
                    max_count = count
                    killed = number_users[i]

            if killed != medic_help and killed != 0:
                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + str(killed) + ".txt") as kill:
                    info = kill.read().split("|")

                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + str(killed) + ".txt", "+w") as kill:
                    kill.write("%s|0|0|%s" % (info[0], info[3]))

                os.remove(os.getcwd() + "/users/" + str(killed) + ".txt")

                game_message += "\n\n💀 *Неприятные известия*:\nСегодня ночью был убит [%s](tg://user?id=%d)\nХодят слухи, что это дело рук мафии..." % (info[3], killed)
            else:
                game_message += "\n\n🗿 Ночь оказалась спокойной..."

            image_day = open(os.getcwd() + "/info/day.jpg", "rb")
            await bot.send_photo(chat_id=chat_id, photo=image_day, caption=game_message, parse_mode="Markdown")
            await progress_to_win_mafia(chat_id)
            await asyncio.sleep(15)
            await set_mafia_mode(chat_id, day + 1, "Voiting", message)
        elif mode == "Voiting":
            await bot.send_message(chat_id, "🍍 *Мафия*\n*Голосование*\n\nНаступает время решить кто-же возможно мафия..", parse_mode="Markdown")
            players = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")                
            for item in players:

                buttons = []
                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + item) as player:
                    get = player.read().split("|")

                if int(get[1]) != 1:
                    continue

                for temp in players:
                    with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp) as player:
                        records = player.read().split("|")

                    if int(records[1]) != 1 or temp == item:
                        continue

                    callback_text = "%d_%d_%s_%d_%d" % (chat_id, day, mode, message, int(temp.replace(".txt", "")))
                    buttons.append(types.InlineKeyboardButton(text=records[3], callback_data=callback_text))
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    keyboard.add(*buttons)
                    
                await bot.send_message(int(item.replace(".txt", "")), "🙎‍♂️ За кого голосуем?", reply_markup=keyboard)

            await asyncio.sleep(50)
            await set_mafia_mode(chat_id, day + 1, "Completed", message)
        elif mode == "Completed":
            voted = []

            players = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")
            for temp in voted:
                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp) as player:
                    get = player.read().split("|")

                if int(get[2]) == 0 or int(get[1]) != 1:
                    continue

                voted.append(int(get[2]))
                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp, "+w") as player:
                    player.write("%s|%s|0|%s" % (get[0], get[1], get[3]))

            killed = 0
            max_count = 0
            counter = 0
            for temp in voted:
                count = 0
                for item in voted:
                    if temp == item:
                        count += 1
                if count > max_count:
                    max_count = count
                    killed = temp

            game_message = ""
            if killed != 0:
                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + str(killed) + ".txt") as player:
                    get = player.read().split("|")

                game_message = "🍍 *Мафия*\n*Голосование*\n\nГолосование было завершено\n\n💀 [%s](tg://user?id=%d) был(-а) подвешен(-а) на вилисице!" % (get[3], killed) 

                with open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + str(killed) + ".txt", "+w") as player:
                    player.write("%s|0|0|%s" % (get[0], get[3]))

                os.remove(os.getcwd() + "/users/" + str(killed) + ".txt")

            else:
                game_message = "🍍 *Мафия*\n*Голосование*\n\nГолосование было завершено\n\nЖители не смогли придти к общему выбору.."

            await bot.send_message(chat_id, game_message, parse_mode="Markdown")
            await progress_to_win_mafia(chat_id)
            await asyncio.sleep(5)
            await set_mafia_mode(chat_id, day + 1, "Night", message)
    except Exception as e:
        pass

async def progress_to_win_mafia(chat_id):
    try:
        players = os.listdir(os.getcwd() + "/chats/" + str(chat_id) + "/mafia")

        mafia = "\tМафия:\n"
        police = ""
        medic = ""
        whore = ""
        humans = ""

        count_mafia = 0
        count_people = 0

        for temp in players:
            player = open(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp)
            get = player.read().split("|")
            player.close()

            if int(get[0]) == 0:
                if int(get[1]) == 0:
                    mafia += "\t🤵 [%s](tg://user?id=%d) - Мёртв(-а)\n" % (get[3] , int(temp.replace(".txt", "")))
                    continue

                mafia += "\t🤵 [%s](tg://user?id=%d)\n" % (get[3] , int(temp.replace(".txt", "")))
                count_mafia += 1
                continue

            if int(get[0]) == 1:
                if int(get[1]) == 0:
                    police += "\t👮‍♂️ [%s](tg://user?id=%d) - Мёртв(-а)\n" % (get[3] , int(temp.replace(".txt", "")))
                    continue

                police += "\t👮‍♂️ [%s](tg://user?id=%d)\n" % (get[3] , int(temp.replace(".txt", "")))
                count_people += 1
                continue

            if int(get[0]) == 2:
                if int(get[1]) == 0:
                    medic += "\t👨‍⚕️ [%s](tg://user?id=%d) - Мёртв(-а)\n" % (get[3] , int(temp.replace(".txt", "")))
                    continue

                medic += "\t👨‍⚕️ [%s](tg://user?id=%d)\n" % (get[3] , int(temp.replace(".txt", "")))
                count_people += 1
                continue

            if int(get[0]) == 3:
                if int(get[1]) == 0:
                    whore += "\t🤷 [%s](tg://user?id=%d) - Мёртв(-а)\n" % (get[3] , int(temp.replace(".txt", "")))
                    continue

                whore += "\t🤷 [%s](tg://user?id=%d)\n" % (get[3] , int(temp.replace(".txt", "")))
                count_people += 1
                continue

            else:
                if int(get[1]) == 0:
                    humans += "\t🙎‍♂️ [%s](tg://user?id=%d) - Мёртв(-а)\n" % (get[3] , int(temp.replace(".txt", "")))
                    continue

                humans += "\t🙎‍♂️ [%s](tg://user?id=%d)\n" % (get[3] , int(temp.replace(".txt", "")))
                count_people += 1
                continue

        DESTROY_GAME = False
        if count_people < 1:
            main_message = "🍍 *Мафия*\nИгра закончена!\n\nПобеда - *Мафия*\n\n" + mafia + "\tМирные:\n" + police + medic + whore + humans
            await bot.send_message(chat_id, main_message, parse_mode="Markdown")
            DESTROY_GAME = True
        elif count_mafia == 0:
            main_message = "🍍 *Мафия*\nИгра закончена!\n\nПобеда - *Мирные*\n\n" + mafia + "Мирные:\n" + police + medic + whore + humans
            await bot.send_message(chat_id, main_message, parse_mode="Markdown")
            DESTROY_GAME = True

        if DESTROY_GAME:
            os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/info.txt")
            destroy_mafia(chat_id)
        return DESTROY_GAME

    except Exception as e:
        pass

# detroy files
def destroy_mafia(chat_id):
    try:
        os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/info.txt")
        for temp in players:
            os.remove(os.getcwd() + "/chats/" + str(chat_id) + "/mafia/" + temp)
            if os.path.isfile(os.getcwd() + "/users/" + temp):
                with open(os.getcwd() + "/users/" + temp) as player:
                    chat_user = int(player.read())

                if chat_user == chat_id:
                    os.remove(os.getcwd() + "/users/" + temp)
    except Exception as e:
        pass 

# Command: associations
@dp.message_handler(commands=['associations'])
async def associations_command(message: types.Message):
    try:
        if message.chat.id == message.from_user.id:
            return await bot.send_message(message.from_user.id, "🍍 Эту игру можно запустить только в группе)")

        if is_game_in_chat(message.chat.id):
            if not await is_admin_group(message.chat.id, bot.id):
                return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
            return await bot.delete_message(message.chat.id, message.message_id)

        if not await is_admin_group(message.chat.id, bot.id):
            return await message.reply("🍍 Для запуска данной игры мне нужны права Администратора.")

        with open("info/words_for_associations.txt", encoding="utf8") as game:
            words = game.read().split(",")

        POS_WORD = random.randint(0, len(words) - 1)

        verification_dirs_chat(message.chat.id)

        step_first_message = await bot.send_message(message.chat.id, "🍍 Ассоциации\n\n[%s](tg://user?id=%d) запустил игру!\n\n✏ Пишите ассоциации к слову в течении 120 секунд\n⚡ Зарабатывайте очки и выигрывайте\n\nСлово для ассоциаций: *%s*" % (message.from_user.first_name,message.from_user.id,words[POS_WORD]), parse_mode="Markdown")

        parse_words(message.chat.id, words[POS_WORD])

        with open("chats/" + str(message.chat.id) + "/info.txt", "+w") as game:
            game.write("ASSOCIATIONS")

        await asyncio.sleep(60)
        step_second_message = await bot.send_message(message.chat.id, "🍍 *Ассоциации*\n\nНапоминаю слово: *%s*\n⌛Осталось: 60 секунд..." % words[POS_WORD], parse_mode="Markdown")

        await asyncio.sleep(30)
        step_third_message = await bot.send_message(message.chat.id, "🍍 *Ассоциации*\n\nНапоминаю слово: *%s*\n⌛Осталось: 30 секунд..." % words[POS_WORD], parse_mode="Markdown")

        await asyncio.sleep(30)
        dirs = os.listdir(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations")

        os.remove("chats/" + str(message.chat.id) + "/info.txt")
        os.remove("chats/" + str(message.chat.id) + "/parse.txt")

        if not dirs:
            if await is_admin_group(message.chat.id, bot.id):
                # Remove messages
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.delete_message(message.chat.id, step_first_message.message_id)
                await bot.delete_message(message.chat.id, step_second_message.message_id)
                return await bot.delete_message(message.chat.id, step_third_message.message_id)

            return await bot.send_message(message.chat.id, "🍍 *Ассоциации*\nИгра завершена!", parse_mode="Markdown")

        game_message = "🍍 *Ассоциации*\nИгра завершена!\n\nУчастники:\n"
        count = 1

        for item in dirs:
            if os.path.isfile("chats/" + str(message.chat.id) + "/associations/" + item):
                with open("chats/" + str(message.chat.id) + "/associations/" + item) as player:
                    score = int(player.read())

                os.remove("chats/" + str(message.chat.id) + "/associations/" + item)
                index = int(item.replace(".txt", ""))
                info = await bot.get_chat_member(message.chat.id, index)
                game_message += "%d. [%s](tg://user?id=%d) - ⚡ %d очков.\n" % (count, info.user.first_name, index, score)
                count += 1

        return await bot.send_message(message.chat.id, game_message, parse_mode="Markdown")   

    except Exception as e:
        pass 

def parse_words(chat_id, word):
    try:
        desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

        url = 'http://sinonim.org/as/%s' % word
        response = requests.get(url, headers={'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})
        soup = BeautifulSoup(response.text, 'lxml')
        sections = soup.find_all('ul', class_="assocPodryad")
        cases = soup.find_all('li')

        with open("chats/" + str(chat_id) + "/parse.txt", "+w") as parse:
            for item in cases:
                text = item.get_text()
                if "." not in text:
                    parse.write(text + ",")

    except Exception as e:
        pass

# Command: Leave
@dp.message_handler(commands=['leave'])
async def leave_command(message: types.Message):
    try:
        if os.path.isfile(os.getcwd() + "/users/" + str(message.from_user.id) + ".txt"):
            with open(os.getcwd() + "/users/" + str(message.from_user.id) + ".txt") as player:
                chat = int(player.read())

            os.remove(os.getcwd() + "/users/" + str(message.from_user.id) + ".txt")

            if os.path.isfile(os.getcwd() + "/chats/" + str(chat) + "/info.txt"):
                with open(os.getcwd() + "/chats/" + str(chat) + "/info.txt") as game:
                    game_result = game.read().split("|")

                if "MAFIA" == game_result[0]:
                    await leave_from_mafia(chat, message.from_user.id)

        return await bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass

async def leave_from_mafia(chat, user):
    try:
        with open(os.getcwd() + "/" + str(chat) + "/info.txt") as game:
            game_result = game.read().split("|")

        if "REGISTER" == game_result[1]:
            os.remove(os.getcwd() + "/chats/" + str(chat) + "/mafia/" + str(user) + ".txt")

            game_message = "🍍 *Мафия*\n\nУчастники:\n"
            players = os.listdir(os.getcwd() + "/chats/" + str(chat) + "/mafia")
            count = 0
            for temp in players:
                try:
                    index = int(temp.replace(".txt", ""))
                    info = await bot.get_chat_member(chat, index)

                    game_message += "[%s](tg://user?id=%d)\n" % (info.user.first_name, index)
                    count += 1
                except Exception as e:
                    os.remove(os.getcwd() + "/chats/" + str(chat) + "/mafia/" + temp)
                    os.remove(os.getcwd() + "/users/" + temp)

            buttons  = [types.InlineKeyboardButton(text='Присоединиться 🤵', callback_data="Мафия")] 
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            game_message += "\nИтого *%d* чел." % count
            if count == 0:
                game_message = "🍍 *Мафия*\n\nИдёт набор участников"
            await bot.edit_message_text(chat_id=chat, message_id=int(game_result[2]), text=game_message, parse_mode="Markdown",reply_markup=keyboard)
        else:
            with open(os.getcwd() + "/chats/" + str(chat) + "/mafia/" + str(user) + ".txt") as player:
                get = player.read().split("|")

                with open(os.getcwd() + "/chats/" + str(chat) + "/mafia/" + str(user) + ".txt", "+w") as killed:
                    killed.write("%s|0|0|%s" % (get[0], get[3]))

                message_to_die = [
                "💀 [%s](tg://user?id=%d) повесился в комнате..",
                "💀 [%s](tg://user?id=%d) спрыгнул(-а) с восьмого этажа..",
                "💀 [%s](tg://user?id=%d) застрелился..",
                "💀 [%s](tg://user?id=%d) выпил таблетки для суицида.."]

                await bot.send_message(chat, choice(message_to_die) % (get[3],user), parse_mode="Markdown")
                await progress_to_win_mafia(chat)
        
        await bot.send_message(user, "🍍 Вы покинули игру")
    except Exception as e:
        pass

# Types: dice
@dp.message_handler(content_types=["dice"])
async def dice_message(message):
    if is_game_in_chat(message.chat.id) and message.chat.id != message.from_user.id:
        if not await is_admin_group(message.chat.id, bot.id):
            return message.answer("🍍 *В чате уже идёт игра!*", parse_mode="Markdown")
        return await bot.delete_message(message.chat.id, message.message_id)

    if message.dice.emoji == "🏀" and message.dice.value > 3:
        await asyncio.sleep(4)
        success = ["Шикарный бросок!", "Великолепный бросок!", "Отличный бросок!", "Хороший бросок!", "Здорово попадаешь!", "Что-же, ты молодец!", "Ух ты, красава!"]
        return await message.reply("🍍 *%s*" % choice(success), parse_mode="Markdown")
    
    if message.dice.emoji == "🎲":
        await asyncio.sleep(5)
        return await message.reply("🍍 *Кубик\nВыпало: %d*" % (message.dice.value), parse_mode="Markdown")

    if message.dice.emoji == "🎯":
        await asyncio.sleep(3)
        if message.dice.value == 6:
            return await message.reply("🍍 *Ух ты, прямо в яблочке*", parse_mode="Markdown")

        if message.dice.value == 5:
            return await message.reply("🍍 *Нуу почти в яблочко*", parse_mode="Markdown")

        if message.dice.value == 4:
            return await message.reply("🍍 *Было близко..*", parse_mode="Markdown")

        if message.dice.value == 3 or message.dice.value == 2:
            return await message.reply("🍍 *Старайся лучше..*", parse_mode="Markdown")

        else: 
            return await message.reply("🍍 *Для приличия, мог(-ла) бы и попасть..*", parse_mode="Markdown")

    if message.dice.emoji == "⚽" and message.dice.value >= 3:
        await asyncio.sleep(4)
        success = ["Шикарный удар!", "Великолепный удар!", "Отличный удар!", "Хороший удар!", "Здорово попадаешь!", "Ты как роналду!", "Хороший удар, 'месси'.."]
        return await message.reply("🍍 *%s*" % choice(success), parse_mode="Markdown")

    if message.dice.emoji == "🎳":
        await asyncio.sleep(3)
        if message.dice.value == 6:
            return await message.reply("🍍 *Боулинг\nСтрайк! Отличный бросок*", parse_mode="Markdown")

        elif message.dice.value == 1:
            return await message.reply("🍍 *Боулинг\nЧто-же можно и попасть*..", parse_mode="Markdown")

        else:
            return await message.reply("🍍 *Боулинг\nПочти страйк:)*", parse_mode="Markdown")

# Types: text
@dp.message_handler(content_types=["text"])
async def check_all_messages(message):
    try:
        with open(os.getcwd() + "/info/bad_words.txt", encoding="utf8") as bad_words:
            text = bad_words.read().split(" ")

        for temp in text:
            if temp in message.text.lower():
                if await is_admin_group(message.chat.id, bot.id):
                    return await bot.delete_message(message.chat.id, message.message_id)
                return await message.reply("🤬 Попрошу не выражаться!")

        if message.chat.id == message.from_user.id:
            if os.path.isfile(os.getcwd() + "/users/" + str(message.from_user.id) + ".txt"):
                with open(os.getcwd() + "/users/" + str(message.from_user.id) + ".txt") as player:
                    chat = player.read()

                if os.path.isfile(os.getcwd() + "/chats/" + chat + "/info.txt"):
                    with open(os.getcwd() + "/chats/" + chat + "/info.txt") as game:
                        info = game.read().split("|")

                    if int(info[2]) == message.from_user.id and info[1] == "NEED_WORD":
                        if "|" in message.text:
                            return await message.reply("🍍 *Шарада*\nСлово должно быть без символов!", parse_mode="Markdown")
                        with open(os.getcwd() + "/chats/" + chat + "/info.txt", "+w") as game:
                            game.write("%s|%s|%s|%s|0" % (info[0],message.text,info[2],info[3]))

                        await bot.send_message(int(chat), "🍍 *Шарада*\nСлово было загадано!\nЗадавайте вопросы чтобы разгадать слово!\n\n⌛ Время игры: *5 минут*", parse_mode="Markdown")
                        await message.reply("🍍 *Шарада*\nОтличное слово!\nИгра начинается!", parse_mode="Markdown")
                        await asyncio.sleep(120)
                        if os.path.isfile(os.getcwd() + "/chats/" + chat + "/info.txt"):
                            with open(os.getcwd() + "/chats/" + chat + "/info.txt") as game:
                                records = game.read().split("|")
                            
                            if int(records[2]) == message.from_user.id and message.text == records[1]:
                                await bot.send_message(int(chat), "🍍 *Шарада*\n⌛ Осталось: *3 минуты*", parse_mode="Markdown")
                            else:
                                return True
                        await asyncio.sleep(120)
                        if os.path.isfile(os.getcwd() + "/chats/" + chat + "/info.txt"):
                            with open(os.getcwd() + "/chats/" + chat + "/info.txt") as game:
                                records = game.read().split("|")
                            
                            if int(records[2]) == message.from_user.id and message.text == records[1]:
                                await bot.send_message(int(chat), "🍍 *Шарада*\n⌛ Осталось: *1 минута*", parse_mode="Markdown")
                            else:
                                return True
                        await asyncio.sleep(60)
                        if os.path.isfile(os.getcwd() + "/chats/" + chat + "/info.txt"):
                            with open(os.getcwd() + "/chats/" + chat + "/info.txt") as game:
                                records = game.read().split("|")
                            
                            if int(records[2]) == message.from_user.id and message.text == records[1]:
                                await bot.send_message(int(chat), "🍍 *Шарада*\n⌛ Время истекло!\n\nЗагаданное слово: %s" % message.text.upper(), parse_mode="Markdown")
                            else:
                                return True

        if not is_game_in_chat(message.chat.id) and message.chat.id != message.from_user.id:
            return True

        with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt") as game:
            game_text = game.read()

        if "CHARADE" in game_text:
            info = game_text.split("|")
            if int(info[2]) == message.from_user.id and message.text.lower() in info[1].lower():
                return await bot.delete_message(message.chat.id, message.message_id)

            if int(info[2]) == message.from_user.id:
                return True

            if info[1].lower() in message.text.lower() and int(info[2]) != message.from_user.id:
                await message.reply("🍍 *Шарада*\n*Игра закончена!*\n\nМолодец! Слово было отгадано", parse_mode="Markdown")
                players = os.listdir(os.getcwd() + "/chats/" + str(message.chat.id) + "/charade")
                os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt")
                for temp in players:
                    os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/charade/" + temp)
                    os.remove(os.getcwd() + "/users/" + temp)
                return True

            buttons = [types.InlineKeyboardButton(text='Да', callback_data="Верным"), types.InlineKeyboardButton(text='Нет', callback_data="Не верным"), types.InlineKeyboardButton(text='Наверное', callback_data="Возможным")] 
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            await message.reply("🍍 *Шарада*\nВерно ли утверждение?", parse_mode="Markdown", reply_markup=keyboard)

        if "CITIES" in game_text:
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(message.text)
            status = observation.weather
            city = message.text.upper() 
            first_letter = city[:1]
            last_letter = city.replace(city[:-1], "")

            FIND = False
            for temp in letters:
                if temp == last_letter:
                    FIND = True
                    break

            if not FIND:
                last_letter = city.replace(city[:len(city) - 2], "").replace(last_letter, "")

            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt") as game:
                records = game.read().split("|")

            if int(records[2]) == message.from_user.id or first_letter != records[1]:
                return True

            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/cities.txt") as city:
                cities = city.read()

            result = cities.split(" ")
            for temp in result:
                if temp.lower() == message.text.lower():
                    return await message.reply("🍍 *Города*\n\nЭтот город уже был!", parse_mode="Markdown")

            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/cities.txt", "+w") as city:
                city.write(cities + message.text + " ")

            with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt", "+w") as game:
                game.write("CITIES|%s|%d|%d" % (last_letter, message.from_user.id, int(records[3]) + 1))

            await message.reply("🍍 *Города*\nГород *%s* засчитано\n\n📌 Напишите город на букву - *%s*\n⌛ Ход: *60 секунд*" % (message.text, last_letter), parse_mode="Markdown")
            await asyncio.sleep(60)
            if os.path.isfile(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt"):
                with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt") as game:
                    record = game.read().split("|")

                if int(record[2]) == message.from_user.id and int(record[3]) == int(records[3]) + 1:
                    os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/info.txt")
                    os.remove(os.getcwd() + "/chats/" + str(message.chat.id) + "/cities.txt")
                    try:
                        info = await bot.get_chat_member(message.chat.id, message.from_user.id)
                        return await message.answer("🍍 *Города*\nИгра закончена!\n\nПобедитель:\n[%s](tg://user?id=%d) - 👑" % (info.user.first_name, message.from_user.id), parse_mode="Markdown")
                    except Exception as e:
                        return await message.answer("🍍 *Города*\nИгра закончена!\n\nБольше никто не написал город", parse_mode="Markdown")
        if "Night" in game_text:
            return await bot.delete_message(message.chat.id, message.message_id)
        if "ASSOCIATIONS" in game_text:

            with open("chats/" + str(message.chat.id) + "/parse.txt") as parse:
                text = parse.read()

            text_split = text.split(",")
            FIND = False

            for item in text_split:
                if message.text.lower() == item:
                    FIND = True
                    break

            if FIND is True:

                with open("chats/" + str(message.chat.id) + "/parse.txt", "+w") as parse:
                    parse.write(text.replace(message.text.lower() + ",", ""))

                await message.reply("🍍 *Ассоциации*\n\nСлово *%s* засчитано\n⚡ *+%d очков*" % (message.text, len(message.text) / 2), parse_mode="Markdown")  
                if os.path.isfile(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations/" + str(message.from_user.id) + ".txt"):
                    with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations/" + str(message.from_user.id) + ".txt") as player:
                        score = int(player.read())

                    with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations/" + str(message.from_user.id) + ".txt" , "+w") as player:
                        player.write(str(score + int(len(message.text) / 2)))
                else:
                    with open(os.getcwd() + "/chats/" + str(message.chat.id) + "/associations/" + str(message.from_user.id) + ".txt" , "+w") as player:
                        player.write(str(int(len(message.text) / 2)))
    except Exception as e:
        print(repr(e))

# Types: callback keyboard
@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    try:
        code = callback_query.data
        if code == "Верным" or code == "Не верным" or code == "Возможным":

            if os.path.isfile(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/info.txt"):
                with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/info.txt") as game:
                    info = game.read().split("|")

                if int(info[2]) == callback_query.from_user.id:
                    return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="🍍 *Шарада*\n[%s](tg://user?id=%d) считает утверждение - *%s*" % (callback_query.from_user.first_name,callback_query.from_user.id,code), parse_mode="Markdown")

        elif code == "Игры":

            message = "🍍 *Игры в группе:*\n/crosses - Игра крестики-нолики\n/associations - Игра в ассоциации\n/mafia - Игра мафия\n/cities - Игра в Города\n/hand - Камень-Ножницы-Бумага\n/charade - Игра в шараду\n\n🍍 *Остальное:*\n/fanta - Игра для 'культурной' посиделки 🔞\n/coinflip - Подбросить монету\n\n🍍 *Стикеры:*\n🏀 - Подбросить мяч\n🎲 - Подбросить кость\n🎯 - Дартс\n⚽ - Пнуть мяч\n🎳 - Кинуть шар"
            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message, parse_mode="Markdown",reply_markup=None)
        
        elif code == "Помощь":

            message = "🍍 *Помощь*\n\nВ случае возникновения технической проблемы\nОбратитесь в техническую поддержку\n\n📌 Используйте: */bag [Текст]*"
            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message, parse_mode="Markdown",reply_markup=None)

        elif code == "Шарада":

            if os.path.isfile(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt"):
                with open(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt") as player:
                    info = player.read()

                    if info == str(callback_query.message.chat.id):
                        return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Вы уже учавствуете в этой игре!", show_alert=True)
                
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Вы уже учавствуете в другой игре!", show_alert=True)
            else:
                try:
                    await bot.send_message(callback_query.from_user.id, "🍍 *Шарада*\nВы присоединились к игре *%s*" % callback_query.message.chat.full_name, parse_mode="Markdown")
                except Exception as e:
                    return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Начните диалог со мной, чтобы все отлично работало!", show_alert=True)

                with open(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt", "+w") as player:
                    player.write(str(callback_query.message.chat.id))

                game_message = "🍍 *Шарада*\n\nУчастники:\n"
                with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/charade/" + str(callback_query.from_user.id) + ".txt", "+w") as player:
                    player.close()

                players = os.listdir(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/charade")
                count = 0
                for temp in players:
                    try:
                        index = int(temp.replace(".txt", ""))
                        info = await bot.get_chat_member(callback_query.message.chat.id, index)

                        game_message += "[%s](tg://user?id=%d)\n" % (info.user.first_name, index)
                        count += 1
                    except Exception as e:
                        os.remove(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/charade/" + temp)
            
            buttons  = [types.InlineKeyboardButton(text='Присоединиться', callback_data="Шарада")] 
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            game_message += "\nИтого *%d* чел." % count
            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=game_message, parse_mode="Markdown",reply_markup=keyboard)

        elif code == "Мафия":
            if os.path.isfile(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt"):
                with open(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt") as player:
                    info = player.read()

                    if info == str(callback_query.message.chat.id):
                        return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Вы уже учавствуете в этой игре!", show_alert=True)
                
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Вы уже учавствуете в другой игре!", show_alert=True)
            else:
                try:
                    await bot.send_message(callback_query.from_user.id, "🍍 *Мафия*\nВы присоединились к игре *%s*" % callback_query.message.chat.full_name, parse_mode="Markdown")
                except Exception as e:
                    return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Начните диалог со мной, чтобы все отлично работало!", show_alert=True)

                with open(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt", "+w") as player:
                    player.write(str(callback_query.message.chat.id))

                game_message = "🍍 *Мафия*\n\nУчастники:\n"
                with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/mafia/" + str(callback_query.from_user.id) + ".txt", "+w") as player:
                    player.close()

                players = os.listdir(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/mafia")
                count = 0
                for temp in players:
                    try:
                        index = int(temp.replace(".txt", ""))
                        info = await bot.get_chat_member(callback_query.message.chat.id, index)

                        game_message += "[%s](tg://user?id=%d)\n" % (info.user.first_name, index)
                        count += 1
                    except Exception as e:
                        os.remove(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/mafia/" + temp)
            
            buttons  = [types.InlineKeyboardButton(text='Присоединиться 🤵', callback_data="Мафия")] 
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            game_message += "\nИтого *%d* чел." % count
            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=game_message, parse_mode="Markdown",reply_markup=keyboard)

        elif code == "Рука":

            if callback_query.from_user.id == callback_query.message.reply_to_message.from_user.id:
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Это ваш вызов...", show_alert=True)

            with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/hand/" + str(callback_query.message.message_id) + ".txt", "w+") as game:
                game.write("%d|%s|%d|%s|None|None" % (callback_query.message.reply_to_message.from_user.id, callback_query.message.reply_to_message.from_user.first_name, callback_query.from_user.id, callback_query.from_user.first_name))

            buttons = [types.InlineKeyboardButton(text="Камень", callback_data="Камень"),types.InlineKeyboardButton(text="Ножницы", callback_data="Ножницы"),types.InlineKeyboardButton(text="Бумага", callback_data="Бумага")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            game_message = "🍍 *Вызов принят..*\n\nУчастники:\n1️⃣ [%s](tg://user?id=%d)\n2️⃣ [%s](tg://user?id=%d)\n\n⌛ Ход: *60 секунд*" % (callback_query.from_user.first_name, callback_query.from_user.id, callback_query.message.reply_to_message.from_user.first_name, callback_query.message.reply_to_message.from_user.id)
            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=game_message, parse_mode="Markdown",reply_markup=keyboard)
        elif code == "Камень" or code == "Ножницы" or code =="Бумага":

            if not os.path.isfile(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/hand/" + str(callback_query.message.message_id) + ".txt"):
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Произошла ошибка!", show_alert=True)

            with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/hand/" + str(callback_query.message.message_id) + ".txt") as game:
                result = game.read().split("|")

            if int(result[0]) != callback_query.from_user.id and int(result[2]) != callback_query.from_user.id:
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Вы не можете ходить", show_alert=True)

            buttons = [types.InlineKeyboardButton(text="Камень", callback_data="Камень"),types.InlineKeyboardButton(text="Ножницы", callback_data="Ножницы"),types.InlineKeyboardButton(text="Бумага", callback_data="Бумага")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            if int(result[0]) == callback_query.from_user.id and result[4] == "None":
                result[4] = code
            elif int(result[2]) == callback_query.from_user.id and result[5] == "None":
                result[5] = code

            with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/hand/" + str(callback_query.message.message_id) + ".txt", "w+") as game:
                game.write("%s|%s|%s|%s|%s|%s" % (result[0], result[1], result[2], result[3], result[4], result[5]))
            
            game_message = "🍍 *Вызов принят..*\n\nУчастники:\n1️⃣ [%s](tg://user?id=%d)\n2️⃣ [%s](tg://user?id=%d)\n\n⌛ Ход: *60 секунд*\n▶ [%s](tg://user?id=%d) - сделал(-а) ход" % (result[1], int(result[0]), result[3], int(result[2]), callback_query.from_user.first_name, callback_query.from_user.id)
            if result[4] != "None" and result[5] != "None":
                os.remove(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/hand/" + str(callback_query.message.message_id) + ".txt")
                keyboard = None
                if result[4] == result[5]:
                    game_message = "🍍 *Ничья*\n\nУчастники:\n1️⃣ [%s](tg://user?id=%d) - %s\n2️⃣ [%s](tg://user?id=%d) - %s" % (result[1], int(result[0]), result[4], result[3], int(result[2]), result[5])
                elif result[4] == "Камень" and result[5] == "Ножницы" or result[4] == "Бумага" and result[5] == "Камень" or result[4] == "Ножницы" and result[5] == "Бумага":
                    game_message = "🍍 *Игра окончена!*\n\nУчастники:\n1️⃣ [%s](tg://user?id=%d) - %s\n2️⃣ [%s](tg://user?id=%d) - %s\n\n*Победитель:*\n[%s](tg://user?id=%d) - 👑" % (result[1], int(result[0]), result[4], result[3], int(result[2]), result[5], result[1], int(result[0]))
                elif result[5] == "Камень" and result[4] == "Ножницы" or result[5] == "Бумага" and result[4] == "Камень" or result[5] == "Ножницы" and result[4] == "Бумага":
                    game_message = "🍍 *Игра окончена!*\n\nУчастники:\n1️⃣ [%s](tg://user?id=%d) - %s\n2️⃣ [%s](tg://user?id=%d) - %s\n\n*Победитель:*\n[%s](tg://user?id=%d) - 👑" % (result[1], int(result[0]), result[4], result[3], int(result[2]), result[5], result[3], int(result[2]))

            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=game_message, parse_mode="Markdown",reply_markup=keyboard)

        elif code == "Крестики-нолики":

            if callback_query.from_user.id == callback_query.message.reply_to_message.from_user.id:
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Вы являетесь участником этой игры...", show_alert=True)

            buttons = [types.InlineKeyboardButton(text="⏺", callback_data="1"),types.InlineKeyboardButton(text="⏺", callback_data="2"),types.InlineKeyboardButton(text="⏺", callback_data="3"),
            types.InlineKeyboardButton(text="⏺", callback_data="4"),types.InlineKeyboardButton(text="⏺", callback_data="5"),types.InlineKeyboardButton(text="⏺", callback_data="6"),
            types.InlineKeyboardButton(text="⏺", callback_data="7"),types.InlineKeyboardButton(text="⏺", callback_data="8"),types.InlineKeyboardButton(text="⏺", callback_data="9")]
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            message = "🍍 Игра началась!\n⌛ На ход: *60 секунд*\n\n❌ [%s](tg://user?id=%d) ходит крестиками\n⭕ [%s](tg://user?id=%d) ходит ноликами\n\nПервым ходит: [%s](tg://user?id=%d) ❌" % (callback_query.message.reply_to_message.from_user.first_name, callback_query.message.reply_to_message.from_user.id, callback_query.from_user.first_name, callback_query.from_user.id, callback_query.message.reply_to_message.from_user.first_name, callback_query.message.reply_to_message.from_user.id)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message, parse_mode="Markdown",reply_markup=keyboard)
    
            with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt", "w+") as game:
                game.write("%d|%s|%d|%s|CROSS|1|0|0|0|0|0|0|0|0|0" % (callback_query.message.reply_to_message.from_user.id, callback_query.message.reply_to_message.from_user.first_name, callback_query.from_user.id, callback_query.from_user.first_name))

            await asyncio.sleep(60)
            if os.path.isfile(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt"):
                with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt") as game:
                    game_split = game.read().split("|")

                if int(game_split[5]) == 1:
                    message = "🍍 *Игра закончилась!*\n\nУчастники:\n❌ [%s](tg://user?id=%d) - Не сделал(-а) ход\n⭕ [%s](tg://user?id=%d)" % (callback_query.message.reply_to_message.from_user.first_name, callback_query.message.reply_to_message.from_user.id, callback_query.from_user.first_name, callback_query.from_user.id)
                    return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message, parse_mode="Markdown",reply_markup=None)

        elif code == "1" or code == "2" or code == "3" or code == "4" or code == "5" or code == "6" or code == "7" or code == "8" or code == "9":
            if os.path.isfile(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt"):                 
                with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt") as game:
                    game_info = game.read().split("|")

                if (callback_query.from_user.id == int(game_info[0]) and game_info[4] == "CROSS") or (callback_query.from_user.id == int(game_info[2]) and game_info[4] == "ZERO"):
                    # Variables
                    position = int(code) - 1
                    keyboard_text = ["⏺","⏺","⏺","⏺","⏺","⏺","⏺","⏺","⏺"]
                    callback_post = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    crosses_position = []
                    game_message = ""
                    write_to_txt = ""

                    for i in range(9):
                        crosses_position.append(int(game_info[i+6]))

                    if callback_query.from_user.id == int(game_info[0]) and game_info[4] == "CROSS":
                        game_message = "🍍 Игра началась!\n⌛ На ход: *60 секунд*\n\n❌ [%s](tg://user?id=%s) ходит крестиками\n⭕ [%s](tg://user?id=%s) ходит ноликами\n\nСейчас ходит: [%s](tg://user?id=%s) ⭕" % (game_info[1], game_info[0], game_info[3], game_info[2], game_info[3], game_info[2])
                        crosses_position[position] = 2
                        write_to_txt = "%s|%s|%s|%s|ZERO|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d" % (game_info[0], game_info[1], game_info[2], game_info[3], int(game_info[5]) + 1, crosses_position[0],crosses_position[1],crosses_position[2],crosses_position[3],crosses_position[4],crosses_position[5],crosses_position[6],crosses_position[7],crosses_position[8])
                    else:
                        game_message = "🍍 Игра началась!\n⌛ На ход: *60 секунд*\n\n❌ [%s](tg://user?id=%s) ходит крестиками\n⭕ [%s](tg://user?id=%s) ходит ноликами\n\nСейчас ходит: [%s](tg://user?id=%s) ❌" % (game_info[1], game_info[0], game_info[3], game_info[2], game_info[1], game_info[0])
                        crosses_position[position] = 3
                        write_to_txt = "%s|%s|%s|%s|CROSS|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d" % (game_info[0], game_info[1], game_info[2], game_info[3], int(game_info[5]) + 1, crosses_position[0],crosses_position[1],crosses_position[2],crosses_position[3],crosses_position[4],crosses_position[5],crosses_position[6],crosses_position[7],crosses_position[8])
                    
                    with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt", "w+") as game:
                        game.write(write_to_txt)

                    for i in range(9):
                        if crosses_position[i] == 2:
                            keyboard_text[i] = "❌"
                            callback_post[i] = "Выбрано"
                        elif crosses_position[i] == 3:
                            keyboard_text[i] = "⭕"
                            callback_post[i] = "Выбрано" 

                    buttons = [types.InlineKeyboardButton(text=keyboard_text[0], callback_data=callback_post[0]),types.InlineKeyboardButton(text=keyboard_text[1], callback_data=callback_post[1]),types.InlineKeyboardButton(text=keyboard_text[2], callback_data=callback_post[2]),
                    types.InlineKeyboardButton(text=keyboard_text[3], callback_data=callback_post[3]),types.InlineKeyboardButton(text=keyboard_text[4], callback_data=callback_post[4]),types.InlineKeyboardButton(text=keyboard_text[5], callback_data=callback_post[5]),
                    types.InlineKeyboardButton(text=keyboard_text[6], callback_data=callback_post[6]),types.InlineKeyboardButton(text=keyboard_text[7], callback_data=callback_post[7]),types.InlineKeyboardButton(text=keyboard_text[8], callback_data=callback_post[8])]
                    keyboard = types.InlineKeyboardMarkup(row_width=3)
                    keyboard.add(*buttons)

                    if progress_to_win_crosses(crosses_position) == 2:
                        game_message = "🍍 *Игра закончилась!*\n\n%s | %s | %s\n%s | %s | %s\n%s | %s | %s\n\nУчастники:\n❌ [%s](tg://user?id=%s) - 👑\n⭕ [%s](tg://user?id=%s)" % (keyboard_text[0],keyboard_text[1],keyboard_text[2],keyboard_text[3],keyboard_text[4],keyboard_text[5],keyboard_text[6],keyboard_text[7],keyboard_text[8],game_info[1], game_info[0], game_info[3], game_info[2])
                        keyboard = None
                    elif progress_to_win_crosses(crosses_position) == 3:
                        game_message = "🍍 *Игра закончилась!*\n\n%s | %s | %s\n%s | %s | %s\n%s | %s | %s\n\nУчастники:\n❌ [%s](tg://user?id=%s)\n⭕ [%s](tg://user?id=%s) - 👑" % (keyboard_text[0],keyboard_text[1],keyboard_text[2],keyboard_text[3],keyboard_text[4],keyboard_text[5],keyboard_text[6],keyboard_text[7],keyboard_text[8],game_info[1], game_info[0], game_info[3], game_info[2])
                        keyboard = None
                    elif progress_to_win_crosses(crosses_position) == 4:
                        game_message = "🍍 *Ничья!*\n\n%s | %s | %s\n%s | %s | %s\n%s | %s | %s\n\nУчастники:\n❌ [%s](tg://user?id=%s)\n⭕ [%s](tg://user?id=%s)" % (keyboard_text[0],keyboard_text[1],keyboard_text[2],keyboard_text[3],keyboard_text[4],keyboard_text[5],keyboard_text[6],keyboard_text[7],keyboard_text[8],game_info[1], game_info[0], game_info[3], game_info[2])
                        keyboard = None

                    if keyboard is None:
                        os.remove(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt")

                    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=game_message, parse_mode="Markdown",reply_markup=keyboard)
                    if keyboard is not None:
                        try:
                            await asyncio.sleep(60)
                            with open(os.getcwd() + "/chats/" + str(callback_query.message.chat.id) + "/crosses/" + str(callback_query.message.message_id) + ".txt") as game:
                                game_info_next = game.read().split("|")

                            if int(game_info_next[5]) == int(game_info[5]) + 1:
                                if game_info_next[4] == "CROSS":
                                    game_message = "🍍 *Игра закончилась!*\n\n%s | %s | %s\n%s | %s | %s\n%s | %s | %s\n\nУчастники:\n❌ [%s](tg://user?id=%s) - Не сделал(-а) ход\n⭕ [%s](tg://user?id=%s)" % (keyboard_text[0],keyboard_text[1],keyboard_text[2],keyboard_text[3],keyboard_text[4],keyboard_text[5],keyboard_text[6],keyboard_text[7],keyboard_text[8],game_info[1], game_info[0], game_info[3], game_info[2])
                                else:
                                    game_message = "🍍 *Игра закончилась!*\n\n%s | %s | %s\n%s | %s | %s\n%s | %s | %s\n\nУчастники:\n❌ [%s](tg://user?id=%s)\n⭕ [%s](tg://user?id=%s) - Не сделал(-а) ход" % (keyboard_text[0],keyboard_text[1],keyboard_text[2],keyboard_text[3],keyboard_text[4],keyboard_text[5],keyboard_text[6],keyboard_text[7],keyboard_text[8],game_info[1], game_info[0], game_info[3], game_info[2])
                                keyboard = None
                                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=game_message, parse_mode="Markdown",reply_markup=keyboard)
                        except FileNotFoundError:
                            return False

            else:
                return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Произошла ошибка!\nПопробуйте позже или создайте новую игру.", show_alert=True)
        elif code == "Выбрано":

            return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Позиция уже занята!", show_alert=True)

        elif code == "Дальше":

            buttons  = [types.InlineKeyboardButton(text='Дальше', callback_data="Дальше")] 
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            with open("info/fanta_message.txt", encoding="utf8") as fanta:
                mission = fanta.read().replace("\\n", "\n").split("|")

            select_mission = random.randint(0,len(mission)) - 1
            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="🍍 %s" % mission[select_mission], parse_mode="Markdown",reply_markup=keyboard)
        else:
            if callback_query.message.chat.id == callback_query.from_user.id:
                try:
                    callback_split = code.split("_")
                    chat = callback_split[0]
                    day = callback_split[1]
                    mode = callback_split[2]
                    msg = callback_split[3]
                    index = callback_split[4]

                    with open(os.getcwd() + "/users/" + str(callback_query.from_user.id) + ".txt") as player:
                        chat_user = player.read()

                    with open(os.getcwd() + "/chats/" + chat + "/info.txt") as game:
                        record = game.read().split("|")

                    if chat != chat_user or record[3] != msg or record[2] != day or record[1] != mode:
                        return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="🍍 *Выбрать уже нельзя!*", parse_mode="Markdown",reply_markup=None)

                    with open(os.getcwd() + "/chats/" + chat + "/mafia/" + str(callback_query.from_user.id) + ".txt") as player:
                        info = player.read().split("|")

                    with open(os.getcwd() + "/chats/" + chat + "/mafia/" + index + ".txt") as player:
                        result = player.read().split("|")

                    if int(result[1]) != 0:
                        with open(os.getcwd() + "/chats/" + chat + "/mafia/" + str(callback_query.from_user.id) + ".txt", "+w") as player:
                            player.write(info[0] + "|" + info[1] + "|" + index + "|" + info[3])

                        if mode == "Voiting":
                            return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="🍍 Вы проголосовали за _%s_" % result[3] , parse_mode="Markdown",reply_markup=None)
                        
                        if mode == "Night":
                            if int(info[0]) == 0:
                                return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="🤵 Вы выбрали _%s_" % result[3] , parse_mode="Markdown",reply_markup=None)
                            elif int(info[0]) == 1:
                                roles = ["*Мафия*", "*Коммисар*", "*Медик*", "*Снежана*", "*Мирный*"]
                                await bot.send_message(int(index), "👮‍♂️ Кто-то занялся вашим личным досье.")
                                return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="👮‍♂️ Вы проверили _%s_\nЕго роль: %s" % (result[3] , roles[int(result[0])]) , parse_mode="Markdown",reply_markup=None)
                            elif int(info[0]) == 2:
                                await bot.send_message(int(index), "👨‍⚕️ Доктор плотно занялся вашим здоровьем.")
                                return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="👨‍⚕️ Вы вылечили _%s_" % (result[3]) , parse_mode="Markdown",reply_markup=None)
                            elif int(info[0]) == 3:
                                await bot.send_message(int(index), "🤷 К вам зашла Снежана")
                                return await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="🤷 Вы провели ночь с _%s_" % (result[3]) , parse_mode="Markdown",reply_markup=None)    
                    return await bot.answer_callback_query(callback_query_id=callback_query.id, text="🍍 Видимо этот игрок без сознания..", show_alert=True)
                except:
                    return await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except Exception as e:
        print(repr(e)) 

if __name__ == "__main__":
    if not os.path.isdir("chats"):
            os.mkdir("chats")

    if not os.path.isdir("users"):
        os.mkdir("users")

    chats = os.listdir(os.getcwd() + "/chats")
    for temp in chats:
        try:
            file = os.getcwd() + "/chats/" + temp + "/info.txt"
            with open(os.getcwd() + "/chats/" + temp + "/info.txt") as game:
                result = game.read()

            if "MAFIA" in result:
                players = os.listdir(os.getcwd() + "/chats/" + temp + "/mafia")
                for item in players:
                    os.remove(os.getcwd() + "/chats/" + temp + "/mafia/" + item)
                    os.remove(os.getcwd() + "/users/" + item)

            if "ASSOCIATIONS" in result:
                players = os.listdir(os.getcwd() + "/chats/" + temp + "/associations")
                for item in players:
                    os.remove(os.getcwd() + "/chats/" + temp + "/associations/" + item)

            if "CITIES" in result:
                os.remove(os.getcwd() + "/chats/" + temp + "/cities.txt")

            os.remove(os.getcwd() + "/chats/" + temp + "/info.txt")
        except Exception as e:
            continue

    executor.start_polling(dp, skip_updates=True)