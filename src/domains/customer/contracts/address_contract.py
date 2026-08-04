from dataclasses import dataclass


@dataclass
class AddressContext:
    customer_id: str
    address_type: str
    line1: str

    city: str | None = None
    township: str | None = None
    phone: str | None = None
