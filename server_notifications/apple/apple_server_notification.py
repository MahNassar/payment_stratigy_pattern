from server_notifications.server_gatway_interface import IPaymentServerGateway, SubscriptionInfo
from server_notifications.constant import BILLING_ACTIONS

import json
import base64


class AppleServer(IPaymentServerGateway):

    def get_subscription_info(self, request):
        subscription_info = SubscriptionInfo()
        # envelope = json.loads(request.data.decode('utf-8'))
        subscription_info.server_payment_gateway = "apple"
        # Map Data ...

        envelope = request
        if envelope:
            subscription_info.original_request = envelope
            subscription_info.purchase_token = envelope['latest_receipt_info']['original_transaction_id']
            subscription_info.plan_package = envelope['auto_renew_product_id']

            notification_type = envelope["notification_type"]
            if notification_type == "RENEWAL" or notification_type == "INTERACTIVE_RENEWAL":  # 2. An active subscription was renewed.
                subscription_info.action = BILLING_ACTIONS["RENEW"]
            elif notification_type == "CANCEL":  # 3. Sent for both voluntary and involuntary cancellation.
                subscription_info.action = BILLING_ACTIONS[
                    "UNSUB"]  # For voluntary cancellation, sent when the user cancels.
            else:  # Un supported notification type
                subscription_info.action = None

        return subscription_info

    def validate(self):
        return True
