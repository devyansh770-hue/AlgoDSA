"""
GeeksforGeeks (GFG) Sync Service.

Fetches user statistics and topic-wise problem solved counts from GFG's public profile API
and web endpoints.
"""
import requests
import json
import re
from django.utils import timezone


def clean_handle(username):
    if not username:
        return ''
    s = str(username).strip().rstrip('/')
    if '/' in s:
        s = s.split('/')[-1]
    return s.lstrip('@')


class GFGSyncService:
    """Service to fetch and parse GeeksforGeeks user statistics."""

    API_URL = 'https://authapi.geeksforgeeks.org/api-get/user-profile-info/'
    PROFILE_URL = 'https://www.geeksforgeeks.org/user/{handle}/'

    def __init__(self, username):
        self.username = clean_handle(username)

    def fetch_stats(self):
        """
        Fetch GFG user stats including total solved and topic breakdown.
        """
        if not self.username:
            return {'success': False, 'error': 'No GeeksforGeeks username provided.'}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html',
        }

        try:
            # 1. Try GFG profile API
            response = requests.get(
                f"{self.API_URL}?user_handle={self.username}",
                headers=headers,
                timeout=10
            )

            total_solved = 0
            easy_solved = 0
            medium_solved = 0
            hard_solved = 0
            school_solved = 0
            basic_solved = 0

            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {})
                if user_data:
                    total_solved = int(user_data.get('total_problems_solved', 0) or 0)
                    easy_solved = int(user_data.get('easy_problems_solved', 0) or 0)
                    medium_solved = int(user_data.get('medium_problems_solved', 0) or 0)
                    hard_solved = int(user_data.get('hard_problems_solved', 0) or 0)
                    basic_solved = int(user_data.get('basic_problems_solved', 0) or 0)

            # 2. Scrape GFG profile page for fallback & topic breakdown if needed
            topic_breakdown = self._fetch_topic_breakdown(headers)

            # If total_solved is still 0, try fallback estimation from topic breakdown
            if total_solved == 0 and topic_breakdown:
                total_solved = sum(topic_breakdown.values())

            return {
                'success': True,
                'username': self.username,
                'total_solved': total_solved,
                'easy_solved': easy_solved,
                'medium_solved': medium_solved,
                'hard_solved': hard_solved,
                'basic_solved': basic_solved,
                'topic_breakdown': topic_breakdown,
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _fetch_topic_breakdown(self, headers):
        """
        Scrape / parse topic breakdown from user's GFG profile.
        Returns a dict of topic name -> question count.
        """
        topic_counts = {
            'Arrays': 0,
            'Strings': 0,
            'Linked Lists': 0,
            'Trees': 0,
            'Graphs': 0,
            'Dynamic Programming': 0,
            'Two Pointers': 0,
            'Stack & Queue': 0,
            'Heap & Sorting': 0,
        }

        try:
            profile_res = requests.get(
                self.PROFILE_URL.format(handle=self.username),
                headers=headers,
                timeout=10
            )

            if profile_res.status_code == 200:
                html = profile_res.text

                # Match GFG JSON state or regex patterns for topic counts
                # GFG embeds __NEXT_DATA__ JSON script
                next_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
                if next_data_match:
                    try:
                        data = json.loads(next_data_match.group(1))
                        props = data.get('props', {}).get('pageProps', {}).get('userInfo', {})
                        tags = props.get('tags', []) or props.get('topicWiseSolved', {})
                        if isinstance(tags, list):
                            for tag in tags:
                                name = tag.get('tagName', '')
                                count = tag.get('solvedCount', 0)
                                self._map_tag_to_topic(name, count, topic_counts)
                        elif isinstance(tags, dict):
                            for name, count in tags.items():
                                self._map_tag_to_topic(str(name), int(count), topic_counts)
                    except Exception:
                        pass

                # Fallback: regex search for common topic strings in GFG profile HTML
                for topic in ['Arrays', 'Strings', 'Tree', 'Graph', 'Linked List', 'Dynamic Programming', 'Searching', 'Sorting', 'Stack', 'Queue']:
                    match = re.search(rf'{topic}\s*\:\s*(\d+)', html, re.IGNORECASE)
                    if match:
                        cnt = int(match.group(1))
                        self._map_tag_to_topic(topic, cnt, topic_counts)

        except Exception:
            pass

        return topic_counts

    def _map_tag_to_topic(self, tag_name, count, topic_counts):
        """Map GFG tag string to normalized AlgoDSA topic categories."""
        tag_lower = tag_name.lower()
        if 'array' in tag_lower or 'matrix' in tag_lower:
            topic_counts['Arrays'] += count
        elif 'string' in tag_lower:
            topic_counts['Strings'] += count
        elif 'link' in tag_lower or 'list' in tag_lower:
            topic_counts['Linked Lists'] += count
        elif 'tree' in tag_lower or 'bst' in tag_lower:
            topic_counts['Trees'] += count
        elif 'graph' in tag_lower or 'bfs' in tag_lower or 'dfs' in tag_lower:
            topic_counts['Graphs'] += count
        elif 'dynamic' in tag_lower or 'dp' in tag_lower:
            topic_counts['Dynamic Programming'] += count
        elif 'pointer' in tag_lower or 'slide' in tag_lower or 'window' in tag_lower:
            topic_counts['Two Pointers'] += count
        elif 'stack' in tag_lower or 'queue' in tag_lower:
            topic_counts['Stack & Queue'] += count
        elif 'heap' in tag_lower or 'sort' in tag_lower or 'search' in tag_lower:
            topic_counts['Heap & Sorting'] += count

    def sync_user(self, user):
        """Sync GeeksforGeeks data to User model."""
        stats = self.fetch_stats()
        if not stats.get('success'):
            return stats

        user.gfg_username = self.username
        user.gfg_total_solved = stats['total_solved']
        user.last_gfg_sync = timezone.now()

        # Update platform_stats_json
        stats_json = user.platform_stats_json or {}
        stats_json['gfg'] = {
            'username': self.username,
            'total_solved': stats['total_solved'],
            'easy_solved': stats.get('easy_solved', 0),
            'medium_solved': stats.get('medium_solved', 0),
            'hard_solved': stats.get('hard_solved', 0),
            'topic_breakdown': stats.get('topic_breakdown', {}),
            'last_synced': timezone.now().isoformat(),
        }
        user.platform_stats_json = stats_json
        user.save()

        return {
            'success': True,
            'gfg_username': self.username,
            'total_solved_gfg': stats['total_solved'],
            'stats': stats,
        }
