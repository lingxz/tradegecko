from app import create_app, run, PoolHandler

app = create_app()
if __name__ == "__main__":
    # PoolHandler()  # uncomment this if using on windows
    run()
