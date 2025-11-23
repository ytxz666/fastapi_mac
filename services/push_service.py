import requests
import time
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class PushService:
    def __init__(self):
        # 从环境变量获取微信公众号配置
        self.app_id = os.getenv("WECHAT_APP_ID", "")
        self.app_secret = os.getenv("WECHAT_APP_SECRET", "")
        self.access_token = ""
        self.token_expires_at = 0

    def get_access_token(self):
        """
        获取微信公众号访问令牌
        :return: 有效的访问令牌
        """
        # 检查令牌是否过期，如果未过期则直接返回
        if self.access_token and time.time() < self.token_expires_at - 60:  # 提前60秒刷新
            return self.access_token

        # 调用微信API获取新的访问令牌
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        try:
            response = requests.get(url)
            result = response.json()

            if "access_token" in result:
                self.access_token = result["access_token"]
                self.token_expires_at = time.time() + result["expires_in"]
                return self.access_token
            else:
                print(f"获取访问令牌失败: {result}")
                return None
        except Exception as e:
            print(f"获取访问令牌异常: {str(e)}")
            return None

    def push_text_message(self, openid, content):
        """
        推送文本消息给指定用户
        :param openid: 用户的OpenID
        :param content: 消息内容
        :return: 推送结果 (True/False, 错误信息)
        """
        access_token = self.get_access_token()
        if not access_token:
            return False, "获取访问令牌失败"

        url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"
        payload = {
            "touser": openid,
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        try:
            response = requests.post(url, json=payload)
            result = response.json()

            if result.get("errcode") == 0:
                return True, "推送成功"
            else:
                return False, f"推送失败: {result.get('errmsg', '未知错误')}"
        except Exception as e:
            return False, f"推送异常: {str(e)}"

    def push_to_all_users(self, content):
        """
        群发消息给所有用户（需先获取用户列表）
        :param content: 消息内容
        :return: 推送结果 (成功数量, 失败数量, 错误信息)
        """
        # 实际应用中需要先获取所有用户的OpenID列表
        # 这里简化处理，假设已获取用户列表
        all_openids = []  # 需要从数据库或其他存储中获取
        success_count = 0
        fail_count = 0
        errors = []

        for openid in all_openids:
            success, msg = self.push_text_message(openid, content)
            if success:
                success_count += 1
            else:
                fail_count += 1
                errors.append(f"用户 {openid}: {msg}")

        return success_count, fail_count, errors