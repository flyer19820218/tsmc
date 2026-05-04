import yfinance as yf
import datetime
import pytz

# ==========================================
# 定義黃金供應鏈 (包含代號與詳細解說)
# ==========================================
supply_chain = {
    "🌟 1. 微影製程 (Lithography)": [
        {"name": "新應材", "ticker": "4749.TWO", "desc": "EUV/DUV 高階光阻液、底層吸收材料。台廠突破外商壟斷的黑馬。"},
        {"name": "三福化", "ticker": "4755.TW", "desc": "TMAH 顯影液回收與製造龍頭，緊跟半導體在地化政策。"},
        {"name": "達興材料", "ticker": "5234.TW", "desc": "半導體高階光學材料、光阻剝離液。"},
        {"name": "家登", "ticker": "3680.TWO", "desc": "EUV 極紫外光光罩盒 (POD) 全球市佔霸主。"}
    ],
    "💧 2. 蝕刻與清洗 (Etch & Clean)": [
        {"name": "崇越", "ticker": "5434.TW", "desc": "代理日本高純度 HF (氫氟酸) 與各類特化材料，濕式製程關鍵。"},
        {"name": "勝一", "ticker": "1773.TW", "desc": "電子級溶劑 (IPA) 龍頭，先進晶圓清洗必備。"},
        {"name": "上品", "ticker": "4770.TW", "desc": "氟素樹脂 (鐵氟龍) 設備廠，專門裝載與輸送致命強酸。"}
    ],
    "💨 3. 沉積與特種氣體 (Deposition)": [
        {"name": "台特化", "ticker": "4772.TWO", "desc": "矽乙烷 (Si2H6) 等先進沉積特用氣體，2nm/A16 關鍵原料。"},
        {"name": "晶呈科技", "ticker": "4768.TWO", "desc": "特殊氣體製造 (如 C4F6)，用於先進蝕刻與沉積。"}
    ],
    "🥏 4. CMP 化學機械平坦化": [
        {"name": "中砂", "ticker": "1560.TW", "desc": "3nm/2nm CMP 鑽石碟主力供應商，隨製程微縮用量暴增。"},
        {"name": "頌勝科技", "ticker": "7768.TWO", "desc": "半導體 CMP 研磨墊。本土供應鏈替代外商壟斷之關鍵。"} # 註：若為興櫃，yfinance 可能抓不到，但卡片仍可點擊
    ],
    "🏗️ 5. 先進封裝與廠務 (CoWoS & Facilities)": [
        {"name": "弘塑", "ticker": "3131.TWO", "desc": "濕製程設備 (酸槽、單晶圓清洗)，CoWoS 擴產最純受惠者。"},
        {"name": "萬潤", "ticker": "6187.TWO", "desc": "自動化點膠機、散熱貼合設備，CoWoS 後段大將。"},
        {"name": "漢唐", "ticker": "2404.TW", "desc": "無塵室工程龍頭，承接台積電多數高階先進製程廠房。"},
        {"name": "竑騰", "ticker": "7751.TWO", "desc": "大尺寸封裝、鋼片散熱設備。掌握先進封裝熱處理核心。"},
        {"name": "竹陞科技", "ticker": "6739.TWO", "desc": "Govison、Gobot 智能廠務系統。全球擴廠自動化標配。"},
        {"name": "巨漢", "ticker": "6903.TWO", "desc": "無塵室、廠務機電工程。台積電全球擴廠最穩定的建設夥伴。"}
    ],
    "🔬 6. 光學檢測與精密耗材 (Inspection & Consumables)": [
        {"name": "倍利科", "ticker": "7822.TWO", "desc": "高精度全自動光學顯微鏡、AOI 缺陷檢測。2nm 品質門神。"},
        {"name": "碩正科技", "ticker": "7669.TWO", "desc": "先進製程離型膜。高階製程中消耗量極大的精密耗材。"},
        {"name": "山太士", "ticker": "3595.TWO", "desc": "探針清洗片、翹曲膜。維持先進封裝良率的幕後功臣。"}
    ]
}

# 取得台灣時間
tw_tz = pytz.timezone('Asia/Taipei')
update_time = datetime.datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')

# 開始組合 HTML
html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>護國群山戰情室 (560億美元花去哪？)</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f0f4f8; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #1a365d; font-size: 2.5em; margin-bottom: 5px; }}
        .subtitle {{ text-align: center; color: #718096; margin-bottom: 10px; font-size: 1.1em; }}
        .update-time {{ text-align: center; color: #e53e3e; font-weight: bold; margin-bottom: 40px; font-size: 0.9em; }}
        .section-title {{ border-bottom: 3px solid #3182ce; padding-bottom: 8px; color: #2b6cb0; margin-top: 40px; font-size: 1.5em; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }}
        .card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-decoration: none; color: inherit; display: block; border-left: 6px solid #4299e1; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-5px); border-left: 6px solid #e53e3e; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }}
        .header-row {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }}
        .company-name {{ font-size: 1.4em; font-weight: 800; color: #2d3748; }}
        .stock-price {{ font-size: 1.3em; font-weight: bold; color: #d69e2e; }}
        .ticker {{ color: #a0aec0; font-size: 0.9em; margin-bottom: 15px; font-family: monospace; }}
        .product {{ font-size: 0.95em; color: #4a5568; line-height: 1.5; }}
        .link-hint {{ margin-top: 15px; font-size: 0.85em; color: #3182ce; text-align: right; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏔️ 護國群山戰情室</h1>
        <div class="subtitle">台積電先進製程供應鏈 ｜ 點擊卡片直達 Yahoo 財報</div>
        <div class="update-time">最後更新時間：{update_time} (依收盤價)</div>
"""

# 依序產生 HTML 卡片並抓取股價
print("⏳ 正在抓取股價並生成網頁...")
for category, companies in supply_chain.items():
    html_content += f'<h2 class="section-title">{category}</h2>\n<div class="grid">\n'
    for comp in companies:
        ticker_code = comp["ticker"].split(".")[0]
        try:
            # 抓最新股價
            stock = yf.Ticker(comp["ticker"])
            hist = stock.history(period="1d")
            price = f"${hist['Close'].iloc[-1]:.1f}" if not hist.empty else "興櫃/無資料"
        except Exception:
            price = "讀取失敗"
            
        print(f"✅ {comp['name']} ({ticker_code}) - {price}")
        
        # 產生該公司的卡片 (連往 Yahoo 奇摩)
        html_content += f"""
            <a href="https://tw.stock.yahoo.com/quote/{ticker_code}" target="_blank" class="card">
                <div class="header-row">
                    <div class="company-name">{comp['name']}</div>
                    <div class="stock-price">{price}</div>
                </div>
                <div class="ticker">{ticker_code}</div>
                <div class="product">{comp['desc']}</div>
                <div class="link-hint">查看財報 ↗</div>
            </a>
        """
    html_content += '</div>\n'

html_content += """
    </div>
</body>
</html>
"""

# 寫入 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("🎉 index.html 更新完成！所有的艦隊都已就位！")
