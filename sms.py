import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
ASSORT_HEALTH_NUMBER = '+18445490474'


def send_sms(phoneNumber, assessment):
    textString = 'Hi ' f'{assessment.name},\n' \
                 + "Your appointment with " + f'{assessment.doctor}' + ' is on ' + assessment.appointment_time + "."
    message = client.messages \
        .create(
        body=textString,
        from_=ASSORT_HEALTH_NUMBER,
        to=phoneNumber
    )
