from django.db import models


class Topic(models.Model):
    """A DSA topic category (Arrays, Trees, Graphs, etc.)."""

    CATEGORY_CHOICES = [
        ('foundations', 'Foundations'),
        ('linear', 'Linear Data Structures'),
        ('non_linear', 'Non-Linear Data Structures'),
        ('algorithms', 'Algorithms & Techniques'),
        ('advanced', 'Advanced Data Structures'),
        ('math_bit', 'Math & Bit Manipulation'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='linear')
    description = models.TextField(blank=True, default='')
    real_world_analogy = models.TextField(blank=True, default='')
    notes_content = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=10, default='📚')  # Emoji icon
    color = models.CharField(max_length=7, default='#6366f1')  # Hex color
    estimated_hours = models.PositiveIntegerField(default=5)
    prerequisites = models.CharField(max_length=200, blank=True, default='None')
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


class Pattern(models.Model):
    """A DSA pattern / subtopic under a topic (e.g., Sliding Window under Arrays)."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='patterns')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, default='⚡')
    description = models.TextField(blank=True)
    visualization_type = models.CharField(max_length=50, default='sliding_window', blank=True)
    order = models.PositiveIntegerField(default=0)

    # Stores section / study guide data
    content_json = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'patterns'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.topic.name} - {self.name}"


class Lesson(models.Model):
    """A specific interactive lesson within a topic or pattern."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=10, default='medium')
    estimated_mins = models.PositiveIntegerField(default=20)
    prerequisites = models.CharField(max_length=200, blank=True, default='')

    # Theory & Intuition
    overview = models.TextField(blank=True, default='')
    learning_objectives = models.JSONField(default=list, blank=True)
    real_world_analogy = models.TextField(blank=True, default='')
    why_use = models.TextField(blank=True, default='')
    when_use = models.TextField(blank=True, default='')
    when_not_to_use = models.TextField(blank=True, default='')
    math_intuition = models.TextField(blank=True, default='')

    # Visualizer config
    visualization_type = models.CharField(max_length=50, default='sliding_window')

    # Multi-language Templates & Code Implementation
    code_python = models.TextField(blank=True, default='')
    code_cpp = models.TextField(blank=True, default='')
    code_java = models.TextField(blank=True, default='')
    code_js = models.TextField(blank=True, default='')
    code_go = models.TextField(blank=True, default='')
    code_rust = models.TextField(blank=True, default='')

    # Complexity & Analysis
    time_complexity_best = models.CharField(max_length=50, default='O(1)')
    time_complexity_avg = models.CharField(max_length=50, default='O(N)')
    time_complexity_worst = models.CharField(max_length=50, default='O(N)')
    space_complexity = models.CharField(max_length=50, default='O(1)')
    edge_cases = models.TextField(blank=True, default='')
    common_mistakes = models.TextField(blank=True, default='')
    interview_tips = models.TextField(blank=True, default='')
    advanced_optimizations = models.TextField(blank=True, default='')

    # Quiz & Flashcards
    content_json = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'lessons'
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.topic.name} -> {self.title}"


class VideoResource(models.Model):
    """Curated YouTube video resources for a lesson or topic."""

    CHANNEL_CHOICES = [
        ('love_babbar', 'Love Babbar'),
        ('striver_a2z', 'Striver A2Z'),
        ('neetcode', 'NeetCode Roadmap'),
        ('mit_stanford', 'MIT / Stanford OpenCourseWare'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='video_resources', null=True, blank=True)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name='video_resources', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='video_resources', null=True, blank=True)
    title = models.CharField(max_length=200)
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES, default='striver_a2z')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='intermediate')
    youtube_url = models.URLField()
    video_id = models.CharField(max_length=50, blank=True, default='')
    duration = models.CharField(max_length=20, default='15m')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'video_resources'
        ordering = ['order', 'title']

    def __str__(self):
        return f"[{self.get_channel_display()}] {self.title}"


class Problem(models.Model):
    """A DSA problem with description, starter code, and editorial."""

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    PRACTICE_TIER_CHOICES = [
        ('concept_building', 'Concept Building (Easy)'),
        ('pattern_recognition', 'Pattern Recognition (Easy-Medium)'),
        ('pattern_mastery', 'Pattern Mastery (Medium)'),
        ('interview_ready', 'Interview Ready (Medium-Hard)'),
        ('expert', 'Expert (Hard)'),
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
    pattern_obj = models.ForeignKey(Pattern, on_delete=models.SET_NULL, null=True, blank=True, related_name='problems')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='problems')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    practice_tier = models.CharField(max_length=30, choices=PRACTICE_TIER_CHOICES, default='concept_building')
    pattern = models.CharField(max_length=30, choices=PATTERN_CHOICES)

    # Roadmaps & Platform Metadata
    roadmap_tags = models.JSONField(default=list, blank=True)  # ['love_babbar', 'striver_a2z', 'neetcode', 'blind75']
    company_tags = models.JSONField(default=list, blank=True)  # ['Google', 'Amazon', 'Meta', 'Microsoft']
    acceptance_rate = models.CharField(max_length=10, default='65%')
    est_time_mins = models.PositiveIntegerField(default=20)

    starter_code_python = models.TextField(blank=True, default='')
    starter_code_javascript = models.TextField(blank=True, default='')
    starter_code_cpp = models.TextField(blank=True, default='')
    starter_code_java = models.TextField(blank=True, default='')
    starter_code_go = models.TextField(blank=True, default='')
    starter_code_rust = models.TextField(blank=True, default='')

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
            'go': self.starter_code_go,
            'rust': self.starter_code_rust,
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


