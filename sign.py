import os
import requests

def parse_cookie_string(cookie_str):
    """解析 Cookie 字符串，但过滤掉包含非 Latin-1 字符的字段"""
    cookies = {}
    for item in cookie_str.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' in item:
            key, value = item.split('=', 1)
            key = key.strip()
            value = value.strip()
            # 如果值包含非 Latin-1 字符，直接跳过这个字段
            try:
                value.encode('latin-1')
                cookies[key] = value
            except UnicodeEncodeError:
                print(f"⚠️ 已跳过无法编码的 Cookie 字段: {key}")
        else:
            cookies[item.strip()] = ''
    return cookies

def sign():
    url = "https://www.ltyun.top/console//php/index.php?action=qiandao"  # 保持双斜杠
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

    if not cookies_dict:
        print("❌ 没有找到任何有效的 Cookie 字段，请检查 Secrets 中的 COOKIE 值")
        return

    print("当前使用的 Cookies (过滤后):")
    for k, v in cookies_dict.items():
        print(f"  {k}: {v}")

    session = requests.Session()
    session.cookies.update(cookies_dict)

    # 预热首页
    print("\n正在访问首页...")
    try:
        pre_resp = session.get("https://www.ltyun.top/console/", headers=headers, timeout=10)
        print(f"首页状态码: {pre_resp.status_code}")
    except Exception as e:
        print(f"首页请求异常（可忽略）: {e}")

    # 签到
    print("\n正在签到...")
    try:
        resp = session.post(url, headers=headers, data={"aiandao": "true"}, timeout=10)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        print(f"❌ 请求或解析失败: {e}")
        if 'resp' in locals() and resp.text:
            print(f"服务器返回内容: {resp.text[:200]}")
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
