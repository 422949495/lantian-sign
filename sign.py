import os
import requests

def sign():
    url = "https://www.ltyun.top/console//php/index.php?action=qiandao"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.ltyun.top",
        "Referer": "https://www.ltyun.top/console/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
        "sec-ch-ua": '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Cookie": os.environ["COOKIE"]
    }

    try:
        resp = requests.post(url, headers=headers, data={"aiandao": "true"})
        resp.raise_for_status()          # 如果 HTTP 状态码不是 2xx 则抛出异常
        result = resp.json()
    except Exception as e:
        print(f"❌ 请求或解析失败: {e}")
        return

    if result.get("status"):
        amount = result.get("amount", "未知")
        message = result.get("message", "签到成功")
        print(f"✅ 签到成功！获得 {amount}，消息: {message}")
    else:
        message = result.get("message", "")
        # 检查是否为“已签到”类提示
        if any(keyword in message for keyword in ["已签到", "已经签到", "重复签到", "今日已签"]):
            print(f"ℹ️ 今日已手动签到，无需重复操作。服务器返回: {message}")
        else:
            print(f"❌ 签到失败，服务器返回: {result}")

if __name__ == "__main__":
    sign()