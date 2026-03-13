from flask import Flask, request

app = Flask(__name__)

# Y2K 크롬 텍스처 & 사이버펑크 감성 CSS
COMMON_HTML_HEAD = """
<head>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            margin-top: 30px;
        }
        .chrome-title {
            background: linear-gradient(to bottom, #ffffff 0%, #a9a9a9 40%, #505050 50%, #e0e0e0 60%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5em;
            font-weight: 900;
            margin-bottom: 5px;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        }
        .nav-bar {
            margin: 20px 0;
            border-top: 1px solid #00ff00;
            border-bottom: 1px solid #00ff00;
            padding: 10px;
        }
        .nav-bar a {
            color: #ff00ff;
            text-decoration: none;
            font-weight: bold;
            margin: 0 15px;
            font-size: 1.2em;
        }
        .nav-bar a:hover {
            color: #fff;
            background-color: #ff00ff;
        }
        .content-box {
            border: 1px dotted #00ff00;
            width: 60%;
            margin: 0 auto;
            padding: 20px;
            text-align: left;
            background: rgba(0, 255, 0, 0.05);
        }
        input, textarea {
            background-color: #111;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 5px;
            width: 90%;
            font-family: 'Courier New', Courier, monospace;
            margin-bottom: 10px;
        }
        button {
            background-color: #000;
            color: #00ff00;
            border: 2px solid #00ff00;
            padding: 5px 15px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #00ff00;
            color: #000;
        }
    </style>
</head>
"""

# 네비게이션 바 (공통)
NAV_BAR = """
<div class="nav-bar">
    <a href="/home">[ HOME ]</a>
    <a href="/write">[ WRITE ]</a>
    <a href="/guestbook">[ GUESTBOOK ]</a>
</div>
"""

# 1. 홈 페이지 (글 목록)
@app.route('/')
@app.route('/home')
def home():
    return COMMON_HTML_HEAD + f"""
    <body>
        <div class="chrome-title">BOB'S CYBER LOG</div>
        <marquee style="color: silver; width: 60%;">>>> WELCOME TO THE YEAR 2000 <<<</marquee>
        {NAV_BAR}
        <div class="content-box">
            <h3 style="color: #ff00ff;">>>> Recent Logs</h3>
            <ul>
                <li>[2026-03-13] SYSTEM INITIALIZED. Hello World.</li>
                <li>[2026-03-12] Thinking about the stock market...</li>
                <li>[2026-03-10] Studying Git branching strategies.</li>
            </ul>
        </div>
    </body>
    """

# 2. 글쓰기 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        return COMMON_HTML_HEAD + f"""
        <body>
            <div class="chrome-title">DATA UPLOADED</div>
            {NAV_BAR}
            <div class="content-box" style="text-align: center;">
                <h3>Upload Success!</h3>
                <p>Post "<b>{title}</b>" has been saved to the mainframe.</p>
                <a href="/home" style="color: #ff00ff;">RETURN TO HOME</a>
            </div>
        </body>
        """
    
    return COMMON_HTML_HEAD + f"""
    <body>
        <div class="chrome-title">NEW LOG ENTRY</div>
        {NAV_BAR}
        <div class="content-box">
            <form action="/write" method="post">
                <label>TITLE:</label><br>
                <input type="text" name="title" required><br><br>
                <label>CONTENT:</label><br>
                <textarea name="content" rows="6" required></textarea><br><br>
                <button type="submit">TRANSMIT DATA</button>
            </form>
        </div>
    </body>
    """

# 3. 방명록 페이지
@app.route('/guestbook')
def guestbook():
    return COMMON_HTML_HEAD + f"""
    <body>
        <div class="chrome-title">GUESTBOOK</div>
        {NAV_BAR}
        <div class="content-box">
            <h3 style="color: #ff00ff;">>>> Leave a Trace</h3>
            <form action="/guestbook" method="get">
                <input type="text" placeholder="Visitor Name" style="width: 30%;"><br>
                <input type="text" placeholder="Drop a line..." style="width: 60%;">
                <button type="submit">SIGN</button>
            </form>
            <hr style="border: 1px dashed #00ff00;">
            <p><b>[CyberSurfer99]</b>: Cool chrome effect!</p>
            <p><b>[Neo]</b>: Follow the white rabbit.</p>
        </div>
    </body>
    """

if __name__ == '__main__':
    app.run(debug=True)