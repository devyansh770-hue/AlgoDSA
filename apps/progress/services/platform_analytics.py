"""
Multi-Platform Analytics Service.

Combines and analyzes problem-solving data across:
1. Native AlgoDSA submissions
2. LeetCode GraphQL API
3. GeeksforGeeks API / Profile

Calculates total combined questions solved, per-topic question count matrix
(Trees, Graphs, Linked Lists, Two Pointers, DP, Arrays, Strings, etc.),
and platform distribution metrics.
"""
from apps.submissions.models import Submission
from apps.problems.models import Problem, Topic
from apps.progress.models import PatternMastery


def clean_handle(username):
    if not username:
        return ''
    s = str(username).strip().rstrip('/')
    if '/' in s:
        s = s.split('/')[-1]
    return s.lstrip('@')


class MultiPlatformAnalyticsService:
    """Service for cross-platform data aggregation and topic analysis."""

    TOPIC_KEYS = [
        {'key': 'arrays', 'name': 'Arrays', 'icon': '📊'},
        {'key': 'strings', 'name': 'Strings', 'icon': '🔤'},
        {'key': 'linked_list', 'name': 'Linked Lists', 'icon': '🔗'},
        {'key': 'trees', 'name': 'Trees & BST', 'icon': '🌳'},
        {'key': 'graphs', 'name': 'Graphs', 'icon': '🕸️'},
        {'key': 'dp', 'name': 'Dynamic Programming', 'icon': '🧩'},
        {'key': 'pointers', 'name': 'Two Pointers', 'icon': '👉'},
        {'key': 'stack_queue', 'name': 'Stack & Queue', 'icon': '📚'},
    ]

    def __init__(self, user):
        self.user = user

    def get_comprehensive_analytics(self):
        """
        Build and return complete analytics dictionary for dashboard rendering.
        """
        user = self.user

        # Clean usernames in case full URLs were stored
        leetcode_username = clean_handle(user.leetcode_username)
        gfg_username = clean_handle(user.gfg_username)
        if user.leetcode_username != leetcode_username or user.gfg_username != gfg_username:
            user.leetcode_username = leetcode_username
            user.gfg_username = gfg_username
            user.save(update_fields=['leetcode_username', 'gfg_username'])

        # 1. Native AlgoDSA stats
        accepted_subs = Submission.objects.filter(
            user=user, status='accepted'
        ).select_related('problem', 'problem__topic')

        algodsa_solved_ids = set()
        algodsa_leetcode_synced_ids = set()

        for sub in accepted_subs:
            algodsa_solved_ids.add(sub.problem_id)
            if sub.is_leetcode_synced:
                algodsa_leetcode_synced_ids.add(sub.problem_id)

        native_algodsa_count = len(algodsa_solved_ids - algodsa_leetcode_synced_ids)
        leetcode_synced_count = len(algodsa_leetcode_synced_ids)

        # 2. LeetCode stats
        leetcode_username = user.leetcode_username
        leetcode_total = user.leetcode_total_solved or leetcode_synced_count
        lc_data = (user.platform_stats_json or {}).get('leetcode', {})
        lc_tag_counts = lc_data.get('tag_counts', {})
        lc_easy = lc_data.get('easy_solved', 0)
        lc_medium = lc_data.get('medium_solved', 0)
        lc_hard = lc_data.get('hard_solved', 0)

        # If user has a LeetCode username but tag_counts is empty or missing, fetch live!
        if leetcode_username and not lc_tag_counts:
            try:
                from apps.progress.services.leetcode import LeetCodeSyncService
                lc_service = LeetCodeSyncService(leetcode_username)
                lc_tag_counts = lc_service.fetch_tag_counts()
                stats_result = lc_service.fetch_stats()
                if stats_result.get('success'):
                    leetcode_total = stats_result['total_solved']
                    user.leetcode_total_solved = leetcode_total
                    lc_easy = stats_result.get('easy_solved', 0)
                    lc_medium = stats_result.get('medium_solved', 0)
                    lc_hard = stats_result.get('hard_solved', 0)

                stats_json = user.platform_stats_json or {}
                if 'leetcode' not in stats_json:
                    stats_json['leetcode'] = {}
                stats_json['leetcode']['tag_counts'] = lc_tag_counts
                stats_json['leetcode']['total_solved'] = leetcode_total
                stats_json['leetcode']['easy_solved'] = lc_easy
                stats_json['leetcode']['medium_solved'] = lc_medium
                stats_json['leetcode']['hard_solved'] = lc_hard
                user.platform_stats_json = stats_json
                user.save(update_fields=['platform_stats_json', 'leetcode_total_solved'])
            except Exception:
                pass

        # 3. GFG stats
        gfg_username = user.gfg_username
        gfg_total = user.gfg_total_solved or 0
        gfg_data = (user.platform_stats_json or {}).get('gfg', {})
        gfg_topic_breakdown = gfg_data.get('topic_breakdown', {})
        gfg_easy = gfg_data.get('easy_solved', 0)
        gfg_medium = gfg_data.get('medium_solved', 0)
        gfg_hard = gfg_data.get('hard_solved', 0)

        # 4. Total Combined Solved
        # Simple sum of non-overlapping sources:
        #   native_algodsa_count = problems solved only on AlgoDSA (excludes LC-synced)
        #   leetcode_total = user's full LC profile solved count
        #   gfg_total = user's full GFG profile solved count
        combined_total = native_algodsa_count + leetcode_total + gfg_total

        # 5. Topic-by-Topic Question Breakdown Matrix
        topic_matrix = self._calculate_topic_matrix(
            user=user,
            accepted_subs=accepted_subs,
            lc_tag_counts=lc_tag_counts,
            gfg_topic_breakdown=gfg_topic_breakdown
        )

        # Sum of the topic matrix totals (may exceed combined_total due to LC tag overlap)
        topic_matrix_sum = sum(row['total_count'] for row in topic_matrix)

        # 6. Determine whether syncs actually returned data
        lc_has_data = bool(leetcode_total > 0)
        gfg_has_data = bool(gfg_total > 0)

        # 7. Active Connected Platforms & Latest Sync Timestamp
        connected_platforms = []
        sync_times = []
        if user.last_leetcode_sync:
            sync_times.append(user.last_leetcode_sync)
        if user.last_gfg_sync:
            sync_times.append(user.last_gfg_sync)

        latest_sync = max(sync_times) if sync_times else None

        if leetcode_username:
            connected_platforms.append({
                'name': 'LeetCode',
                'username': leetcode_username,
                'badge_color': '#ffa116',
                'icon': 'globe',
                'solved': leetcode_total,
                'last_sync': user.last_leetcode_sync,
            })
        if gfg_username:
            connected_platforms.append({
                'name': 'GeeksforGeeks',
                'username': gfg_username,
                'badge_color': '#2f9d57',
                'icon': 'code-2',
                'solved': gfg_total,
                'last_sync': user.last_gfg_sync,
            })

        return {
            'has_external_platforms': bool(leetcode_username or gfg_username),
            'connected_platforms': connected_platforms,
            'latest_sync': latest_sync,
            'leetcode_username': leetcode_username,
            'gfg_username': gfg_username,
            'leetcode_total': leetcode_total,
            'gfg_total': gfg_total,
            'native_algodsa_count': native_algodsa_count,
            'leetcode_synced_count': leetcode_synced_count,
            'combined_total': combined_total,
            'topic_matrix': topic_matrix,
            'topic_matrix_sum': topic_matrix_sum,
            # Difficulty breakdown across platforms (for chart)
            'lc_easy': lc_easy,
            'lc_medium': lc_medium,
            'lc_hard': lc_hard,
            'gfg_easy': gfg_easy,
            'gfg_medium': gfg_medium,
            'gfg_hard': gfg_hard,
            # Sync status flags
            'lc_has_data': lc_has_data,
            'gfg_has_data': gfg_has_data,
        }

    def _calculate_topic_matrix(self, user, accepted_subs, lc_tag_counts, gfg_topic_breakdown):
        """
        Build per-topic question count breakdown across platforms.
        """
        # Count native AlgoDSA & LeetCode synced per topic
        local_topic_counts = {
            'Arrays': {'algodsa': 0, 'leetcode': 0},
            'Strings': {'algodsa': 0, 'leetcode': 0},
            'Linked Lists': {'algodsa': 0, 'leetcode': 0},
            'Trees': {'algodsa': 0, 'leetcode': 0},
            'Graphs': {'algodsa': 0, 'leetcode': 0},
            'Dynamic Programming': {'algodsa': 0, 'leetcode': 0},
            'Two Pointers': {'algodsa': 0, 'leetcode': 0},
            'Stack & Queue': {'algodsa': 0, 'leetcode': 0},
        }

        # Collect from AlgoDSA submissions
        processed_problems = set()
        for sub in accepted_subs:
            if sub.problem_id in processed_problems:
                continue
            processed_problems.add(sub.problem_id)

            t_name = sub.problem.topic.name
            pattern = sub.problem.pattern

            # Normalize category
            category = 'Arrays'
            if 'tree' in t_name.lower() or 'tree' in pattern:
                category = 'Trees'
            elif 'graph' in t_name.lower() or 'bfs' in pattern or 'dfs' in pattern:
                category = 'Graphs'
            elif 'link' in t_name.lower() or 'list' in pattern:
                category = 'Linked Lists'
            elif 'string' in t_name.lower() or 'string' in pattern:
                category = 'Strings'
            elif 'dynamic' in t_name.lower() or 'dp' in pattern:
                category = 'Dynamic Programming'
            elif 'pointer' in pattern or 'window' in pattern:
                category = 'Two Pointers'
            elif 'stack' in pattern or 'queue' in pattern:
                category = 'Stack & Queue'

            if category not in local_topic_counts:
                local_topic_counts[category] = {'algodsa': 0, 'leetcode': 0}

            if sub.is_leetcode_synced:
                local_topic_counts[category]['leetcode'] += 1
            else:
                local_topic_counts[category]['algodsa'] += 1

        categories = [
            ('Trees & BST', 'tree-deciduous', 'Trees'),
            ('Graphs', 'network', 'Graphs'),
            ('Linked Lists', 'link', 'Linked Lists'),
            ('Two Pointers & Window', 'move-horizontal', 'Two Pointers'),
            ('Dynamic Programming', 'layers', 'Dynamic Programming'),
            ('Arrays', 'table', 'Arrays'),
            ('Strings', 'type', 'Strings'),
            ('Stack & Queue', 'rows', 'Stack & Queue'),
        ]

        matrix = []
        for display_name, lucide_icon, key in categories:
            local = local_topic_counts.get(key, {'algodsa': 0, 'leetcode': 0})
            algodsa_cnt = local['algodsa']

            # Use exact LeetCode tag count if available, otherwise synced count or fallback
            leetcode_cnt = lc_tag_counts.get(key, 0)
            if leetcode_cnt == 0:
                leetcode_cnt = local['leetcode']

            gfg_cnt = gfg_topic_breakdown.get(key, 0)

            total_topic_solved = algodsa_cnt + leetcode_cnt + gfg_cnt

            matrix.append({
                'name': display_name,
                'topic': display_name,
                'icon': lucide_icon,
                'lucide_icon': lucide_icon,
                'algodsa_count': algodsa_cnt,
                'algodsa_solved': algodsa_cnt,
                'leetcode_count': leetcode_cnt,
                'leetcode_solved': leetcode_cnt,
                'gfg_count': gfg_cnt,
                'gfg_solved': gfg_cnt,
                'total_count': total_topic_solved,
                'combined_solved': total_topic_solved,
            })

        return matrix
