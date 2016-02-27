from rcblog import handlers


def main():
    handlers.app.run(host='0.0.0.0', debug=True)
