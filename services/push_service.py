import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class PushService:
    def __init__(self):
        # 从环境变量获取微信公众号配置（保留以备将来扩展使用）
        self.app_id = os.getenv("WECHAT_APP_ID", "")
        self.app_secret = os.getenv("WECHAT_APP_SECRET", "")

    def push_text_message(self, openid, content):
        """
        推送文本消息给指定用户
        使用云托管服务器的云调用方式，无需携带 access_token
        :param openid: 用户的OpenID
        :param content: 消息内容
        :return: 推送结果 (True/False, 错误信息)
        """
        # 云调用方式不需要携带 access_token
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send"
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
        使用云托管服务器的云调用方式
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