import os
import json
import smtplib
from email.message import EmailMessage
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler, MessageHandler, filters
)

# =================== CONFIG ===================
TOKEN = "8338265637:AAG7zi_nXgOzhPqeRjYLQkYRQTK-p85jNb8"   # <--- Replace with bot token

# Use environment variables for safety (or replace directly)
EMAIL_ADDRESS = "mikkyrose297@gmail.com"
EMAIL_PASSWORD = "ugtr glqf bfno mukq"   # Use an app password here

PREMIUM_FILE = "premium_users.json"
ALL_USERS_FILE = "all_users.json"

WHATSAPP_SUPPORT_EMAILS = [
    "support@support.whatsapp.com",
    "support@whatsapp.com",
    "security@support.whatsapp.com",
    "abuse@whatsapp.com",
]

OWNER_ID = 7243305432

OWNER_URL = "https://t.me/daxhr"
CHANNEL_URL = "https://t.me/Exodustrust"
BUG_BOT_URL = "https://t.me/YourBugBot"   # <--- Define properly
CPANEL_URL = "https://your-cpanel-link.com"  # <--- Define properly

EMAIL_TEMPLATES = {
    "spam": "مرحباً، أود الإبلاغ عن هذا الرقم على أنه يرسل رسائل غير مرغوب فيها: {number}. يرجى اتخاذ الإجراء المناسب.",
    "scam": "مرحباً، هذا الرقم يقوم بعمليات احتيال: {number}. نرجو منكم مراجعته فوراً.",
    "fakeaccount": "مرحباً، أبلغ عن هذا الرقم لأنه يستخدم حساباً مزيفاً: {number}. يرجى التحقق.",
    "voilence": "مرحباً، هذا الرقم يشارك في محتوى عنيف: {number}. نرجو منكم اتخاذ الإجراءات اللازمة.",
    "childabouse": "مرحباً، أبلغ عن هذا الرقم لنشره محتوى مسيء للأطفال: {number}. يرجى التحرك فوراً.",
    "pronograph": "مرحباً، هذا الرقم يشارك في مواد إباحية: {number}. يرجى اتخاذ الإجراء المناسب.",
    "copyright": "مرحباً، أبلغ عن انتهاك حقوق الطبع والنشر من هذا الرقم: {number}. نرجو منكم فحص ذلك.",
    "selfharm": "مرحباً، هذا الرقم قد يعرض نفسه للأذى: {number}. يرجى التدخل.",
    "drug": "مرحباً، هذا الرقم يروج للمخدرات: {number}. يرجى اتخاذ اللازم.",
    "terrorism": "مرحباً، أشتبه في نشاط إرهابي من هذا الرقم: {number}. نرجو اتخاذ إجراء عاجل.",
    "harassment": "مرحباً، هذا الرقم يقوم بالتحرش: {number}. يرجى مراجعة البلاغ.",
    "animalabouse": "مرحباً، أبلغ عن إساءة معاملة الحيوانات من قبل هذا الرقم: {number}.",
    "others": "مرحباً، أبلغ عن نشاط مشبوه من هذا الرقم: {number}. يرجى النظر في هذا الأمر."
}

# Conversation states
ADD_PREM, DEL_PREM, BROADCAST = range(3)

premium_users_cache = None
all_users_cache = None

# =================== UTILS ===================
def load_premium_users():
    global premium_users_cache
    if premium_users_cache is not None:
        return premium_users_cache
    if not os.path.exists(PREMIUM_FILE):
        premium_users_cache = []
    else:
        try:
            with open(PREMIUM_FILE, "r") as f:
                premium_users_cache = json.load(f)
        except json.JSONDecodeError:
            premium_users_cache = []
    return premium_users_cache

def save_premium_users(users):
    global premium_users_cache
    premium_users_cache = users
    with open(PREMIUM_FILE, "w") as f:
        json.dump(users, f)

def load_all_users():
    global all_users_cache
    if all_users_cache is not None:
        return all_users_cache
    if not os.path.exists(ALL_USERS_FILE):
        all_users_cache = []
    else:
        try:
            with open(ALL_USERS_FILE, "r") as f:
                all_users_cache = json.load(f)
        except json.JSONDecodeError:
            all_users_cache = []
    return all_users_cache

def save_all_users(users):
    global all_users_cache
    all_users_cache = users
    with open(ALL_USERS_FILE, "w") as f:
        json.dump(users, f)

def is_premium(user_id):
    return user_id in load_premium_users()

def send_email(subject: str, content: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(WHATSAPP_SUPPORT_EMAILS)
    msg.set_content(content)
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# =================== HANDLERS ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    all_users = load_all_users()
    if user_id not in all_users:
        all_users.append(user_id)
        save_all_users(all_users)

    keyboard = [
        [InlineKeyboardButton("𝐑𝐞𝐩𝐨𝐫𝐭 𝐌𝐞𝐧𝐮", callback_data="report_menu")],
        [InlineKeyboardButton("𝐀𝐝𝐦𝐢𝐧 𝐌𝐞𝐧𝐮", callback_data="admin_menu")],
        [InlineKeyboardButton("𝐀𝐛𝐨𝐫𝐭", callback_data="abort")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "𝑻𝒉𝒆 𝒐𝒏𝒍𝒚 𝒅𝒊𝒔𝒕𝒂𝒏𝒄𝒆 𝒃𝒆𝒕𝒘𝒆𝒆𝒏 𝒚𝒐𝒖 𝒂𝒏𝒅 𝒇𝒆𝒂𝒓 𝒊𝒔 𝒎𝒆.\n"
        "𝑫𝒐 𝒚𝒐𝒖 𝒘𝒊𝒔𝒉 𝒕𝒐 𝒑𝒓𝒐𝒄𝒆𝒆𝒅?",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    special_buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("OWNER", url=OWNER_URL),
            InlineKeyboardButton("CHANNEL", url=CHANNEL_URL)
        ]]
    )

    if query.data == "report_menu":
        report_text = """🔥𝗘𝗫𝗢𝗗𝗨𝗦 𝗠𝗗 𝗧𝗘𝗟𝗘 𝗕𝗔𝗡 🔥

╭━━━⊰ 💎 𝗥𝗘𝗣𝗢𝗥𝗧 𝗠𝗘𝗡𝗨 💎 ⊱━━━╮
┃ 📍 1. /spam <number>
┃ 📍 2. /fakeaccount <number>
┃ 📍 3. /voilence <number>
┃ 📍 4. /childabouse <number>
┃ 📍 5. /pronograph <number>
┃ 📍 6. /copyright <number>
┃ 📍 7. /scam <number>
┃ 📍 8. /selfharm <number>
┃ 📍 9. /drug <number>
┃ 📍 10. /terrorism <number>
┃ 📍 11. /harassment <number>
┃ 📍 12. /animalabouse <number>
┃ 📍 13. /others <number>
╰━━━━━━━━━━━━━━━━━━━╯

𝗡𝗢𝗧𝗘: 𝐎𝐍𝐋𝐘 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐔𝐒𝐄𝐑𝐒 𝐂𝐀𝐍 𝐔𝐒𝐄 𝐑𝐄𝐏𝐎𝐑𝐓.
"""
        await query.edit_message_text(text=report_text, reply_markup=special_buttons)

    elif query.data == "admin_menu":
        if user_id != OWNER_ID:
            await query.edit_message_text("❌ You are not authorized to access the admin menu.")
            return

        admin_text = """👑 𝗔𝗱𝗺𝗶𝗻 𝗠𝗲𝗻𝘂 👑

Commands:
/addprem <user_id> - Add Premium User
/deleprem <user_id> - Remove Premium User
/listprem - List Premium Users
/broadcast - Broadcast Message to all users
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Premium User", callback_data="admin_addprem")],
            [InlineKeyboardButton("Remove Premium User", callback_data="admin_deleprem")],
            [InlineKeyboardButton("List Premium Users", callback_data="admin_listprem")],
            [InlineKeyboardButton("Broadcast Message", callback_data="admin_broadcast")],
            [InlineKeyboardButton("Back to Start", callback_data="start_over")],
            [
                InlineKeyboardButton("𝐁𝐔𝐆 𝐁𝐎𝐓", url=BUG_BOT_URL),
                InlineKeyboardButton("𝐂𝐏𝐀𝐍𝐄𝐋", url=CPANEL_URL)
            ]
        ])

        await query.edit_message_text(text=admin_text, reply_markup=keyboard)

    elif query.data == "start_over":
        await start(update, context)

    elif user_id == OWNER_ID:
        if query.data == "admin_listprem":
            users = load_premium_users()
            text = "✅ Premium Users IDs:\n" + ("\n".join(str(u) for u in users) if users else "No premium users yet.")
            await query.edit_message_text(text)
        elif query.data == "admin_addprem":
            await query.edit_message_text("Send me the user ID to ADD to premium:")
            return ADD_PREM
        elif query.data == "admin_deleprem":
            await query.edit_message_text("Send me the user ID to REMOVE from premium:")
            return DEL_PREM
        elif query.data == "admin_broadcast":
            await query.edit_message_text("Send me the message text to BROADCAST to all users:")
            return BROADCAST
        elif query.data == "abort":
            await query.edit_message_text("❌ Operation Aborted.")
        else:
            await query.edit_message_text("❌ Unknown admin action.")
    else:
        await query.edit_message_text("❌ You are not authorized to perform this action.")

async def add_premium_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Please send a numeric user ID.")
        return ADD_PREM

    users = load_premium_users()
    if user_id in users:
        await update.message.reply_text(f"User {user_id} is already a premium user.")
    else:
        users.append(user_id)
        save_premium_users(users)
        await update.message.reply_text(f"✅ User {user_id} added to premium.")

async def del_premium_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Please send a numeric user ID.")
        return DEL_PREM

    users = load_premium_users()
    if user_id not in users:
        await update.message.reply_text(f"User {user_id} is not a premium user.")
    else:
        users.remove(user_id)
        save_premium_users(users)
        await update.message.reply_text(f"✅ User {user_id} removed from premium.")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    broadcast_text = update.message.text.strip()
    all_users = load_all_users()

    if not all_users:
        await update.message.reply_text("⚠️ No users to broadcast to.")
        return

    sent_count = 0
    failed_users = []
    for uid in all_users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 Broadcast message:\n\n{broadcast_text}")
            sent_count += 1
        except Exception:
            failed_users.append(str(uid))

    await update.message.reply_text(f"✅ Broadcast sent to {sent_count} users.\nFailures: {', '.join(failed_users) if failed_users else 'None'}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    command = update.message.text.split()[0][1:]
    args = context.args

    if not is_premium(user_id):
        await update.message.reply_text("❌ Only premium users can report.")
        return

    if command not in EMAIL_TEMPLATES or not args:
        await update.message.reply_text(f"❌ Usage: /{command} <number>")
        return

    number = " ".join(args)  # FIXED: convert list to string
    message_body = EMAIL_TEMPLATES[command].format(number=number)
    try:
        send_email(subject="محتوى مسيء في واتساب", content=message_body)
        await update.message.reply_text("📩 تم إرسال البلاغ إلى واتساب بنجاح.")
    except Exception as e:
        await update.message.reply_text("⚠️ فشل إرسال البريد الإلكتروني.")
        print(e)

async def simple_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✅ You used {update.message.text}")

async def addprem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /addprem <user_id>")
        return
    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ User ID must be a number.")
        return
    users = load_premium_users()
    if user_id not in users:
        users.append(user_id)
        save_premium_users(users)
        await update.message.reply_text(f"✅ User {user_id} added to premium.")
    else:
        await update.message.reply_text("User is already premium.")

async def deleprem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /deleprem <user_id>")
        return
    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ User ID must be a number.")
        return

    users = load_premium_users()
    if user_id in users:
        users.remove(user_id)
        save_premium_users(users)
        await update.message.reply_text(f"✅ User {user_id} removed from premium.")
    else:
        await update.message.reply_text("User was not premium.")

# =================== MAIN ===================
if name == "main":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    for cmd in EMAIL_TEMPLATES.keys():
        app.add_handler(CommandHandler(cmd, report_command))

    for cmd in ["connect", "buy", "reportsystem", "help", "sessions", "price"]:
        app.add_handler(CommandHandler(cmd, simple_reply))

    app.add_handler(CommandHandler("addprem", addprem))
    app.add_handler(CommandHandler("deleprem", deleprem))

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button, pattern="admin_addprem"),
            CallbackQueryHandler(button, pattern="admin_deleprem"),
            CallbackQueryHandler(button, pattern="admin_broadcast")
        ],
        states={
            ADD_PREM: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_premium_user)],
            DEL_PREM: [MessageHandler(filters.TEXT & ~filters.COMMAND, del_premium_user)],
            BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    app.add_handler(conv_handler)

    print("✅ Bot is running...")
    app.run_polling()
