from strategy.payment_gateway_interface import IPaymentGateway
import json
import requests


class Spreedly(IPaymentGateway):
    """
    Implement the Spereedly algorithm using the Strategy interface.
    """
    user_id = ""
    success_ids = []
    failed_ids = []
    success_count = failed_count = gateway_failure = 0

    def __init__(self):
        with open('strategy/payment_gateways_settings.json') as f:
            self._settings = json.load(f)

    def pay(self, payment_info):
        endpoint = self._settings['spreedly']['api_url']

        output = {"spreedly": {"result": {}, "server_response": {}}}
        output['spreedly']['sent_data'] = payment_info
        output['spreedly']['result']['response'] = "response=3&transactionid=Not provided"
        output['spreedly']['result']['success'] = False
        output['spreedly']['result']['server_status'] = "Failed"
        try:
            response = requests.post(endpoint, data=payment_info)
            status_code = response.status_code
            response = response.json()
            output['spreedly']['server_response'] = response
            if status_code == 200:
                output['spreedly']['result']['server_status'] = "OK"

            if response['success']:
                payment_action, rep_txt = self.get_response_action(response)
                if str(payment_action) == "1":
                    output['spreedly']['result']['response'] = response.get('response', None)
                    output['spreedly']['result']['success'] = True

                    self.success_count = self.success_count + 1
                    self.success_ids.append(self.user_id)
                else:
                    self.failed_count = self.failed_count + 1
                    self.failed_ids.append(self.user_id)
                    error_response_code = ["502", "500", "504", "501", "503"]
                    if str(payment_action) in error_response_code:
                        output['spreedly']['result']['server_status'] = 'Failed'
                        self.gateway_failure = self.gateway_failure + 1
                    output['spreedly']['result']['response'] = response.get('response', None)
            return output
        except:
            self.failed_ids.append(self.user_id)
            self.gateway_failure = self.gateway_failure + 1
            return output

    def parse_payment_info(self, payment_data):
        self.user_id = payment_data.user_email
        return {
            'order_id': payment_data.order_id,
            'amount': str(payment_data.price),
            'payment_method_token': payment_data.payment_token
        }

    def get_response_action(self, result):
        response = result.get('response', "")
        response_data = self.convert_response(response)
        action_code = response_data.get('response', "")
        rep_text = response_data.get('responsetext', "")
        return action_code, rep_text

    def convert_response(self, response):
        response_dect = {}
        response_data = response.split('&')
        for item in response_data:
            item_data = item.split('=')
            response_dect[item_data[0]] = item_data[1]
        return response_dect
