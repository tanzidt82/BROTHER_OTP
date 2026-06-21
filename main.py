
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import requests
import time

# --- CONFIGURATION ---
BOT_TOKEN = "8604217157:AAGRJrxh6RDsX6SEOfK7O3u1AJCjpuYlJ-Q"
REQUIRED_CHANNEL = "@Brother_United_Team"
OWNER_CHAT_ID = 8503127840  # ржЖржкржирж┐ рж╣рж▓рзЗржи ржорзЗржЗржи ржУржирж╛рж░

# --- GITHUB GIST CONFIGURATION ---
GITHUB_TOKEN = "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"
GIST_ID = "6eafa1d07f00649e8139d926b39ed9ac"

bot = telebot.TeleBot(BOT_TOKEN)

# рж░рж┐ржпрж╝рзЗрж▓-ржЯрж╛ржЗржо ржбрж╛ржЯрж╛ ржЯрзНрж░рзНржпрж╛ржХрж┐ржВ ржбрж┐ржХрж╢ржирж╛рж░рж┐
user_data = {}
bot_db = {
    "saved_apk": None,  
    "user_limits": {},
    "admins": [OWNER_CHAT_ID]  # ржорзЗржЗржи ржУржирж╛рж░ ржбрж┐ржлрж▓рзНржЯ ржЕрзНржпрж╛ржбржорж┐ржи рж▓рж┐рж╕рзНржЯрзЗ ржерж╛ржХржмрзЗ
}

# --- SAFE GITHUB FUNCTIONS ---
def fetch_gist_content():
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    gist_url = f"https://api.github.com/gists/{GIST_ID}"
    try:
        res = requests.get(gist_url, headers=headers, timeout=15)
        if res.status_code == 200:
            gist_data = res.json()
            filename = list(gist_data['files'].keys())[0]
            content = gist_data['files'][filename]['content']
            return json.loads(content), filename
    except Exception as e:
        print(f"Error fetching gist: {e}")
    return [], None

def push_gist_content(filename, updated_list):
    if not filename: return False
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    gist_url = f"https://api.github.com/gists/{GIST_ID}"
    payload = {"files": {filename: {"content": json.dumps(updated_list, indent=4)}}}
    try:
        res = requests.patch(gist_url, headers=headers, json=payload, timeout=15)
        return res.status_code == 200
    except Exception as e:
        print(f"Error patching gist: {e}")
        return False

# --- CHANNEL JOIN CHECK ---
def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# --- DYNAMIC KEYBOARDS ---
def get_main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in bot_db["admins"]:
        markup.row(KeyboardButton("ЁЯФН Check Activation"), KeyboardButton("ЁЯУе Get Tools"))
        markup.row(KeyboardButton("ЁЯСитАНЁЯТ╗ Support"), KeyboardButton("ЁЯЫа Admin Panel"))
    else:
        markup.row(KeyboardButton("ЁЯФН Check Activation"), KeyboardButton("ЁЯУе Get Tools"))
        markup.row(KeyboardButton("ЁЯСитАНЁЯТ╗ Support"))
    return markup

def get_admin_menu(user_id):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("ЁЯСе See Users", callback_data="see_users"))
    markup.row(InlineKeyboardButton("ЁЯУж Add APK", callback_data="add_apk"), InlineKeyboardButton("тЭМ Delete APK", callback_data="delete_apk"))
    
    # рж╢рзБржзрзБржорж╛рждрзНрж░ ржорзЗржЗржи ржУржирж╛рж░ ржЕрзНржпрж╛ржбржорж┐ржи ржЕрзНржпрж╛ржб ржПржмржВ рж░рж┐ржорзЛржн ржХрж░рж╛рж░ ржмрж╛ржЯржи ржжрзЗржЦрждрзЗ ржкрж╛ржмрзЗ
    if user_id == OWNER_CHAT_ID:
        markup.row(InlineKeyboardButton("тЮХ Add Admin", callback_data="add_admin_flow"), InlineKeyboardButton("тЭМ Remove Admin", callback_data="remove_admin_flow"))
        
    markup.row(InlineKeyboardButton("ЁЯУЭ Edit Activation", url="https://gist.github.com/tanzidt82/6eafa1d07f00649e8139d926b39ed9ac"))
    return markup

def get_support_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("ЁЯСС Support Admin 1", url="https://t.me/info_as_tamim")) 
    markup.row(InlineKeyboardButton("ЁЯЫбя╕П Support Admin 2", url="https://t.me/Silent_Hasan69"))
    return markup

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    
    if is_user_joined(user_id):
        bot.send_message(user_id, "ЁЯдЦ <b>Welcome back to Activation Panel!</b>\nNicher button use korun:", parse_mode="HTML", reply_markup=get_main_menu(user_id))
    else:
        markup = InlineKeyboardMarkup()
        btn_join = InlineKeyboardButton("ЁЯУв Join Channel", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")
        btn_confirm = InlineKeyboardButton("тЬЕ Confirmed", callback_data="check_join_initial")
        markup.row(btn_join)
        markup.row(btn_confirm)
        
        welcome_msg = """ЁЯОЙ рж╕рзНржмрж╛ржЧрждржо! ржмржЯржЯрж┐ ржмрзНржпржмрж╣рж╛рж░ ржХрж░рж╛рж░ ржЬржирзНржп ржЖржкржирж╛ржХрзЗ ржкрзНрж░ржержорзЗ ржЖржорж╛ржжрзЗрж░ ржЪрзНржпрж╛ржирзЗрж▓рзЗ ржЬрзЯрзЗржи ржХрж░рждрзЗ рж╣ржмрзЗред ЁЯСЗ

ЁЯОЙ Welcome! To use this bot, you need to join our channel first. ЁЯСЗ"""
        bot.send_message(user_id, welcome_msg, reply_markup=markup)

# --- ADMIN PANEL COMMAND ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in bot_db["admins"]:
        bot.send_message(message.chat.id, "ЁЯЫа *Welcome to Admin Control Panel*\nSEE ADMIN FEATURES:", parse_mode="Markdown", reply_markup=get_admin_menu(message.from_user.id))

# --- TEXT HANDLER ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    text = message.text.strip()
    tg_username = message.from_user.username.lower() if message.from_user.username else str(user_id)

    # рж▓рж┐ржорж┐ржЯ рж╕рзЗржЯржЖржк рж░рзБрж▓
    if user_id in bot_db["admins"] and " /" in text:
        try:
            target_user, limit_val = text.split(" /")
            target_user = target_user.replace("@", "").strip().lower()
            bot_db["user_limits"][target_user] = int(limit_val)
            bot.send_message(user_id, f"тЬЕ Target User <b>@{target_user}</b> er total limit <b>{limit_val}</b> set kora hoyeche!", parse_mode="HTML")
            return
        except:
            bot.send_message(user_id, "тЭМ INVALID FORMET: <code>username /2</code>", parse_mode="HTML")
            return

    # ржЕрзНржпрж╛ржбржорж┐ржи ржкрзНржпрж╛ржирзЗрж▓ ржмрж╛ржЯржи ржХрзНрж▓рж┐ржХ рж╣рзНржпрж╛ржирзНржбрж▓рж╛рж░
    if text == "ЁЯЫа Admin Panel" and user_id in bot_db["admins"]:
        bot.send_message(user_id, "ЁЯЫа <b>Welcome to Admin Control Panel</b>\nSee admin features", parse_mode="HTML", reply_markup=get_admin_menu(user_id))
        return

    # рж╕рж╛ржкрзЛрж░рзНржЯ ржмрж╛ржЯржи ржХрзНрж▓рж┐ржХ рж╣рзНржпрж╛ржирзНржбрж▓рж╛рж░
    if text == "ЁЯСитАНЁЯТ╗ Support":
        bot.send_message(user_id, "ЁЯТм <b>Our Official Support Team</b>\n\nANY HELP TO CONTACT ADMIN SUPPORT:", parse_mode="HTML", reply_markup=get_support_menu())
        return

    if not is_user_joined(user_id):
        bot.send_message(user_id, "тЭМ Please join channel and try again! (/start type)")
        return

    if text == "ЁЯФН Check Activation":
        bot.send_message(user_id, "тП│ Checking database, please wait...")
        db_list, _ = fetch_gist_content()
        
        user_entries = [x for x in db_list if str(x.get("tg_username", "")).lower() == tg_username or str(x.get("tg_id", "")) == str(user_id)]
        allowed_limit = bot_db["user_limits"].get(tg_username, 1)

        if user_entries:
            last_entry = user_entries[-1]
            invoice_text = (
                f"ЁЯУЛ <b>Your Activation Profile</b>\n"
                f"тФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБ\n"
                f"ЁЯФС <b>Device key:</b> <code>{last_entry.get('Device Id')}</code>\n"
                f"ЁЯСд <b>USERNAME:</b> <code>{last_entry.get('username')}</code>\n"
                f"ЁЯФТ <b>PASSWORD:</b> <code>{last_entry.get('password')}</code>\n"
                f"ЁЯУК <b>STATUS:</b> ЁЯЯв Active\n"
                f"ЁЯУИ <b>Approved Count:</b> {len(user_entries)}/{allowed_limit}\n"
                f"тФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБ"
            )
            if len(user_entries) < allowed_limit:
                markup = InlineKeyboardMarkup()
                markup.row(InlineKeyboardButton("ЁЯОБ Get Another Activation", callback_data="get_activation"))
                bot.send_message(user_id, invoice_text + "\nЁЯТб <i>YOU HAVE MORE ACTIVATION SLOT</i>", parse_mode="HTML", reply_markup=markup)
            else:
                bot.send_message(user_id, invoice_text + "\nтЭМ <i>Apnar limit sesh! Aro slot pete Admin er sathe jogajog korun.</i>", parse_mode="HTML")
        else:
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton("ЁЯОБ Get Activation", callback_data="get_activation"))
            
            not_found_msg = """ЁЯФН ржжрзБржГржЦрж┐ржд! ржЖржкржирж╛рж░ ржХрзЛржирзЛ ржЕрзНржпрж╛ржХрзНржЯрж┐ржн рж╕рж╛ржмрж╕рзНржХрзНрж░рж┐ржкрж╢ржи ржЦрзБржБржЬрзЗ ржкрж╛ржУрзЯрж╛ ржпрж╛рзЯржирж┐ред

тЬи ржирждрзБржи ржХрж░рзЗ рж╕рж╛рж░рзНржнрж┐рж╕ржЯрж┐ ржЕрзНржпрж╛ржХрзНржЯрж┐ржнрзЗржЯ ржХрж░рждрзЗ ржЕржирзБржЧрзНрж░рж╣ ржХрж░рзЗ ржирж┐ржЪрзЗрж░ ржмрж╛ржЯржирзЗ ржХрзНрж▓рж┐ржХ ржХрж░рзБржи: ЁЯСЗ

ЁЯФН Sorry! No active subscription was found for your account.

тЬи To activate a new subscription, please click the button below: ЁЯСЗ:"""
            bot.send_message(user_id, not_found_msg, reply_markup=markup)

    elif text == "ЁЯУе Get Tools":
        if bot_db["saved_apk"]:
            try: bot.send_document(user_id, bot_db["saved_apk"], caption="ЁЯУж Here is your requested APK tool!")
            except: bot.send_message(user_id, "тЭМ APK рж╕рзЗржирзНржб ржХрж░рждрзЗ рж╕ржорж╕рзНржпрж╛ рж╣рзЯрзЗржЫрзЗред")
        else:
            bot.send_message(user_id, "тП│ The administrator has not uploaded the file yet.")

# --- CALLBACK QUERY HANDLER ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    
    if call.data == "check_join_initial":
        if is_user_joined(user_id):
            bot.answer_callback_query(call.id, "Dhonnobad! Registration confirm.")
            bot.send_message(user_id, "ЁЯдЦ Welcome! BROTHER UNITED TEAM ACTIVATION CENTER.", reply_markup=get_main_menu(user_id))
        else:
            bot.answer_callback_query(call.id, "тЭМ Please join channel and try again!", show_alert=True)
            
    elif call.data == "get_activation":
        bot.answer_callback_query(call.id)
        user_data[user_id] = {}
        msg = bot.send_message(user_id, "ЁЯФС <b>Please send your valid 16-digit Device Key:</b>\n(Example: <code>f467186806e88144</code>)", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_device_key)
        
    elif call.data == "see_users" and user_id in bot_db["admins"]:
        bot.answer_callback_query(call.id, "Loading users...")
        db_list, _ = fetch_gist_content()
        if not db_list:
            bot.send_message(user_id, "ЁЯУВ Database empty!")
            return
        report = "ЁЯСе <b>Approved Users List:</b>\n\n"
        counts = {}
        for x in db_list:
            uname = x.get('tg_username', 'Unknown')
            counts[uname] = counts.get(uname, 0) + 1
            
        seen = set()
        for x in db_list:
            uname = x.get('tg_username', 'Unknown')
            if uname in seen: continue
            seen.add(uname)
            report += f"ЁЯСд <b>TG:</b> @{uname}\nЁЯФС <b>Device:</b> <code>{x.get('Device Id')}</code>\nЁЯСд <b>Login User:</b> {x.get('username')}\nЁЯУК <b>Approved Count:</b> {counts[uname]}\nтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБ\n"
        bot.send_message(user_id, report, parse_mode="HTML")
        
    elif call.data == "add_apk" and user_id in bot_db["admins"]:
        bot.answer_callback_query(call.id)
        msg = bot.send_message(user_id, "ЁЯУБ Please upload/send the <b>.apk</b> file now:")
        bot.register_next_step_handler(msg, process_apk_upload)
        
    elif call.data == "delete_apk" and user_id in bot_db["admins"]:
        bot.answer_callback_query(call.id)
        bot_db["saved_apk"] = None
        bot.send_message(user_id, "тЭМ APK has been deleted successfully.")

    # ржЕрзНржпрж╛ржбржорж┐ржи ржпрзЛржЧ ржХрж░рж╛рж░ ржкрзНрж░рзЛрж╕рзЗрж╕ ржлрзНрж▓рзЛ (ржЕржирж▓рж┐ ржлрж░ ржорзЗржЗржи ржУржирж╛рж░)
    elif call.data == "add_admin_flow" and user_id == OWNER_CHAT_ID:
        bot.answer_callback_query(call.id)
        msg = bot.send_message(OWNER_CHAT_ID, "ЁЯЖФ <b>Please send the Telegram User ID of the new Admin:</b>\n(Example: <code>123456789</code>)", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_admin_addition)

    # ржЕрзНржпрж╛ржбржорж┐ржи рж░рж┐ржорзЛржн ржХрж░рж╛рж░ ржкрзНрж░рзЛрж╕рзЗрж╕ ржлрзНрж▓рзЛ (ржЕржирж▓рж┐ ржлрж░ ржорзЗржЗржи ржУржирж╛рж░)
    elif call.data == "remove_admin_flow" and user_id == OWNER_CHAT_ID:
        bot.answer_callback_query(call.id)
        msg = bot.send_message(OWNER_CHAT_ID, "тЭМ <b>Please send the Telegram User ID you want to REMOVE from Admin:</b>\n(Example: <code>123456789</code>)", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_admin_removal)

    elif call.data.startswith("approve_") or call.data.startswith("reject_"):
        action = call.data.split("_")[0]
        target_user_id = int(call.data.split("_")[1])
        target_data = user_data.get(target_user_id, {})
        
        if user_id in bot_db["admins"]:
            if action == "approve":
                status_text = "ЁЯЯв Active (Added to GitHub Gist)"
                user_msg = "ЁЯОЙ YOUR DEVICE KEY SUCCESFULLY <b>ACTIVATED</b> WAIT 5 MINIT TO LOGIN!"
                
                if 'device_id' in target_data:
                    new_entry = {
                        "Device Id": target_data['device_id'],
                        "username": target_data['username'],
                        "password": target_data['password'],
                        "expiry": "2026-12-31",
                        "tg_username": target_data['tg_username'],
                        "tg_id": target_user_id
                    }
                    bot.send_message(user_id, "тП│ Updating database, please hold...")
                    db_list, filename = fetch_gist_content()
                    db_list.append(new_entry)
                    if push_gist_content(filename, db_list):
                        raw_url = f"https://gist.githubusercontent.com/tanzidt82/{GIST_ID}/raw/"
                        bot.send_message(user_id, f"ЁЯУв <b>GitHub Database Updated!</b>\nRaw URL: <code>{raw_url}</code>", parse_mode="HTML")
                    else:
                        status_text = "тЭМ Gist Update Failed"
            else:
                status_text = "ЁЯФ┤ Deactivated"
                user_msg = "тЭМ YOUR DEVICE REQUEST <b>REJECTED</b> PLEASE CONTACT SUPPORT ЁЯУ▓!"
                
            try: bot.send_message(target_user_id, user_msg, parse_mode="HTML")
            except: pass
            
            try:
                original_text = call.message.text
                bot.edit_message_text(f"{original_text}\n\n<b>Decision:</b> {status_text}\n<b>By Admin ID:</b> {user_id}", chat_id=user_id, message_id=call.message.message_id, parse_mode="HTML")
            except Exception as e:
                print(f"Admin menu edit error: {e}")
            bot.answer_callback_query(call.id)

# --- NEW ADMIN ADDITION PROCESS ---
def process_admin_addition(message):
    if message.text and message.text.isdigit():
        new_admin_id = int(message.text.strip())
        if new_admin_id not in bot_db["admins"]:
            bot_db["admins"].append(new_admin_id)
            bot.send_message(OWNER_CHAT_ID, f"тЬЕ <b>Success!</b> User ID <code>{new_admin_id}</code> is now added as an Admin.\nSei user ekhon <code>/start</code> dile Admin Panel dekhte pabe.", parse_mode="HTML")
            
            try:
                bot.send_message(new_admin_id, "ЁЯОЙ <b>CONGRATULATION!</b> ADMIN WAS ADDED TO SUB ADMIN CHECK <code>/start</code> TYPE.", parse_mode="HTML")
            except:
                pass
        else:
            bot.send_message(OWNER_CHAT_ID, "тЪая╕П ржПржЗ ржЗржЙржЬрж╛рж░ ржЖржЗржбрж┐ ржЕрж▓рж░рзЗржбрж┐ ржЕрзНржпрж╛ржбржорж┐ржи рж▓рж┐рж╕рзНржЯрзЗ ржЖржЫрзЗред")
    else:
        bot.send_message(OWNER_CHAT_ID, "тЭМ ржнрзБрж▓ ржлрж░ржорзНржпрж╛ржЯ! ржЕрзНржпрж╛ржбржорж┐ржи ржХрж░рж╛рж░ ржЬржирзНржп рж╢рзБржзрзБржорж╛рждрзНрж░ рж╕ржВржЦрзНржпрж╛рж░ ржЯрзЗрж▓рж┐ржЧрзНрж░рж╛ржо ржЖржЗржбрж┐ (Numeric ID) ржкрж╛ржарж╛ржиред")

# --- ADMIN REMOVAL PROCESS ---
def process_admin_removal(message):
    if message.text and message.text.isdigit():
        remove_id = int(message.text.strip())
        
        if remove_id == OWNER_CHAT_ID:
            bot.send_message(OWNER_CHAT_ID, "тЭМ ржЖржкржирж┐ ржирж┐ржЬрзЗржХрзЗ ржУржирж╛рж░ рж▓рж┐рж╕рзНржЯ ржерзЗржХрзЗ рж░рж┐ржорзЛржн ржХрж░рждрзЗ ржкрж╛рж░ржмрзЗржи ржирж╛ ржнрж╛ржЗ!")
            return
            
        if remove_id in bot_db["admins"]:
            bot_db["admins"].remove(remove_id)
            bot.send_message(OWNER_CHAT_ID, f"ЁЯЧСя╕П <b>Removed!</b> User ID <code>{remove_id}</code> ржХрзЗ ржЕрзНржпрж╛ржбржорж┐ржи рж▓рж┐рж╕рзНржЯ ржерзЗржХрзЗ рж╕ржлрж▓ржнрж╛ржмрзЗ рж╕рж░рж┐рзЯрзЗ ржжрзЗржУрзЯрж╛ рж╣рзЯрзЗржЫрзЗред", parse_mode="HTML")
            
            try:
                bot.send_message(remove_id, "тЪая╕П <b>ALERT!</b> YOU ARE REMOVED FROM ADMIN PANEL BY MAIN OWNER.", parse_mode="HTML")
            except:
                pass
        else:
            bot.send_message(OWNER_CHAT_ID, "тЪая╕П ржПржЗ ржЖржЗржбрж┐ржЯрж┐ ржЕрзНржпрж╛ржбржорж┐ржи рж▓рж┐рж╕рзНржЯрзЗ ржЦрзБржБржЬрзЗ ржкрж╛ржУрзЯрж╛ ржпрж╛рзЯржирж┐ред")
    else:
        bot.send_message(OWNER_CHAT_ID, "тЭМ ржнрзБрж▓ ржлрж░ржорзНржпрж╛ржЯ! рж░рж┐ржорзЛржн ржХрж░рж╛рж░ ржЬржирзНржп рж╢рзБржзрзБржорж╛рждрзНрж░ рж╕ржВржЦрзНржпрж╛рж░ ржЯрзЗрж▓рж┐ржЧрзНрж░рж╛ржо ржЖржЗржбрж┐ (Numeric ID) ржкрж╛ржарж╛ржиред")

# --- STEPS CAPTURE FLOW ---
def process_device_key(message):
    user_id = message.from_user.id
    dev_key = message.text.strip()
    
    if len(dev_key) != 16:
        msg = bot.send_message(user_id, "тЪая╕П <b>Invalid Format!</b> Device key 16-digit er hote hobe. Abar pathan:")
        bot.register_next_step_handler(msg, process_device_key)
        return

    user_data[user_id]['device_id'] = dev_key
    user_data[user_id]['tg_username'] = message.from_user.username.lower() if message.from_user.username else f"id_{user_id}"
    
    msg = bot.send_message(user_id, "ЁЯСд SEND YOUR <b>USERNAME</b> ")
    bot.register_next_step_handler(msg, process_username)

def process_username(message):
    user_id = message.from_user.id
    user_data[user_id]['username'] = message.text.strip()
    msg = bot.send_message(user_id, "ЁЯФТ SEND YOUR PASSWORD <b>PASSWORD</b> ")
    bot.register_next_step_handler(msg, process_password)

def process_password(message):
    user_id = message.from_user.id
    user_data[user_id]['password'] = message.text.strip()
    
    dev_id = user_data[user_id]['device_id']
    uname = user_data[user_id]['username']
    pword = user_data[user_id]['password']
    tg_user = user_data[user_id]['tg_username']
    
    invoice_text = (
        "ЁЯУЛ <b>Your Activation Invoice</b>\n"
        "тФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБ\n"
        f"ЁЯФС <b>Device key:</b> <code>{dev_id}</code>\n"
        f"ЁЯСд <b>USERNAME:</b> <code>{uname}</code>\n"
        f"ЁЯФТ <b>PASSWORD:</b> <code>{pword}</code>\n"
        "ЁЯУК <b>STATUS:</b> тП│ Pending Approval\n"
        "тФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБтФБ\n"
    )
    bot.send_message(user_id, invoice_text, parse_mode="HTML")
    
    json_string = json.dumps({"Device Id": dev_id, "username": uname, "password": pword, "expiry": "2026-12-31"}, indent=4)
    
    admin_markup = InlineKeyboardMarkup()
    admin_markup.row(InlineKeyboardButton("ЁЯЯв Active", callback_data=f"approve_{user_id}"), InlineKeyboardButton("ЁЯФ┤ Deactivate", callback_data=f"reject_{user_id}"))
    
    for adm_id in bot_db["admins"]:
        try:
            bot.send_message(adm_id, f"ЁЯУе <b>New Activation Request!</b>\n\nЁЯСд <b>From User:</b> @{tg_user}\n\n<pre>{json_string}</pre>", parse_mode="HTML", reply_markup=admin_markup)
        except:
            pass

# --- PROCESS APK UPLOAD ---
def process_apk_upload(message):
    if message.document:
        bot_db["saved_apk"] = message.document.file_id
        bot.send_message(message.from_user.id, "тЬЕ APK Successfully added to database!")
    else:
        bot.send_message(message.from_user.id, "тЭМ Format error. Kono valid file/apk/document pathan.")

# --- AUTO CONNECT LOOPS ---
print("ЁЯЪА Mega Upgrade System with Multi-Admin & Support Live!")
while True:
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"Connection drop error ({e}). Reconnecting in 5 seconds...")
        time.sleep(5)
