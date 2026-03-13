module.exports = {
  // 数据库配置
  database: {
    type: 'sqlite',
    path: './n8n.db'
  },
  // 服务器配置
  server: {
    host: 'localhost',
    port: 5678
  },
  // 安全配置
  security: {
    basicAuth: {
      active: false
    }
  },
  // 日志配置
  logging: {
    level: 'info'
  }
};
