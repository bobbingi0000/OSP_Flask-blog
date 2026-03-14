from flask import Flask, render_template, request

app = Flask(__name__)

# 1. 홈 페이지 (글 목록)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# 2. 글쓰기 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        # Here we would normally save to db, ignoring for now as per original code
        return render_template('write.html', title=title)
    
    return render_template('write.html')

# 3. 방명록 페이지
@app.route('/guestbook')
def guestbook():
    return render_template('guestbook.html')

if __name__ == '__main__':
    app.run(debug=True)
