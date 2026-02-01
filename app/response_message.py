from linebot.v3.messaging import TextMessage

def response_message(event):
    request_message = event.message.text
    print(request_message)
    return TextMessage(text = f"hello from response_message.py, you said: {request_message}")