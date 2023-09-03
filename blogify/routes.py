from blogify import app

@app.route('/')
def home():
    return "<p>Hello World</p>"