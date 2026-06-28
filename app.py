import streamlit as st
import yfinance as yf
import feedparser
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="StockPilot AI",
    layout="wide"
)

st.title("📈 StockPilot AI")
st.caption("투자 의사결정 지원 AI Agent")
# =====================
# 마지막 업데이트
# =====================

current_time = datetime.now(
    ZoneInfo("Asia/Seoul")
).strftime("%Y-%m-%d %H:%M")

st.caption(f"🕒 마지막 업데이트 : {current_time}")

# =====================
# 주요 시장지수
# =====================

st.markdown("---")
st.subheader("📊 오늘의 주요 시장")

market_list = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "NASDAQ": "^IXIC",
    "S&P500": "^GSPC"
}

cols = st.columns(4)

for i, (name, ticker) in enumerate(market_list.items()):

    try:

        data = yf.Ticker(ticker).history(period="5d")

        current = round(data["Close"].iloc[-1], 2)

        yesterday = data["Close"].iloc[-2]

        change = round(
            ((current - yesterday) / yesterday) * 100,
            2
        )

        cols[i].metric(
            name,
            current,
            f"{change}%"
        )

    except:

        cols[i].metric(
            name,
            "-",
            "-"
        )

st.markdown("---")

st.subheader("🌍 AI 시장 브리핑")

try:

    kospi = yf.Ticker("^KS11").history(period="2d")
    nasdaq = yf.Ticker("^IXIC").history(period="2d")

    kospi_change = (
        kospi["Close"].iloc[-1] -
        kospi["Close"].iloc[-2]
    )

    nasdaq_change = (
        nasdaq["Close"].iloc[-1] -
        nasdaq["Close"].iloc[-2]
    )

    if kospi_change > 0:
        korea = "📈 국내시장은 상승 흐름을 보이고 있습니다."
    else:
        korea = "📉 국내시장은 다소 약세를 보이고 있습니다."

    if nasdaq_change > 0:
        usa = "🚀 미국 기술주 중심의 강세가 이어지고 있습니다."
    else:
        usa = "⚠ 미국 기술주는 조정을 받고 있습니다."

    if kospi_change > 0 and nasdaq_change > 0:
        risk = "🟢 시장 위험도 : 낮음"
    elif kospi_change < 0 and nasdaq_change < 0:
        risk = "🔴 시장 위험도 : 높음"
    else:
        risk = "🟡 시장 위험도 : 보통"

    st.success(korea)
    st.info(usa)
    st.warning(risk)

except:

    st.info("시장 정보를 불러오는 중입니다.")


st.markdown(
    "<div style='text-align:right; color:gray; font-size:13px;'>Developed by <b>JaeWon Lee</b></div>",
    unsafe_allow_html=True
)


# =====================
# 종목 데이터
# =====================

stock_map = {

    # 삼성
    "삼성전자": "005930.KS",
    "삼성전기": "009150.KS",
    "삼성SDI": "006400.KS",
    "삼성바이오로직스": "207940.KS",
    "삼성물산": "028260.KS",

    # SK
    "SK하이닉스": "000660.KS",
    "SK텔레콤": "017670.KS",
    "SK이노베이션": "096770.KS",
    "SK스퀘어": "402340.KS",

    # 국내
    "NAVER": "035420.KS",
    "카카오": "035720.KS",

    # 미국
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    
    # 기타
    "한미반도체": "042700.KQ",
    "LG에너지솔루션": "373220.KS",
    "삼성SDI": "006400.KS",
    "에코프로비엠": "247540.KQ",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "NVIDIA": "NVDA",
    "AMD": "AMD",
    "Intel": "INTC",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Meta": "META",
    "Amazon": "AMZN",
    "Tesla": "TSLA"
}

# =====================
# 별칭
# =====================

alias_map = {

    "하이닉스": "SK하이닉스",
    "sk하이닉스": "SK하이닉스",

    "애플": "Apple",
    "apple": "Apple",
    "APPLE": "Apple",

    "엔비디아": "NVIDIA",
    "nvidia": "NVIDIA",

    "테슬라": "Tesla",
    "tesla": "Tesla",

    "구글": "Google",
    "google": "Google"
}

# =====================
# 함수
# =====================

def calculate_rsi(data, period=14):

    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return round(rsi.iloc[-1], 2)


def format_price(price, currency):

    if currency == "KRW":
        return f"{price:,.0f} 원"

    elif currency == "USD":
        return f"${price:,.2f}"

    else:
        return f"{price:,.2f} {currency}"

# =====================
# 검색
# =====================

def format_market_cap(value):

    if value is None:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.1f}조"

    elif value >= 1_000_000:
        return f"{value / 1_000_000:.0f}백만"

    else:
        return f"{value:,}"

# =====================
# 검색
# =====================



    prompt = f"""
당신은 전문 투자 애널리스트입니다.

종목: {name}
투자점수: {score}
RSI: {rsi}
PER: {pe}
ROE: {roe}

분석 근거:
{reasons}

조건:
- 5~7줄 투자 리포트
- 마지막 줄 BUY / HOLD / SELL
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional equity analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


query = st.text_input(
    "종목명 입력",
    placeholder="예: SK, 삼성, 애플, 테슬라, 엔비디아"
)
selected_stock = None

if query:

    query = query.strip()

    candidates = []

    if query in alias_map:
        candidates.append(alias_map[query])

    for stock_name in stock_map.keys():

        if query.lower() in stock_name.lower():
            candidates.append(stock_name)

    candidates = list(dict.fromkeys(candidates))

    if len(candidates) == 0:

        st.error("검색 결과가 없습니다.")
        st.stop()

    selected_stock = st.selectbox(
        "검색 결과",
        candidates
    )

# =====================
# 분석
# =====================

if selected_stock:

    try:

        ticker = stock_map[selected_stock]

        stock = yf.Ticker(ticker)

        info = stock.info
        market_cap = info.get("marketCap")

        hist = stock.history(period="1y")

        if hist.empty:
            st.error("주가 데이터를 가져오지 못했습니다.")
            st.stop()

        current_price = round(
            hist["Close"].iloc[-1],
            2
        )

        currency = info.get("currency", "")

        year_high = round(
            hist["High"].max(),
            2
        )

        year_low = round(
            hist["Low"].min(),
            2
        )

        pe = info.get("trailingPE")

        roe = info.get("returnOnEquity")

        market_cap = info.get("marketCap")

        if roe:
            roe = round(roe * 100, 2)

        rsi = calculate_rsi(hist)

        ma20 = hist["Close"].rolling(20).mean().iloc[-1]

        # =====================
        # 투자 매력도
        # =====================

        score = 50

        if pe and pe < 25:
            score += 15

        if roe and roe > 10:
            score += 15

        if 40 <= rsi <= 70:
            score += 20

        if current_price > ma20:
            score += 10

        score = min(score, 100)

        confidence = min(
            95,
            round(score * 0.9)
        )

        # =====================
        # 투자기간
        # =====================

        if score >= 85:

            invest_period = "장기 (1년 이상)"
            grade = "🟢 매우 우수"

        elif score >= 70:

            invest_period = "중장기 (3개월 ~ 1년)"
            grade = "🟡 양호"

        else:

            invest_period = "단기 (1주 ~ 3개월)"
            grade = "🔴 관망"

        # =====================
        # 출력
        # =====================

        st.markdown("---")

        st.header(selected_stock)

        st.subheader("📈 최근 1년 주가 추이")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.update_layout(
            title="1년 주가 추이",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)
        

        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "현재가",
                format_price(current_price, currency)
            )

        with col2:
            st.metric(
                "연중 최고가",
                format_price(year_high, currency)
            )

        with col3:
            st.metric(
                "연중 최저가",
                format_price(year_low, currency)
            )

        with col4:
            st.metric(
                "PER",
                f"{round(pe,2)}배" if pe else "N/A"
            )

        st.markdown("---")
        col5, col6, col7, col8, col9 = st.columns(5)

        with col5:
            st.metric(
                "ROE",
                f"{roe}%" if roe else "N/A"
            )

        with col6:
            st.metric(
                "RSI",
                rsi
            )

        with col7:
            st.metric(
                "투자 매력도",
                f"{score}점"
            )

        with col8:
            st.metric(
                "AI 신뢰도",
                f"{confidence}%"
            )

        with col9:
            st.metric(
                "시가총액",
                format_market_cap(market_cap)
            )

        st.success(
            f"추천 투자기간 : {invest_period}"
        )

        st.info(
            f"투자 등급 : {grade}"
        )


        # =====================
        # AI 의견
        # =====================

        st.markdown("---")

        st.subheader("🤖 AI 리포트 (LLM 생성)")

        opinion = []

        opinion.append(
            f"현재 RSI는 {rsi} 수준입니다."
        )

        opinion.append(
            f"투자 매력도는 {score}점입니다."
        )

        opinion.append(
            f"AI 신뢰도는 {confidence}% 수준입니다."
        )

        if rsi > 70:
            opinion.append(
                "단기적으로 과열 가능성이 있습니다."
            )

        elif rsi < 30:
            opinion.append(
                "과매도 구간으로 해석될 수 있습니다."
            )

        else:
            opinion.append(
                "기술적 지표상 과열 상태는 아닙니다."
            )

        if roe and roe > 10:
            opinion.append(
                "ROE가 양호하여 수익성이 우수합니다."
            )

        if pe and pe < 25:
            opinion.append(
                "PER 기준 과도한 고평가 상태는 아닙니다."
            )

        for item in opinion:
            st.write("•", item)

        # =====================
# LLM AI 리포트 생성
# =====================


        # =====================
        # 뉴스
        # =====================

        st.markdown("---")

        st.subheader("📰 최신 뉴스")

        rss_url = (
            f"https://news.google.com/rss/search?q={selected_stock}"
        )

        feed = feedparser.parse(rss_url)

        if len(feed.entries) == 0:

            st.write(
                "관련 뉴스를 찾지 못했습니다."
            )

        else:

            for article in feed.entries[:5]:

                st.markdown(
                    f"- [{article.title}]({article.link})"
                )

    except Exception as e:

        st.error(
            f"오류 발생 : {e}"
        )


def ai_score_and_reason(ticker, name):

    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    if hist.empty:
        return None

    info = stock.info

    rsi = calculate_rsi(hist)
    ma20 = hist["Close"].rolling(20).mean().iloc[-1]
    current = hist["Close"].iloc[-1]

    pe = info.get("trailingPE")
    roe = info.get("returnOnEquity")

    score = 50
    reasons = []

    # RSI
    if rsi > 70:
        reasons.append("RSI 과열 구간 (단기 부담)")
    elif rsi < 30:
        reasons.append("RSI 과매도 구간 (반등 가능성)")
    else:
        score += 10
        reasons.append("RSI 안정 구간")

    # MA
    if current > ma20:
        score += 15
        reasons.append("이동평균선 상향 돌파")
    else:
        reasons.append("이동평균선 하회")

    # PER
    if pe and pe < 25:
        score += 15
        reasons.append("PER 저평가 구간")

    # ROE
    if roe and roe > 0.1:
        score += 15
        reasons.append("ROE 수익성 우수")

    final_score = min(score, 100)

    return {
        "name": name,
        "ticker": ticker,
        "score": final_score,
        "reasons": reasons
    }

st.markdown("---")
st.subheader("🔥 오늘의 AI 추천 종목")

results = []

for name, ticker in stock_map.items():

    try:
        res = ai_score_and_reason(ticker, name)

        if res:
            results.append(res)

    except:
        continue

results = sorted(results, key=lambda x: x["score"], reverse=True)[:5]

for r in results:

    st.metric(
        label=r["name"],
        value=f"{r['score']}점"
    )

    with st.expander("AI 분석 이유 보기"):
        for reason in r["reasons"]:
            st.write("•", reason)



kr_stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "삼성SDI": "006400.KS",
    "LG에너지솔루션": "373220.KS"
}
us_stocks = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL"
}


st.subheader("🔥 국내 상승 TOP5")

kr_results = []

for name, ticker in kr_stocks.items():
    try:
        df = yf.Ticker(ticker).history(period="5d")
        if len(df) < 2:
            continue

        change = (df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2] * 100

        if change > 0:   # 🔥 핵심 필터
            kr_results.append({
                "name": name,
                "change": change
            })

    except:
        continue

kr_results = sorted(kr_results, key=lambda x: x["change"], reverse=True)[:3]

for r in kr_results:
    st.metric(r["name"], f"+{r['change']:.2f}%")


st.subheader("🚀 미국 상승 TOP5")

us_results = []

for name, ticker in us_stocks.items():
    try:
        df = yf.Ticker(ticker).history(period="5d")
        if len(df) < 2:
            continue

        change = (df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2] * 100

        if change > 0:   # 🔥 핵심 필터
            us_results.append({
                "name": name,
                "change": change
            })

    except:
        continue

us_results = sorted(us_results, key=lambda x: x["change"], reverse=True)[:3]

for r in us_results:
    st.metric(r["name"], f"+{r['change']:.2f}%")


st.markdown("---")
st.subheader("🤖 오늘의 AI 시장 한줄 요약")

try:
    kospi = yf.Ticker("^KS11").history(period="2d")
    nasdaq = yf.Ticker("^IXIC").history(period="2d")

    kospi_change = kospi["Close"].iloc[-1] - kospi["Close"].iloc[-2]
    nasdaq_change = nasdaq["Close"].iloc[-1] - nasdaq["Close"].iloc[-2]

    if kospi_change > 0 and nasdaq_change > 0:
        sentiment = "상승"
    elif kospi_change < 0 and nasdaq_change < 0:
        sentiment = "하락"
    else:
        sentiment = "혼조"

    if abs(kospi_change) + abs(nasdaq_change) > 100:
        intensity = "강한"
    else:
        intensity = "완만한"

    if kospi_change > nasdaq_change:
        driver = "국내 시장"
    else:
        driver = "미국 시장"

    summary = f"📊 오늘 시장은 {driver} 중심의 {intensity} {sentiment} 흐름을 보이고 있습니다."

    st.success(summary)

except:
    st.info("시장 요약 생성 중입니다.")


