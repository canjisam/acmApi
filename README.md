# 编程竞赛日历工具&&邮件提醒系统
2025-3-26 为了方便查看竞赛信息，我写了一个小工具。希望大家都能拿牌子。
本工具旨在为编程竞赛爱好者提供一个集中查看各大平台竞赛信息的日历视图。  
2025-08-24 新增邮件提醒系统 简单配置githubAction即可使用每天邮件自动推送竞赛信息

## 🌟 主要功能

### 1. 可视化日历
- 日历视图与列表视图自由切换
- 支持多平台竞赛信息集中展示
- 移动端响应式布局适配
- 平台快速筛选功能
- 竞赛详情一键访问

### 2. 邮件提醒系统
- 自动筛选未来24小时内的比赛信息
- 精美的 HTML 邮件模板
  - 平台特色标签（不同平台不同颜色）
  - 比赛时间、时长清晰展示
  - 支持一键跳转比赛页面
- 每日定时发送（可自定义时间）
- 支持多收件人配置

## 📊 支持平台

| 平台 | 说明 | 官网 |
|------|------|------|
| Codeforces | 全球最大的竞赛平台之一 | https://codeforces.com |
| AtCoder | 日本顶级竞赛平台 | https://atcoder.jp |
| LeetCode | 著名的算法题库和竞赛平台 | https://leetcode.com |
| 牛客网 | 国内知名竞赛和面试平台 | https://www.nowcoder.com |
| 洛谷 | 国内著名算法竞赛平台 | https://www.luogu.com.cn |


## 使用说明

1. 打开index.html文件
2. 使用顶部平台筛选按钮查看特定平台竞赛
3. 点击竞赛卡片查看详细信息

## 自动更新机制

- 每15分钟自动从各平台API获取最新竞赛信息
- 数据缓存机制保障网络中断时的信息可用性
- 更新失败时自动重试（最多3次）
- 更新内容包括竞赛时间、名称、链接等信息

### 3. 数据更新机制
- 每15分钟自动同步各平台最新竞赛信息
- 智能缓存确保离线可用
- 失败自动重试（最多3次）
- 记录详细比赛信息（时间、名称、链接等）


## 🚀 快速开始

### 网页访问
1. 访问官网：[https://canjisam.github.io/acmApi/](https://canjisam.github.io/acmApi/)
2. 使用平台筛选按钮选择感兴趣的平台
3. 点击竞赛卡片查看详情并跳转报名

### 配置邮件提醒
1. 克隆仓库：
   ```bash
   git clone https://github.com/canjisam/acmApi.git
   cd acmApi
   ```

2. 配置邮件服务：
   ```bash
   # 复制示例配置
   cp mailer/config.example.json mailer/config.json
   
   # 编辑配置文件填入 SMTP 信息
   vim mailer/config.json
   ```

3. 本地测试：
   ```bash
   # 只查看邮件内容（不发送）
   python3 -m mailer.send_contest_email
   
   # 实际发送邮件
   python3 -m mailer.send_contest_email --send
   ```

4. 启用自动提醒：
   在 GitHub 仓库设置中配置以下 Secrets：
   - SMTP_HOST：SMTP 服务器地址
   - SMTP_PORT：服务器端口（推荐 465）
   - SMTP_USERNAME：邮箱用户名
   - SMTP_PASSWORD：密码或授权码
   - SMTP_FROM：发件人地址
   - TO_ADDRESSES：收件人列表（逗号分隔）

## 🔧 开发说明

### 技术栈
- 前端：Vue.js + 原生 CSS
- 后端：Python（邮件服务）
- 自动化：GitHub Actions
- 数据源：各平台 API + 定时更新

### 自定义开发
1. 修改前端界面
   - 编辑 `index.html` 和相关 CSS 文件
   - 所有样式文件都有详细注释

2. 调整邮件模板
   - 在 `mailer/templates.py` 中修改 HTML 模板
   - 支持自定义 CSS 样式

3. 添加新平台
   - 在 `contests.json` 中添加新平台数据
   - 更新平台标签样式（在 `mailer/templates.py` 中）

## 📝 维护说明

- 项目持续维护，欢迎提交 Issue 和 PR
- 邮件服务采用 GitHub Actions，无需额外服务器
- 建议使用 Gmail 等可靠的 SMTP 服务

## 🔒 安全说明

- 所有密钥通过 GitHub Secrets 管理
- 邮件使用 SSL/TLS 加密传输
- 配置文件已加入 .gitignore

## 📄 许可证

MIT License - 详见 LICENSE 文件

