# Telegram Receipt Generator Bot 🤖🧾

A fun Telegram bot that generates **custom receipt images** for various stores. Perfect for mock receipts, testing, or just playing around.

---

## Features

* Generate receipts for multiple stores
* Supports **multiple products** per receipt
* Add customer info: name, email, address
* Automatically calculates totals and taxes
* Randomized barcodes with alphanumeric codes
* Optional store logos
* Payment info (mock card number)
* Easy-to-use interactive prompts

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/telegram-receipt-bot.git
cd telegram-receipt-bot
```

2. Install dependencies:

```bash
pip install python-telegram-bot Pillow
```

3. Add your bot token in `script.py`:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

4. Optional: Add store logos in `logos/` named `<StoreName>.png`

5. Run the bot:

```bash
python script.py
```

---

## Usage

1. Start the bot with `/start`
2. View available commands using `/help`
3. Choose a store with `/run <store_name>`
4. Enter required info in this order:

   1. Product name
   2. Amount
   3. Price per unit
   4. Customer email
   5. Street address
   6. Customer full name
   7. Date & time of purchase (`YYYY-MM-DD HH:MM` or `now`)
   8. Tax (leave empty for 0)
   9. Store address (optional)

> Multiple products are supported — enter **Product, Amount, Price** consecutively.

---

## File Structure

```
telegram-receipt-bot/
│
├─ logos/                  # Optional store logos
├─ script.py               # Main bot script
├─ README.md               # This file
└─ requirements.txt        # Optional dependencies
```

---

## Customization

* Change receipt **size**:

```python
img = Image.new("RGB", (500, 1100), color=(255, 255, 255))
```

* Change **logo size**:

```python
logo = logo.resize((100, 100))
```

* Modify fonts via:

```python
bold_font_path = "C:\\Windows\\Fonts\\courbd.ttf"
regular_font_path = "C:\\Windows\\Fonts\\cour.ttf"
```

* Adjust barcode position or spacing in `create_store_image` function.

---

## Troubleshooting

* If the bot doesn't respond, check your **bot token**.
* Make sure all dependencies are installed.
* Missing logos will default to text placeholders.
* For multiple products, always enter **Product, Amount, Price** in the correct order.

---

## License

MIT License
