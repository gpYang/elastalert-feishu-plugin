# elastalert-feishu-plugin
## 安装
sudo apt install -y  python-pip python-dev libffi-dev libssl-dev

pip install elastalert
## 修改配置
### config.yaml:

``` 
es_host: elasticsearch 地址
es_port: elasticsearch 端口
```
### rules/example_frequency.yaml
``` 
alert:
- "elastalert_modules.feishu_alert.FeishuAlert"

# 飞书机器人接口地址
feishualert_url: "https://open.feishu.cn/open-apis/bot/v2/hook/"
# 飞书机器人id
feishualert_botid:
  "botid"

# 告警标题
feishualert_title:
  "test"

# 这个时间段内的匹配将不告警，适用于某些时间段请求低谷避免误报警
feishualert_skip:
  start: "01:00:00"
  end: "09:00:00"

# 告警内容
# 使用{}可匹配matches
# 如匹配到的es数据为{"host":"aa.com","ip":"127.0.0.1"}
feishualert_body:
  "
  告警策略:  {feishualert_title}\n
  总请求数:  {num_hits}\n
  触发时间:  {feishualert_time}\n
  匹配域名:  {host}\n
  匹配ip:  {ip}
  "
```

## 运行
elastalert-create-index --config config.yaml

python -m elastalert.elastalert --verbose
