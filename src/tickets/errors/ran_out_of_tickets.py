class RanOutOfTicketsError(ValueError):
    def __init__(self, *args, race_id: str | None = None):
        super().__init__(*args)
        self.race_id = race_id
