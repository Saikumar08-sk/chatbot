from twilio.rest import Client
from wyn_agent_x.helper import register_function

@register_function("send_sms")
def send_sms(payload, secrets, event_stream):
    print(f"[DEBUG] MOCKED SMS send_sms triggered with: {payload}")
    return {"message": f"MOCK SMS to {payload['phone_number']}: {payload['message']}"}
    try:
        account_sid = secrets["account_sid"]
        auth_token = secrets["auth_token"]
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=payload["message"],
            from_='+18777804236',
            to=payload["phone_number"]
        )

        return {"message": f"✅ SMS sent to {payload['phone_number']}"}

    except Exception as e:
        return {"message": f"❌ Twilio error: {str(e)}"}
