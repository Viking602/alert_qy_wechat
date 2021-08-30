import json
import requests
from dateutil import parser
import datetime
import time

url = ""


def time_zone_conversion(utctime):
    # UTC时间转换
    format_time = parser.parse(utctime).strftime('%Y-%m-%dT%H:%M:%SZ')
    if format_time == "1-01-01T00:00:00Z":
        format_time = "0001-01-01T00:00:00Z"
    time_format = datetime.datetime.strptime(str(format_time), "%Y-%m-%dT%H:%M:%SZ")
    return str(time_format + datetime.timedelta(hours=8))


def time_stamp(tm):
    # 时间转换时间戳
    timearray = time.strptime(str(tm), "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timearray)
    return timestamp


def duration(a_time, b_time):
    # 持续时间计算
    a = time_stamp(a_time)
    b = time_stamp(b_time)
    return time.strftime("%H小时%M分钟%S秒", time.gmtime(a - b))


def message(data):
    print(json.dumps(data))
    alerts = data['alerts']
    alert_message = []
    for i in range(len(alerts)):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert = alerts[i]
        status = alert['status']
        if status == "firing":
            status = "<font color = \"warning\">" + "告警发生" + "</font>"
        elif status == "resolved":
            status = "<font color = \"info\">" + "告警恢复" + "</font>"
        else:
            status = status
        labels = alert['labels']
        annotations = alert['annotations']
        startsat = alert['startsAt']
        start_time = time_zone_conversion(startsat)
        endsat = alert['endsAt']
        end_time = time_zone_conversion(endsat)
        severity = labels['severity']
        alertname = labels['alertname']
        instance = labels['instance']
        description = annotations['description']
        duration_time = duration(now_time, start_time)
        if end_time != "0001-01-01 08:00:00":
            duration_time = duration(end_time, start_time)
        markdown_text = ">状态: " + status + '\n' \
                        ">告警名称: " + alertname + '\n' \
                        ">告警实例: " + instance + '\n' \
                        ">告警等级: " + "<font color = \"warning\">" + severity + "</font>" + '\n' \
                        ">告警描述: " + description + '\n' \
                        ">开始时间: " + start_time + '\n' \
                        ">恢复时间: " + end_time + '\n' \
                        ">持续时间: " + duration_time + '\n'
        alert_message.append(markdown_text)
    return alert_message


def send_wechat(msg):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    nm = len(msg)
    data = "<font color = \"comment\">===================</font>\n".join(msg)
    body = {
        "msgtype": "markdown",
        "markdown": {
            "content": "<font color = \"comment\">" + "告警通知[" + str(nm) + "]</font>" + '\n' + data
        }
    }
    requests.post(url, json.dumps(body), headers=headers)
