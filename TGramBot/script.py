from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont
import random
import string
import datetime

# Fonts
bold_font_path = "C:\\Windows\\Fonts\\courbd.ttf"
regular_font_path = "C:\\Windows\\Fonts\\cour.ttf"

# Telegram bot token
TOKEN = "YOUR_TOKEN"

# Valid stores, You can add your own. Uploads logo of your choice into logos folder
VALID_STORES = ["Starbucks", "Chanel","Apple", "Zara", "Bershka", "Gucci"]

# Data storage
user_choices = {}  # store chosen by user
user_inputs = {}   # inputs from user

# New required inputs
FIELDS = [
    "Product name",
    "Amount",
    "Price per unit",
    "Customer email",
    "Street address",
    "Customer full name",
    "Date & time of purchase (format: YYYY-MM-DD HH:MM, or 'now')",
    "Tax (leave empty for 0)",
    "Store address (optional, leave empty for random)"
]
REQUIRED_INPUTS = len(FIELDS)

# ---------------- Commands ---------------- #

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm your chat-bot 🤖 Message /help to get the commands💻"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = (
        "/start - start the chat\n"
        "/help - command list\n"
        "/run <store_name> - generate a receipt\n"
    )
    await update.message.reply_text(commands)

# ---------------- Receipt Image ---------------- #
def create_store_image(store_name, user_text_list):
    img = Image.new("RGB", (500, 1100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    bold_font = ImageFont.truetype(bold_font_path, size=20)
    font = ImageFont.truetype(regular_font_path, size=20)

    # Extract inputs
    product = user_text_list[0]
    amount = int(user_text_list[1])
    price = float(user_text_list[2])
    email = user_text_list[3]
    street = user_text_list[4]
    customer_name = user_text_list[5]

    # Handle date
    date_input = user_text_list[6]
    if date_input.lower() == "now":
        purchase_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        purchase_date = date_input

    # Tax
    try:
        tax = float(user_text_list[7]) if user_text_list[7] else 0.0
    except:
        tax = 0.0

    # Store address
    if user_text_list[8]:
        store_address = user_text_list[8]
    else:
        store_address = f"{random.randint(10,999)} Example St."

    total = amount * price
    total_with_tax = total + tax

    # Logo & barcode
    logo_path = f"logos/{store_name}.png"
    barcode_path = f"logos/barcode.png"
    barcode = Image.open(barcode_path).convert("RGBA")
    barcode = barcode.resize((400, 150))

    try:
        logo = Image.open(logo_path).convert("RGBA")
        if(store_name != 'Apple'):
           logo = logo.resize((200, 200))
           img.paste(logo, (150, 2), logo)
        else:
            logo = logo.resize((90, 90))
            img.paste(logo, (20, 20), logo)

    except FileNotFoundError:
        draw.text((60, 120), f"LOGO: {store_name}", fill="black", font=font)

    # Store info
    draw.text((20, 120), f"{store_name}", fill="black", font=bold_font)
    draw.text((20, 140), store_address, fill="black", font=font)
    zipcode = random.randint(101010, 999999)
    phone_number = random.randint(101010101, 999999999)
    draw.text((20, 160), f"ZIP CODE-{zipcode}", fill="black", font=font)
    draw.text((20, 180), f"{phone_number}", fill="black", font=font)
    draw.text((20, 200), f"{store_name}@gmail.com", fill="black", font=font)

    draw.text((20, 240), "_" * 39, fill="black", font=bold_font)
    draw.text((20, 270), f"Customer: {customer_name}", fill="black", font=font)
    draw.text((20, 300), f"Email: {email}", fill="black", font=font)
    draw.text((20, 330), f"Purchase Date: {purchase_date}", fill="black", font=font)

    # Items
    draw.text((20, 360), "_" * 39, fill="black", font=font)
    draw.text((20, 390), str(amount), fill="black", font=bold_font)
    draw.text((60, 390), str(product), fill="black", font=bold_font)
    draw.text((400, 390), f"${str(price)}", fill="black", font=bold_font)

    # Part number
    model = random.randint(101010, 999999)
    chars = ''.join(random.choices(string.ascii_uppercase, k=2))
    code = chars + '-' + str(model)
    draw.text((60, 420), f"Part Number {code}", fill="black", font=font)
    draw.text((40, 450), f"For support visit {store_name}@gmail.com", fill="black", font=font)  # support

    # Totals
    draw.text((20, 720), "_" * 39, fill="black", font=font)
    draw.text((270, 780), "Sub-Total", fill="black", font=font)
    draw.text((400, 780), f"${total:.2f}", fill="black", font=font)
    draw.text((270, 810), "Tax", fill="black", font=font)
    draw.text((400, 810), f"${tax:.2f}", fill="black", font=font)
    draw.text((270, 840), "Total", fill="black", font=bold_font)
    draw.text((400, 840), f"${total_with_tax:.2f}", fill="black", font=bold_font)

    # Payment
    draw.text((160, 870), "Card", fill="black", font=bold_font)
    draw.text((230, 870), "xxxx xxxx xxxx 4561", fill="black", font=bold_font)
    draw.text((20, 910), "_" * 39, fill="black", font=font)

    img.paste(barcode, (50, 930), barcode)
    # Generate random alphanumeric characters
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    spaced_chars = ' '.join(chars)

    #   the barcode
    barcode_width = 400
    bbox = draw.textbbox((0, 0), spaced_chars, font=font)  # returns (x0, y0, x1, y1)
    text_width = bbox[2] - bbox[0]
    x_pos = 50 + (barcode_width - text_width) // 2
    y_pos = 1060  # adjust based on image height

    draw.text((x_pos, y_pos), spaced_chars, fill="black", font=font)

    img_path = f"{store_name}_{len(user_text_list)}.png"
    img.save(img_path)
    return img_path

# Store temporary unknown store info
pending_logos = {}  # chat_id -> store_name

# Modify run_the_bot
async def run_the_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if context.args:
        store = context.args[0]
        if store in VALID_STORES:
            user_choices[chat_id] = store
            user_inputs[chat_id] = []

            instructions = f"✅ You've chosen: {store}\nPlease input in this order:\n"
            for i, f in enumerate(FIELDS, 1):
                instructions += f"{i}. {f}\n"
            await update.message.reply_text(instructions)
        else:
            # Ask user if they want to upload a logo for this new store
            pending_logos[chat_id] = store
            await update.message.reply_text(
                f"❌ Store '{store}' not found!\n"
                "Do you want to provide a custom logo for this store? "
                "Send it now as a photo or type 'no' to skip."
            )
    else:
        stores_text = "\n".join(VALID_STORES)
        await update.message.reply_text(
            "Choose a store first by running '/run <store_name>':\n" + stores_text
        )

# Add handler to receive logo
async def handle_logo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id in pending_logos and update.message.photo:
        # Get the highest resolution photo
        photo_file = await update.message.photo[-1].get_file()
        store_name = pending_logos[chat_id]
        logo_path = f"logos/{store_name}.png"
        await photo_file.download_to_drive(logo_path)

        # Add store to valid stores temporarily
        VALID_STORES.append(store_name)
        user_choices[chat_id] = store_name
        user_inputs[chat_id] = []

        await update.message.reply_text(
            f"Logo received! ✅ Store '{store_name}' is now ready.\n"
            "Please provide the other inputs as usual."
        )
        del pending_logos[chat_id]

    elif chat_id in pending_logos and update.message.text.lower() == "no":
        store_name = pending_logos[chat_id]
        VALID_STORES.append(store_name)
        user_choices[chat_id] = store_name
        user_inputs[chat_id] = []

        await update.message.reply_text(
            f"No logo provided. Store '{store_name}' will use text placeholder.\n"
            "Please provide the other inputs as usual."
        )
        del pending_logos[chat_id]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id in user_choices:
        user_inputs[chat_id].append(text)

        if len(user_inputs[chat_id]) == REQUIRED_INPUTS:
            img_path = create_store_image(user_choices[chat_id], user_inputs[chat_id])
            with open(img_path, "rb") as f:
                await context.bot.send_photo(chat_id=chat_id, photo=f)
            user_inputs[chat_id] = []  # reset
        else:
            await update.message.reply_text(f"Please enter: {FIELDS[len(user_inputs[chat_id])]}")
    else:
        await update.message.reply_text("Choose the store first by running '/run <store_name>'")

# ---------------- Main ---------------- #
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("run", run_the_bot))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()

