import json
from datetime import datetime, timedelta
from typing import List, Dict


def load_contests(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_upcoming(contests: List[Dict], within_days: int = 3) -> List[Dict]:
    """Return contests within the next `within_days` days from now."""
    now = datetime.now()
    end = now + timedelta(days=within_days)
    out = []
    for c in contests:
        try:
            st = datetime.strptime(c["start_time"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue
        if now <= st <= end:
            out.append({**c, "start_dt": st})
    out.sort(key=lambda x: x["start_dt"])
    return out


def parse_duration(duration: str) -> timedelta:
    """解析比赛时长字符串为 timedelta 对象"""
    try:
        hours = minutes = 0
        if "小时" in duration and "分钟" in duration:
            h, m = duration.split("小时")
            hours = int(h)
            minutes = int(m.replace("分钟", ""))
        elif "小时" in duration:
            hours = int(duration.replace("小时", ""))
        elif "分钟" in duration:
            minutes = int(duration.replace("分钟", ""))
        return timedelta(hours=hours, minutes=minutes)
    except (ValueError, AttributeError):
        return timedelta(hours=2)  # 默认时长 2 小时

def filter_next_24h(contests: List[Dict]) -> List[Dict]:
    """筛选未来24小时内的且结束时间在当前时间之后的比赛"""
    now = datetime.now()
    end_window = now + timedelta(hours=24)
    out = []
    
    for c in contests:
        try:
            start_time = datetime.strptime(c["start_time"], "%Y-%m-%d %H:%M:%S")
            duration = parse_duration(c["duration"])
            end_time = start_time + duration
            
            # 比赛开始时间在 24 小时窗口内，且结束时间在当前时间之后
            if start_time <= end_window and end_time > now:
                out.append({
                    **c,
                    "start_dt": start_time,
                    "end_dt": end_time
                })
        except Exception as e:
            print(f"Warning: 无法解析比赛时间: {c.get('name')} - {str(e)}")
            continue
    
    # 按开始时间排序
    out.sort(key=lambda x: x["start_dt"])
    return out


def format_contest(c: Dict) -> str:
    lines = [
        f"平台: {c.get('platform', '')}",
        f"名称: {c.get('name', '')}",
        f"开始时间: {c['start_dt'].strftime('%Y-%m-%d %H:%M:%S')}",
        f"结束时间: {c['end_dt'].strftime('%Y-%m-%d %H:%M:%S')}",
        f"时长: {c.get('duration', '')}",
        f"链接: {c.get('url', '')}",
    ]
    return "\n".join(lines)


def build_email_text(contests: List[Dict]) -> str:
    if not contests:
        return "未来24小时内没有检测到新的比赛。"
    parts = ["以下为未来24小时内的比赛日程：\n"]
    for i, c in enumerate(contests, 1):
        parts.append(f"{i}. {c.get('name')} ({c.get('platform')})")
        parts.append(f"   开始: {c.get('start_dt').strftime('%Y-%m-%d %H:%M:%S')}")
        parts.append(f"   时长: {c.get('duration')}")
        parts.append(f"   链接: {c.get('url')}")
        parts.append("")
    return "\n".join(parts)
