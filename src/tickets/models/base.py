from sqlmodel import SQLModel, Field


class BaseDBModel(SQLModel):
    __tablename__ = "tickets"

    id: int | None = Field(default=None, primary_key=True)
