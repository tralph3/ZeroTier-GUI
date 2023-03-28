from ZTService import ZTService
from view import View


class Controller():
    def __init__(self) -> None:
        self.zt_service = ZTService()
        self.view = View(self.zt_service)

    def main(self):
        self.view.main()


if __name__ == "__main__":
    Controller().main()
