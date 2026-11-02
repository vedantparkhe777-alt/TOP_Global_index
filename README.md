# 🌐 [Global Financial Terminal: AI Stock Analyzer (Ultra Speed Edition)](https://topglobalindex-m3nfzypt5nsgchf7zkbzxh.streamlit.app/)

A high-performance, real-time financial tracking dashboard built with **Python**, **Streamlit**, **yfinance**, and **Plotly**. Designed like an institutional terminal, this app features lightning-fast bulk data downloading, lazy-loaded market views, and deep-dive fundamental analytics across major global indices.

[![Live Demo](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://topglobalindex-m3nfzypt5nsgchf7zkbzxh.streamlit.app/)

---

## 🚀 Key Features

* **⚡ Ultra-Fast Bulk Fetch Engine**: Downloads 2 days of daily market data for entire index baskets in a single batched network call, eliminating lag.
* **🌍 Multi-Market Coverage**: Instantly switch between 6 major international equity benchmarks:
  * 🇮🇳 **Nifty 50** (NSE India)
  * 🇺🇸 **Nasdaq Top 50** (US Tech & Growth)
  * 🇪🇺 **Euro Stoxx 50** (European Blue Chips)
  * 🇨🇳 **China Top 50** (Shanghai, Shenzhen & HK)
  * 🇯🇵 **Nikkei Top 50** (Tokyo Stock Exchange)
  * 🇰🇷 **KOSPI Top 50** (Korea Exchange)
* **📊 Market Deep Dive & Analytics**: Click any stock ticker to access a comprehensive fundamental breakdown:
  * Valuation metrics: Trailing & Forward P/E, P/B ratio, EPS, and Book Value.
  * Dividend stats: Dividend Rate, Yield, and Ex-Dividend Dates.
  * Live Intraday Charts: Switch instantly between **Line** and **Candlestick** views powered by interactive Plotly graphs.
* **🌙 Dark Financial Terminal Theme**: Custom CSS styling optimized for low-eye-strain trading and data monitoring.
* **🔄 Auto-Refresh Controls**: Configurable auto-refresh interval slider with manual refresh overrides.

---

## 🛠️ Tech Stack

* **Frontend & Framework**: [Streamlit](https://streamlit.io/)
* **Data Retrieval**: [yfinance](https://github.com/ranaroussi/yfinance)
* **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
* **Interactive Visualization**: [Plotly](https://plotly.com/python/)

---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.8 or higher installed on your system.

### 2. Clone or Download the Repository
Save your application script as `app.py` in your working directory.

### 3. Install Dependencies
Open your terminal or command prompt and install the required Python packages:

```bash
pip install streamlit yfinance pandas plotly
