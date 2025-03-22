# app.py

from flask import Flask 

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def home():
        return 'Hey Guys ! This is my python App1'

    return app

    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80, debug=True)
