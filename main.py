from app import App, Logic
import csv_utils


def main():
    credentials = csv_utils.read(".env")
    print(credentials)
    world_app = App()
    world_app_logic = Logic(world_app,credentials)

    world_app.mainloop()

if __name__ == "__main__":
    main()