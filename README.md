# 微信公众号管理系统

基于Python/FastAPI开发的微信公众号管理系统，支持消息接收存储、自动回复和主动推送功能。

## 功能特点

- **消息接收与存储**：接收微信公众号推送的XML消息并存储到Excel
- **自动回复**：对文本消息实现自动回复功能
- **主动推送**：支持通过API和前端界面主动推送消息给指定用户
- **消息管理**：查看所有接收的消息记录
- **容器化部署**：适配腾讯云托管的Docker配置

## 环境准备

### 前置条件
- Python 3.9+ 
- pip (Python包管理工具)
- Docker (用于容器化部署)
- 微信公众号账号(需获取AppID和AppSecret)

### 本地开发环境搭建

1. 克隆项目代码
```bash
# 克隆仓库(假设使用Git管理)
git clone <repository-url>
cd fastapi_tzy
```

2. 创建并激活虚拟环境
```bash
# 创建虚拟环境
conda create -n venv python=3.9
# 激活虚拟环境
conda activate venv

```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
编辑.env文件，填入微信公众号的AppID和AppSecret：
```
WECHAT_APP_ID=你的微信公众号AppID
WECHAT_APP_SECRET=你的微信公众号AppSecret
```

## 运行方式

### 本地开发运行
```bash
uvicorn main:app --reload
```
系统将在 http://127.0.0.1:8000 启动

### 容器化运行
```bash
# 构建镜像
docker build -t wechat-mp-system .

# 运行容器
docker run -d -p 8000:8000 --name wechat-mp wechat-mp-system
```

## 功能使用说明

### 消息接收
系统自动监听`/wechat`路径，接收微信公众号推送的消息并存储到`data/messages.xlsx`文件中。

### 自动回复
文本消息自动回复内容可在`main.py`的`handle_wechat_message`函数中修改：
```python
content="感谢您的留言！我们会尽快回复您。"  # 可自定义回复内容
```

### 主动推送消息
1. 访问系统首页 http://localhost:8000
2. 在"主动推送消息"区域填写用户OpenID和消息内容
3. 点击"发送消息"按钮提交

### 查看消息记录
系统首页"消息记录"区域会显示所有接收的消息，包括发送者、时间、内容等信息。

## 项目结构

```
fastapi_tzy/
├── main.py              # 应用入口文件
├── requirements.txt     # 项目依赖
├── Dockerfile           # Docker配置
├── .env                 # 环境变量配置
├── services/
│   ├── message_service.py  # 消息接收与存储服务
│   └── push_service.py     # 消息推送服务
├── templates/
│   └── index.html        # 前端管理界面
└── data/
    └── messages.xlsx     # 消息存储Excel文件
```

## 部署到腾讯云托管

1. 准备工作
- 将代码推送到GitHub/GitLab仓库
- 在腾讯云容器服务中创建应用

2. 部署配置
- 选择代码仓库
- 构建方式：使用Dockerfile
- 端口映射：容器端口8000映射到服务端口

3. 环境变量配置
在腾讯云应用配置中设置环境变量：
- WECHAT_APP_ID: 你的微信公众号AppID
- WECHAT_APP_SECRET: 你的微信公众号AppSecret

4. 启动服务
完成部署后，腾讯云将自动构建并启动服务。

## 注意事项
- 微信公众号开发需确保服务器能被公网访问
- 主动推送功能需要公众号具备相应权限
- 敏感信息(如AppID、AppSecret)不要提交到代码仓库
- Excel文件存储适用于小规模数据，大规模应用建议使用数据库