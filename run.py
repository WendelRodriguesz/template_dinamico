from app.main import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5057, debug=True)
