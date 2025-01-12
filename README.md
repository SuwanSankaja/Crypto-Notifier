# 🚀 Crypto Notifier 📈

Welcome to **Crypto Notifier**, your go-to solution for staying ahead of the cryptocurrency market! 💹 Get real-time alerts for major price movements directly in your inbox. 📧

---

## ✨ Features

- 🔍 **Track USDT Pairs**: Monitors all cryptocurrencies paired with USDT on Binance.
- 📬 **Email Alerts**: Sends notifications for:
  - 🚀 Positive changes of **+10%** or more (Daily, Hourly, 24 hour) (Buy signals).
  - 📉 Negative changes of **-10%** or more (Daily, Hourly, 24 hour) (Sell signals).
- 🔄 **Automatic Updates**: Continuously checks prices every 30 minutes.

---

## 🛠 Prerequisites

Before you get started, make sure you have:

1. 🐍 **Python** (version 3.6 or higher).
2. 🧾 A **Binance account** with API access.
3. ✉️ Email credentials for sending notifications.

---

## 📥 Installation

Follow these simple steps to set up Crypto Notifier:

1. Clone this repo:

   ```bash
   git clone https://github.com/SuwanSankaja/Crypto-Notifier.git
   cd crypto-notifier

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file for environment variables:
   ```plaintext
   BINANCE_API_KEY=your_api_key
   BINANCE_API_SECRET=your_api_secret
   SENDER_EMAIL=your_email@example.com
   SENDER_PASSWORD=your_email_password
   RECEIVER_EMAIL=receiver_email@example.com
   ```

4. Run the script:
   ```bash
   python crypto_notifier.py
   ```

---

## 📦 Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t crypto-notifier .
   ```

2. Run using Docker Compose:
   ```bash
   docker-compose up
   ```

---

## 📄 How It Works

1. **Fetches Market Data**: Uses the Binance API to fetch price changes for USDT trading pairs.
2. **Analyzes Movements**: Identifies coins with significant price changes (+/- 10%).
3. **Sends Notifications**: Sends a detailed email with the analysis results.

---

## 📂 File Structure

- `crypto_notifier.py`: Main script for monitoring and notifications.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Instructions to containerize the app.
- `docker-compose.yml`: Simplifies multi-container Docker applications.
- `.gitignore`: Excludes unnecessary files from version control.

---

## 🛡 Security
- **Environment Variables**: API keys and email credentials are stored securely in a `.env` file.
- **Email Password**: Use app-specific passwords if using Gmail for enhanced security.

---

## 🤝 Contributions

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue to discuss your ideas first.

---


## ⭐️ Show Your Support

If you found this project helpful, give it a star ⭐ on GitHub!
