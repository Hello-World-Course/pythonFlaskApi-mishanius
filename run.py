from app import create_app

# This is the entry point to your application

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
