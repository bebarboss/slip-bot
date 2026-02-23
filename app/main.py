import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, Header

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent,ImageMessageContent
from linebot.v3.messaging import MessagingApiBlob,MessagingApi, ReplyMessageRequest, FlexMessage

from postgrest.exceptions import APIError
from flex_message import flex_message
from flex_message_ocr import flex_message_ocr
from linebot.v3.messaging import TextMessage
import re

from ocr import payment_method

from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest, 
    TextMessage, 
    FlexContainer, 
    # Emoji,
)

load_dotenv(override=True)

from supabase import create_client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


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
def handle_text(event):
    user_text = event.message.text.strip()
    match = re.match(r"^\+\s*(\d+)$", user_text)
    if match:
        amount = int(match.group(1))
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            profile = messaging_api.get_profile(event.source.user_id)
            supabase.table("receive_transaction").insert({
                "user_name": profile.display_name,
                "transaction_type": "income",
                "amount": amount
            }).execute()
            flex_message["body"]["contents"][3]["contents"][0]["contents"][1]["text"] = f"{amount} Baht"
            flex_message["body"]["contents"][5]["contents"][1]["text"] = profile.display_name
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        FlexMessage(
                            alt_text="Receipt Money",
                            contents=FlexContainer.from_dict(flex_message)
                        )
                    ]
                )
            )

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event: MessageEvent):
    message_id = event.message.id

    with ApiClient(configuration) as api_client:
        blob_api = MessagingApiBlob(api_client)
        content = blob_api.get_message_content(message_id)
        messaging_api = MessagingApi(api_client)
        file_path = os.path.join(UPLOAD_FOLDER, f"{message_id}.jpg")
        with open(file_path, "wb") as f:
            f.write(content)

    with open(file_path, "rb") as f:
        image_bytes = f.read()

    result = payment_method(image_bytes)

    if not isinstance(result, dict):
        reply_text = f"Payment Method: {result}"
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )
        return
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        profile = messaging_api.get_profile(event.source.user_id)
    exists = (
        supabase.table("payment_transection")
        .select("id")
        .eq("refid", result["refid"])
        .limit(1)
        .execute()
    )

    if exists.data:
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=f"Duplicate Slip\nRef ID: {result['refid']}")
                ]
            )
        )
        return

    supabase.table("payment_transection").insert({
        "user": profile.display_name,
        "user_id": event.source.user_id,
        "payment_method": result["payment_method"],
        "refid": result["refid"],
        "pay_date": result["date"],
        "pay_time": result["time"],
        "sender": result["sender"],
        "receiver": result["receiver"],
        "amount": result["amount"],
    }).execute()

    flex_message_ocr["body"]["contents"][1]["text"] = result["amount"]
    flex_message_ocr["body"]["contents"][2]["text"] = result["payment_method"]
    flex_message_ocr["body"]["contents"][4]["contents"][0]["contents"][1]["text"] = result["date"]
    flex_message_ocr["body"]["contents"][4]["contents"][1]["contents"][1]["text"] = result["time"]
    flex_message_ocr["body"]["contents"][4]["contents"][2]["contents"][1]["text"] = result["sender"]
    flex_message_ocr["body"]["contents"][4]["contents"][3]["contents"][1]["text"] = result["receiver"]
    flex_message_ocr["body"]["contents"][6]["contents"][1]["text"] = result["refid"]

    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                FlexMessage(
                    alt_text="Receipt Money",
                    contents=FlexContainer.from_dict(flex_message_ocr)
                )
            ]
        )
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")


