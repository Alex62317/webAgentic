# AI - Django 版本

## 项目介绍

AI 是一个企业级AI助手平台，基于Django框架重构，提供智能AI聊天、知识库管理、文件上传等功能。

## 技术栈

- **后端框架**：Django 4.2 + Django REST Framework
- **认证系统**：JWT + Django Auth
- **数据库**：SQLite（默认）
- **AI集成**：OpenAI SDK
- **API文档**：drf-yasg（Swagger/ReDoc）

## 核心功能

1. **用户认证系统**：登录、注册、获取用户信息
2. **AI模型集成**：支持多种AI模型的集成和调用
3. **聊天功能**：基于会话的聊天功能，支持上下文管理
4. **知识库管理**：创建、管理知识库，上传和处理附件
5. **文件上传**：支持多种类型文件的上传和管理
6. **系统配置**：管理系统的各种配置参数

## 项目结构

```
temp/
├── chat/            # 聊天功能模块
├── file/            # 文件上传模块
├── knowledge/       # 知识库模块
├── system/          # 系统配置模块
├── users/           # 用户认证模块
├── ruoyi_ai/        # 项目配置
├── log/             # 日志目录
├── media/           # 媒体文件目录
├── venv/            # 虚拟环境
├── start.sh         # 启动脚本
└── README.md        # 项目文档
```

## 快速开始

### 环境要求

- Python 3.9+
- Django 4.2+
- 虚拟环境

### 安装和运行

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd temp
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   - 复制 `.env.example` 文件为 `.env`
   - 编辑 `.env` 文件，设置相应的配置参数

5. **运行数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

7. **启动项目**
   ```bash
   ./start.sh
   ```

8. **访问地址**
   - 管理后台：http://localhost:8000/admin/
   - API文档：http://localhost:8000/swagger/

## API接口

### 用户认证
- `POST /auth/login/` - 用户登录
- `POST /auth/register/` - 用户注册
- `POST /auth/refresh/` - 刷新token
- `GET /auth/info/` - 获取用户信息

### 聊天功能
- `GET /chat/models/` - 获取AI模型列表
- `GET /chat/sessions/` - 获取聊天会话列表
- `POST /chat/sessions/create/` - 创建聊天会话
- `DELETE /chat/sessions/{id}/delete/` - 删除聊天会话
- `GET /chat/sessions/{id}/messages/` - 获取会话消息
- `POST /chat/send/` - 发送聊天消息

### 知识库管理
- `GET /knowledge/info/` - 获取知识库列表
- `POST /knowledge/info/create/` - 创建知识库
- `GET /knowledge/info/{id}/` - 获取知识库详情
- `PUT /knowledge/info/{id}/update/` - 更新知识库
- `DELETE /knowledge/info/{id}/delete/` - 删除知识库
- `GET /knowledge/info/{id}/attachments/` - 获取知识库附件
- `POST /knowledge/info/{id}/attachments/upload/` - 上传知识库附件
- `DELETE /knowledge/attachments/{id}/delete/` - 删除知识库附件

### 文件上传
- `POST /file/upload/` - 上传文件
- `GET /file/list/` - 获取文件列表
- `DELETE /file/delete/{id}/` - 删除文件

### 系统配置
- `GET /system/config/` - 获取系统配置列表
- `POST /system/config/create/` - 创建系统配置
- `GET /system/config/{id}/` - 获取系统配置详情
- `PUT /system/config/{id}/update/` - 更新系统配置
- `DELETE /system/config/{id}/delete/` - 删除系统配置

## 注意事项

1. **安全配置**：在生产环境中，需要修改SECRET_KEY并配置HTTPS
2. **数据库配置**：生产环境建议使用PostgreSQL或MySQL
3. **AI模型配置**：需要在系统配置中添加AI模型的API密钥
4. **文件存储**：生产环境建议使用对象存储服务
5. **性能优化**：对于高并发场景，需要配置缓存和负载均衡

## 故障排查

1. **服务器启动失败**：检查端口是否被占用
2. **数据库连接失败**：检查数据库配置是否正确
3. **AI模型调用失败**：检查API密钥和网络连接
4. **文件上传失败**：检查文件大小和权限设置

## 开发指南

### 代码规范
- 遵循PEP 8编码规范
- 为所有函数添加文档字符串
- 使用Type Hints

### 测试
- 使用Django的测试框架进行单元测试
- 为API接口编写集成测试

### 部署
- 使用Gunicorn作为WSGI服务器
- 使用Nginx作为反向代理
- 配置环境变量

## 许可证

MIT License

## 致谢
本项目基于RUOYI AI、crewAI、n8n、Djingo等开源项目重构而来，更加适配Agentic时代