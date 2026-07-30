"""
LeetCode Sync Service using LeetCode GraphQL API.

Fetches user solved statistics and recent accepted submissions from LeetCode,
matches them against AlgoDSA problems, and updates pattern mastery, topic progress,
streaks, and submission records.
"""
import requests
from datetime import datetime
from django.utils import timezone
from apps.problems.models import Problem
from apps.submissions.models import Submission
from apps.progress.services.spaced_repetition import update_mastery


def clean_handle(username):
    if not username:
        return ''
    s = str(username).strip().rstrip('/')
    if '/' in s:
        s = s.split('/')[-1]
    return s.lstrip('@')


class LeetCodeSyncService:
    """Service to fetch and sync LeetCode activity."""

    GRAPHQL_URL = 'https://leetcode.com/graphql'

    USER_STATS_QUERY = """
    query userProblemsSolved($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """

    RECENT_AC_QUERY = """
    query userRecentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """

    TAG_COUNTS_QUERY = """
    query userTagProblemCounts($username: String!) {
      matchedUser(username: $username) {
        tagProblemCounts {
          advanced { tagName tagSlug problemsSolved }
          intermediate { tagName tagSlug problemsSolved }
          fundamental { tagName tagSlug problemsSolved }
        }
      }
    }
    """

    def __init__(self, username):
        self.username = clean_handle(username)

    def fetch_stats(self):
        """Fetch total solved count and difficulty stats for username."""
        if not self.username:
            return {'success': False, 'error': 'No username provided'}

        try:
            response = requests.post(
                self.GRAPHQL_URL,
                json={'query': self.USER_STATS_QUERY, 'variables': {'username': self.username}},
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            if response.status_code != 200:
                return {'success': False, 'error': f'LeetCode API returned status {response.status_code}'}

            data = response.json()
            matched_user = data.get('data', {}).get('matchedUser')
            if not matched_user:
                return {'success': False, 'error': f'LeetCode user "{self.username}" not found'}

            stats = matched_user.get('submitStatsGlobal', {}).get('acSubmissionNum', [])
            total_solved = 0
            easy_solved = 0
            medium_solved = 0
            hard_solved = 0

            for item in stats:
                diff = item.get('difficulty')
                count = item.get('count', 0)
                if diff == 'All':
                    total_solved = count
                elif diff == 'Easy':
                    easy_solved = count
                elif diff == 'Medium':
                    medium_solved = count
                elif diff == 'Hard':
                    hard_solved = count

            return {
                'success': True,
                'total_solved': total_solved,
                'easy_solved': easy_solved,
                'medium_solved': medium_solved,
                'hard_solved': hard_solved,
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def fetch_recent_ac(self, limit=50):
        """Fetch recent accepted submissions."""
        if not self.username:
            return []

        try:
            response = requests.post(
                self.GRAPHQL_URL,
                json={'query': self.RECENT_AC_QUERY, 'variables': {'username': self.username, 'limit': limit}},
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('recentAcSubmissionList', [])
        except Exception:
            pass
        return []

    def fetch_tag_counts(self):
        """Fetch exact tag/topic problem counts from LeetCode."""
        if not self.username:
            return {}

        tag_counts = {
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
            response = requests.post(
                self.GRAPHQL_URL,
                json={'query': self.TAG_COUNTS_QUERY, 'variables': {'username': self.username}},
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                tag_data = data.get('data', {}).get('matchedUser', {}).get('tagProblemCounts', {})
                if tag_data:
                    for level in ['fundamental', 'intermediate', 'advanced']:
                        items = tag_data.get(level, []) or []
                        for item in items:
                            t_name = item.get('tagName', '')
                            cnt = item.get('problemsSolved', 0)
                            self._map_lc_tag_to_topic(t_name, cnt, tag_counts)
        except Exception:
            pass

        return tag_counts

    def _map_lc_tag_to_topic(self, tag_name, count, tag_counts):
        """Map LeetCode tag to normalized topic categories."""
        tag_lower = tag_name.lower()
        if 'array' in tag_lower or 'matrix' in tag_lower:
            tag_counts['Arrays'] += count
        elif 'string' in tag_lower:
            tag_counts['Strings'] += count
        elif 'linked' in tag_lower or 'list' in tag_lower:
            tag_counts['Linked Lists'] += count
        elif 'tree' in tag_lower or 'binary tree' in tag_lower or 'bst' in tag_lower:
            tag_counts['Trees'] += count
        elif 'graph' in tag_lower or 'breadth-first' in tag_lower or 'depth-first' in tag_lower:
            tag_counts['Graphs'] += count
        elif 'dynamic' in tag_lower or 'dp' in tag_lower:
            tag_counts['Dynamic Programming'] += count
        elif 'two pointer' in tag_lower or 'sliding window' in tag_lower:
            tag_counts['Two Pointers'] += count
        elif 'stack' in tag_lower or 'queue' in tag_lower:
            tag_counts['Stack & Queue'] += count
        elif 'heap' in tag_lower or 'sort' in tag_lower or 'binary search' in tag_lower:
            tag_counts['Heap & Sorting'] += count

    def sync_user(self, user):
        """
        Full sync for a Django user object.

        Returns dict with status and summary of newly synced problems.
        """
        if not self.username:
            return {'success': False, 'error': 'LeetCode username is not configured.'}

        stats_result = self.fetch_stats()
        if not stats_result.get('success'):
            return stats_result

        # Update user LeetCode stats
        user.leetcode_username = self.username
        user.leetcode_total_solved = stats_result['total_solved']

        # Fetch exact tag problem counts from LeetCode
        lc_tag_counts = self.fetch_tag_counts()

        # Fetch recent AC submissions from LeetCode
        recent_ac = self.fetch_recent_ac(limit=50)

        newly_synced_count = 0
        matched_problems = []

        # Get existing problem map by slug
        all_problems = {p.slug: p for p in Problem.objects.all()}

        for sub in recent_ac:
            title_slug = sub.get('titleSlug', '')
            sub_id = str(sub.get('id', ''))
            timestamp_str = sub.get('timestamp')

            # Find matching problem in our DB
            problem = all_problems.get(title_slug)
            if not problem:
                # Try matching by title fallback
                title = sub.get('title', '').strip().lower()
                for p in all_problems.values():
                    if p.title.strip().lower() == title:
                        problem = p
                        break

            if problem:
                matched_problems.append(problem.title)

                # Check if submission already recorded
                existing = Submission.objects.filter(
                    user=user,
                    problem=problem,
                    status='accepted'
                ).exists()

                if not existing:
                    # Parse timestamp if available
                    created_dt = timezone.now()
                    if timestamp_str:
                        try:
                            created_dt = datetime.fromtimestamp(int(timestamp_str), tz=timezone.utc)
                        except (ValueError, TypeError):
                            pass

                    # Create synced submission record
                    sub_record = Submission.objects.create(
                        user=user,
                        problem=problem,
                        code=f"# Synced automatically from LeetCode ({sub.get('title')})\n# Submission ID: {sub_id}",
                        language=user.preferred_language or 'python',
                        status='accepted',
                        runtime_ms=0.0,
                        memory_kb=0.0,
                        test_cases_passed=problem.test_cases.count() or 1,
                        test_cases_total=problem.test_cases.count() or 1,
                        is_leetcode_synced=True,
                        leetcode_submission_id=sub_id,
                    )
                    # Backdate creation date to match LeetCode timestamp
                    Submission.objects.filter(id=sub_record.id).update(created_at=created_dt)

                    # Update pattern mastery & topic progress
                    update_mastery(user, problem, correct=True)
                    newly_synced_count += 1

        # Recalculate user's solved count
        distinct_solved = Submission.objects.filter(
            user=user,
            status='accepted'
        ).values('problem').distinct().count()

        user.solved_count = distinct_solved
        user.last_leetcode_sync = timezone.now()

        # Update platform_stats_json with exact LC tag counts
        stats_json = user.platform_stats_json or {}
        stats_json['leetcode'] = {
            'username': self.username,
            'total_solved': stats_result['total_solved'],
            'easy_solved': stats_result.get('easy_solved', 0),
            'medium_solved': stats_result.get('medium_solved', 0),
            'hard_solved': stats_result.get('hard_solved', 0),
            'tag_counts': lc_tag_counts,
            'last_synced': timezone.now().isoformat(),
        }
        user.platform_stats_json = stats_json

        user.update_streak()
        user.save()

        return {
            'success': True,
            'leetcode_username': self.username,
            'total_solved_leetcode': stats_result['total_solved'],
            'newly_synced_count': newly_synced_count,
            'matched_problems': list(set(matched_problems)),
            'stats': stats_result,
            'tag_counts': lc_tag_counts,
        }
