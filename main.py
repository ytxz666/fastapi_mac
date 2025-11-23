from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import os

# 初始化FastAPI应用
app = FastAPI(title="微信公众号管理系统", description="基于FastAPI开发的微信公众号管理系统", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置模板目录
templates = Jinja2Templates(directory="templates")

# 创建数据存储目录（如果不存在）
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

from fastapi import Request

# 根路由 - 渲染管理系统前端页面
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from services.message_service import MessageService

# 微信消息接收端点
@app.post("/wechat", response_class=HTMLResponse)
async def handle_wechat_message(request: Request):
    # 读取请求体中的XML数据
    xml_data = await request.body()
    xml_str = xml_data.decode("utf-8")

    # 解析XML消息
    message = MessageService.parse_xml_message(xml_str)
    if message:
        # 保存消息到Excel
        MessageService.save_message_to_excel(message)

        # 文本消息自动回复
        if message.get("MsgType") == "text":
            # 构建回复XML
            reply_xml = f"""
            <xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{content}]]></Content>
            </xml>
            """.format(
                to_user=message["FromUserName"],
                from_user=message["ToUserName"],
                content="感谢您的留言！我们会尽快回复您。"  # 可自定义回复内容
            )
            return reply_xml.strip()

    # 默认回复（微信要求必须返回success，否则会重试）
    return "success"

from services.push_service import PushService
from pydantic import BaseModel
from fastapi import HTTPException

# 定义推送消息请求模型
class PushRequest(BaseModel):
    openid: str
    content: str

# 主动推送消息接口
@app.post("/api/push")
def push_message(request: PushRequest):
    """
    主动推送文本消息给指定用户
    :param request: 包含openid和content的请求体
    :return: 推送结果
    """
    if not request.openid or not request.content:
        raise HTTPException(status_code=400, detail="openid和content为必填项")

    push_service = PushService()
    success, message = push_service.push_text_message(request.openid, request.content)

    if success:
        return {"status": "success", "message": message}
    else:
        return {"status": "error", "message": message}

# 消息记录查看接口
@app.get("/api/messages")
def get_messages():
    """
    获取所有消息记录
    :return: 消息记录列表
    """
    messages = MessageService.get_all_messages()
    return {"status": "success", "messages": messages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)