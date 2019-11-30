import telegram
from telegram.ext import Updater, CommandHandler, Filters
import sqlite3
import random

bot = telegram.Bot(token='[REDACTED TOKEN]')
updater = Updater(token='[REDACTED TOKEN]', use_context=True)
dispatcher = updater.dispatcher


# various connections to database to add the various points from @werewolfbot's end-game message
def connect_candy_corn(name, userid, candy_corn):
    connection = sqlite3.connect("test.db")
    check = connection.execute("SELECT ID FROM Player")
    check = check.fetchall()
    if (userid,) in check:
        current = connection.execute("SELECT CandyCorn FROM Player WHERE ID = ?", (userid,))
        entry = current.fetchall()
        connection.execute("UPDATE Player SET CandyCorn = ? WHERE ID = ?", (entry[0][0] + candy_corn, userid))
    else:
        connection.execute("INSERT INTO Player VALUES (?, ?, ?, ?, ?)", (name, userid, candy_corn, 0, 0))
        current = connection.execute("SELECT CandyCorn FROM Player WHERE ID = ?", (userid,))
        print(current.fetchall())
    connection.commit()
    connection.close()

def connect_damage(name, userid, win, alive):
    connection = sqlite3.connect("players.db")
    check = connection.execute("SELECT ID FROM Player")
    check = check.fetchall()
    if win and alive:
        damage = 10
    elif win:
        damage = 7
    elif alive:
        damage = 5
    else:
        damage = 3
    if (userid,) in check:
        current = connection.execute("SELECT Damage FROM Player WHERE ID = ?", (userid,))
        entry = current.fetchall()
        connection.execute("UPDATE Player SET Damage = ? WHERE ID = ?", (entry[0][0] + damage, userid))
    else:
        connection.execute("INSERT INTO Player VALUES (?, ?, ?, ?, ?)", (name, userid, 0, damage, 0))
        current = connection.execute("SELECT Damage FROM Player WHERE ID = ?", (userid,))
    connection.commit()
    connection.close()

def connect_rune_tag(name, userid, rune_tag):
    connection = sqlite3.connect("players.db")
    check = connection.execute("SELECT ID FROM Player")
    check = check.fetchall()
    if (userid,) in check:
        current = connection.execute("SELECT RuneTag FROM Player WHERE ID = ?", (userid,))
        entry = current.fetchall()
        connection.execute("UPDATE Player SET RuneTag = ? WHERE ID = ?", (entry[0][0] + rune_tag, userid))
    else:
        connection.execute("INSERT INTO Player VALUES (?, ?, ?, ?, ?)", (name, userid, 0, 0, rune_tag))
        current = connection.execute("SELECT RuneTag FROM Player WHERE ID = ?", (userid,))
        print(current.fetchall())
    connection.commit()
    connection.close()



# count the number of players who won in the game
def count(message):
    return message.split().count("Won")



# various readings of @werewolfbot's end-game messages to add various points to database
def candy_corn(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID]":
        og_game_message = update.message.reply_to_message.text_markdown
        if "Game Length:" in og_game_message:
            game_message = og_game_message.split("\n")[:-2]
            total_players = int(game_message[0].split(" ")[-1])
            win_players = count(og_game_message)
            game_message = game_message[1:]
            total_candy_corn = random.randrange(total_players * 3, total_players * 5)
            indiv_candy_corn = total_candy_corn // win_players
            for player in game_message:
                if "](tg://user?id=" not in player:
                    player = player.split(": ")
                    name = player[0]
                    if "Won" in player[1]:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Warning: The player, " + name + ", has no visible ID. Please inform @PlaceholderUsername to update this entry manually. \nCandy corn received: " + str(indiv_candy_corn))
                else:
                    player = player.split("](tg://user?id=")
                    name = player[0][1:]
                    userid, win = player[1].split(")")
                    if "Won" in win:
                        connect_candy_corn(name, int(userid), indiv_candy_corn)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Updated!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an end-game message.")
candy_corn_handler = CommandHandler('candy_corn', candy_corn, filters=Filters.reply)
dispatcher.add_handler(candy_corn_handler)

def damage(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID]":
        og_game_message = update.message.reply_to_message.text_markdown
        if "Game Length:" in og_game_message:
            game_message = og_game_message.split("\n")[:-2]
            game_message = game_message[1:]
            for player in game_message:
                if "](tg://user?id=" not in player:
                    player = player.split(": ")
                    name = player[0]
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Warning: The player, " + name + ", has no visible ID. Please inform @PlaceholderUsername to update this entry manually.")
                else:
                    player = player.split("](tg://user?id=")
                    name = player[0][1:]
                    userid, win = player[1].split(")")
                    if "Won" in win:
                        if "Alive" in win:
                            connect_damage(name, int(userid), True, True)
                        else:
                            connect_damage(name, int(userid), True, False)
                    else:
                        if "Alive" in win:
                            connect_damage(name, int(userid), False, True)
                        else:
                            connect_damage(name, int(userid), False, False)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Updated!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an end-game message.")
damage_handler = CommandHandler('damage', damage, filters=Filters.reply)
dispatcher.add_handler(damage_handler)

def rune_tag(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID]":
        og_game_message = update.message.reply_to_message.text_markdown
        if "Game Length:" in og_game_message:
            game_message = og_game_message.split("\n")[:-2]
            total_players = int(game_message[0].split(" ")[-1])
            win_players = count(og_game_message)
            game_message = game_message[1:]
            total_rune_tag = random.randrange(total_players * 3, total_players * 5)
            indiv_rune_tag = total_rune_tag // win_players
            for player in game_message:
                if "](tg://user?id=" not in player:
                    player = player.split(": ")
                    name = player[0]
                    if "Won" in player[1]:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Warning: The player, " + name + ", has no visible ID. Please inform @PlaceholderUsername to update this entry manually. \nRune tags received: " + str(indiv_rune_tag))
                else:
                    player = player.split("](tg://user?id=")
                    name = player[0][1:]
                    userid, win = player[1].split(")")
                    if "Won" in win:
                        connect_rune_tag(name, int(userid), indiv_rune_tag)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Updated!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an end-game message.")
rune_tag_handler = CommandHandler('rune_tag', rune_tag, filters=Filters.reply)
dispatcher.add_handler(rune_tag_handler)



# leaderboard for various scores
def candy_corn_scores(update, context):
    connection = sqlite3.connect("test.db")
    cursor_cc = connection.execute("SELECT Name, CandyCorn FROM Player ORDER BY CandyCorn DESC")
    top_10_cc = cursor_cc.fetchall()
    if len(top_10_cc) < 10:
        num = len(top_10_cc)
    else:
        num = 10
    result_cc = "*Top 10 candy corn collectors:*\n\n"
    for cc in range(num):
        result_cc += "*" + top_10_cc[cc][0] + "*" + ": " + str(top_10_cc[cc][1])+ "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=result_cc, parse_mode='Markdown')
candy_corn_scores_handler = CommandHandler('candy_corn_scores', candy_corn_scores)
dispatcher.add_handler(candy_corn_scores_handler)

def damage_scores(update, context):
    connection = sqlite3.connect("players.db")
    cursor = connection.execute("SELECT Name, Damage FROM Player ORDER BY Damage DESC")
    cursor_hp = connection.execute("SELECT HP FROM Monster")
    top_10 = cursor.fetchall()
    monster_hp = cursor_hp.fetchall()
    monster_hp = monster_hp[0][0]
    if len(top_10) < 10:
        num = len(top_10)
    else:
        num = 10
    result = "_Monster's health bar:_\n"
    total = 0
    for value in top_10:
        total += value[1]
    if total >= monster_hp:
        result += "░░░░░░░░░░\n\n"
    elif total >= monster_hp * 0.9:
        result += "█░░░░░░░░░\n\n"
    elif total >= monster_hp * 0.8:
        result += "██░░░░░░░░\n\n"
    elif total >= monster_hp * 0.7:
        result += "███░░░░░░░\n\n"
    elif total >= monster_hp * 0.6:
        result += "████░░░░░░\n\n"
    elif total >= monster_hp * 0.5:
        result += "█████░░░░░\n\n"
    elif total >= monster_hp * 0.4:
        result += "██████░░░░\n\n"
    elif total >= monster_hp * 0.3:
        result += "███████░░░\n\n"
    elif total >= monster_hp * 0.2:
        result += "████████░░\n\n"
    elif total >= monster_hp * 0.1:
        result += "█████████░\n\n"
    else:
        result += "██████████\n\n"
    result += "*Top 10 attackers:*\n\n"
    for value in range(num):
        result += "*" + str(value + 1) + ". " + top_10[value][0] + "*" + ": " + str(top_10[value][1])+ "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, parse_mode='Markdown')
damage_scores_handler = CommandHandler('damage_scores', damage_scores)
dispatcher.add_handler(damage_scores_handler)

def rune_tag_scores(update, context):
    connection = sqlite3.connect("players.db")
    cursor = connection.execute("SELECT Name, RuneTag FROM Player ORDER BY RuneTag DESC")
    top_10 = cursor.fetchall()
    if len(top_10) < 10:
        num = len(top_10)
    else:
        num = 10
    result = "_Rune tag collection progress:_\n"
    total = 0
    for value in top_10:
        total += value[1]
    print(total)
    if total < 100:
        result += "░░░░░░░░░░\n\n"
    elif total < 200:
        result += "█░░░░░░░░░\n\n"
    elif total < 300:
        result += "██░░░░░░░░\n\n"
    elif total < 400:
        result += "███░░░░░░░\n\n"
    elif total < 500:
        result += "████░░░░░░\n\n"
    elif total < 600:
        result += "█████░░░░░\n\n"
    elif total < 700:
        result += "██████░░░░\n\n"
    elif total < 800:
        result += "███████░░░\n\n"
    elif total < 900:
        result += "████████░░\n\n"
    elif total < 1000:
        result += "█████████░\n\n"
    else:
        result += "██████████\n_Completed!_\n\n"
    result += "*Top 10 rune tag collectors:*\n"
    for value in range(num):
        result += "*" + str(value + 1) + ". " + top_10[value][0] + "*" + ": " + str(top_10[value][1])+ "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, parse_mode='Markdown')
rune_tag_scores_handler = CommandHandler('rune_tag_scores', rune_tag_scores)
dispatcher.add_handler(rune_tag_scores_handler)



# find a player in the database and return the scores
def find(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID]":
        text = update.message.text
        text = text.split(" ")
        connection = sqlite3.connect("players.db")
        if len(text) == 2:
            cursor = connection.execute("SELECT Name, CandyCorn, Damage, RuneTag FROM Player WHERE ID = ?", (int(text[1]),))
            results = cursor.fetchall()
            if len(results) == 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text="User not in database.")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Name: " + results[0][0] + "\nCandy corn: " + str(results[0][1]) + "\nDamage: " + str(results[0][2]) + "\nRune tags: " + str(results[0][3]))
find_handler = CommandHandler('find', find)
dispatcher.add_handler(find_handler)



# add scores manually
def add_candy_corn(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID]":
        text = update.message.text
        text = text.split(" ")
        userid = int(text[-2])
        score = int(text[-1])
        name = " ".join(text[1:-2])
        connection = sqlite3.connect("players.db")
        connection.execute("INSERT INTO Player VALUES (?,?,?,?,?)", (name, userid, score, 0, 0))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Entry added!")
        connection.commit()
        connection.close()
add_candy_corn_handler = CommandHandler('add_candy_corn', add_candy_corn)
dispatcher.add_handler(add_candy_corn_handler)

def add_damage(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID]":
        text = update.message.text
        text = text.split(" ")
        userid = int(text[-2])
        score = int(text[-1])
        name = " ".join(text[1:-2])
        connection = sqlite3.connect("players.db")
        connection.execute("INSERT INTO Player VALUES (?,?,?,?,?)", (name, userid, 0, score, 0))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Entry added!")
        connection.commit()
        connection.close()
add_damage_handler = CommandHandler('add_damage', add_damage)
dispatcher.add_handler(add_damage_handler)

def add_rune_tag(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID (INTEGER)]":
        text = update.message.text
        text = text.split(" ")
        userid = int(text[-2])
        score = int(text[-1])
        name = " ".join(text[1:-2])
        connection = sqlite3.connect("players.db")
        connection.execute("INSERT INTO Player VALUES (?,?,?,?,?)", (name, userid, 0, 0, score))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Entry added!")
        connection.commit()
        connection.close()
add_handler = CommandHandler('add_rune_tag', add_rune_tag)
dispatcher.add_handler(add_handler)



# update scores manually
def update_candy_corn(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID (INTEGER)]":
        text = update.message.text
        text = text.split(" ")
        userid = int(text[-2])
        candy_corn = int(text[-1])
        connection = sqlite3.connect("players.db")
        current = connection.execute("SELECT CandyCorn FROM Player WHERE ID = ?", (userid,))
        entry = current.fetchall()
        connection.execute("UPDATE Player SET CandyCorn = ? WHERE ID = ?", (entry[0][0] + candy_corn, userid))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Entry updated!")
        connection.commit()
        connection.close()
update_candy_corn_handler = CommandHandler('update_candy_corn', update_candy_corn)
dispatcher.add_handler(update_candy_corn_handler)

def update_damage(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID (INTEGER)]":
        text = update.message.text
        text = text.split(" ")
        userid = int(text[-2])
        damage = int(text[-1])
        connection = sqlite3.connect("players.db")
        current = connection.execute("SELECT Damage FROM Player WHERE ID = ?", (userid,))
        entry = current.fetchall()
        connection.execute("UPDATE Player SET Damage = ? WHERE ID = ?", (entry[0][0] + damage, userid))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Entry updated!")
        connection.commit()
        connection.close()
update_damage_handler = CommandHandler('update_damage', update_damage)
dispatcher.add_handler(update_damage_handler)

def update_rune_tag(update, context):
    if update.message.chat.id == "[REDACTED CHAT ID (INTEGER)]":
        text = update.message.text
        text = text.split(" ")
        userid = int(text[-2])
        rune_tag = int(text[-1])
        connection = sqlite3.connect("players.db")
        current = connection.execute("SELECT RuneTag FROM Player WHERE ID = ?", (userid,))
        entry = current.fetchall()
        connection.execute("UPDATE Player SET RuneTag = ? WHERE ID = ?", (entry[0][0] + rune_tag, userid))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Entry updated!")
        connection.commit()
        connection.close()
update_rune_tag_handler = CommandHandler('update_rune_tag', update_rune_tag)
dispatcher.add_handler(update_rune_tag_handler)



# check the health of the monster or add/minus health points from the monster
def health(update, context):
    if update.message.chat.id == -1001211150863:
        text = update.message.text
        text = text.split(" ")
        connection = sqlite3.connect("players.db")
        if len(text) == 1:
            cursor = connection.execute("SELECT HP FROM Monster")
            cursor_player = connection.execute("SELECT Name, Damage FROM Player ORDER BY Damage DESC")
            players = cursor_player.fetchall()
            total = 0
            for value in players:
                total += value[1]
            hp = cursor.fetchall()
            hp = hp[0][0]
            context.bot.send_message(chat_id=update.effective_chat.id, text="Current HP: " + str(hp - total))
        else:
            cursor = connection.execute("SELECT HP FROM Monster")
            hp = cursor.fetchall()
            hp = hp[0][0]
            new_hp = hp + int(text[1])
            connection.execute("UPDATE Monster SET HP = ? WHERE HP = ?", (new_hp, hp))
            connection.commit()
            connection.close()
            context.bot.send_message(chat_id=update.effective_chat.id, text="HP updated!\n\nOld HP: " + str(hp) + "\nNew HP: " + str(new_hp))
health_handler = CommandHandler('health', health)
dispatcher.add_handler(health_handler)

updater.start_polling()
