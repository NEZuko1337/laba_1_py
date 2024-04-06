from dataclasses import dataclass


@dataclass
class Item:
    store_id: int | str | None
    provider_id: int | str | None
    name: str
    cost: float

    def __str__(self):
        return self.name
