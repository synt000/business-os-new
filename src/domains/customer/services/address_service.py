class CustomerAddressService:
    """
    Customer address capability boundary.

    Core customer domain only.
    Industry layers consume this contract.
    """

    def create_address(self, context):
        raise NotImplementedError

    def get_customer_addresses(self, customer_id: str):
        raise NotImplementedError

    def set_default_address(
        self,
        customer_id: str,
        address_id: str
    ):
        raise NotImplementedError
