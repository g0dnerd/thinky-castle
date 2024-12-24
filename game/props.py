class Prop:
    def __init__(self):
        self.visible = True


class Ladder(Prop):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "L"
