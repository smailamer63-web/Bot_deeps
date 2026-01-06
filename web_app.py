from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json

app = Flask(__name__)

# بيانات وهمية (استبدلها بقاعدة بيانات حقيقية)
users_db = {}

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Telegram Web App</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 500px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            input, button {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                background: #4CAF50;
                color: white;
                cursor: pointer;
                font-weight: bold;
            }
            .data-box {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 15px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Telegram Web App</h1>
            <p>املأ النموذج وأرسل البيانات إلى البوت:</p>
            
            <form id="dataForm">
                <input type="text" id="name" placeholder="اسمك" required>
                <input type="email" id="email" placeholder="بريدك الإلكتروني" required>
                <input type="text" id="phone" placeholder="رقم الهاتف">
                <button type="submit">📤 إرسال إلى البوت</button>
            </form>
            
            <div id="result" class="data-box" style="display:none;">
                <h3>✅ تم الإرسال!</h3>
                <p>ارجع إلى البوت لرؤية البيانات</p>
            </div>
        </div>
        
        <script>
            // Telegram Web App initialization
            let tg = window.Telegram.WebApp;
            tg.expand();
            tg.MainButton.setText("فتحت Web App").show();
            
            document.getElementById('dataForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const data = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    timestamp: new Date().toISOString()
                };
                
                // إرسال البيانات إلى البوت
                tg.sendData(JSON.stringify(data));
                
                // إظهار رسالة النجاح
                document.getElementById('result').style.display = 'block';
                document.getElementById('dataForm').reset();
                
                // إغلاق Web App بعد 2 ثانية
                setTimeout(() => {
                    tg.close();
                }, 2000);
            });
            
            // إذا كان هناك بيانات من Telegram
            if (tg.initDataUnsafe.user) {
                const user = tg.initDataUnsafe.user;
                document.getElementById('name').value = user.first_name || '';
            }
        </script>
    </body>
    </html>
    """

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    user_id = data.get('user_id')
    users_db[user_id] = data
    return jsonify({"status": "success", "user_id": user_id})

@app.route('/user/<user_id>')
def show_user_data(user_id):
    data = users_db.get(user_id, {})
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
