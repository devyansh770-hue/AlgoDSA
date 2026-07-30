"""
Management command to seed the database with DSA problems.
Creates topics, problems, test cases, and hints.
"""
from django.core.management.base import BaseCommand
from apps.problems.models import Topic, Problem, TestCase, Hint


class Command(BaseCommand):
    help = 'Seed the database with DSA topics and problems'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # Create Topics
        topics_data = [
            {'name': 'Arrays', 'slug': 'arrays', 'icon': '📊', 'color': '#6366f1', 'order': 1,
             'description': 'Master array manipulation, searching, and sorting techniques.',
             'real_world_analogy': 'Think of a row of numbered theater seats (0 to N). You can instantly jump to seat #5 in O(1) time by index!',
             'notes_content': '• O(1) random access by index.\n• Common Patterns: Two Pointers, Sliding Window, Prefix Sum.\n• Avoid O(N^2) nested loops when N > 10^4.'},
            {'name': 'Strings', 'slug': 'strings', 'icon': '🔤', 'color': '#8b5cf6', 'order': 2,
             'description': 'String processing, pattern matching, and manipulation algorithms.',
             'real_world_analogy': 'Think of text messages, search queries, or DNA sequences — arrays of characters where order and sub-patterns matter!',
             'notes_content': '• String immutability in Python/Java requires list conversion for O(1) mutations.\n• Common Patterns: HashMap Char Frequency, Two Pointers (Anagrams/Palindromes), KMP Algorithm.'},
            {'name': 'Linked Lists', 'slug': 'linked-lists', 'icon': '🔗', 'color': '#06b6d4', 'order': 3,
             'description': 'Singly, doubly linked lists and pointer manipulation.',
             'real_world_analogy': 'Think of Chrome Browser Tabs (forward/back history navigation) or a Music Playlist where each song holds a pointer to the next track!',
             'notes_content': '• Fast insertions/deletions at head (O(1)).\n• Pointer manipulation techniques: Dummy Head Node, Slow & Fast Pointers (Floyd\'s Cycle Detection).'},
            {'name': 'Trees', 'slug': 'trees', 'icon': '🌳', 'color': '#10b981', 'order': 4,
             'description': 'Binary trees, BST, tree traversals, and recursive algorithms.',
             'real_world_analogy': 'Think of a Computer File System (Folders -> Subfolders -> Files) or a Company Organizational Chart with CEO -> Managers -> Engineers!',
             'notes_content': '• DFS Traversals: Inorder (sorted for BST), Preorder, Postorder.\n• BFS Traversal: Level-order using Queue.\n• Base Case: if not root: return.'},
            {'name': 'Graphs', 'slug': 'graphs', 'icon': '🕸️', 'color': '#f59e0b', 'order': 5,
             'description': 'Graph traversal, shortest paths, and connected components.',
             'real_world_analogy': 'Think of Social Networks (friends connected to friends) or Google Maps (cities connected by roads with distance weights)!',
             'notes_content': '• BFS: Shortest path in unweighted graphs.\n• DFS: Path finding, cycle detection, topological sort.\n• Always maintain a visited set to avoid infinite loops.'},
            {'name': 'Dynamic Programming', 'slug': 'dynamic-programming', 'icon': '🧩', 'color': '#ef4444', 'order': 6,
             'description': 'Optimization problems using memoization and tabulation.',
             'real_world_analogy': 'Think of remembering answers to smaller subproblems (like knowing 1+1=2, so when asked 1+1+1 you just add 1 to your stored answer 2)!',
             'notes_content': '• 5 Steps to DP: 1. Define subproblem state 2. Write recurrence relation 3. Identify base cases 4. Choose memoization vs tabulation 5. Optimize space.'},
        ]

        topics = {}
        for td in topics_data:
            topic, created = Topic.objects.update_or_create(
                slug=td['slug'],
                defaults=td
            )
            topics[td['name']] = topic
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status}: {td["name"]}')

        # Create Problems
        problems_data = [
            # ===== ARRAYS =====
            {
                'topic': 'Arrays',
                'title': 'Two Sum',
                'slug': 'two-sum',
                'difficulty': 'easy',
                'pattern': 'hash_map',
                'order': 1,
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
                'examples': 'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]',
                'constraints': '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists.',
                'starter_code_python': "def two_sum(nums, target):\n    # Your code here\n    pass\n\n# Read input\nnums = list(map(int, input().split()))\ntarget = int(input())\nresult = two_sum(nums, target)\nprint(result)",
                'starter_code_javascript': "function twoSum(nums, target) {\n    // Your code here\n}\n\n// Read input and run",
                'editorial': 'Use a hash map to store each number and its index. For each number, check if (target - number) exists in the hash map.\n\nTime: O(n), Space: O(n)',
                'test_cases': [
                    {'input': '2 7 11 15\n9', 'output': '[0, 1]', 'is_sample': True, 'explanation': 'nums[0] + nums[1] = 2 + 7 = 9'},
                    {'input': '3 2 4\n6', 'output': '[1, 2]', 'is_sample': True, 'explanation': 'nums[1] + nums[2] = 2 + 4 = 6'},
                    {'input': '3 3\n6', 'output': '[0, 1]', 'is_sample': False},
                ],
                'hints': [
                    {1: 'What data structure allows O(1) lookup?'},
                    {2: 'Use a Hash Map to store each number as you iterate. For each number, check if its complement exists.'},
                    {3: 'Pseudocode:\n1. Create empty hash map\n2. For each index i, number n in array:\n   a. complement = target - n\n   b. If complement in hash map -> return [hash_map[complement], i]\n   c. Else -> hash_map[n] = i'},
                ],
            },
            {
                'topic': 'Arrays',
                'title': 'Best Time to Buy and Sell Stock',
                'slug': 'best-time-to-buy-and-sell-stock',
                'difficulty': 'easy',
                'pattern': 'sliding_window',
                'order': 2,
                'description': 'You are given an array prices where prices[i] is the price of a given stock on the ith day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.',
                'examples': 'Input: prices = [7,1,5,3,6,4]\nOutput: 5\nExplanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.\n\nInput: prices = [7,6,4,3,1]\nOutput: 0\nExplanation: No profitable transaction is possible.',
                'constraints': '1 <= prices.length <= 10^5\n0 <= prices[i] <= 10^4',
                'starter_code_python': "def max_profit(prices):\n    # Your code here\n    pass\n\nprices = list(map(int, input().split()))\nprint(max_profit(prices))",
                'editorial': 'Track the minimum price seen so far and the maximum profit at each step.\n\nTime: O(n), Space: O(1)',
                'test_cases': [
                    {'input': '7 1 5 3 6 4', 'output': '5', 'is_sample': True},
                    {'input': '7 6 4 3 1', 'output': '0', 'is_sample': True},
                    {'input': '1 2', 'output': '1', 'is_sample': False},
                ],
                'hints': [
                    {1: 'Think about tracking the minimum value as you scan through the array.'},
                    {2: "Use a Sliding Window / Kadane's approach. Keep track of the minimum price seen so far."},
                    {3: 'Pseudocode:\n1. min_price = infinity, max_profit = 0\n2. For each price:\n   a. min_price = min(min_price, price)\n   b. profit = price - min_price\n   c. max_profit = max(max_profit, profit)\n3. Return max_profit'},
                ],
            },
            {
                'topic': 'Arrays',
                'title': 'Maximum Subarray',
                'slug': 'maximum-subarray',
                'difficulty': 'medium',
                'pattern': 'dynamic_programming',
                'order': 3,
                'description': 'Given an integer array nums, find the subarray with the largest sum, and return its sum.\n\nA subarray is a contiguous non-empty sequence of elements within an array.',
                'examples': 'Input: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6\nExplanation: The subarray [4,-1,2,1] has the largest sum 6.\n\nInput: nums = [1]\nOutput: 1',
                'constraints': '1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4',
                'starter_code_python': "def max_subarray(nums):\n    # Your code here\n    pass\n\nnums = list(map(int, input().split()))\nprint(max_subarray(nums))",
                'editorial': "Kadane's Algorithm: maintain current sum and max sum. Reset current sum to 0 when it goes negative.\n\nTime: O(n), Space: O(1)",
                'test_cases': [
                    {'input': '-2 1 -3 4 -1 2 1 -5 4', 'output': '6', 'is_sample': True},
                    {'input': '1', 'output': '1', 'is_sample': True},
                    {'input': '5 4 -1 7 8', 'output': '23', 'is_sample': False},
                ],
                'hints': [
                    {1: 'Can you solve this in a single pass through the array?'},
                    {2: "This is Kadane's Algorithm - a form of Dynamic Programming."},
                    {3: 'Pseudocode:\n1. current_sum = nums[0], max_sum = nums[0]\n2. For each num from index 1:\n   a. current_sum = max(num, current_sum + num)\n   b. max_sum = max(max_sum, current_sum)\n3. Return max_sum'},
                ],
            },
            # ===== STRINGS =====
            {
                'topic': 'Strings',
                'title': 'Valid Anagram',
                'slug': 'valid-anagram',
                'difficulty': 'easy',
                'pattern': 'hash_map',
                'order': 1,
                'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.\n\nAn Anagram is a word formed by rearranging the letters of a different word, using all the original letters exactly once.',
                'examples': 'Input: s = "anagram", t = "nagaram"\nOutput: True\n\nInput: s = "rat", t = "car"\nOutput: False',
                'constraints': '1 <= s.length, t.length <= 5 * 10^4\ns and t consist of lowercase English letters.',
                'starter_code_python': "def is_anagram(s, t):\n    # Your code here\n    pass\n\ns = input()\nt = input()\nprint(is_anagram(s, t))",
                'editorial': 'Count character frequencies using a hash map and compare.\n\nTime: O(n), Space: O(1) since alphabet is fixed.',
                'test_cases': [
                    {'input': 'anagram\nnagaram', 'output': 'True', 'is_sample': True},
                    {'input': 'rat\ncar', 'output': 'False', 'is_sample': True},
                ],
                'hints': [
                    {1: 'What makes two strings anagrams of each other?'},
                    {2: 'Count the frequency of each character in both strings using a Hash Map.'},
                    {3: 'Pseudocode:\n1. If len(s) != len(t) -> return False\n2. Count chars in s, count chars in t\n3. Compare both counts\n4. Return True if equal'},
                ],
            },
            {
                'topic': 'Strings',
                'title': 'Longest Substring Without Repeating Characters',
                'slug': 'longest-substring-without-repeating',
                'difficulty': 'medium',
                'pattern': 'sliding_window',
                'order': 2,
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'examples': 'Input: s = "abcabcbb"\nOutput: 3\nExplanation: The answer is "abc", with the length of 3.\n\nInput: s = "bbbbb"\nOutput: 1',
                'constraints': '0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.',
                'starter_code_python': "def length_of_longest_substring(s):\n    # Your code here\n    pass\n\ns = input()\nprint(length_of_longest_substring(s))",
                'editorial': 'Use sliding window with a set to track characters in current window.\n\nTime: O(n), Space: O(min(m, n)) where m is charset size.',
                'test_cases': [
                    {'input': 'abcabcbb', 'output': '3', 'is_sample': True},
                    {'input': 'bbbbb', 'output': '1', 'is_sample': True},
                    {'input': 'pwwkew', 'output': '3', 'is_sample': False},
                ],
                'hints': [
                    {1: 'Can you use two pointers to define a window?'},
                    {2: 'Sliding Window: expand right pointer, shrink left pointer when duplicate found.'},
                    {3: 'Pseudocode:\n1. left = 0, max_len = 0, char_set = {}\n2. For right in range(len(s)):\n   a. While s[right] in char_set:\n      Remove s[left], left++\n   b. Add s[right] to set\n   c. max_len = max(max_len, right - left + 1)\n3. Return max_len'},
                ],
            },
            # ===== LINKED LISTS =====
            {
                'topic': 'Linked Lists',
                'title': 'Reverse Linked List',
                'slug': 'reverse-linked-list',
                'difficulty': 'easy',
                'pattern': 'linked_list',
                'order': 1,
                'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.\n\nFor this problem, represent the linked list as space-separated values. Output the reversed list.',
                'examples': 'Input: 1 2 3 4 5\nOutput: 5 4 3 2 1\n\nInput: 1 2\nOutput: 2 1',
                'constraints': 'The number of nodes in the list is in the range [0, 5000].\n-5000 <= Node.val <= 5000',
                'starter_code_python': "# Reverse a list (simplified as array for I/O)\ndef reverse_list(nums):\n    # Your code here\n    pass\n\nnums = list(map(int, input().split()))\nresult = reverse_list(nums)\nprint(' '.join(map(str, result)))",
                'editorial': 'Use three pointers: prev, current, next. Iterate through the list reversing pointers.\n\nTime: O(n), Space: O(1)',
                'test_cases': [
                    {'input': '1 2 3 4 5', 'output': '5 4 3 2 1', 'is_sample': True},
                    {'input': '1 2', 'output': '2 1', 'is_sample': True},
                ],
                'hints': [
                    {1: 'Can you reverse the connections one by one?'},
                    {2: 'Use three pointers: previous, current, and next.'},
                    {3: 'Pseudocode:\n1. prev = None, current = head\n2. While current:\n   a. next_node = current.next\n   b. current.next = prev\n   c. prev = current\n   d. current = next_node\n3. Return prev'},
                ],
            },
            {
                'topic': 'Linked Lists',
                'title': 'Detect Cycle in Linked List',
                'slug': 'detect-cycle',
                'difficulty': 'easy',
                'pattern': 'two_pointers',
                'order': 2,
                'description': 'Given an array representing linked list values, determine if the array contains duplicate values (simulating a cycle detection).\n\nReturn True if any value appears more than once, False otherwise.',
                'examples': 'Input: 3 1 0 -4 1\nOutput: True\nExplanation: Value 1 appears twice.\n\nInput: 1 2 3\nOutput: False',
                'constraints': 'The number of nodes is in [0, 10^4].\n-10^5 <= Node.val <= 10^5',
                'starter_code_python': "def has_cycle(nums):\n    # Your code here\n    pass\n\nnums = list(map(int, input().split()))\nprint(has_cycle(nums))",
                'editorial': "Floyd's Tortoise and Hare: use two pointers, slow (1 step) and fast (2 steps). If they meet, cycle exists.\n\nTime: O(n), Space: O(1)",
                'test_cases': [
                    {'input': '3 1 0 -4 1', 'output': 'True', 'is_sample': True},
                    {'input': '1 2 3', 'output': 'False', 'is_sample': True},
                ],
                'hints': [
                    {1: 'Can you use two runners moving at different speeds?'},
                    {2: "Floyd's cycle detection uses a slow and fast pointer (Two Pointers)."},
                    {3: 'Pseudocode:\n1. slow = head, fast = head\n2. While fast and fast.next:\n   a. slow = slow.next\n   b. fast = fast.next.next\n   c. If slow == fast -> return True\n3. Return False'},
                ],
            },
            # ===== TREES =====
            {
                'topic': 'Trees',
                'title': 'Maximum Depth of Binary Tree',
                'slug': 'maximum-depth-binary-tree',
                'difficulty': 'easy',
                'pattern': 'tree_traversal',
                'order': 1,
                'description': 'Given a binary tree represented as a list (level-order), find the maximum depth.\n\nThe maximum depth is the number of nodes along the longest path from the root to the farthest leaf.\n\nUse "null" for empty nodes.',
                'examples': 'Input: 3 9 20 null null 15 7\nOutput: 3\n\nInput: 1 null 2\nOutput: 2',
                'constraints': 'The number of nodes is in [0, 10^4].\n-100 <= Node.val <= 100',
                'starter_code_python': "import math\n\ndef max_depth(tree_list):\n    # Your code here\n    pass\n\nvalues = input().split()\nprint(max_depth(values))",
                'editorial': 'Recursive DFS: depth = 1 + max(depth(left), depth(right)). Base case: empty node returns 0.\n\nTime: O(n), Space: O(h) where h is tree height.',
                'test_cases': [
                    {'input': '3 9 20 null null 15 7', 'output': '3', 'is_sample': True},
                    {'input': '1 null 2', 'output': '2', 'is_sample': True},
                ],
                'hints': [
                    {1: "Think recursively - what's the depth of a leaf node?"},
                    {2: 'Use DFS Tree Traversal. The depth is 1 + max(left_depth, right_depth).'},
                    {3: 'Pseudocode:\n1. If node is None -> return 0\n2. left_depth = maxDepth(node.left)\n3. right_depth = maxDepth(node.right)\n4. Return 1 + max(left_depth, right_depth)'},
                ],
            },
            {
                'topic': 'Trees',
                'title': 'Invert Binary Tree',
                'slug': 'invert-binary-tree',
                'difficulty': 'easy',
                'pattern': 'recursion',
                'order': 2,
                'description': 'Given a binary tree as a level-order list, invert (mirror) it and output the level-order traversal.\n\nUse "null" for empty nodes.',
                'examples': 'Input: 4 2 7 1 3 6 9\nOutput: 4 7 2 9 6 3 1\n\nInput: 2 1 3\nOutput: 2 3 1',
                'constraints': 'The number of nodes is in [0, 100].\n-100 <= Node.val <= 100',
                'starter_code_python': "def invert_tree(values):\n    # Your code here\n    pass\n\nvalues = input().split()\nresult = invert_tree(values)\nprint(' '.join(map(str, result)))",
                'editorial': 'Recursively swap left and right children at every node.\n\nTime: O(n), Space: O(h)',
                'test_cases': [
                    {'input': '4 2 7 1 3 6 9', 'output': '4 7 2 9 6 3 1', 'is_sample': True},
                    {'input': '2 1 3', 'output': '2 3 1', 'is_sample': True},
                ],
                'hints': [
                    {1: 'What happens if you swap left and right at every node?'},
                    {2: 'Use Recursion - swap children then recurse on both subtrees.'},
                    {3: 'Pseudocode:\n1. If node is None -> return None\n2. Swap node.left and node.right\n3. invertTree(node.left)\n4. invertTree(node.right)\n5. Return node'},
                ],
            },
            # ===== GRAPHS =====
            {
                'topic': 'Graphs',
                'title': 'Number of Islands',
                'slug': 'number-of-islands',
                'difficulty': 'medium',
                'pattern': 'bfs',
                'order': 1,
                'description': 'Given a 2D grid of "1"s (land) and "0"s (water), count the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.\n\nInput: First line is rows and cols. Following lines are the grid.',
                'examples': 'Input:\n4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0\nOutput: 1\n\nInput:\n4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1\nOutput: 3',
                'constraints': 'm == grid.length\nn == grid[i].length\n1 <= m, n <= 300\ngrid[i][j] is "0" or "1".',
                'starter_code_python': "def num_islands(grid):\n    # Your code here\n    pass\n\nr, c = map(int, input().split())\ngrid = []\nfor _ in range(r):\n    grid.append(list(map(int, input().split())))\nprint(num_islands(grid))",
                'editorial': 'BFS/DFS from each unvisited land cell. Each BFS/DFS traversal marks one island.\n\nTime: O(m*n), Space: O(m*n)',
                'test_cases': [
                    {'input': '4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0', 'output': '1', 'is_sample': True},
                    {'input': '4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1', 'output': '3', 'is_sample': True},
                ],
                'hints': [
                    {1: 'How would you explore all connected land cells from a starting point?'},
                    {2: 'Use BFS or DFS. Start from each unvisited "1" and mark all connected "1"s as visited.'},
                    {3: 'Pseudocode:\n1. count = 0\n2. For each cell (i, j) in grid:\n   a. If grid[i][j] == 1:\n      count++\n      BFS/DFS from (i, j), marking all connected 1s as 0\n3. Return count'},
                ],
            },
            # ===== DYNAMIC PROGRAMMING =====
            {
                'topic': 'Dynamic Programming',
                'title': 'Climbing Stairs',
                'slug': 'climbing-stairs',
                'difficulty': 'easy',
                'pattern': 'dynamic_programming',
                'order': 1,
                'description': 'You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?',
                'examples': 'Input: 2\nOutput: 2\nExplanation: 1+1 or 2.\n\nInput: 3\nOutput: 3\nExplanation: 1+1+1, 1+2, or 2+1.',
                'constraints': '1 <= n <= 45',
                'starter_code_python': "def climb_stairs(n):\n    # Your code here\n    pass\n\nn = int(input())\nprint(climb_stairs(n))",
                'editorial': 'This is the Fibonacci sequence. dp[i] = dp[i-1] + dp[i-2].\n\nTime: O(n), Space: O(1) with two variables.',
                'test_cases': [
                    {'input': '2', 'output': '2', 'is_sample': True},
                    {'input': '3', 'output': '3', 'is_sample': True},
                    {'input': '5', 'output': '8', 'is_sample': False},
                ],
                'hints': [
                    {1: 'How many ways can you reach step n if you know the answer for n-1 and n-2?'},
                    {2: "This is Dynamic Programming - it's essentially the Fibonacci sequence!"},
                    {3: 'Pseudocode:\n1. If n <= 2 -> return n\n2. a = 1, b = 2\n3. For i from 3 to n:\n   a, b = b, a + b\n4. Return b'},
                ],
            },
            {
                'topic': 'Dynamic Programming',
                'title': 'Coin Change',
                'slug': 'coin-change',
                'difficulty': 'medium',
                'pattern': 'dynamic_programming',
                'order': 2,
                'description': 'Given an array of coin denominations and a total amount, find the fewest number of coins needed to make up that amount.\n\nIf that amount cannot be made up, return -1.\n\nInput: First line is coins, second line is amount.',
                'examples': 'Input:\n1 5 10\n11\nOutput: 2\nExplanation: 10 + 1 = 11\n\nInput:\n2\n3\nOutput: -1',
                'constraints': '1 <= coins.length <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4',
                'starter_code_python': "def coin_change(coins, amount):\n    # Your code here\n    pass\n\ncoins = list(map(int, input().split()))\namount = int(input())\nprint(coin_change(coins, amount))",
                'editorial': 'Bottom-up DP: dp[i] = min coins to make amount i. For each amount, try all coins.\n\nTime: O(amount * coins), Space: O(amount)',
                'test_cases': [
                    {'input': '1 5 10\n11', 'output': '2', 'is_sample': True},
                    {'input': '2\n3', 'output': '-1', 'is_sample': True},
                    {'input': '1 2 5\n11', 'output': '3', 'is_sample': False},
                ],
                'hints': [
                    {1: 'For each amount, what are your choices?'},
                    {2: 'Use Dynamic Programming. Build up the solution from amount 0 to target amount.'},
                    {3: 'Pseudocode:\n1. dp = [infinity] * (amount + 1)\n2. dp[0] = 0\n3. For i from 1 to amount:\n   For each coin:\n      If coin <= i:\n         dp[i] = min(dp[i], dp[i - coin] + 1)\n4. Return dp[amount] if != infinity else -1'},
                ],
            },
            {
                'topic': 'Dynamic Programming',
                'title': 'Longest Increasing Subsequence',
                'slug': 'longest-increasing-subsequence',
                'difficulty': 'medium',
                'pattern': 'dynamic_programming',
                'order': 3,
                'description': 'Given an integer array nums, return the length of the longest strictly increasing subsequence.',
                'examples': 'Input: 10 9 2 5 3 7 101 18\nOutput: 4\nExplanation: [2, 3, 7, 101]\n\nInput: 0 1 0 3 2 3\nOutput: 4',
                'constraints': '1 <= nums.length <= 2500\n-10^4 <= nums[i] <= 10^4',
                'starter_code_python': "def length_of_lis(nums):\n    # Your code here\n    pass\n\nnums = list(map(int, input().split()))\nprint(length_of_lis(nums))",
                'editorial': 'DP: dp[i] = length of LIS ending at index i. For each i, check all j < i.\n\nTime: O(n^2), Space: O(n). Can be optimized to O(n log n) with binary search.',
                'test_cases': [
                    {'input': '10 9 2 5 3 7 101 18', 'output': '4', 'is_sample': True},
                    {'input': '0 1 0 3 2 3', 'output': '4', 'is_sample': True},
                    {'input': '7 7 7 7', 'output': '1', 'is_sample': False},
                ],
                'hints': [
                    {1: 'What if you knew the LIS ending at every previous index?'},
                    {2: 'Use Dynamic Programming. dp[i] = length of LIS ending at index i.'},
                    {3: 'Pseudocode:\n1. dp = [1] * len(nums)\n2. For i from 1 to n:\n   For j from 0 to i:\n      If nums[j] < nums[i]:\n         dp[i] = max(dp[i], dp[j] + 1)\n3. Return max(dp)'},
                ],
            },
            # ===== MORE ARRAYS =====
            {
                'topic': 'Arrays',
                'title': 'Container With Most Water',
                'slug': 'container-with-most-water',
                'difficulty': 'medium',
                'pattern': 'two_pointers',
                'order': 4,
                'description': 'Given n non-negative integers representing vertical lines, find two lines that together with the x-axis form a container that holds the most water.\n\nReturn the maximum amount of water a container can store.',
                'examples': 'Input: 1 8 6 2 5 4 8 3 7\nOutput: 49\n\nInput: 1 1\nOutput: 1',
                'constraints': 'n == height.length\n2 <= n <= 10^5\n0 <= height[i] <= 10^4',
                'starter_code_python': "def max_area(height):\n    # Your code here\n    pass\n\nheight = list(map(int, input().split()))\nprint(max_area(height))",
                'editorial': 'Two Pointers: Start from both ends, move the shorter line inward.\n\nTime: O(n), Space: O(1)',
                'test_cases': [
                    {'input': '1 8 6 2 5 4 8 3 7', 'output': '49', 'is_sample': True},
                    {'input': '1 1', 'output': '1', 'is_sample': True},
                ],
                'hints': [
                    {1: 'What if you start with the widest possible container?'},
                    {2: 'Use Two Pointers starting from both ends. Move the shorter pointer inward.'},
                    {3: 'Pseudocode:\n1. left = 0, right = n-1, max_water = 0\n2. While left < right:\n   a. width = right - left\n   b. h = min(height[left], height[right])\n   c. max_water = max(max_water, width * h)\n   d. Move the shorter pointer inward\n3. Return max_water'},
                ],
            },
            {
                'topic': 'Arrays',
                'title': 'Binary Search',
                'slug': 'binary-search',
                'difficulty': 'easy',
                'pattern': 'binary_search',
                'order': 5,
                'description': 'Given a sorted array of integers nums and a target value, return the index of the target if found, otherwise return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.',
                'examples': 'Input:\n-1 0 3 5 9 12\n9\nOutput: 4\n\nInput:\n-1 0 3 5 9 12\n2\nOutput: -1',
                'constraints': '1 <= nums.length <= 10^4\n-10^4 < nums[i], target < 10^4\nAll integers in nums are unique.\nnums is sorted in ascending order.',
                'starter_code_python': "def binary_search(nums, target):\n    # Your code here\n    pass\n\nnums = list(map(int, input().split()))\ntarget = int(input())\nprint(binary_search(nums, target))",
                'editorial': 'Classic binary search: maintain left and right pointers, check mid element.\n\nTime: O(log n), Space: O(1)',
                'test_cases': [
                    {'input': '-1 0 3 5 9 12\n9', 'output': '4', 'is_sample': True},
                    {'input': '-1 0 3 5 9 12\n2', 'output': '-1', 'is_sample': True},
                ],
                'hints': [
                    {1: 'The array is sorted - how can you eliminate half the elements each step?'},
                    {2: 'Use Binary Search - compare target with mid element.'},
                    {3: 'Pseudocode:\n1. left = 0, right = len(nums) - 1\n2. While left <= right:\n   a. mid = (left + right) // 2\n   b. If nums[mid] == target -> return mid\n   c. If nums[mid] < target -> left = mid + 1\n   d. Else -> right = mid - 1\n3. Return -1'},
                ],
            },
            # ===== GRAPHS =====
            {
                'topic': 'Graphs',
                'title': 'Course Schedule',
                'slug': 'course-schedule',
                'difficulty': 'medium',
                'pattern': 'graph_traversal',
                'order': 2,
                'description': 'There are numCourses courses labeled from 0 to numCourses - 1. You are given pairs [a, b] meaning course b must be taken before course a.\n\nReturn True if you can finish all courses, False if there is a cycle.\n\nInput: First line is numCourses. Second line is number of prerequisites. Following lines are pairs.',
                'examples': 'Input:\n2\n1\n1 0\nOutput: True\n\nInput:\n2\n2\n1 0\n0 1\nOutput: False',
                'constraints': '1 <= numCourses <= 2000\n0 <= prerequisites.length <= 5000',
                'starter_code_python': "def can_finish(num_courses, prerequisites):\n    # Your code here\n    pass\n\nn = int(input())\nm = int(input())\nprereqs = []\nfor _ in range(m):\n    a, b = map(int, input().split())\n    prereqs.append([a, b])\nprint(can_finish(n, prereqs))",
                'editorial': "Topological sort using DFS or BFS (Kahn's algorithm). Detect cycles.\n\nTime: O(V + E), Space: O(V + E)",
                'test_cases': [
                    {'input': '2\n1\n1 0', 'output': 'True', 'is_sample': True},
                    {'input': '2\n2\n1 0\n0 1', 'output': 'False', 'is_sample': True},
                ],
                'hints': [
                    {1: 'Think of this as a graph problem. When is it impossible to finish all courses?'},
                    {2: 'This is cycle detection in a directed graph. Use topological sort or DFS.'},
                    {3: "Pseudocode (Kahn's BFS):\n1. Build adjacency list and in-degree count\n2. Add all nodes with in-degree 0 to queue\n3. While queue not empty:\n   a. Pop node, increment processed count\n   b. For each neighbor, decrement in-degree\n   c. If in-degree becomes 0, add to queue\n4. Return processed == numCourses"},
                ],
            },
        ]

        for pd in problems_data:
            topic = topics[pd['topic']]
            test_cases = pd.pop('test_cases', [])
            hints = pd.pop('hints', [])
            pd.pop('topic')

            problem, created = Problem.objects.update_or_create(
                slug=pd['slug'],
                defaults={**pd, 'topic': topic}
            )

            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status} [{pd["difficulty"].upper()}] {pd["title"]}')

            # Create test cases
            if created:
                for tc in test_cases:
                    TestCase.objects.create(
                        problem=problem,
                        input_data=tc['input'],
                        expected_output=tc['output'],
                        is_sample=tc.get('is_sample', False),
                        explanation=tc.get('explanation', ''),
                    )

                # Create hints
                for hint_group in hints:
                    for level, content in hint_group.items():
                        Hint.objects.create(
                            problem=problem,
                            level=level,
                            content=content,
                        )

        total_problems = Problem.objects.count()
        total_test_cases = TestCase.objects.count()
        total_hints = Hint.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete! '
            f'{total_problems} problems, '
            f'{total_test_cases} test cases, '
            f'{total_hints} hints.'
        ))

