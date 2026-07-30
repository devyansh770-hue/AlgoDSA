import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.progress.services.leetcode import LeetCodeSyncService

service = LeetCodeSyncService('DevyanshVerma01')
counts = service.fetch_tag_counts()
print('Mapped LeetCode Tag Counts for DevyanshVerma01:')
for k, v in counts.items():
    print(f'  {k}: {v}')
