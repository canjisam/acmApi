# ACM比赛信息获取器

这个项目用于自动获取并更新未来一个月的编程竞赛信息，支持多个主流竞赛平台，并提供列表和日历两种查看方式。

## 功能特点

- 支持多个主流竞赛平台：
  - Codeforces
  - LeetCode
  - 牛客网
  - 洛谷
- 提供两种比赛信息展示方式：
  - 列表视图：按时间顺序展示所有比赛
  - 日历视图：在日历上直观显示比赛安排
- 支持按平台筛选比赛信息
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
nowcoder_contests = api.get_contests_by_platform('NowCoder')
luogu_contests = api.get_contests_by_platform('Luogu')

# 也可以直接调用特定平台的方法
codeforces_contests = api.get_codeforces_contests()
leetcode_contests = api.get_leetcode_contests()
nowcoder_contests = api.get_nowcoder_contests()
luogu_contests = api.get_luogu_contests()
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
    },
    {
      "platform": "NowCoder",
      "name": "2023牛客挑战赛XXX",
      "start_time": "2023-10-22 19:00:00",
      "duration": "2小时",
      "url": "https://ac.nowcoder.com/acm/contest/xxx"
    },
    {
      "platform": "Luogu",
      "name": "洛谷XXX月月赛",
      "start_time": "2023-10-23 14:00:00",
      "duration": "3小时",
      "url": "https://www.luogu.com.cn/contest/xxx"
    }
  ]
}
```

## 界面使用说明

### 视图切换
- 列表视图：以卡片形式展示所有比赛信息
- 日历视图：在日历上标注比赛日期，方便查看每天的比赛安排

### 平台筛选
- 可以选择特定平台查看其比赛信息
- 点击"全部"显示所有平台的比赛

### 日历导航
在日历视图中：
- 可以通过"上个月