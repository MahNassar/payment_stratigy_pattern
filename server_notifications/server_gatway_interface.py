import abc


class SubscriptionInfo:
    action = plan_package = purchase_token = original_request = server_payment_gateway = None

    def __init__(self):
        pass


class IPaymentServerGateway:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self):
        pass

    @abc.abstractmethod
    def get_subscription_info(self, request):
        pass
