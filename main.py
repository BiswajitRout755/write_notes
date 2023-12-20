from WEBSITE import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


#both auth and views blueprint have different url_routes