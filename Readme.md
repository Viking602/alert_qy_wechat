# alert_qy_wechat
AlertManager for qy_wechat webhook

### AlertManager企业微信告警
使用前修改 message.py 内URL

### 使用方法
安装依赖
```
pip3 install -r requirements.txt
```
启动 默认端口 9998
```bash
gunicorn app:app -c gunicorn.conf.py
```