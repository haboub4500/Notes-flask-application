from website import create_app

app = create_app()

if __name__ == '__main__': # only if we run this file the app will run
    app.run(debug=True) # every time we make a change to the code it s gonna rerun automatically
