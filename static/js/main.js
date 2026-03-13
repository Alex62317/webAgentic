// 全局变量
let currentSessionId = null;
let isLoginMode = true;

// 页面加载完成后执行
window.onload = function() {
    // 检查是否有登录凭证（cookie）
    if (getCookie('access_token')) {
        // 验证 token 是否有效
        verifyToken();
    } else {
        // 显示登录按钮
        document.getElementById('loginBtn').style.display = 'block';
        document.getElementById('userInfo').style.display = 'none';
    }
};

// 显示认证模态框
function showAuthModal() {
    document.getElementById('authModal').style.display = 'flex';
}

// 关闭认证模态框
function closeAuthModal() {
    document.getElementById('authModal').style.display = 'none';
    // 清空表单
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('email').value = '';
    document.getElementById('errorMessage').textContent = '';
}

// 切换登录/注册模式
function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    
    if (isLoginMode) {
        document.getElementById('authTitle').textContent = '用户登录';
        document.getElementById('authSubmit').textContent = '登录';
        document.getElementById('authToggleText').textContent = '还没有账号？';
        document.getElementById('authToggleLink').textContent = '立即注册';
        document.getElementById('emailGroup').style.display = 'none';
    } else {
        document.getElementById('authTitle').textContent = '用户注册';
        document.getElementById('authSubmit').textContent = '注册';
        document.getElementById('authToggleText').textContent = '已有账号？';
        document.getElementById('authToggleLink').textContent = '立即登录';
        document.getElementById('emailGroup').style.display = 'block';
    }
    
    // 清空错误信息
    document.getElementById('errorMessage').textContent = '';
}

// 提交认证表单
async function submitAuth() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const errorMessage = document.getElementById('errorMessage');
    
    // 验证表单
    if (!username || !password) {
        errorMessage.textContent = '用户名和密码不能为空';
        return;
    }
    
    if (!isLoginMode && !email) {
        errorMessage.textContent = '邮箱不能为空';
        return;
    }
    
    try {
        // 构建请求数据
        const data = isLoginMode ? {
            username: username,
            password: password
        } : {
            username: username,
            password: password,
            email: email
        };
        
        // 发送请求
        const url = isLoginMode ? '/auth/login/' : '/auth/register/';
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: 'include' // 包含 cookie
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // 保存 token 到 cookie
            setCookie('access_token', result.access, 7);
            setCookie('refresh_token', result.refresh, 7);
            
            // 更新用户信息
            updateUserInfo(result.user);
            
            // 关闭模态框
            closeAuthModal();
            
            // 加载会话列表
            loadSessions();
        } else {
            errorMessage.textContent = result.error || '认证失败，请重试';
        }
    } catch (error) {
        errorMessage.textContent = '网络错误，请重试';
    }
}

// 验证 token
async function verifyToken() {
    try {
        const response = await fetch('/auth/me/', {
            method: 'GET',
            credentials: 'include' // 包含 cookie
        });
        
        if (response.ok) {
            // token 有效，更新用户信息
            const user = await response.json();
            updateUserInfo(user);
            
            // 加载会话列表
            loadSessions();
        } else {
            // token 无效，清除 cookie 并显示登录按钮
            deleteCookie('access_token');
            deleteCookie('refresh_token');
            document.getElementById('loginBtn').style.display = 'block';
            document.getElementById('userInfo').style.display = 'none';
        }
    } catch (error) {
        // 网络错误，清除 cookie 并显示登录按钮
        deleteCookie('access_token');
        deleteCookie('refresh_token');
        document.getElementById('loginBtn').style.display = 'block';
        document.getElementById('userInfo').style.display = 'none';
    }
}

// 更新用户信息
function updateUserInfo(user) {
    if (user) {
        document.getElementById('userName').textContent = user.username;
        document.getElementById('userInfo').style.display = 'flex';
        document.getElementById('loginBtn').style.display = 'none';
        // 保存用户信息到 cookie
        setCookie('user', JSON.stringify(user), 7);
    }
}

// 退出登录
function logout() {
    // 清除 cookie
    deleteCookie('access_token');
    deleteCookie('refresh_token');
    deleteCookie('user');
    document.getElementById('userInfo').style.display = 'none';
    document.getElementById('loginBtn').style.display = 'block';
}

// 发送消息
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const content = messageInput.value.trim();
    
    if (!content) return;
    
    const modelSelect = document.getElementById('modelSelect');
    const modelName = modelSelect.value;
    
    // 显示加载状态
    document.getElementById('loading').style.display = 'block';
    
    // 添加用户消息到界面
    addMessage('user', content);
    
    // 清空输入框
    messageInput.value = '';
    
    try {
        // 统一通过后端 API 发送消息
        const response = await fetch('/chat/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                model_name: modelName,
                session_id: currentSessionId
            }),
            credentials: 'include' // 包含 cookie
        });
        
        if (response.ok) {
            const result = await response.json();
            currentSessionId = result.session_id;
            
            // 添加助手消息到界面
            addMessage('assistant', result.message.content);
            
            // 加载会话列表
            loadSessions();
        } else {
            const error = await response.json();
            addMessage('assistant', `抱歉，发生了错误: ${error.error || '请稍后再试'}`);
        }
    } catch (error) {
        addMessage('assistant', '抱歉，发生了错误，请稍后再试。');
    } finally {
        // 隐藏加载状态
        document.getElementById('loading').style.display = 'none';
    }
}

// 添加消息到界面
function addMessage(role, content) {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const messageRole = role === 'user' ? 'You' : 'Assistant';
    
    messageDiv.innerHTML = `
        <div>
            <div class="message-role">${messageRole}</div>
            <div class="message-content">${content}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    
    // 滚动到底部
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 快捷操作
function quickAction(content) {
    document.getElementById('messageInput').value = content;
    sendMessage();
}

// 清空历史
function clearHistory() {
    document.getElementById('messages').innerHTML = `
        <div class="message assistant">
            <div>
                <div class="message-role">Assistant</div>
                <div class="message-content">
                    👋 你好！我是你的AI助手，有什么可以帮助你的吗？
                </div>
            </div>
        </div>
    `;
    currentSessionId = null;
}

// 加载会话列表
async function loadSessions() {
    try {
        const response = await fetch('/chat/sessions/', {
            method: 'GET',
            credentials: 'include' // 包含 cookie
        });
        
        if (response.ok) {
            const sessions = await response.json();
            updateSessionList(sessions);
        }
    } catch (error) {
        console.error('加载会话列表失败:', error);
    }
}

// 更新会话列表
function updateSessionList(sessions) {
    const sessionList = document.getElementById('sessionList');
    sessionList.innerHTML = '';
    
    if (sessions.length === 0) {
        sessionList.innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">暂无会话历史</div>';
        return;
    }
    
    sessions.forEach(session => {
        const sessionItem = document.createElement('div');
        sessionItem.className = 'session-item';
        sessionItem.textContent = session.title;
        sessionItem.onclick = () => loadSession(session.id);
        sessionList.appendChild(sessionItem);
    });
}

// 加载会话
async function loadSession(sessionId) {
    try {
        const response = await fetch(`/chat/messages/${sessionId}/`, {
            method: 'GET',
            credentials: 'include' // 包含 cookie
        });
        
        if (response.ok) {
            const messages = await response.json();
            currentSessionId = sessionId;
            
            // 清空消息容器
            const messagesContainer = document.getElementById('messages');
            messagesContainer.innerHTML = '';
            
            // 添加消息到界面
            messages.forEach(message => {
                addMessage(message.role, message.content);
            });
        }
    } catch (error) {
        console.error('加载会话失败:', error);
    }
}

// 处理回车键发送消息
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Cookie 操作函数
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const cookieName = `${name}=`;
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return '';
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}