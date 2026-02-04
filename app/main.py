import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, Header

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent,ImageMessageContent
from linebot.v3.messaging import MessagingApiBlob


from ocr import analyze_slip, delect_image

from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest, 
    TextMessage, 
    # FlexMessage, 
    # Emoji,
)
from response_message import response_message


app = FastAPI()

load_dotenv(override=True)

# LINE Access Key
get_access_token = os.getenv('ACCESS_TOKEN')
configuration = Configuration(access_token=get_access_token)
# LINE Secret Key
get_channel_secret = os.getenv('CHANNEL_SECRET')
handler = WebhookHandler(channel_secret=get_channel_secret)

UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # reply_message = "Hello from Dev Environment"
        reply_message = response_message (event)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_message]
            )
        )

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event: MessageEvent):
    message_id = event.message.id

    with ApiClient(configuration) as api_client:
        blob_api = MessagingApiBlob(api_client)
        content = blob_api.get_message_content(message_id)
        line_bot_api = MessagingApi(api_client)
        file_path = os.path.join(UPLOAD_FOLDER, f"{message_id}.jpg")
        with open(file_path, "wb") as f:
            f.write(content)
    result = analyze_slip(file_path)
    if isinstance(result, dict):
        reply_text = (f"Payment Method: {result['payment_method']}\n"
                      f"ID: {result['ID']}\n"
                      f"Date: {result['Date']}\n"
                      f"Time: {result['Time']}\n"
                      f"Amount: {result['Amount']}\n"
                      f"Who : {line_bot_api.get_profile(event.source.user_id).display_name}")
    
    else: 
        reply_text = f"Payment Method: {result}"

    line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )
    
    delect_image(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")