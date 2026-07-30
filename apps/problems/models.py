from django.db import models


class Topic(models.Model):
    """A DSA topic category (Arrays, Trees, Graphs, etc.)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    real_world_analogy = models.TextField(blank=True, default='')
    notes_content = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=10, default='📚')  # Emoji icon
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'topics'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def problem_count(self):
        return self.problems.count()


class Problem(models.Model):
    """A DSA problem with description, starter code, and editorial."""

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    PATTERN_CHOICES = [
        ('two_pointers', 'Two Pointers'),
        ('sliding_window', 'Sliding Window'),
        ('binary_search', 'Binary Search'),
        ('bfs', 'BFS'),
        ('dfs', 'DFS'),
        ('dynamic_programming', 'Dynamic Programming'),
        ('greedy', 'Greedy'),
        ('backtracking', 'Backtracking'),
        ('hash_map', 'Hash Map'),
        ('stack', 'Stack'),
        ('queue', 'Queue'),
        ('linked_list', 'Linked List'),
        ('tree_traversal', 'Tree Traversal'),
        ('graph_traversal', 'Graph Traversal'),
        ('sorting', 'Sorting'),
        ('recursion', 'Recursion'),
        ('bit_manipulation', 'Bit Manipulation'),
        ('math', 'Math'),
        ('string_manipulation', 'String Manipulation'),
        ('heap', 'Heap'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    pattern = models.CharField(max_length=30, choices=PATTERN_CHOICES)
    starter_code_python = models.TextField(blank=True, default='')
    starter_code_javascript = models.TextField(blank=True, default='')
    starter_code_cpp = models.TextField(blank=True, default='')
    starter_code_java = models.TextField(blank=True, default='')
    editorial = models.TextField(blank=True, default='')
    constraints = models.TextField(blank=True, default='')
    examples = models.TextField(blank=True, default='')  # Markdown formatted
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'problems'
        ordering = ['order', 'difficulty', 'title']

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title}"

    def get_starter_code(self, language='python'):
        """Return starter code for the given language."""
        code_map = {
            'python': self.starter_code_python,
            'javascript': self.starter_code_javascript,
            'cpp': self.starter_code_cpp,
            'java': self.starter_code_java,
        }
        return code_map.get(language, self.starter_code_python)

    @property
    def leetcode_url(self):
        """Direct URL to problem on LeetCode."""
        return f"https://leetcode.com/problems/{self.slug}/"

    @property
    def gfg_url(self):
        """Direct URL to problem search on GeeksforGeeks."""
        import urllib.parse
        encoded_title = urllib.parse.quote(self.title)
        return f"https://www.geeksforgeeks.org/explore?page=1&search={encoded_title}"

    @property
    def difficulty_color(self):
        colors = {
            'easy': '#10b981',
            'medium': '#f59e0b',
            'hard': '#ef4444',
        }
        return colors.get(self.difficulty, '#6366f1')


class TestCase(models.Model):
    """Test case for a problem."""

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)  # Visible to user
    explanation = models.TextField(blank=True, default='')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'test_cases'
        ordering = ['order']

    def __str__(self):
        return f"TestCase for {self.problem.title} ({'Sample' if self.is_sample else 'Hidden'})"


class Hint(models.Model):
    """Progressive hints for a problem (3 levels)."""

    LEVEL_CHOICES = [
        (1, 'Level 1 - Direction'),
        (2, 'Level 2 - Pattern'),
        (3, 'Level 3 - Pseudocode'),
    ]

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='hints')
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    content = models.TextField()

    class Meta:
        db_table = 'hints'
        ordering = ['level']
        unique_together = ['problem', 'level']

    def __str__(self):
        return f"Hint L{self.level} for {self.problem.title}"

class Pattern(models.Model):
    """A DSA pattern under a topic (e.g., Sliding Window under Arrays)."""
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='patterns')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, default='⚡')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    # Stores the 21 sections of study guide data
    content_json = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'patterns'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.topic.name} - {self.name}"

