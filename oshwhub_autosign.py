import json
import re
import os
import requests
import hashlib


def cookies2dict(_cookies):
    _cookieDict = {}
    _cookies = _cookies.split("; ")
    for co in _cookies:
        co = co.strip()
        p = co.split('=')
        value = co.replace(p[0] + '=', '').replace('"', '')
        _cookieDict[p[0]] = value
    return _cookieDict


User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 " \
             "Safari/537.36 "
oshw_url = "https://oshwhub.com"
oshw_res = requests.get(oshw_url)

# 后面需要用到acw_tc oshwhub_session oshwhubReferer
_oshw_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])
print("未登录状态oshw网域的cookies:", _oshw_cookies)

oshw_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": requests.get(oshw_url).headers['Set-Cookie'],
    "Host": "oshwhub.com",
    "Pragma": "no-cache",
    "Referer": "https://oshwhub.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
oshw2passport_url = "https://oshwhub.com/login?from=https%3A%2F%2Foshwhub.com"
login_res = requests.get(oshw2passport_url, headers=oshw_headers, allow_redirects=False)
oshw2passport_cookies = cookies2dict(login_res.headers['Set-Cookie'])
print("跳转到PASSPORT过程中获取CASAuth:", oshw2passport_cookies['CASAuth'])

passport_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "passport.szlcsc.com",
    "Pragma": "no-cache",
    "Referer": "https://oshwhub.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
passport_res = requests.get(login_res.headers['Location'], headers=passport_headers, allow_redirects=False)
passport_cookies = cookies2dict(passport_res.headers['Set-Cookie'])
print("PASSPORT网域下acw_tc:", passport_cookies['acw_tc'])

passport_headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": passport_res.headers['Set-Cookie'],
    "Host": "passport.szlcsc.com",
    "Pragma": "no-cache",
    "Referer": "https://oshwhub.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
passport_res = requests.get(passport_res.headers['Location'], headers=passport_headers2)
passport_cookies2 = cookies2dict(passport_res.headers['Set-Cookie'])
SSESION = passport_res.headers['Set-Cookie'].split(";")[-4].split("=")[-1]
print("获取新SSESION:", SSESION)

# print(passport_res.text)

LT = re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', passport_res.text)
print("获取登录表单里lt参数:", LT[0])

login_url = "https://passport.szlcsc.com/login"
login_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "373",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "passport.szlcsc.com",
    "Origin": "https://passport.szlcsc.com",
    "Pragma": "no-cache",
    "Referer": "https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
login_cookies = {
    "AGL_USER_ID": "247a99b7-7854-4c3e-8d47-92dc695f22c8",
    "fromWebSite": "oshwhub",
    "SESSION": SSESION
}
form_data = {
    "lt": LT[0],
    "execution": "e1s1",
    "_eventId": "submit",
    "loginUrl": "https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub",
    "afsId": "",
    "sig": "",
    "token": "",
    "scene": "login",
    "loginFromType": "shop",
    "showCheckCodeVal": "false",
    "pwdSource": "",
    "username": os.environ['phone'],
    "password": hashlib.md5(os.environ['passwd'].encode("utf8")).hexdigest(),
    "rememberPwd": "yes",
}
passport_res = requests.post(url=login_url, data=form_data, headers=login_headers, cookies=login_cookies,
                             allow_redirects=False)
print(passport_res.headers['Location'])
print(passport_res.headers['Set-Cookie'])
# print(passport_res.json)


# 验证ticket
oshw_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "oshwhub.com",
    "Pragma": "no-cache",
    "Referer": "https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
oshw_cookies = {
    "acw_tc": _oshw_cookies['acw_tc'],
    "oshwhubReferer": _oshw_cookies['acw_tc'],
    "oshwhub_session": _oshw_cookies['acw_tc'],
    "CASAuth": oshw2passport_cookies['CASAuth']
}

# 验证ticket
oshw_res = requests.get(passport_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies,allow_redirects=False)
print(oshw_res.headers['Location'])
# 更新session
oshw_res = requests.get(oshw_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies, allow_redirects=False)
print(oshw_res.headers['Set-Cookie'])
# 跳转oshw主页
oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
oshw_res = requests.get(oshw_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies, allow_redirects=False)
print(oshw_res.headers['Set-Cookie'])

sign_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])

oshw_sign = requests.post("https://oshwhub.com/api/user/sign_in", headers=oshw_headers, cookies=sign_cookies)
print(json.loads(oshw_sign.content))
