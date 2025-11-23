import xml.etree.ElementTree as ET
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
import os

# 消息存储Excel文件路径
EXCEL_FILE_PATH = os.path.join("data", "messages.xlsx")

class MessageService:
    @staticmethod
    def parse_xml_message(xml_data):
        """
        解析微信公众号推送的XML格式消息
        :param xml_data: XML格式的请求体字符串
        :return: 解析后的消息字典
        """
        try:
            root = ET.fromstring(xml_data)
            # 提取基础消息字段
            message = {
                "ToUserName": root.findtext("ToUserName", ""),
                "FromUserName": root.findtext("FromUserName", ""),
                "CreateTime": root.findtext("CreateTime", ""),
                "MsgType": root.findtext("MsgType", ""),
                "MsgId": root.findtext("MsgId", "")
            }

            # 根据消息类型提取特定字段
            if message["MsgType"] == "text":
                message["Content"] = root.findtext("Content", "")
            elif message["MsgType"] == "image":
                message["PicUrl"] = root.findtext("PicUrl", "")
                message["MediaId"] = root.findtext("MediaId", "")
            elif message["MsgType"] == "voice":
                message["MediaId"] = root.findtext("MediaId", "")
                message["Format"] = root.findtext("Format", "")
            elif message["MsgType"] == "video":
                message["MediaId"] = root.findtext("MediaId", "")
                message["ThumbMediaId"] = root.findtext("ThumbMediaId", "")

            # 转换创建时间为可读性更好的格式
            if message["CreateTime"]:
                try:
                    timestamp = int(message["CreateTime"])
                    message["CreateTimeFormatted"] = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    message["CreateTimeFormatted"] = "Invalid time"
            else:
                message["CreateTimeFormatted"] = ""

            return message
        except Exception as e:
            print(f"解析XML消息失败: {str(e)}")
            return {}

    @staticmethod
    def save_message_to_excel(message):
        """
        将解析后的消息数据追加保存到Excel文件
        :param message: 解析后的消息字典
        :return: 保存结果 (True/False)
        """
        try:
            # 检查文件是否存在，如果不存在则创建并添加表头
            if not os.path.exists(EXCEL_FILE_PATH):
                workbook = Workbook()
                sheet = workbook.active
                sheet.title = "消息记录"
                # 添加表头
                headers = [
                    "消息ID", "接收时间", "格式化时间", "消息类型", 
                    "发送者OpenID", "接收者ID", "内容", "图片URL", 
                    "媒体ID", "格式", "缩略图媒体ID"
                ]
                sheet.append(headers)
                # 设置表头居中对齐
                for col in sheet.columns:
                    for cell in col:
                        cell.alignment = Alignment(horizontal='center', vertical='center')
                workbook.save(EXCEL_FILE_PATH)

            # 打开现有文件并追加数据
            workbook = load_workbook(EXCEL_FILE_PATH)
            sheet = workbook.active

            # 准备要写入的数据行
            row_data = [
                message.get("MsgId", ""),
                message.get("CreateTime", ""),
                message.get("CreateTimeFormatted", ""),
                message.get("MsgType", ""),
                message.get("FromUserName", ""),
                message.get("ToUserName", ""),
                message.get("Content", ""),
                message.get("PicUrl", ""),
                message.get("MediaId", ""),
                message.get("Format", ""),
                message.get("ThumbMediaId", "")
            ]

            sheet.append(row_data)
            workbook.save(EXCEL_FILE_PATH)
            return True
        except Exception as e:
            print(f"保存消息到Excel失败: {str(e)}")
            return False

    @staticmethod
    def get_all_messages():
        """
        从Excel文件中获取所有消息记录
        :return: 消息记录列表
        """
        try:
            if not os.path.exists(EXCEL_FILE_PATH):
                return []

            workbook = load_workbook(EXCEL_FILE_PATH)
            sheet = workbook.active
            messages = []

            # 获取表头
            headers = [cell.value for cell in sheet[1]]

            # 遍历数据行
            for row in sheet.iter_rows(min_row=2, values_only=True):
                message_dict = {}
                for header, value in zip(headers, row):
                    message_dict[header] = value
                messages.append(message_dict)

            return messages
        except Exception as e:
            print(f"读取消息记录失败: {str(e)}")
            return []