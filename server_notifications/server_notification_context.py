from object_builder import Build


class PaymentServer:
    payment_gateway_server = None

    def __init__(self, payment_gateway_server):
        object_builder = Build(payment_gateway_server)
        self.payment_gateway_server = object_builder.create_object()

    def get_subscription_info(self, request):
        if self.payment_gateway_server is None:
            return "error"

        if not (self.payment_gateway_server.validate()):
            return "validation_error"

        subscription_info = self.payment_gateway_server.get_subscription_info(request)
        return subscription_info.__dict__

    def log_info(self, subscription_info):
        # ToDo Log information in file
        pass
