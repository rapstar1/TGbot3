import asyncio
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from wallet_manager import create_wallet, import_wallet
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize Telegram bot with your Bot Token
TOKEN = '7224912163:AAH46VSr7vyuP5-oaHt7vzwgkD1YUgG28hk'  # 请替换为你的 Telegram Bot Token
application = Application.builder().token(TOKEN).build()

# Route for serving the index.html
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to create wallet
@app.route('/api/create-wallet', methods=['POST'])
def api_create_wallet():
    try:
        response = create_wallet()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Flask route to import wallet
@app.route('/api/import-wallet', methods=['POST'])
def api_import_wallet():
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")
        response = import_wallet(data)
        return jsonify(response), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Telegram command to create a wallet
async def create_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Make a request to Flask API to create a wallet
        response = requests.post('https://tgbot3.onrender.com/api/create-wallet')  # 确保Flask应用的URL正确
        result = response.json()
        if 'error' in result:
            await update.message.reply_text(f"Error: {result['error']}")
        else:
            await update.message.reply_text(f"Wallet created successfully: {result}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Telegram command to import a wallet
async def import_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the wallet data from the user
        wallet_data = context.args[0] if context.args else None
        if not wallet_data:
            await update.message.reply_text("Please provide wallet data to import.")
            return
        
        # Make a request to Flask API to import a wallet
        response = requests.post('https://tgbot3.onrender.com/api/import-wallet', json={'wallet_data': wallet_data})
        result = response.json()
        if 'error' in result:
            await update.message.reply_text(f"Error: {result['error']}")
        else:
            await update.message.reply_text(f"Wallet imported successfully: {result}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# New: Telegram command to start and show Open APP button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Creating an inline button for opening the app
        keyboard = [[InlineKeyboardButton("Open APP", url="https://tgbot3.onrender.com/")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Sending a message with the inline button
        await update.message.reply_text('点击打开应用程序:', reply_markup=reply_markup)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Register the Telegram commands
application.add_handler(CommandHandler('create_wallet', create_wallet_command))
application.add_handler(CommandHandler('import_wallet', import_wallet_command))

# Register the start command to send the inline button
application.add_handler(CommandHandler('start', start))

# Function to run Flask app and Telegram bot
def run_flask():
    app.run(debug=True, use_reloader=False)

# Function to start Telegram bot
def start_bot():
    print("Starting Telegram bot...")
    application.run_polling()

if __name__ == '__main__':
    from threading import Thread
    import nest_asyncio

    # Apply the patch to allow nested event loops
    nest_asyncio.apply()

    # Start Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start the bot
    start_bot()
