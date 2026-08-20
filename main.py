from app import App, Logic


def main():
    world_app = App()
    world_app_logic = Logic(world_app)

    world_app.mainloop()

if __name__ == "__main__":
    main()