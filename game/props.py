class Prop:
    def __init__(self, visible=True):
        self.visible = visible


class Ladder(Prop):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "L"
