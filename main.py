from strategy.payment_context import PaymentContext, PaymentData
from strategy.spreedly_gateway import Spreedly
from strategy.greenpay_gateway import Greenpay

payment_with_spereedly = Spreedly()
payment_with_greenpay = Greenpay()
context = PaymentContext([payment_with_spereedly, payment_with_greenpay])

payment_data = PaymentData()
payment_data.order_id = "11111"
payment_data.price = 5
payment_data.payment_token = "dddddddddd"
payment_data.user_hash = "hashhhhhhhhhhhhhhhhh"
payment_data.currency = "EGP"
payment_data.user_name = "Nassar"
payment_data.user_email = "teststts@mmmm.com"
context.pay(payment_data)
#
# for x in range(10):
#     payment_data.order_id = "11111%d" % x
#     payment_data.price = 5
#     payment_data.payment_token = "dddddddddd%d" % x
#     payment_data.user_hash = "hashhhhhhhhhhhhhhhhh%d" % x
#     payment_data.currency = "EGP"
#     payment_data.user_name = "Nassar%d" % x
#     payment_data.user_email = "teststts@mmmm.com%d" % x
#     context.pay(payment_data)
#
# print "============================= REPORT =========================="
#
# context.get_payment_report("")
