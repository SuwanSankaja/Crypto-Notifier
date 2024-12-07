import os
import time
import smtplib
from binance.client import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get Binance API keys from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')      # Replace with your actual API Key
API_SECRET = os.getenv('BINANCE_API_SECRET')  # Replace with your actual API Secret

# Set up the Binance client
client = Client(API_KEY, API_SECRET)

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()

# Function to fetch the price and percentage change from Binance
def fetch_price(symbol):
    try:
        ticker = client.get_ticker(symbol=symbol)
        price = float(ticker['lastPrice'])
        percent_change = float(ticker['priceChangePercent'])
        return price, percent_change
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None

# Fetch all available trading pairs (symbols) on Binance
def get_all_symbols():
    exchange_info = client.get_exchange_info()
    symbols = []
    for symbol in exchange_info['symbols']:
        # Only include symbols that are actively traded and have USDT as one of the pairs
        if symbol['status'] == 'TRADING' and 'USDT' in symbol['symbol']:
            symbols.append(symbol['symbol'])
    return symbols

# Main loop to check prices every 10 minutes
while True:
    cryptos = get_all_symbols()  # Get all trading pairs that include USDT
    print({EMAIL})
    print(f"Using PASSWORD: {'*' * len(PASSWORD) if PASSWORD else 'None'}")

    for symbol in cryptos:
        price, percent_change = fetch_price(symbol)
        if price is not None and percent_change is not None:
            print(f"{symbol} - Price: ${price} | 24h Change: {percent_change}%")
            
            # Check for positive or negative change and send an email accordingly
            if percent_change >= 10.00:
                send_email(f"Buy {symbol}", f"Price: ${price}\n24h Change: {percent_change}%\nIt's a good time to buy {symbol}!")
            elif percent_change <= -10.00:
                send_email(f"Sell {symbol}", f"Price: ${price}\n24h Change: {percent_change}%\nIt's a good time to sell {symbol}!")

    time.sleep(600)  # Sleep for 10 minutes (600 seconds)
