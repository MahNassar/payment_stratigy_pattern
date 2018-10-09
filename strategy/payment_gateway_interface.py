import abc


class IPaymentGateway:
    __metaclass__ = abc.ABCMeta
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    """

    @abc.abstractmethod
    def pay(self, payment_info):
        pass

    @abc.abstractmethod
    def parse_payment_info(self, record):
        pass
