import requests

# 设置 API URL
url = "http://127.0.0.1:8000/Strategy"

# 请求数据
data = {
    "stock_code": "000001.SZ",
    "start_date": "20230101",
    "end_date": "20231231",
    "principal": 1000000,
    "buy_percent": 0.2
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 输出响应结果
print(response.status_code)
print(response.json())#可以直接在这里查看输出结果，或者访问“http://127.0.0.1:8000/results”
