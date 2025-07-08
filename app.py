import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Signature Error", 400
    return "OK", 200

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    msg = line_bot_api.get_message_content(event.message.id)
    with open("input.jpg", "wb") as f:
        for chunk in msg.iter_content():
            f.write(chunk)
    # ขั้นตอนถัดไป: อัปโหลด input.jpg ไป 1688 แล้วดึงชื่อสินค้า
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="รับภาพแล้ว กำลังค้นชื่อสินค้าจาก 1688 ให้ครับ...")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
