from typing import List, Dict, Optional
from contest_fetcher import ContestFetcher

class ContestAPI:
    """统一的比赛信息获取API接口"""
    
    def __init__(self):
        self._fetcher = ContestFetcher()
    
    def get_all_contests(self) -> List[Dict]:
        """获取所有平台的比赛信息
        
        Returns:
            List[Dict]: 包含所有平台比赛信息的列表
        """
        contests = []
        contests.extend(self.get_codeforces_contests())
        contests.extend(self.get_leetcode_contests())
        return sorted(contests, key=lambda x: x['start_time'])
    
    def get_codeforces_contests(self) -> List[Dict]:
        """获取Codeforces平台的比赛信息
        
        Returns:
            List[Dict]: Codeforces比赛信息列表
        """
        return self._fetcher.fetch_codeforces_contests()
    
    def get_leetcode_contests(self) -> List[Dict]:
        """获取LeetCode平台的比赛信息
        
        Returns:
            List[Dict]: LeetCode比赛信息列表
        """
        return self._fetcher.fetch_leetcode_contests()
    
    def get_contests_by_platform(self, platform: str) -> List[Dict]:
        """根据平台名称获取比赛信息
        
        Args:
            platform (str): 平台名称，可选值：'Codeforces', 'LeetCode'
            
        Returns:
            List[Dict]: 指定平台的比赛信息列表
        """
        platform = platform.lower()
        if platform == 'codeforces':
            return self.get_codeforces_contests()
        elif platform == 'leetcode':
            return self.get_leetcode_contests()
        else:
            return []
