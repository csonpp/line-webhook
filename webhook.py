from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent

app = Flask(__name__)

# 替換成你自己的 Channel access token & secret
LINE_CHANNEL_ACCESS_TOKEN = "UCWxMVzypOWSEB2qUaBF+kIzUtKQYAAAsvR5k1praIARx4K2gR7v3/FaSYG8k7K9LcRDdn1Pzf/okys0TN2V+UoHtwXKaZ4a21AZ8vzkjMwLtZTWHuR5RuHXtkltpFxP+t4D0NxxrpRV2l261spcXwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "3bc4a8915aa16df814c3bf8208bc970f"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理加群組事件（Bot 被邀請進群組）
@handler.add(JoinEvent)
def handle_join(event):
    gid = None
    if event.source.type == "group":
        gid = event.source.group_id
        print(f"📣 強哥！你的 Bot 被加進了一個群組，groupId 是：{gid}")
        # 可以考慮自動回傳一段歡迎詞
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"強哥的 Bot 加入群組囉！本群組ID：{gid}")
        )

# 處理收到文字訊息（不管個人還是群組）
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type == "group":
        gid = event.source.group_id
        print(f"👥 來自群組的訊息，groupId：{gid}")
        print(f"訊息內容：{event.message.text}")
        # 也可以選擇自動回覆，幫你測試 webhook 正常
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"強哥好！收到來自群組({gid})的訊息：{event.message.text}")
        )
    elif event.source.type == "user":
        uid = event.source.user_id
        print(f"🙋 來自個人的訊息，userId：{uid}")
        print(f"訊息內容：{event.message.text}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"強哥好！這是你的 userId：{uid}")
        )
    elif event.source.type == "room":
        rid = event.source.room_id
        print(f"🟦 來自聊天室 roomId：{rid}")
        print(f"訊息內容：{event.message.text}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
