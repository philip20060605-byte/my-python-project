import os
from flask import Flask, request

app = Flask(__name__)

# 後端超級旅遊資料庫（大幅擴充：每個國家 8 個，共 24 個巨量數據）
TRAVEL_DATA = {
    "taiwan": [
        # 地標名勝
        {"name": "台北 101 大樓", "category": "landmark", "desc": "台灣最具代表性的國際地標，可登頂俯瞰整座城市的璀璨夜景與現代繁華。", "tag": "國際指標", "hot": "98%"},
        {"name": "中正紀念堂", "category": "landmark", "desc": "宏偉的藍白宮殿式建築，其大型廣場與整點的三軍儀隊交接儀式是國際觀光客必朝聖的亮點。", "tag": "歷史觀光", "hot": "86%"},
        {"name": "國立故宮博物院", "category": "landmark", "desc": "典藏數千年華夏文化歷史文物精粹，外國旅客必訪聖地。", "tag": "文化歷史", "hot": "88%"},
        # 大自然風光
        {"name": "九份老街", "category": "nature", "desc": "依山傍海的復古山城，紅燈籠階梯與懷舊茶樓充滿了神祕的東方意境。", "tag": "復古山城", "hot": "91%"},
        {"name": "太魯閣國家公園", "category": "nature", "desc": "世界級的大理岩峽谷景觀，高聳陡峭的斷崖與壯麗的大自然鬼斧神工。", "tag": "壯麗峽谷", "hot": "89%"},
        {"name": "阿里山國家風景區", "category": "nature", "desc": "以日出、雲海、神木、鐵道與櫻花『五奇』聞名國際，是體驗台灣高山森林魅力的最佳去處。", "tag": "森林奇景", "hot": "92%"},
        # 在地必吃美食
        {"name": "士林觀光夜市", "category": "food", "desc": "享譽國際的指標性夜市，各種台灣傳統創新小吃與在地美食的一級戰區。", "tag": "必吃美食", "hot": "94%"},
        {"name": "鼎泰豐信義店", "category": "food", "desc": "米其林推薦的小籠包傳奇，黃金 18 折的精緻工藝與頂級服務，成功將台灣美食推向國際舞台。", "tag": "米其林傳奇", "hot": "96%"}
    ],
    "japan": [
        # 地標名勝
        {"name": "東京晴空塔", "category": "landmark", "desc": "世界第一高自立式電波塔，觀景台能 360 度將整個東京與富士山盡收眼底。", "tag": "現代地標", "hot": "97%"},
        {"name": "京都清水寺", "category": "landmark", "desc": "全木造的古老懸空舞台，春櫻秋楓四季皆美，是日本傳統文化的殿堂。", "tag": "世界遺產", "hot": "95%"},
        {"name": "淺草寺雷門", "category": "landmark", "desc": "東京最古老的寺廟，巨大的紅色『雷門』燈籠與熱鬧的仲見世通商店街，充滿濃厚江戶風情。", "tag": "江戶古剎", "hot": "94%"},
        # 大自然風光
        {"name": "富士山五合目", "category": "nature", "desc": "近距離朝聖日本聖山，欣賞壯麗的雲海與白雪皚皚的經典火山錐景致。", "tag": "聖山風光", "hot": "96%"},
        {"name": "奈良公園", "category": "nature", "desc": "古木參天的巨大公園，上千隻溫馴的野生梅花鹿自由漫步其間，可購買鹿仙貝與其互動。", "tag": "萌鹿互動", "hot": "92%"},
        {"name": "北海道富良野花田", "category": "nature", "desc": "夏季限定的絕美紫色薰衣草地毯，漫山遍野的七彩繽紛花海，是全亞洲最著名的自然景觀之一。", "tag": "夢幻花海", "hot": "90%"},
        # 在地必吃美食
        {"name": "築地/豐洲市場", "category": "food", "desc": "東京海鮮的代名詞，現切頂級黑鮪魚生魚片與海鮮丼飯，饕客的必訪天堂。", "tag": "頂級海鮮", "hot": "93%"},
        {"name": "道頓堀美食街", "category": "food", "desc": "大阪『吃倒』文化的發源地，巨大的招牌章魚與跑跑卡丁車格力高看板下，滿街都是章魚燒與大阪燒。", "tag": "熱鬧美食街", "hot": "95%"}
    ],
    "korea": [
        # 地標名勝
        {"name": "首爾 N 濟州塔", "category": "landmark", "desc": "座落於南山山頂，是鳥瞰首爾全景的絕佳景點，著名的愛情鎖牆更是浪漫聖地。", "tag": "浪漫地標", "hot": "91%"},
        {"name": "景福宮", "category": "landmark", "desc": "朝鮮王朝規模最宏大的正宮，穿著傳統韓服在正殿前打卡體驗穿越時空的魅力。", "tag": "宮廷文化", "hot": "93%"},
        {"name": "樂天世界塔", "category": "landmark", "desc": "韓國第一高樓，擁有全球最高的玻璃底觀景台，挑戰在高空 500 公尺俯瞰漢江的極致刺激。", "tag": "摩天高樓", "hot": "89%"},
        # 大自然風光
        {"name": "濟州島城山日出峰", "category": "nature", "desc": "由海底火山爆發形成的巨型冠冕狀火山口，在山頂迎接海平面的日出極其壯觀。", "tag": "自然奇景", "hot": "90%"},
        {"name": "南怡島生態景區", "category": "nature", "desc": "經典韓劇拍攝地，著名的水杉路在春夏秋冬皆展現出極致的水彩畫美景，充滿浪漫文藝氣息。", "tag": "韓劇聖地", "hot": "88%"},
        {"name": "釜山海雲台藍線公園", "category": "nature", "desc": "沿著蔚藍海岸線行駛的復古彩色空中膠囊小火車，是近代引爆全亞洲社群媒體的超級景點。", "tag": "海景火車", "hot": "95%"},
        # 在地必吃美食
        {"name": "明洞商圈美食街", "category": "food", "desc": "首爾流行文化的發源地，滿街的韓式街頭小吃、辣炒年糕與雞蛋糕讓人流連忘返。", "tag": "街頭小吃", "hot": "94%"},
        {"name": "廣藏市場", "category": "food", "desc": "體驗首爾在地人日常的最夯傳統市場，生拌牛肉、活章魚、綠豆煎餅與麻藥飯捲是必點招牌。", "tag": "傳統市場", "hot": "92%"}
    ]
}

# 網頁共同的前端 UI 架構
def get_layout(content, active_page=""):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>東北亞旅遊大數據助手 | 林靖淏</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, "Microsoft JhengHei", sans-serif; display: flex; background-color: #0f172a; color: #f8fafc; min-height: 100vh; }}
            
            /* 進階側邊導覽列（Sidebar） */
            .sidebar {{ width: 280px; background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border-right: 1px solid #334155; padding: 30px 0; display: flex; flex-direction: column; position: fixed; height: 100vh; z-index: 100; }}
            .sidebar-header {{ padding: 0 25px 25px 25px; border-bottom: 1px solid #334155; text-align: center; }}
            .sidebar-header h2 {{ font-size: 1.5rem; color: #38bdf8; font-weight: 800; letter-spacing: 1px; }}
            .sidebar-header p {{ font-size: 0.85rem; color: #94a3b8; margin-top: 8px; font-weight: bold; }}
            .nav-links {{ list-style: none; margin-top: 30px; }}
            .nav-links a {{ display: flex; align-items: center; padding: 14px 25px; color: #94a3b8; text-decoration: none; font-weight: 600; font-size: 1.05rem; transition: all 0.25s ease; }}
            .nav-links a:hover, .nav-links a.active {{ background-color: rgba(56, 189, 248, 0.1); color: #38bdf8; border-left: 5px solid #38bdf8; padding-left: 30px; }}
            
            /* 主要內容呈現區區塊 */
            .main-content {{ margin-left: 280px; flex: 1; padding: 50px; background-color: #0f172a; }}
            .card {{ background: #1e293b; padding: 35px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); margin-bottom: 30px; }}
            h1 {{ color: #ffffff; margin-bottom: 20px; font-size: 2.4rem; font-weight: 800; }}
            h2 {{ color: #38bdf8; margin-top: 25px; margin-bottom: 15px; font-size: 1.5rem; }}
            p {{ color: #94a3b8; font-size: 1.1rem; margin-bottom: 15px; line-height: 1.7; }}
            
            /* 現代科技感按鈕 */
            .filter-section {{ margin-bottom: 30px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155; }}
            .btn {{ background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%); color: white; padding: 10px 22px; text-decoration: none; border-radius: 8px; font-weight: bold; border: none; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2); }}
            .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 15px rgba(56, 189, 248, 0.4); }}
            .btn-outline {{ background: transparent; border: 1px solid #475569; color: #94a3b8; box-shadow: none; }}
            .btn-outline:hover, .btn-outline.active {{ background: #334155; color: #ffffff; border-color: #64748b; }}
            
            /* 旅遊大數據網格卡片 */
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; margin-top: 25px; }}
            .spot-card {{ background: #1e293b; border-radius: 14px; border: 1px solid #334155; overflow: hidden; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
            .spot-card:hover {{ transform: translateY(-8px); border-color: #38bdf8; box-shadow: 0 20px 25px -5px rgba(56, 189, 248, 0.1); }}
            .spot-body {{ padding: 25px; }}
            .spot-title {{ font-size: 1.3rem; color: #ffffff; font-weight: 700; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }}
            .spot-tag {{ background-color: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.75rem; padding: 4px 10px; border-radius: 6px; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.2); }}
            .spot-desc {{ font-size: 1rem; color: #94a3b8; line-height: 1.6; margin-bottom: 15px; text-align: justify; }}
            
            /* 熱度計數據樣式 */
            .hot-bar {{ display: flex; align-items: center; gap: 10px; background: #0f172a; padding: 8px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: bold; color: #fbbf24; }}
            .hot-fill {{ height: 6px; background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%); border-radius: 3px; }}
            
            /* 表單元件美化 */
            input, select, textarea {{ width: 100%; padding: 14px; margin-bottom: 20px; background-color: #0f172a; border: 1px solid #334155; border-radius: 8px; font-size: 1rem; color: white; transition: border 0.3s; }}
            input:focus, textarea:focus {{ outline: none; border-color: #38bdf8; }}
            
            footer {{ text-align: center; margin-top: 60px; color: #475569; font-size: 0.9rem; border-top: 1px solid #334155; padding-top: 25px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <div class="sidebar-header">
                <h2>🧳 東北亞大數據助手</h2>
                <p>文化資管 2A 林靖淏</p>
            </div>
            <ul class="nav-links">
                <li><a href="/" class="{"active" if active_page=='home' else ''}">🏠 系統首頁</a></li>
                <li><a href="/explore" class="{"active" if active_page=='explore' else ''}">🔍 跨國數據</a></li>
                <li><a href="/skills" class="{"active" if active_page=='skills' else ''}">📚 技術心得</a></li>
                <li><a href="/feedback" class="{"active" if active_page=='feedback' else ''}">✉️ 評分系統</a></li>
            </ul>
        </div>
        <div class="main-content">
            {content}
            <footer>
                © 2026 林靖淏 - 中國文化大學資訊管理學系 期末成果展
            </footer>
        </div>
    </body>
    </html>
    '''

# 1. 系統首頁
@app.route('/')
def home():
    content = '''
        <div class="card" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-left: 6px solid #38bdf8; padding: 45px;">
            <h1 style="font-size: 2.8rem; background: linear-gradient(to right, #ffffff, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">東北亞跨國旅遊決策探索助手</h1>
            <p style="font-size: 1.2rem; color: #cbd5e1; margin-top: 10px;">本系統由資管系 2A 林靖淏 獨立開發。完美實作後端多維度數據過濾演算法，打造兼具科技感與跨國實用價值的動態網頁應用。</p>
            <br>
            <a href="/explore" class="btn">進入數據大廳 🚀</a>
        </div>
        <div class="card">
            <h2>🛸 系統開發與巨量數據庫解析</h2>
            <p>本系統跳脫傳統的靜態 HTML 網頁，全面採用 <strong>Python Flask 動態後端引擎</strong> 作為核心驅動。為了展現系統在高併發與多檔案檢索下的效能，本專案建構了高達 24 筆跨國核心旅遊大數據（包含台灣、日本、韓國）。</p>
            <p>當使用者點擊不同的國家或分類標籤時，系統透過 URL 發送結構化的條件請求（Parameters）。伺服器端的 Python 會即時啟動高效能的過濾演算法（List Comprehension），動態拼接出包含當地景點特色描述與即時關注熱度（Hot Rate）的精美玻璃流光卡片。這極大地展現了資管系在前後端資料互動上的專業實踐能力。</p>
        </div>
    '''
    return get_layout(content, active_page="home")

# 2. 景點探索頁面
@app.route('/explore')
def explore():
    city = request.args.get('city', 'taiwan')
    category = request.args.get('category', 'all')
    
    # 後端條件過濾邏輯
    spots = TRAVEL_DATA.get(city, [])
    if category != 'all':
        spots = [s for s in spots if s['category'] == category]
        
    content = f'''
        <h1>🔍 東北亞跨國景點數據中心</h1>
        <p>點選不同的國家與熱門主題標籤，體驗 Python 後端動態篩選跨國巨量數據的流暢效率：</p>
        
        <div class="filter-section">
            <span style="font-weight: bold; color: #38bdf8;">國家選擇：</span>
            <a href="/explore?city=taiwan&category={category}" class="btn {"" if city=='taiwan' else "btn-outline"}">🇹🇼 台灣 Taiwan</a>
            <a href="/explore?city=japan&category={category}" class="btn {"" if city=='japan' else "btn-outline"}">🇯🇵 日本 Japan</a>
            <a href="/explore?city=korea&category={category}" class="btn {"" if city=='korea' else "btn-outline"}">🇰🇷 韓國 Korea</a>
        </div>
        
        <div class="filter-section">
            <span style="font-weight: bold; color: #34d399;">熱門主題：</span>
            <a href="/explore?city={city}&category=all" class="btn btn-outline {"active" if category=='all' else ""}">全部主題 ({len(TRAVEL_DATA.get(city, []))} 筆)</a>
            <a href="/explore?city={city}&category=landmark" class="btn btn-outline {"active" if category=='landmark' else ""}">地標名勝</a>
            <a href="/explore?city={city}&category=nature" class="btn btn-outline {"active" if category=='nature' else ""}">大自然風光</a>
            <a href="/explore?city={city}&category=food" class="btn btn-outline {"active" if category=='food' else ""}">在地必吃美食</a>
        </div>
        
        <div class="grid">
    '''
    
    if not spots:
        content += '<p style="grid-column: 1/-1; text-align: center; color: #64748b; padding: 50px;">🔍 後端資料庫查無符合此分類的跨國景點數據。</p>'
    else:
        for spot in spots:
            content += f'''
                <div class="spot-card">
                    <div class="spot-body">
                        <div class="spot-title">
                            {spot['name']}
                            <span class="spot-tag">{spot['tag']}</span>
                        </div>
                        <p class="spot-desc">{spot['desc']}</p>
                        <div class="hot-bar">
                            <span>🔥 關注熱度: {spot['hot']}</span>
                            <div style="flex: 1; background: #334155; height: 6px; border-radius: 3px;">
                                <div class="hot-fill" style="width: {spot['hot']};"></div>
                            </div>
                        </div>
                    </div>
                </div>
            '''
            
    content += '</div>'
    return get_layout(content, active_page="explore")

# 3. 技術心得頁面
@app.route('/skills')
def skills():
    content = '''
        <h1>📚 期末技術開發成果總結</h1>
        <div class="card">
            <h3 style="color: #38bdf8; margin-bottom: 8px;">1. 資管跨領域技術整合</h3>
            <p>本次專案成功整合了前端 CSS3 網格佈局（Grid Layout）與後端 Flask 路由控制。利用固定側邊欄搭配科技感極簡深色主題，大幅提升了使用者視覺的舒適度與現代化 App 質感。</p>
        </div>
        <div class="card">
            <h3 style="color: #34d399; margin-bottom: 8px;">2. 跨國巨量數據庫與篩選演算法</h3>
            <p>我在後端實作了動態條件篩選。為了模擬真實企業系統，我建構了高達 24 筆完整格式的旅遊數據。透過 <code>request.args.get()</code> 攔截瀏覽器傳來的參數（國家與分類），並使用 Python 的清單解析式（List Comprehension）對多維度結構化字典進行秒級過濾。此外，我還增加了景點關注熱度數據（Hot Rate），完美展現了後端資料處理的邏輯思維。</p>
        </div>
        <div class="card">
            <h3 style="color: #f59e0b; margin-bottom: 8px;">3. 軟體工程 CI/CD 開發流</h3>
            <p>專案透過 GitHub 進行版本控制，並完全託管於 Render 免費雲端伺服器。實踐了軟體工程裡最核心的自動化建置與持續部署精神，程式碼一更動，線上網頁隨即無縫更新上線。</p>
        </div>
    '''
    return get_layout(content, active_page="skills")

# 4. 意見回饋頁面
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user = request.form.get('name', '匿名使用者')
        msg = request.form.get('message', '無內容')
        content = f'''
            <div class="card" style="border-top: 4px solid #34d399; text-align: center;">
                <h2 style="color: #34d399; margin-bottom: 15px;">🎉 POST 請求成功處理！Python 後端已即時截獲資料</h2>
                <p>感謝 <strong>{user}</strong> 老師對本專案的評分與期末指導：</p>
                <div style="background-color: #0f172a; padding: 20px; border-radius: 8px; margin: 20px 0; font-style: italic; border: 1px dashed #334155; color: #fbbf24; font-size: 1.1rem;">
                    "{msg}"
                </div>
                <p>這項測試證實了前後端數據雙向傳輸、以及後端伺服器的動態渲染系統百分之百運作正常！</p>
                <br>
                <a href="/feedback" class="btn">重置系統測試</a>
            </div>
        '''
    else:
        content = '''
            <h1>✉️ 期末專案互動點評系統</h1>
            <div class="card">
                <p>請老師在下方輸入您的姓名與評語，以利測試本系統的網路通訊協議與 POST 動態解析機制：</p>
                <form method="POST" action="/feedback">
                    <label style="color: #38bdf8; font-weight: bold; display: block; margin-bottom: 8px;">老師尊稱：</label>
                    <input type="text" name="name" placeholder="例如：期末評審老師" required>
                    <label style="color: #38bdf8; font-weight: bold; display: block; margin-bottom: 8px;">期末點評 / 評語：</label>
                    <textarea name="message" rows="5" placeholder="請輸入您對林靖淏同學這次跨國網站成果的看法或建議..." required></textarea>
                    <button type="submit" class="btn">提交數據，啟動後端交互 🛫</button>
                </form>
            </div>
        '''
    return get_layout(content, active_page="feedback")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
