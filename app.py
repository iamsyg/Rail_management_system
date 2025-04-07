from threading import Thread
from website.user.server import app as user_app

def run_user():
    user_app.run(port=5001, debug=True, use_reloader=False)


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # Needed for Windows

    Thread(target=run_user).start()
