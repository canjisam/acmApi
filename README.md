# ACM比赛信息获取器

这个项目用于自动获取并更新未来一个月的Codeforces和LeetCode比赛信息。

## 功能特点

- 自动获取Codeforces未来一个月的比赛信息
- 自动获取LeetCode未来一个月的比赛信息
- 将比赛信息保存为JSON格式
- 通过GitHub Actions自动每日更新数据
- 提供统一的API接口获取比赛信息

## API使用说明

项目提供了统一的API接口用于获取比赛信息：

```python
from contest_api import ContestAPI

# 创建API实例
api = ContestAPI()

# 获取所有平台的比赛信息
all_contests = api.get_all_contests()

# 获取指定平台的比赛信息
codeforces_contests = api.get_contests_by_platform('Codeforces')
leetcode_contests = api.get_contests_by_platform('LeetCode')

# 也可以直接调用特定平台的方法
codeforces_contests = api.get_codeforces_contests()
leetcode_contests = api.get_leetcode_contests()
```

## 数据格式

获取的比赛数据保存在`contests.json`文件中，格式如下：

```json
{
  "last_updated": "2023-10-25 08:00:00",
  "contests": [
    {
      "platform": "Codeforces",
      "name": "Codeforces Round #XXX",
      "start_time": "2023-10-20 19:35:00",
      "duration": "2小时15分钟",
      "url": "https://codeforces.com/contest/1234"
    },
    {
      "platform": "LeetCode",
      "name": "Weekly Contest XXX",
      "start_time": "2023-10-21 22:30:00",
      "duration": "1小时30分钟",
      "url": "https://leetcode.com/contest/weekly-contest-xxx"
    }
  ]
}
```

## 本地运行

如果你想在本地运行脚本，请按照以下步骤操作：

1. 安装依赖：

```bash
pip install requests beautifulsoup4 pytz
```

2. 运行脚本：

```bash
python contest_fetcher.py
```

脚本会在当前目录下生成`contests.json`文件。

## GitHub Actions自动更新

本项目已配置GitHub Actions工作流，会在每天UTC时间0点（北京时间8点）自动运行脚本并更新数据。

你也可以在GitHub仓库页面手动触发工作流运行。

## 依赖库

- requests: 用于发送HTTP请求
- beautifulsoup4: 用于解析HTML页面
- pytz: 用于处理时区信息