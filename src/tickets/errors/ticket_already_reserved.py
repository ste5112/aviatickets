class TicketAlreadyReservedError(ValueError):
    def __init__(self, *args, ticket_id=None) -> None:
        super().__init__(*args)
        self.ticket_id = ticket_id
