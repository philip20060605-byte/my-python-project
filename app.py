import os
from flask import Flask, request

app = Flask(__name__)

# 共同的 HTML 頭部結構與 CSS 樣式
def get_header(title):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ font-family: "Segoe UI", Arial, sans-serif; background-color: #f0f2f5; color: #333; line-height: 1.6; }}
            nav {{ background-color: #2c3e50; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            nav a {{ color: white; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem; transition: color 0.3s; }}
            nav a:hover {{ color: #3498db; }}
            .container {{ max-width: 800px; margin: 4px auto; padding: 40px 20px; }}
            .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; border-left: 5px solid #3498db; }}
            h1 {{ color: #2c3e50; margin-bottom: 20px; font-size: 2.2rem; }}
            h2 {{ color: #34495e; margin-top: 20px; margin-bottom: 10px; }}
            h3 {{ color: #2c3e50; margin-bottom: 10px; font-size: 1.3rem; }}
            p {{ margin-bottom: 15px; color: #555; font-size: 1.1rem; text-align: justify; }}
            ul {{ margin-left: 20px; margin-bottom: 15px; color: #666; }}
            li {{ margin-bottom: 5px; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; transition: background 0.3s; border: none; cursor: pointer; }}
            .btn:hover {{ background-color: #2980b9; }}
            .skills {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; }}
            .skill-tag {{ background: #e1f5fe; color: #0288d1; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; }}
            footer {{ text-align: center; padding: 20px; color: #7f8c8d; font-size: 0.9rem; margin-top: 40px; }}
            input, textarea {{ width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }}
        </style>
    </head>
    <body>
        <nav>
            <a href="/">🏠 首頁導覽</a>
            <a href="/about">👨 關於林靖淏</a>
            <a href="/skills">📚 學習心得</a>
            <a href="/contact">✉️ 互動聯絡</a>
        </nav>
        <div class="container">
    '''

def get_footer():
    return '''
        </div>
        <footer>
            © 林靖淏 - 中國文化大學資管系 2A 期末成果展
        </footer>
    </body>
    </html>
    '''

# 1. 首頁路由
@app.route('/')
def home():
    html = get_header("林靖淏的期末成果首頁")
    html += '''
        <div class="card" style="text-align: center; border-left: none;">
            <h1>歡迎來到我的 Python 期末成果應用程式</h1>
            <p style="font-size: 1.3rem; color: #7f8c8d;">網頁開發、雲端部署與架構實踐</p>
            <hr style="margin: 20px 0; border: 0; border-top: 1px solid #eee;">
            <p>本網站由文化大學資管系 2A <strong>林靖淏</strong> 獨立開發完成。</p>
            <p>這是一個全動態的 Web 網站，前端採用響應式網頁設計（RWD），後端由 Python Flask 驅動，並透過自動化 CI/CD 機制完全託管於雲端平台。</p>
            <br>
            <a href="/about" class="btn">開始導覽網站 🚀</a>
        </div>
    '''
    html += get_footer()
    return html

# 2. 關於我路由
@app.route('/about')
def about():
    html = get_header("關於林靖淏")
    html += '''
        <div class="card">
            <h1>👨 關於開發者</h1>
            <h2>基本資料</h2>
            <p><strong>姓名：</strong>林靖淏</p>
            <p><strong>單位：</strong>中國文化大學 資訊管理學系 2A</p>
            <p><strong>專案主題：</strong>基於微型網頁框架的雲端服務部署實務</p>
            
            <h2>專業資管技能儲備</h2>
            <p>在資管系的跨領域學習中，我致力於將資訊技術應用於解決實際商務與系統問題，目前掌握的技術包括：</p>
            <div class="skills">
                <span class="skill-tag">Python 程式設計</span>
                <span class="skill-tag">Flask 網頁框架</span>
                <span class="skill-tag">Git & GitHub 版本控制</span>
                <span class="skill-tag">雲端架構部署 (PaaS)</span>
                <span class="skill-tag">HTML5 / CSS3 網頁設計</span>
            </div>
        </div>
    '''
    html += get_footer()
    return html

# 3. 學習心得路由 (★此次大幅擴充技術細節與心得，適合講述 5 分鐘以上★)
@app.route('/skills')
def skills():
    html = get_header("Python 學習心得成果")
    html += '''
        <h1>📚 本學期 Python 核心學習成果與架構心得</h1>
        <p style="color: #7f8c8d; margin-bottom: 30px;">在此頁面中，我將深入探討本專案開發過程中所涉及的核心技術與理論實踐：</p>
        
        <div class="card" style="border-left-color: #3498db;">
            <h3>核心知識一：後端邏輯與動態路由控制 (Routing)</h3>
            <p>在傳統的靜態網頁中，每一個頁面都需要一個獨立的 HTML 檔案，管理起來非常不方便。而透過本學期學到的 Python Flask 微型網頁框架，我學會了如何使用<strong>「路由裝飾器（Route Decorators）」</strong>來動態控制網頁行為。</p>
            <p>例如，當使用者連線到主網址、關於我、或是提交聯絡表單時，後端 Python 程式會自動進行事件監聽，並將請求分流給對應的視圖函式（View Functions）。這讓我深刻體會到資管系在軟體開發中所強調的「模組化設計」與「代碼高重用性」。</p>
        </div>
        
        <div class="card" style="border-left-color: #9b59b6;">
            <h3>核心知識二：HTTP 請求方法與前後端資料交互 (GET & POST)</h3>
            <p>這學期最重要的突破之一，就是理解了瀏覽器與伺服器之間是如何透過網路協議溝通的。在這個專案的『互動聯絡』功能中，我成功實作了雙向交互機制：</p>
            <ul>
                <li><strong>GET 請求：</strong>當使用者點擊頁面時，伺服器主動發送精美的表單介面供使用者檢視。</li>
                <li><strong>POST 請求：</strong>當使用者輸入完姓名、評語並按下送出，Python 後端會利用 <code>request.form</code> 接收資料並動態處理，不需要刷新整個網頁，就能給予使用者即時的回饋。這對於未來學習電子商務系統或資料庫互動打下了扎實的基礎。</li>
            </ul>
        </div>
        
        <div class="card" style="border-left-color: #e67e22;">
            <h3>核心知識三：生產環境與雲端環境適應性 (WSGI Server)</h3>
            <p>在本地端電腦測試時，我們通常只使用 Flask 內建的測試伺服器。但在資管的系統管理視角中，系統必須具備高併發與穩定性。因此在部署到 Render 雲端平台時，我引入了 <strong>Gunicorn（WSGI 伺服器）</strong>。</p>
            <p>此外，雲端主機的外網連接埠（Port）是系統動態隨機分配的。為了修正這個問題，我特別在主程式利用 <code>os.environ.get('PORT')</code> 來讀取系統環境變數。這個調優的經驗讓我明白，寫好程式只是第一步，如何讓系統適應不同的生產環境才是工程師的考驗。</p>
        </div>
        
        <div class="card" style="border-left-color: #2ecc71;">
            <h3>核心知識四：DevOps 雲端自動化整合與部署 (CI/CD)</h3>
            <p>最後，是關於開發工具鏈的整合。本專案完全顛覆了傳統本地開發的繁瑣。我透過 GitHub 網頁版管理所有的原始碼（`app.py`、`requirements.txt`、`Procfile`），並利用 Webhook 整合技術與 Render 免費雲端平台進行連動。</p>
            <p>這達成了一種現代軟體開發非常推崇的 <strong>CI/CD（持續整合/持續部署）</strong> 精神。這意味著未來我只要在 GitHub 上進行任何程式碼的修改或優化，雲端伺服器在幾秒鐘內就會自動抓取、自動建置、自動上線，大大降低了維運的成本，讓我對雲端運算的威力有了第一線的認識。</p>
        </div>
    '''
    html += get_footer()
    return html

# 4. 互動聯絡路由 (包含 GET 和 POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    html = get_header("互動聯絡表單")
    if request.method == 'POST':
        teacher_name = request.form.get('name', '老師')
        feedback = request.form.get('message', '無建議')
        html += f'''
            <div class="card" style="border-left: 5px solid #2ecc71;">
                <h2 style="color: #2ecc71;">🎉 表單提交成功！後端 Python 已成功接收資料</h2>
                <br>
                <p><strong>感謝 {teacher_name} 老師的指導！</strong></p>
                <p><strong>您留下的評語或建議：</strong></p>
                <div style="background: #f9f9f9; padding: 15px; border-radius: 6px; margin: 10px 0; border: 1px dashed #ccc;">
                    {feedback}
                </div>
                <p>這證明了我們的後端表單處理系統（POST 請求機制）運作完全正常！</p>
                <br>
                <a href="/contact" class="btn" style="background-color: #e74c3c;">重新填寫</a>
            </div>
        '''
    else:
        html += '''
            <div class="card" style="border-left-color: #e74c3c;">
                <h1>✉️ 互動成果評分表單</h1>
                <p>老師好！請在下方輸入您的姓名與對本網站專案的評語或點評，點擊送出後，網頁將展示 Python 後端即時接收並動態渲染資料的成果：</p>
                <form method="POST" action="/contact">
                    <label><strong>您的姓名：</strong></label>
                    <input type="text" name="name" placeholder="例如：期末評審老師" required>
                    
                    <label><strong>給予林靖淏的期末評語 / 建議：</strong></label>
                    <textarea name="message" rows="5" placeholder="請輸入您對這個雲端網站的看法..." required></textarea>
                    
                    <button type="submit" class="btn">送出表單，測試後端功能 🛫</button>
                </form>
            </div>
        '''
    html += get_footer()
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
