class PaymentData:
    user_name = user_email = payment_token = order_id = user_hash = user_order = price = currency = None

    def __init__(self):
        pass


class PaymentContext:
    """
    Define the interface of interest to clients.
    Maintain a reference to a Strategy object.
    """

    def __init__(self, payment_gateways):
        # check if strategy list ....
        if type(payment_gateways) != 'list':
            print("Nooooooo")
        else:
            self._paymentGateways = payment_gateways

    def pay(self, payment_data):
        # check payment_data instance of  PaymentData
        final_output = {"user_id": payment_data.user_email, "success_gateway": {}}
        for paymentGateway in self._paymentGateways:
            payment_info = paymentGateway.parse_payment_info(payment_data)
            gatway_output = paymentGateway.pay(payment_info)
            final_output.update(gatway_output)
            gateway_status, gateway_response, gateway_name = self.check_payment_states(paymentGateway, gatway_output)
            if gateway_status:
                final_output['success_gateway']['gateway_name'] = gateway_name
                final_output['success_gateway']['gateway_response'] = gateway_response
                break
        print(final_output)

    def check_payment_states(self, payment_gateway, result):
        payment_name = payment_gateway.__class__.__name__.lower()
        return result[payment_name]['result']['success'], result[payment_name]['result']['response'], payment_name

    def logger_payment_info(self):
        # todo put it in file
        pass

    def get_payment_report(self, users_report):
        # todo put it in file
        report = {"users_report": users_report, "spreedly": {}, "greenpay": {}}
        for paymentGateway in self._paymentGateways:
            payment_name = paymentGateway.__class__.__name__.lower()
            report[payment_name]['success_count'] = paymentGateway.success_count
            report[payment_name]['failed_count'] = paymentGateway.failed_count
            report[payment_name]['gateway_failure'] = paymentGateway.gateway_failure
            report[payment_name]['success_ids'] = paymentGateway.success_ids
            report[payment_name]['failed_ids'] = paymentGateway.failed_ids
        print(report)
