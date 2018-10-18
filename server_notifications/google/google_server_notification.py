from server_notifications.server_gatway_interface import IPaymentServerGateway, SubscriptionInfo
from server_notifications.constant import BILLING_ACTIONS

import json
import base64


class GoogleServer(IPaymentServerGateway):

    def get_subscription_info(self, request):
        subscription_info = SubscriptionInfo()
        # envelope = json.loads(request.data.decode('utf-8'))
        subscription_info.server_payment_gateway = "google"
        # Map Data ...

        envelope = request
        if envelope:
            message_data = base64.b64decode(envelope['message']['data'])
            payload = json.loads(message_data.decode('utf-8'))

            subscription_info.original_request = envelope
            subscription_info.purchase_token = payload['subscriptionNotification']['purchaseToken']
            subscription_info.plan_package = payload['subscriptionNotification']['subscriptionId']

            notification_type = payload['subscriptionNotification']['notificationType']
            if notification_type == 2:  # 2. An active subscription was renewed.
                subscription_info.action = BILLING_ACTIONS["RENEW"]
            elif notification_type == 3:  # 3. Sent for both voluntary and involuntary cancellation.
                subscription_info.action = BILLING_ACTIONS[
                    "UNSUB"]  # For voluntary cancellation, sent when the user cancels.
            else:  # Un supported notification type
                subscription_info.action = None

        return subscription_info

    def validate(self):
        return True
