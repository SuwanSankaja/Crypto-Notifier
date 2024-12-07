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

# Email credentials (can also be set via environment variables for security)
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
    ticker = client.get_ticker(symbol=symbol)
    price = float(ticker['lastPrice'])
    percent_change = float(ticker['priceChangePercent'])
    return price, percent_change

# List of cryptos to monitor (e.g., BTC/USDT, ETH/USDT)
cryptos = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']

# Main loop to check prices every 10 minutes
while True:
    for symbol in cryptos:
        price, percent_change = fetch_price(symbol)
        print(f"{symbol} - Price: ${price} | 24h Change: {percent_change}%")
        
        if percent_change >= 10.00:
            send_email(f"Buy {symbol}", f"Price: ${price}\n24h Change: {percent_change}%\nIt's a good time to buy {symbol}!")
        elif percent_change <= -10.00:
            send_email(f"Sell {symbol}", f"Price: ${price}\n24h Change: {percent_change}%\nIt's a good time to sell {symbol}!")
    
    time.sleep(600)  # Sleep for 10 minutes (600 seconds)
