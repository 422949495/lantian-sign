import os
import requests

def parse_cookie_string(cookie_str):
    cookies = {}
    for item in cookie_str.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
        else:
            cookies[item.strip()] = ''
    return cookies

def sign():
    # ！！恢复你抓包时的原始 URL（双斜杠）！！
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
        "X-Requested-With": "XMLHttpRequest",
    }

    cookie_str = os.environ["COOKIE"]
    cookies_dict = parse_cookie_string(cookie_str)

    session = requests.Session()
    session.cookies.update(cookies_dict)

    # 调试输出：确认解析后的 Cookie
    print("当前使用的 Cookies:")
    for k, v in session.cookies.get_dict().items():
        print(f"  {k}: {v[:30] if len(v) > 30 else v}")  # 只打印前30字符避免刷屏

    print("\n正在访问首页预热...")
    try:
        pre_resp = session.get(
            "https://www.ltyun.top/console/",
            headers=headers,
            timeout=10
        )
        print(f"首页状态码: {pre_resp.status_code}")
    except Exception as e:
        print(f"首页请求异常（可忽略）: {e}")

    print("\n正在签到...")
    try:
        resp = session.post(url, headers=headers, data={"aiandao": "true"}, timeout=10)
        print(f"签到状态码: {resp.status_code}")
        print(f"签到响应体前300字符: {resp.text[:300]}")
        if not resp.text.strip():
            print("⚠️ 仍然空响应，请确认：")
            print("  1. Secrets 中的 COOKIE 是否为最新抓包的完整 Cookie")
            print("  2. 是否包含了 Transfers 等全部字段")
            return
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
        if any(keyword in message for keyword in ["已签到", "已经签到", "重复签到", "今日已签"]):
            print(f"ℹ️ 今日已手动签到，无需重复操作。服务器返回: {message}")
        else:
            print(f"❌ 签到失败，服务器返回: {result}")

if __name__ == "__main__":
    sign()
