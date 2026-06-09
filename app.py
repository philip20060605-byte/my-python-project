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
            .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            h1 {{ color: #2c3e50; margin-bottom: 20px; font-size: 2.2rem; }}
            h2 {{ color: #34495e; margin-top: 20px; margin-bottom: 10px; }}
            p {{ margin-bottom: 15px; color: #555; font-size: 1.1rem; }}
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
        <div class="card" style="text-align: center;">
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

# 3. 學習心得路由
@app.route('/skills')
def skills():
    html = get_header("Python 學習心得成果")
    html += '''
        <h1>📚 本學期 Python 核心學習成果</h1>
        <p>在這次的專題開發中，我將這學期學到的三大核心知識做了整合：</p>
        
        <div class="card">
            <h3>1. 後端邏輯與路由控制 (Routing)</h3>
            <p>理解伺服器如何接收瀏覽器的 HTTP 請求，並透過 Python 的裝飾器功能，精準地將不同的網址（URL）分流給對應的函式處理，實現動態網頁的切換。</p>
        </div>
        
        <div class="card">
            <h3>2. 生產環境與雲端適應</h3>
            <p>學習到本地端測試環境（Development）與雲端生產環境（Production）的差異。透過調整動態連接埠（Port），讓網站能夠完美適應現代雲端主機的規範。</p>
        </div>
        
        <div class="card">
            <h3>3. DevOps 開發流程體驗</h3>
            <p>透過 GitHub 網頁管理程式碼，並與 Render 平台進行 webhook 連動。達成了「代碼即部署」的現代開發精神，省去了傳統繁瑣的伺服器架設時間。</p>
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
            <div class="card">
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
