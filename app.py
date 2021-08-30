from flask import Flask, request
import json
import message as msg

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    prometheus_data = json.loads(request.data)
    send_msg = msg.message(prometheus_data)
    msg.send_wechat(send_msg)
    return 'qy_wechat_webhook'


if __name__ == '__main__':
    app.run()
