from strategy.payment_gateway_interface import IPaymentGateway
import json
import requests


class Greenpay(IPaymentGateway):
    """
        Implement the Greenpay algorithm using the Strategy interface.
    """
    user_id = ""
    success_ids = []
    failed_ids = []
    success_count = failed_count = gateway_failure = 0

    def __init__(self):
        with open('strategy/payment_gateways_settings.json') as f:
            self._settings = json.load(f)

    def pay(self, payment_info):
        endpoint = self._settings['greenpay']['api_url']

        output = {"greenpay": {"result": {}}}
        output['greenpay']['sent_data'] = payment_info
        output['greenpay']['result']['response'] = "response=3&transactionid=Not provided"
        output['greenpay']['result']['success'] = False
        output['greenpay']['result']['server_status'] = "Failed"
        try:
            response = requests.post(endpoint, data=payment_info)
            status_code = response.status_code

            if status_code == 200:
                output['greenpay']['server_status'] = "OK"
            if response['success']:
                payment_action, rep_txt, ret_ref_num = self.get_response_action(response)
                if str(payment_action) == "00":
                    output['greenpay']['result']['response'] = "response=1&transactionid=" + str(ret_ref_num)
                    output['greenpay']['result']['server_status'] = "OK"
                    output['greenpay']['result']['success'] = True

                    self.success_count = self.success_count + 1
                    self.success_ids.append(self.user_id)


                else:
                    self.failed_count = self.failed_count + 1
                    self.failed_ids.append(self.user_id)

                    error_response_code = ["502", "500", "504", "501", "503"]
                    if str(payment_action) in error_response_code:
                        output['greenpay']['result']['server_status'] = 'Failed'
                        self.gateway_failure = self.gateway_failure + 1
                    output['greenpay']['result']['response'] = "response=2&transactionid=" + str(ret_ref_num)
            return output
        except:
            self.failed_ids.append(self.user_id)
            self.gateway_failure = self.gateway_failure + 1
            return output

    def parse_payment_info(self, payment_data):
        self.user_id = payment_data.user_email
        return {
            'order_reference': payment_data.order_id,
            'amount': str(payment_data.price),
            'hash': payment_data.user_hash,
            'currency': payment_data.currency,
            'description': "green pay order amount:{}, currency:{} for use name{}".format(str(payment_data.price),
                                                                                          payment_data.currency,
                                                                                          payment_data.user_name),
            'card_holder': payment_data.user_name,
        }

    def get_response_action(self, result):
        action_code = rep_text = ret_ref_num = ""
        response = result.get('response', "")
        action_code = response.get('result', None)
        if action_code:
            rep_text = action_code.get('reserved_private4', "")
            ret_ref_num = action_code.get('retrieval_ref_num')
            action_code = action_code.get('resp_code', "")
        else:
            action_code = result.get('status', None)

        return action_code, rep_text, ret_ref_num
