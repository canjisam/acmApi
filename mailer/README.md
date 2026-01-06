Mailer - 自动比赛通知

说明
- 该模块从仓库根目录的 `contests.json` 读取比赛数据，并筛选未来 24 小时内的比赛，生成邮件正文并发送。

快速开始（本地测试）
1. 复制示例配置：
   cp mailer/config.example.json mailer/config.json
2. 填写 `mailer/config.json` 中的 SMTP 配置和收件人。
3. 运行 dry-run（只打印邮件内容）：
   python3 -m mailer.send_contest_email
4. 实际发送（谨慎操作）：
   python3 -m mailer.send_contest_email --send

GitHub Actions
- 我们在 `.github/workflows/send_contest_email.yml` 中添加了一个每日定时任务。
- 在仓库 Settings -> Secrets 中添加以下 Secrets：
  - SMTP_HOST（例如："smtp.gmail.com"）
  - SMTP_PORT（例如："587"，纯数字）
  - SMTP_USERNAME（SMTP 用户名）
  - SMTP_PASSWORD（SMTP 密码或应用密码）
  - SMTP_FROM（发件人邮箱地址）
  - TO_ADDRESSES（收件人邮箱列表，用逗号分隔，如："user1@example.com,user2@example.com"）

安全建议
- 切勿将 `mailer/config.json` 提交到公共仓库。`.gitignore` 已包含该文件路径。
