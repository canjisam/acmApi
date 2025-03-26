import requests
import json
import datetime
import os
from bs4 import BeautifulSoup
import pytz
import re
import urllib.parse


class ContestFetcher:
    def __init__(self):
        self.output_file = 'contests.json'
        self.timezone = pytz.timezone('Asia/Shanghai')
        
    def fetch_codeforces_contests(self):
        """
        获取Codeforces比赛信息
        """
        print("Fetching Codeforces contests...")
        url = "https://codeforces.com/api/contest.list"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error fetching Codeforces contests: {response.status_code}")
            return []
        
        data = response.json()
        if data.get('status') != 'OK':
            print(f"Error in Codeforces API response: {data.get('comment', 'Unknown error')}")
            return []
        
        contests = data.get('result', [])
        
        # 获取当前时间和一个月后的时间
        now = datetime.datetime.now()
        one_month_later = now + datetime.timedelta(days=30)
        now_timestamp = int(now.timestamp())
        one_month_later_timestamp = int(one_month_later.timestamp())
        
        # 过滤未来一个月的比赛
        future_contests = []
        for contest in contests:
            # 只获取未来的比赛（包括正在进行的）
            if contest['phase'] == 'BEFORE' or contest['phase'] == 'CODING':
                start_time = contest['startTimeSeconds']
                if start_time >= now_timestamp and start_time <= one_month_later_timestamp:
                    contest_time = datetime.datetime.fromtimestamp(contest['startTimeSeconds'], self.timezone)
                    future_contests.append({
                        'platform': 'Codeforces',
                        'name': contest['name'],
                        'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'duration': f"{contest['durationSeconds'] // 3600}小时{(contest['durationSeconds'] % 3600) // 60}分钟",
                        'url': f"https://codeforces.com/contest/{contest['id']}"
                    })
        
        print(f"Found {len(future_contests)} future Codeforces contests")
        return future_contests
    
    def fetch_leetcode_contests(self):
        """
        获取LeetCode比赛信息
        """
        print("Fetching LeetCode contests...")
        url = "https://leetcode.com/graphql"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com/contest/'
        }
        
        # GraphQL查询获取比赛信息
        query = '''
        {
          allContests {
            title
            titleSlug
            startTime
            duration
            description
          }
        }
        '''
        
        try:
            response = requests.post(url, json={'query': query}, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            contests = data.get('data', {}).get('allContests', [])
            
            # 获取当前时间和一个月后的时间
            now = datetime.datetime.now()
            one_month_later = now + datetime.timedelta(days=30)
            now_timestamp = int(now.timestamp())
            one_month_later_timestamp = int(one_month_later.timestamp())
            
            future_contests = []
            
            for contest in contests:
                start_timestamp = contest.get('startTime')
                if start_timestamp and int(start_timestamp) >= now_timestamp and int(start_timestamp) <= one_month_later_timestamp:
                    contest_time = datetime.datetime.fromtimestamp(int(start_timestamp), self.timezone)
                    # LeetCode的duration字段是以分钟为单位的
                    duration_mins = int(contest.get('duration', 90))  # 默认90分钟
                    
                    # LeetCode比赛通常是1.5小时，如果API返回的值不合理，使用默认值
                    if duration_mins > 180:  # 如果超过3小时，可能是单位错误
                        duration_mins = 90  # 默认使用90分钟
                    
                    future_contests.append({
                        'platform': 'LeetCode',
                        'name': contest.get('title', 'Unknown Contest'),
                        'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'duration': f"{duration_mins // 60}小时{duration_mins % 60}分钟",
                        'url': f"https://leetcode.com/contest/{contest.get('titleSlug', '')}"
                    })
            
            print(f"Found {len(future_contests)} future LeetCode contests")
            return future_contests
            
        except Exception as e:
            print(f"Error fetching LeetCode contests: {e}")
            # 如果GraphQL API失败，尝试备用方法
            return self._fetch_leetcode_contests_backup()
    
    def _fetch_leetcode_contests_backup(self):
        """
        备用方法获取LeetCode比赛信息
        """
        print("Trying backup method for LeetCode contests...")
        url = "https://leetcode.com/contest/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            contest_cards = soup.select('.contest-card')
            
            # 获取当前时间和一个月后的时间
            now = datetime.datetime.now()
            one_month_later = now + datetime.timedelta(days=30)
            
            future_contests = []
            
            for card in contest_cards:
                try:
                    title_elem = card.select_one('.card-title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    
                    # 获取比赛时间信息
                    time_elem = card.select_one('.contest-time')
                    if not time_elem:
                        continue
                    
                    time_text = time_elem.text.strip()
                    
                    # 尝试解析时间
                    try:
                        # LeetCode时间格式可能会变，这里做一个简单处理
                        # 假设格式为 "Oct 21, 2023 22:30"
                        date_parts = time_text.split(',')
                        if len(date_parts) >= 2:
                            date_str = date_parts[0].strip() + ',' + date_parts[1].strip()
                            contest_time = datetime.datetime.strptime(date_str, "%b %d, %Y")
                            
                            # 如果比赛时间在未来一个月内
                            if contest_time >= now and contest_time <= one_month_later:
                                # 获取比赛链接
                                link_elem = card.select_one('a')
                                url = f"https://leetcode.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else "#"
                                
                                future_contests.append({
                                    'platform': 'LeetCode',
                                    'name': title,
                                    'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'duration': '1小时30分钟',  # LeetCode比赛通常是1.5小时
                                    'url': url
                                })
                    except Exception as e:
                        print(f"Error parsing LeetCode contest time: {e}")
                        continue
                        
                except Exception as e:
                    print(f"Error processing LeetCode contest card: {e}")
                    continue
            
            print(f"Found {len(future_contests)} future LeetCode contests")
            return future_contests
            
        except Exception as e:
            print(f"Error fetching LeetCode contests with backup method: {e}")
            return []
    
    def fetch_nowcoder_contests(self):
        """
        获取牛客网比赛信息
        """
        print("Fetching Nowcoder contests...")
        url = "https://ac.nowcoder.com/acm/calendar/contest"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://ac.nowcoder.com',
            'Referer': 'https://ac.nowcoder.com/acm/contest/vip-index'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # 解析JSON响应
            calendar_data = response.json().get('data', [])
            
            # 获取当前时间和一个月后的时间
            now = datetime.datetime.now()
            one_month_later = now + datetime.timedelta(days=30)
            
            future_contests = []
            
            # 遍历日历数据
            for contest in calendar_data:
                try:
                    start_time_str = contest.get('startTime')
                    end_time_str = contest.get('endTime')
                    
                    if not start_time_str or not end_time_str:
                        continue
                    
                    # 将时间戳转换为datetime对象
                    contest_time = datetime.datetime.fromtimestamp(int(start_time_str) / 1000)
                    end_time = datetime.datetime.fromtimestamp(int(end_time_str) / 1000)
                    
                    # 计算持续时间
                    duration_seconds = (end_time - contest_time).total_seconds()
                    hours = int(duration_seconds // 3600)
                    minutes = int((duration_seconds % 3600) // 60)
                    
                    # 如果比赛时间在未来一个月内
                    if contest_time >= now and contest_time <= one_month_later:
                        future_contests.append({
                            'platform': '牛客网',
                            'name': contest.get('contestName', 'Unknown Contest'),
                            'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'duration': f"{hours}小时{minutes}分钟",
                            'url': contest.get('link','https://ac.nowcoder.com/acm/contest/vip-index')
                        })
                except Exception as e:
                    print(f"Error processing Nowcoder contest: {e}")
                    continue
            
            print(f"Found {len(future_contests)} future Nowcoder contests")
            return future_contests
            
        except Exception as e:
            print(f"Error fetching Nowcoder contests: {e}")
            return []
    
    def fetch_jisuanke_contests(self):
        """
        获取计蒜客比赛信息
        """
        print("Fetching Jisuanke contests...")
        url = "https://www.jisuanke.com/contest"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.jisuanke.com/'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            contest_items = soup.select('.contest-item')
            
            # 获取当前时间和一个月后的时间
            now = datetime.datetime.now()
            one_month_later = now + datetime.timedelta(days=30)
            
            future_contests = []
            
            for item in contest_items:
                try:
                    # 获取比赛名称
                    title_elem = item.select_one('.contest-name')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    
                    # 获取比赛时间信息
                    time_elem = item.select_one('.contest-time')
                    if not time_elem:
                        continue
                    
                    time_text = time_elem.text.strip()
                    
                    # 尝试解析时间，计蒜客时间格式可能为 "比赛时间：2023-10-21 19:00 - 2023-10-21 21:00"
                    try:
                        # 提取开始时间
                        start_time_match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', time_text)
                        if not start_time_match:
                            continue
                            
                        start_time_str = start_time_match.group(1)
                        contest_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
                        
                        # 提取结束时间以计算持续时间
                        end_time_match = re.search(r'-\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', time_text)
                        if end_time_match:
                            end_time_str = end_time_match.group(1)
                            end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
                            duration_seconds = (end_time - contest_time).total_seconds()
                            hours = int(duration_seconds // 3600)
                            minutes = int((duration_seconds % 3600) // 60)
                            duration = f"{hours}小时{minutes}分钟"
                        else:
                            duration = "2小时0分钟"  # 默认2小时
                        
                        # 如果比赛时间在未来一个月内
                        if contest_time >= now and contest_time <= one_month_later:
                            # 获取比赛链接
                            link_elem = item.select_one('a')
                            url = f"https://www.jisuanke.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else "https://www.jisuanke.com/contest"
                            
                            future_contests.append({
                                'platform': '计蒜客',
                                'name': title,
                                'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'duration': duration,
                                'url': url
                            })
                    except Exception as e:
                        print(f"Error parsing Jisuanke contest time: {e}")
                        continue
                        
                except Exception as e:
                    print(f"Error processing Jisuanke contest item: {e}")
                    continue
            
            print(f"Found {len(future_contests)} future Jisuanke contests")
            return future_contests
            
        except Exception as e:
            print(f"Error fetching Jisuanke contests: {e}")
            return []
    
    def fetch_luogu_contests(self):
        """
        获取洛谷比赛信息
        """
        print("Fetching Luogu contests...")
        url = "https://www.luogu.com.cn/contest/list"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': '_uid=0',  # 添加一个空的用户ID cookie以避免重定向
            'Accept': 'text/html,application/xhtml+xml,application/xml'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # 洛谷页面使用了特殊的数据加载方式，尝试从页面提取JSON数据
            json_data_match = re.search(r'window\.__INITIAL_STATE__=(.+?);</script>', response.text)
            if not json_data_match:
                # 尝试另一种可能的格式
                json_data_match = re.search(r'decodeURIComponent\("(.+?)"\)', response.text)
                if not json_data_match:
                    print("Could not find contest data in Luogu page")
                    return []
                    
                # 解码URL编码的JSON数据
                json_str = urllib.parse.unquote(json_data_match.group(1))
            else:
                json_str = json_data_match.group(1)
                
            try:
                json_data = json.loads(json_str)
                contests = json_data.get('contests', {}).get('result', [])
                if not contests:
                    # 尝试其他可能的数据结构
                    contests = json_data.get('currentData', {}).get('contests', {}).get('result', [])
            except json.JSONDecodeError:
                print("Failed to parse Luogu contest JSON data")
                return []
            
            # 获取当前时间和一个月后的时间
            now = datetime.datetime.now()
            one_month_later = now + datetime.timedelta(days=30)
            now_timestamp = int(now.timestamp())
            one_month_later_timestamp = int(one_month_later.timestamp())
            
            future_contests = []
            
            for contest in contests:
                try:
                    start_time = contest.get('startTime')
                    end_time = contest.get('endTime')
                    
                    if not start_time or not end_time:
                        continue
                        
                    # 洛谷的时间戳通常是秒级的
                    if start_time >= now_timestamp and start_time <= one_month_later_timestamp:
                        contest_time = datetime.datetime.fromtimestamp(start_time, self.timezone)
                        duration_seconds = end_time - start_time
                        hours = duration_seconds // 3600
                        minutes = (duration_seconds % 3600) // 60
                        
                        future_contests.append({
                            'platform': '洛谷',
                            'name': contest.get('name', 'Unknown Contest'),
                            'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'duration': f"{hours}小时{minutes}分钟",
                            'url': f"https://www.luogu.com.cn/contest/{contest.get('id')}"
                        })
                except Exception as e:
                    print(f"Error processing Luogu contest: {e}")
                    continue
            
            # 如果从JSON数据中无法获取比赛信息，尝试解析HTML
            if not future_contests:
                soup = BeautifulSoup(response.text, 'html.parser')
                contest_items = soup.select('.am-g.lg-table-bg0, .am-g.lg-table-bg1')
                
                for item in contest_items:
                    try:
                        # 检查是否是未来的比赛
                        status_elem = item.select_one('.lg-lg-table-status')
                        if not status_elem or '已结束' in status_elem.text:
                            continue
                        
                        # 获取比赛名称
                        title_elem = item.select_one('a[href^="/contest/"]')
                        if not title_elem:
                            continue
                        
                        title = title_elem.text.strip()
                        contest_id = title_elem['href'].split('/')[-1]
                        
                        # 获取比赛时间信息
                        time_elems = item.select('.lg-inline-up')
                        if len(time_elems) < 2:
                            continue
                        
                        start_time_text = time_elems[0].text.strip()
                        end_time_text = time_elems[1].text.strip()
                        
                        try:
                            # 解析时间，格式可能为 "2023-10-21 19:00:00"
                            contest_time = datetime.datetime.strptime(start_time_text, "%Y-%m-%d %H:%M:%S")
                            end_time = datetime.datetime.strptime(end_time_text, "%Y-%m-%d %H:%M:%S")
                            
                            # 计算持续时间
                            duration_seconds = (end_time - contest_time).total_seconds()
                            hours = int(duration_seconds // 3600)
                            minutes = int((duration_seconds % 3600) // 60)
                            
                            # 如果比赛时间在未来一个月内
                            if contest_time >= now and contest_time <= one_month_later:
                                future_contests.append({
                                    'platform': '洛谷',
                                    'name': title,
                                    'start_time': contest_time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'duration': f"{hours}小时{minutes}分钟",
                                    'url': f"https://www.luogu.com.cn/contest/{contest_id}"
                                })
                        except Exception as e:
                            print(f"Error parsing Luogu contest time: {e}")
                            continue
                    except Exception as e:
                        print(f"Error processing Luogu contest item: {e}")
                        continue
            
            print(f"Found {len(future_contests)} future Luogu contests")
            return future_contests
            
        except Exception as e:
            print(f"Error fetching Luogu contests: {e}")
            return []
    
    def fetch_all_contests(self):
        """
        获取所有平台的比赛信息并合并
        """
        codeforces_contests = self.fetch_codeforces_contests()
        leetcode_contests = self.fetch_leetcode_contests()
        nowcoder_contests = self.fetch_nowcoder_contests()
        jisuanke_contests = self.fetch_jisuanke_contests()
        luogu_contests = self.fetch_luogu_contests()
        
        all_contests = codeforces_contests + leetcode_contests + nowcoder_contests + jisuanke_contests + luogu_contests
        
        # 按开始时间排序
        all_contests.sort(key=lambda x: x['start_time'], reverse=True)
        
        return all_contests
    
    def save_contests(self, contests):
        """
        保存比赛信息到JSON文件
        """
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'last_updated': datetime.datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S'),
                'contests': contests
            }, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(contests)} contests to {self.output_file}")
    
    def run(self):
        """
        运行获取器
        """
        contests = self.fetch_all_contests()
        self.save_contests(contests)
        return contests


if __name__ == "__main__":
    fetcher = ContestFetcher()
    fetcher.run()