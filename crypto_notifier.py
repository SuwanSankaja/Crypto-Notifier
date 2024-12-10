import os
import time
import smtplib
from datetime import datetime, timedelta
from binance.client import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz

# Get Binance API keys from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')      # Replace with your actual API Key
API_SECRET = os.getenv('BINANCE_API_SECRET')  # Replace with your actual API Secret

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


# Set up the Binance client
client = Client(API_KEY, API_SECRET)

# Dictionary to store coin data
coin_data = {}

# Timezone
timezone = pytz.timezone('Asia/Kolkata')  # 5:30 timezone

# Function to send email
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
        print(f"Email sent successfully: {subject}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        if "Daily user sending limit exceeded" in str(e):
            print("Gmail daily sending limit reached. Pausing until the next day...")
            wait_until_next_day()

# Function to wait until the next day
def wait_until_next_day():
    now = datetime.now(timezone)
    next_day = now + timedelta(days=1)
    next_midnight = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
    wait_seconds = (next_midnight - now).total_seconds()
    print(f"Waiting for {wait_seconds / 3600:.2f} hours until the next day...")
    time.sleep(wait_seconds)

# Fetch all available trading pairs (symbols) on Binance
def get_all_symbols():
    print("Fetching all trading pairs...")
    try:
        exchange_info = client.get_exchange_info()
        symbols = []
        for symbol in exchange_info['symbols']:
            if symbol['status'] == 'TRADING' and 'USDT' in symbol['symbol']:
                symbols.append(symbol['symbol'])
        print(f"Fetched {len(symbols)} trading pairs.")
        return symbols
    except Exception as e:
        print(f"Error fetching trading pairs: {e}")
        return []

# Function to fetch price and percentage change
def fetch_price(symbol):
    try:
        ticker = client.get_ticker(symbol=symbol)
        price = float(ticker['lastPrice'])
        percent_change = float(ticker['priceChangePercent'])
        return price, percent_change
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None

# Function to calculate changes
def calculate_changes(symbol, now_value):
    if symbol not in coin_data:
        # Initialize a new list for the day's values
        coin_data[symbol] = {'values': [now_value]}
        return None, None

    # Append the current value to the list
    coin_data[symbol]['values'].append(now_value)

    # Calculate daily and 30-min changes
    first_value = coin_data[symbol]['values'][0]  # First value of the day
    last_value = coin_data[symbol]['values'][-2] if len(coin_data[symbol]['values']) > 1 else first_value  # Last value from the previous iteration
    daily_change = ((now_value - first_value) / first_value) * 100
    thirty_min_change = ((now_value - last_value) / first_value) * 100

    return daily_change, thirty_min_change

# Function to reset daily data
def reset_daily_data():
    for symbol in coin_data:
        # Keep the last value of the day as the first value for the next day
        last_value = coin_data[symbol]['values'][-1]
        coin_data[symbol] = {'values': [last_value]}
    print("Daily data reset. Retained the last value of each symbol for the next day.")

# Main loop
def main():
    print("Starting main loop...")
    last_reset_date = datetime.now(timezone).date()

    try:
        while True:
            iteration_start_time = datetime.now(timezone)
            print(f"Iteration started at: {iteration_start_time.strftime('%Y-%m-%d %H:%M:%S')}")

            buy_count = 0
            sell_count = 0

            now = datetime.now(timezone)
            if now.date() != last_reset_date:
                print(f"New day detected ({now.date()}). Resetting daily data...")
                reset_daily_data()
                print("Daily data has been reset.")
                last_reset_date = now.date()

            cryptos = get_all_symbols()[:500]
            print(f"Processing {len(cryptos)} cryptocurrencies...")

            for index, symbol in enumerate(cryptos):
                print(f"Processing {index + 1}/{len(cryptos)}: {symbol}")
                now_value, percent_change = fetch_price(symbol)

                if now_value is None or percent_change is None:
                    print(f"Failed to fetch data for {symbol}. Skipping.")
                    continue

                # Calculate daily and 30-min changes
                daily_change, thirty_min_change = calculate_changes(symbol, now_value)

                # Format the values for logging
                thirty_min_change_str = f"{thirty_min_change:.2f}%" if thirty_min_change is not None else "N/A"
                daily_change_str = f"{daily_change:.2f}%" if daily_change is not None else "N/A"

                # Log with all data
                print(
                    f"Fetched data for {symbol}: "
                    f"Price = ${now_value:.2f}, "
                    f"24h Change = {percent_change:.2f}%, "
                    f"30-min Change = {thirty_min_change_str}, "
                    f"Daily Change = {daily_change_str}"
                )

                historical_values = ", ".join(f"${v:.2f}" for v in coin_data[symbol]['values'])

                # Buy Email Logic
                if (thirty_min_change is not None and thirty_min_change >= 10) or \
                   (daily_change is not None and daily_change >= 10):
                    send_email(
                        f"Buy {symbol}",
                        f"""
                        Symbol: {symbol}
                        Current Price: ${now_value}
                        30-min Change: {thirty_min_change_str}
                        Daily Change: {daily_change_str}
                        24h Change: {percent_change:.2f}%

                        Historical Prices Today: {historical_values}

                        It's a good time to buy {symbol}!
                        """
                    )
                    buy_count += 1

                # Sell Email Logic
                elif (thirty_min_change is not None and thirty_min_change <= -10) or \
                     (daily_change is not None and daily_change <= -10):
                    send_email(
                        f"Sell {symbol}",
                        f"""
                        Symbol: {symbol}
                        Current Price: ${now_value}
                        30-min Change: {thirty_min_change_str}
                        Daily Change: {daily_change_str}
                        24h Change: {percent_change:.2f}%

                        Historical Prices Today: {historical_values}

                        It's a good time to sell {symbol}!
                        """
                    )
                    sell_count += 1
                else:
                    print("30 min Change and Daily Change is N/A")

            summary_subject = "Iteration Summary"
            summary_body = f"""
            Iteration Start Time: {iteration_start_time.strftime('%Y-%m-%d %H:%M:%S')}
            Total Buy Emails Sent: {buy_count}
            Total Sell Emails Sent: {sell_count}
            """
            if buy_count == 0 and sell_count == 0:
                summary_body += "No buy or sell emails were sent during this iteration."

            send_email(summary_subject, summary_body)
            print("Summary email sent.")
            print(coin_data)
            next_interval = now + timedelta(minutes=30 - (now.minute % 30), seconds=-now.second, microseconds=-now.microsecond)
            sleep_duration = (next_interval - datetime.now(timezone)).total_seconds()
            print(f"Next iteration scheduled at {next_interval.strftime('%Y-%m-%d %H:%M:%S')} (in {sleep_duration:.2f} seconds).")
            time.sleep(sleep_duration)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


