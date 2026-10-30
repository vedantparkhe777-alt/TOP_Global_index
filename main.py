import streamlit as st
import yfinance as yf
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import datetime

# Configure the web page
st.set_page_config(page_title="AI Stock Analyzer - Ultra Speed Edition", layout="wide")

# -------------------------------------------------------------------
# CUSTOM UI STYLING (Financial Terminal Theme)
# -------------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
    }
    div[data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #f0f6fc !important;
        font-weight: 600;
    }
    /* Segmented Radio Navigation (Acts like Instant Tabs) */
    div[data-testid="stRadio"] > div {
        background-color: #161b22;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SYMBOL LISTS
# -------------------------------------------------------------------
NIFTY_50_SYMBOLS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BHARTIARTL.NS",
    "BPCL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "ETERNAL.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS",
    "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
    "INDUSINDBK.NS", "INFY.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS",
    "LT.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS",
    "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS",
    "SHRIRAMFIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS", "TMPV.NS", "TMCV.NS", "TATASTEEL.NS",
    "TCS.NS", "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

NASDAQ_50_SYMBOLS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "COST",
    "ASML", "TMUS", "CSCO", "PEP", "ADBE", "LIN", "AMD", "NFLX", "AZN", "QCOM",
    "TXN", "INTC", "AMGN", "HON", "AMAT", "CMCSA", "BKNG", "SBUX", "VRTX", "ADP",
    "GILD", "MDLZ", "REGN", "ADI", "PDD", "ISRG", "LRCX", "MU", "INTU", "MELI",
    "CSX", "PANW", "SNPS", "CDNS", "KLAC", "ORLY", "MAR", "PYPL", "CRWD", "CTAS"
]

EURO_STOXX_50_SYMBOLS = [
    "ASML.AS", "MC.PA", "SAP.DE", "OR.PA", "SIE.DE", "TTE.PA", "ALV.DE", "AIR.PA",
    "SAN.MC", "SU.PA", "IBE.MC", "RMS.PA", "EL.PA", "CDI.PA", "DG.PA", "BNP.PA",
    "BBVA.MC", "ITX.MC", "ENEL.MI", "INGA.AS", "ISP.MI", "BAS.DE", "MBG.DE", "BAYN.DE",
    "DTE.DE", "MUV2.DE", "DB1.DE", "CS.PA", "BN.PA", "ABI.BR", "RACE.MI", "ENI.MI",
    "IFX.DE", "DHL.DE", "ADS.DE", "ADYEN.AS", "BMW.DE", "CRH.L", "AENA.MC", "HEIA.AS",
    "ENGGI.PA", "AD.AS", "SASY.PA", "NOKIA.HE", "GLE.PA", "VOW3.DE", "REP.MC", "PRX.AS"
]

CHINA_TOP_50_SYMBOLS = [
    "601318.SS", "600519.SS", "600036.SS", "601398.SS", "601857.SS",
    "601288.SS", "600028.SS", "601988.SS", "601628.SS", "600030.SS",
    "601088.SS", "600900.SS", "601668.SS", "601888.SS", "600309.SS",
    "600276.SS", "600887.SS", "601012.SS", "601328.SS", "600000.SS",
    "000858.SZ", "000333.SZ", "002594.SZ", "300750.SZ", "000651.SZ",
    "002475.SZ", "000725.SZ", "300014.SZ", "000002.SZ", "002714.SZ",
    "000568.SZ", "002352.SZ", "300274.SZ", "002415.SZ", "000001.SZ",
    "9988.HK", "0700.HK", "3690.HK", "1810.HK", "9618.HK",
    "2318.HK", "0939.HK", "1398.HK", "3988.HK", "0883.HK",
    "1211.HK", "2269.HK", "2020.HK", "1024.HK", "9888.HK"
]

JAPAN_TOP_50_SYMBOLS = [
    "7203.T", "6758.T", "9984.T", "6861.T", "8306.T",
    "6501.T", "9983.T", "8035.T", "4519.T", "7741.T",
    "6367.T", "4063.T", "6098.T", "7267.T", "8058.T",
    "8001.T", "8316.T", "8411.T", "9432.T", "9433.T",
    "7974.T", "6902.T", "6954.T", "6503.T", "7201.T",
    "6702.T", "6752.T", "4502.T", "4503.T", "4568.T",
    "6981.T", "7751.T", "8031.T", "8801.T", "8802.T",
    "9020.T", "9022.T", "9101.T", "9104.T", "9107.T",
    "6273.T", "6301.T", "7270.T", "7309.T", "6971.T",
    "4901.T", "5108.T", "2503.T", "2802.T", "3382.T"
]

KOREA_TOP_50_SYMBOLS = [
    "005930.KS", "000660.KS", "373220.KS", "207940.KS", "005380.KS",
    "000270.KS", "035420.KS", "005490.KS", "068270.KS", "035720.KS",
    "051910.KS", "006400.KS", "003550.KS", "105560.KS", "055550.KS",
    "012330.KS", "028260.KS", "015760.KS", "032830.KS", "086790.KS",
    "018260.KS", "000810.KS", "010130.KS", "009150.KS", "034730.KS",
    "011200.KS", "003670.KS", "034080.KS", "329180.KS", "251270.KS",
    "010950.KS", "000120.KS", "030200.KS", "017670.KS", "005935.KS",
    "003490.KS", "000720.KS", "036570.KS", "011170.KS", "004020.KS",
    "267250.KS", "024110.KS", "000100.KS", "005830.KS", "000060.KS",
    "006800.KS", "021240.KS", "005385.KS", "001040.KS", "033780.KS"
]

# -------------------------------------------------------------------
# HIGH-SPEED BULK FETCH ENGINE (SINGLE BATCH HTTP CALL)
# -------------------------------------------------------------------
@st.cache_data(ttl=10)
def get_market_data_bulk(symbols, currency_symbol="$"):
    # Download 2 days of daily data for ALL tickers in 1 single network request
    data = yf.download(symbols, period="2d", interval="1d", group_by="ticker", progress=False)
    
    records = []
    for symbol in symbols:
        try:
            clean_symbol = symbol.split('.')[0]
            
            # Retrieve data slice for the specific ticker
            if len(symbols) > 1:
                df_ticker = data[symbol]
            else:
                df_ticker = data

            # Drop missing values
            df_ticker = df_ticker.dropna(subset=['Close'])
            if len(df_ticker) < 2:
                continue

            prev_close = float(df_ticker['Close'].iloc[-2])
            curr_price = float(df_ticker['Close'].iloc[-1])
            volume = int(df_ticker['Volume'].iloc[-1])

            if prev_close == 0:
                continue

            change = curr_price - prev_close
            p_change = (change / prev_close) * 100

            if p_change >= 1.5:
                sentiment = "🟢 Strong Bullish"
            elif p_change > 0:
                sentiment = "📈 Leaning Bullish"
            elif p_change <= -1.5:
                sentiment = "🔴 Strong Bearish"
            elif p_change < 0:
                sentiment = "📉 Leaning Bearish"
            else:
                sentiment = "⚖️ Neutral"

            records.append({
                'Ticker': f"/?symbol={clean_symbol}#{clean_symbol}",
                'Stock Name': clean_symbol,
                f'Price ({currency_symbol})': curr_price,
                f'Change ({currency_symbol})': change,
                '% Change': p_change,
                'Volume': volume,
                'Market Sentiment': sentiment
            })
        except Exception:
            pass

    df = pd.DataFrame(records)
    if not df.empty:
        return df.sort_values(by='Volume', ascending=False)
    return df

def color_cells(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return 'color: #00E676; font-weight: 600;'
        elif val < 0:
            return 'color: #FF5252; font-weight: 600;'
    return ''

# -------------------------------------------------------------------
# VIEW 1: FUNDAMENTALS & GRAPH (The Deep Dive)
# -------------------------------------------------------------------
if "symbol" in st.query_params:
    if st.button("⬅️ Back to Dashboard"):
        st.query_params.clear()
        st.rerun()

    symbol = st.query_params["symbol"]

    all_symbols = (
        NIFTY_50_SYMBOLS + NASDAQ_50_SYMBOLS + EURO_STOXX_50_SYMBOLS +
        CHINA_TOP_50_SYMBOLS + JAPAN_TOP_50_SYMBOLS + KOREA_TOP_50_SYMBOLS
    )
    matched = [s for s in all_symbols if s.startswith(symbol)]
    ticker_symbol = matched[0] if matched else symbol

    st.title(f"📊 {symbol} — Market Deep Dive")

    chart_type = st.radio("Select Chart View:", ["Line", "Candlestick"], horizontal=True)
    live_placeholder = st.empty()

    ticker = yf.Ticker(ticker_symbol)

    with live_placeholder.container():
        info = ticker.info

        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        prev_close = info.get('previousClose', 0)
        change = current_price - prev_close
        currency = info.get('currency', 'USD')

        if currency == "INR": curr_sym = "₹"
        elif currency == "EUR": curr_sym = "€"
        elif currency in ["CNY", "JPY"]: curr_sym = "¥"
        elif currency == "KRW": curr_sym = "₩"
        elif currency == "HKD": curr_sym = "HK$"
        else: curr_sym = "$"

        st.subheader("Price Action & Fundamentals")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"{curr_sym}{current_price:.2f}", f"{change:.2f}")
        col2.metric("Today's High", f"{curr_sym}{info.get('dayHigh', 'N/A')}")
        col3.metric("Today's Low", f"{curr_sym}{info.get('dayLow', 'N/A')}")
        col4.metric("Market Cap", f"{curr_sym}{info.get('marketCap', 0) // 10**7} Cr/M" if info.get('marketCap') else 'N/A')

        st.divider()

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("P/E Ratio (Trailing)", round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A')
        col6.metric("EPS (Trailing 12M)", f"{curr_sym}{info.get('trailingEps', 'N/A')}")
        col7.metric("Book Value", f"{curr_sym}{info.get('bookValue', 'N/A')}")
        col8.metric("Price to Book (P/B)", round(info.get('priceToBook', 0), 2) if info.get('priceToBook') else 'N/A')

        st.divider()

        col9, col10, col11, col12 = st.columns(4)

        ex_div_timestamp = info.get('exDividendDate')
        if ex_div_timestamp:
            formatted_div_date = datetime.fromtimestamp(ex_div_timestamp).strftime('%d %b, %Y')
        else:
            formatted_div_date = "N/A"

        div_rate = info.get('dividendRate')
        div_yield = info.get('dividendYield')

        col9.metric("Dividend Rate", f"{curr_sym}{div_rate}" if div_rate else 'N/A')
        col10.metric("Dividend Yield", f"{div_yield * 100:.2f}%" if div_yield else 'N/A')
        col11.metric("Ex-Dividend Date", formatted_div_date)
        col12.metric("Forward P/E", round(info.get('forwardPE', 0), 2) if info.get('forwardPE') else 'N/A')

        st.divider()

        st.subheader("Intraday Chart")
        st.caption(f"⚡ Live Feed Updated: {time.strftime('%H:%M:%S')}")

        history = ticker.history(period="1d", interval="1m")

        if not history.empty:
            fig = go.Figure()

            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=history.index,
                    open=history['Open'],
                    high=history['High'],
                    low=history['Low'],
                    close=history['Close'],
                    name='Candlestick',
                    increasing_line_color='#00E676',
                    decreasing_line_color='#FF5252'
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=history.index, 
                    y=history['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(width=2, color='#00B0FF')
                ))

            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                xaxis_title="Time",
                yaxis_title=f"Price ({curr_sym})",
                xaxis_rangeslider_visible=False, 
                margin=dict(l=0, r=0, t=30, b=0),
                hovermode="x unified" 
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No intraday data available for today yet.")

# -------------------------------------------------------------------
# VIEW 2: MAIN DASHBOARD (LAZY LOADED BY ACTIVE TAB)
# -------------------------------------------------------------------
else:
    st.title("🌐 Global Financial Terminal")
    st.markdown("Ultra-fast live volume, price movement, and sentiment tracking across international markets.")

    # Expandable Terminal Settings
    with st.expander("⚙️ Terminal Settings & Auto-Refresh Controls"):
        col_set1, col_set2 = st.columns([2, 1])
        with col_set1:
            refresh_rate = st.slider("Auto-Refresh Interval (seconds)", min_value=1, max_value=60, value=15)
        with col_set2:
            st.write("")
            st.write("")
            if st.button("🔄 Manual Refresh Now"):
                st.cache_data.clear()
                st.rerun()

    # Lazy-load market selection using segmented controls
    selected_market = st.radio(
        "Select Market Exchange:",
        [
            "🇮🇳 Nifty 50", 
            "🇺🇸 Nasdaq Top 50", 
            "🇪🇺 Euro Stoxx 50", 
            "🇨🇳 China Top 50", 
            "🇯🇵 Nikkei Top 50", 
            "🇰🇷 KOSPI Top 50"
        ],
        horizontal=True
    )

    def render_active_market(symbols, currency, title, desc):
        st.header(title)
        st.caption(desc)
        df = get_market_data_bulk(symbols, currency_symbol=currency)
        if not df.empty:
            st.write(f"⚡ **Live Bulk Feed Updated:** `{time.strftime('%H:%M:%S')}` (Next update in {refresh_rate}s)")
            styled = df.style.map(color_cells, subset=[f'Change ({currency})', '% Change'])
            st.dataframe(
                styled,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ticker": st.column_config.LinkColumn("Ticker", display_text=r"#(.+)$"),
                    "Stock Name": st.column_config.TextColumn("Stock Name"),
                    f"Price ({currency})": st.column_config.NumberColumn(f"Price ({currency})", format=f"{currency}%.2f"),
                    f"Change ({currency})": st.column_config.NumberColumn(f"Change ({currency})", format="%.2f"),
                    "% Change": st.column_config.NumberColumn("% Change", format="%.2f%%"),
                    "Volume": st.column_config.NumberColumn("Volume", format="%d")
                }
            )
        else:
            st.warning("Fetching market data... please wait.")

    # LAZY LOADING ROUTER: Only fetch data for the single active tab!
    if "Nifty" in selected_market:
        render_active_market(NIFTY_50_SYMBOLS, "₹", "🇮🇳 Indian Equity Market (Nifty 50)", "Top constituent stocks of NSE India sorted by trading volume.")
    elif "Nasdaq" in selected_market:
        render_active_market(NASDAQ_50_SYMBOLS, "$", "🇺🇸 US Market (Nasdaq Top 50)", "Top mega-cap US tech and growth stocks sorted by trading volume.")
    elif "Euro" in selected_market:
        render_active_market(EURO_STOXX_50_SYMBOLS, "€", "🇪🇺 European Market (Euro Stoxx 50)", "Top European blue-chip equities sorted by trading volume.")
    elif "China" in selected_market:
        render_active_market(CHINA_TOP_50_SYMBOLS, "¥", "🇨🇳 Chinese Market (Top 50)", "Top Chinese mega-cap stocks across Shanghai, Shenzhen & Hong Kong.")
    elif "Nikkei" in selected_market:
        render_active_market(JAPAN_TOP_50_SYMBOLS, "¥", "🇯🇵 Japanese Market (Nikkei Top 50)", "Top blue-chip equities on the Tokyo Stock Exchange.")
    elif "KOSPI" in selected_market:
        render_active_market(KOREA_TOP_50_SYMBOLS, "₩", "🇰🇷 Korean Market (KOSPI Top 50)", "Top South Korean equities on the Korea Exchange.")

    # -------------------------------------------------------------------
    # CONTINUOUS REFRESH TRIGGER
    # -------------------------------------------------------------------
    time.sleep(refresh_rate)
    st.rerun()