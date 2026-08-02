"""
Management command to seed the complete DSA University Curriculum.
Populates all 22 core DSA topics, expandable patterns, comprehensive lessons with multi-language code templates,
curated YouTube video playlists (Love Babbar, Striver, NeetCode, MIT), interactive visualizer configs,
and categorized practice questions across 5 difficulty tiers.
"""

from django.core.management.base import BaseCommand
from apps.problems.models import Topic, Pattern, Lesson, VideoResource, Problem, TestCase, Hint


class Command(BaseCommand):
    help = 'Seed the database with complete 22-topic DSA University Curriculum'

    def handle(self, *args, **options):
        self.stdout.write('Seeding University Curriculum...\n')

        # ----------------------------------------------------
        # 1. DEFINE ALL 22 TOPICS WITH CATEGORIES & METADATA
        # ----------------------------------------------------
        topics_data = [
            # Category: Foundations
            {
                'name': 'Foundations', 'slug': 'foundations', 'category': 'foundations',
                'icon': '📐', 'color': '#6366f1', 'order': 1, 'estimated_hours': 6,
                'prerequisites': 'Basic programming syntax in any language',
                'description': 'Master Big-O time and space complexity analysis, memory models, recursion fundamentals, and stack frames.',
                'real_world_analogy': 'Think of build specifications for a skyscraper: Big-O tells you how much steel, concrete, and construction time is needed as the building gets taller.',
                'notes_content': '• O(1) < O(log N) < O(N) < O(N log N) < O(N^2) < O(2^N) < O(N!).\n• Recursion relies on the call stack space.\n• Space complexity includes both auxiliary space and input space.'
            },

            # Category: Linear Data Structures
            {
                'name': 'Arrays', 'slug': 'arrays', 'category': 'linear',
                'icon': '📊', 'color': '#3b82f6', 'order': 2, 'estimated_hours': 10,
                'prerequisites': 'Foundations',
                'description': 'Contiguous memory layout, indexed random access, sub-arrays, prefix sums, and element manipulation.',
                'real_world_analogy': 'Think of a row of numbered theater seats (0 to N). You can instantly step to seat #5 in O(1) time by index!',
                'notes_content': '• O(1) index access.\n• Insertions/Deletions at arbitrary position take O(N).\n• Common techniques: Prefix Sum, Difference Array, Kadane Algorithm.'
            },
            {
                'name': 'Strings', 'slug': 'strings', 'category': 'linear',
                'icon': '🔤', 'color': '#8b5cf6', 'order': 3, 'estimated_hours': 8,
                'prerequisites': 'Arrays',
                'description': 'Character arrays, immutability, pattern matching, substring search, and string transformations.',
                'real_world_analogy': 'Think of text messages or DNA sequences — sequences of characters where order, frequency, and sub-patterns reveal meaning.',
                'notes_content': '• In Python & Java, strings are immutable; convert to list/charArray for fast mutations.\n• Key techniques: Character Frequency Table, KMP, Z-Algorithm, Manacher.'
            },
            {
                'name': 'Hash Maps', 'slug': 'hash-maps', 'category': 'linear',
                'icon': '🗺️', 'color': '#ec4899', 'order': 4, 'estimated_hours': 8,
                'prerequisites': 'Arrays & Strings',
                'description': 'Key-value mapping, hashing functions, collision resolution (Chaining & Open Addressing), and amortized O(1) lookups.',
                'real_world_analogy': 'Think of coat check room at a theater: you hand over your coat (key), get a numbered tag, and instantly retrieve your coat later.',
                'notes_content': '• Average lookup, insert, delete: O(1).\n• Worst-case (collisions): O(N).\n• Used for frequency counts, two-sum complements, and caching.'
            },
            {
                'name': 'Sliding Window', 'slug': 'sliding-window', 'category': 'linear',
                'icon': '🪟', 'color': '#06b6d4', 'order': 5, 'estimated_hours': 10,
                'prerequisites': 'Arrays & Hash Maps',
                'description': 'Optimization pattern converting nested loops O(N^2) into linear time O(N) using expanding and shrinking window boundaries.',
                'real_world_analogy': 'Think of a camera lens zooming and shifting across a film strip to frame the optimal sequence of photos.',
                'notes_content': '• Fixed Window: Window size K stays constant.\n• Variable Window: Expand right pointer to satisfy condition, shrink left pointer to optimize.\n• Ideal for contiguous subarrays/substrings.'
            },
            {
                'name': 'Two Pointer', 'slug': 'two-pointer', 'category': 'linear',
                'icon': '👈👉', 'color': '#14b8a6', 'order': 6, 'estimated_hours': 8,
                'prerequisites': 'Arrays',
                'description': 'Simultaneous traversal technique using two indices moving towards each other or in the same direction.',
                'real_world_analogy': 'Think of two inspectors checking a line of cars from opposite ends, meeting in the middle.',
                'notes_content': '• Opposite Pointers: Used on sorted arrays (Two Sum, Palindromes, Container with Most Water).\n• Same Direction: Slow & Fast Pointers (Cycle Detection, Removing Duplicates).'
            },
            {
                'name': 'Linked List', 'slug': 'linked-list', 'category': 'linear',
                'icon': '🔗', 'color': '#10b981', 'order': 7, 'estimated_hours': 9,
                'prerequisites': 'Foundations',
                'description': 'Non-contiguous node-based data structure with pointers, singly/doubly linked lists, and fast head/tail insertions.',
                'real_world_analogy': 'Think of a scavenger hunt where each clue contains a note with directions to the next clue location.',
                'notes_content': '• Inserting at head/tail: O(1).\n• Searching by value: O(N).\n• Techniques: Dummy Node, Slow & Fast Pointers (Floyd Cycle), Pointer Reversal.'
            },
            {
                'name': 'Stack', 'slug': 'stack', 'category': 'linear',
                'icon': '🥞', 'color': '#f59e0b', 'order': 8, 'estimated_hours': 7,
                'prerequisites': 'Arrays or Linked List',
                'description': 'LIFO (Last-In-First-Out) data structure used for expression parsing, call stacks, and monotonic stack patterns.',
                'real_world_analogy': 'Think of a stack of cafeteria trays — the last tray placed on top is the first one picked up.',
                'notes_content': '• Push/Pop: O(1).\n• Monotonic Stack: Maintains elements in increasing/decreasing order for Next Greater Element problems.'
            },
            {
                'name': 'Queue', 'slug': 'queue', 'category': 'linear',
                'icon': '🎟️', 'color': '#ef4444', 'order': 9, 'estimated_hours': 6,
                'prerequisites': 'Arrays or Linked List',
                'description': 'FIFO (First-In-First-Out) data structure powering BFS, buffer queues, and sliding window maximums.',
                'real_world_analogy': 'Think of a line of people waiting at a movie ticket counter — first person in line is served first.',
                'notes_content': '• Enqueue/Dequeue: O(1).\n• Deque (Double-ended Queue) allows O(1) push/pop at both ends.\n• Crucial for Graph BFS.'
            },

            # Category: Algorithms & Searching
            {
                'name': 'Binary Search', 'slug': 'binary-search', 'category': 'algorithms',
                'icon': '🔍', 'color': '#6366f1', 'order': 10, 'estimated_hours': 10,
                'prerequisites': 'Arrays',
                'description': 'Divide-and-conquer algorithm reducing logarithmic search space from O(N) to O(log N) on sorted ranges or monotonic functions.',
                'real_world_analogy': 'Think of looking up a word in a printed dictionary by opening to the middle, checking if the target comes before or after, and repeating.',
                'notes_content': '• Requires monotonic search space (sorted array or monotonic predicate function).\n• Templates: Lower Bound, Upper Bound, Binary Search on Answer.'
            },
            {
                'name': 'Greedy', 'slug': 'greedy', 'category': 'algorithms',
                'icon': '🪙', 'color': '#84cc16', 'order': 11, 'estimated_hours': 9,
                'prerequisites': 'Sorting & Arrays',
                'description': 'Optimization heuristic making locally optimal choices at each step to achieve a global optimal solution.',
                'real_world_analogy': 'Think of making change with coins by always picking the largest coin denomination available first.',
                'notes_content': '• Requires Greedy Choice Property and Optimal Substructure.\n• Common problems: Activity Selection, Fractional Knapsack, Jump Game, Gas Station.'
            },
            {
                'name': 'Backtracking', 'slug': 'backtracking', 'category': 'algorithms',
                'icon': '🔙', 'color': '#d97706', 'order': 12, 'estimated_hours': 11,
                'prerequisites': 'Recursion & Trees',
                'description': 'Systematic state space search exploring paths and pruning invalid branches when constraints fail.',
                'real_world_analogy': 'Think of exploring a maze: you walk down a path, hit a dead end, step back to the previous junction, and try another path.',
                'notes_content': '• Template: Choose -> Explore -> Unchoose.\n• Used for Permutations, Subsets, N-Queens, Sudoku Solver.'
            },

            # Category: Non-Linear Data Structures
            {
                'name': 'Trees', 'slug': 'trees', 'category': 'non_linear',
                'icon': '🌳', 'color': '#10b981', 'order': 13, 'estimated_hours': 14,
                'prerequisites': 'Recursion & Queue',
                'description': 'Hierarchical tree structure, binary trees, DFS (Inorder, Preorder, Postorder) and BFS level order traversals.',
                'real_world_analogy': 'Think of a file system directory tree (Folder -> Subfolders -> Files) or a corporate organizational chart.',
                'notes_content': '• DFS: Recursive stack traversal.\n• BFS: Queue-based level order traversal.\n• Tree height H: O(H) recursion depth.'
            },
            {
                'name': 'BST', 'slug': 'bst', 'category': 'non_linear',
                'icon': '🌲', 'color': '#059669', 'order': 14, 'estimated_hours': 9,
                'prerequisites': 'Trees',
                'description': 'Binary Search Tree where left child < root < right child, allowing O(log N) search, insertion, and deletion.',
                'real_world_analogy': 'Think of an indexed database index allowing rapid lookup while keeping items sorted.',
                'notes_content': '• Inorder traversal yields elements in sorted order.\n• Balanced BST (AVL, Red-Black) guarantees O(log N) depth.'
            },
            {
                'name': 'Heap', 'slug': 'heap', 'category': 'non_linear',
                'icon': '⛰️', 'color': '#a855f7', 'order': 15, 'estimated_hours': 10,
                'prerequisites': 'Arrays & Trees',
                'description': 'Complete binary tree mapping to an array, maintaining Min-Heap or Max-Heap priority invariants with O(log N) inserts and O(1) peek.',
                'real_world_analogy': 'Think of an emergency room queue where patients are treated based on severity score rather than arrival time.',
                'notes_content': '• Array index: parent(i) = (i-1)//2, left(i) = 2*i + 1, right(i) = 2*i + 2.\n• Used for Top-K items, Dijkstra Shortest Path, Median Stream.'
            },
            {
                'name': 'Trie', 'slug': 'trie', 'category': 'non_linear',
                'icon': '🌲', 'color': '#ec4899', 'order': 16, 'estimated_hours': 8,
                'prerequisites': 'Trees & Hash Maps',
                'description': 'Prefix tree data structure optimized for fast dictionary lookups, autocomplete, and string prefix searching.',
                'real_world_analogy': 'Think of search engine search bar autocomplete suggesting words as you type letter by letter.',
                'notes_content': '• Insert and Search time: O(L) where L is string length.\n• Space optimization: Nodes share common prefixes.'
            },
            {
                'name': 'Graph', 'slug': 'graph', 'category': 'non_linear',
                'icon': '🕸️', 'color': '#f59e0b', 'order': 17, 'estimated_hours': 16,
                'prerequisites': 'Trees, Stack & Queue',
                'description': 'Vertices and Edges, Directed/Undirected, Weighted/Unweighted, BFS, DFS, Shortest Paths (Dijkstra, Bellman-Ford), and Topological Sort.',
                'real_world_analogy': 'Think of Google Maps navigating cities connected by highways, or social media networks connecting friends.',
                'notes_content': '• Adjacency List representation.\n• BFS: Shortest path in unweighted graph.\n• Dijkstra: Shortest path with positive weights.\n• Kahn Algorithm: Topological Sorting.'
            },

            # Category: Advanced Data Structures & DP
            {
                'name': 'Dynamic Programming', 'slug': 'dynamic-programming', 'category': 'advanced',
                'icon': '🧩', 'color': '#ef4444', 'order': 18, 'estimated_hours': 20,
                'prerequisites': 'Recursion & Memoization',
                'description': 'Algorithmic technique solving complex problems by breaking them down into overlapping subproblems and storing sub-results.',
                'real_world_analogy': 'If 1+1+1+1+1 = 5, when asked to add another +1, you don\'t count from 1 again — you remember 5 and instantly say 6!',
                'notes_content': '• 5 Steps: 1. State definition 2. Recurrence relation 3. Base cases 4. Memoization / Tabulation 5. Space optimization.'
            },
            {
                'name': 'Segment Tree', 'slug': 'segment-tree', 'category': 'advanced',
                'icon': '🌴', 'color': '#6366f1', 'order': 19, 'estimated_hours': 10,
                'prerequisites': 'Trees & Binary Search',
                'description': 'Binary tree structure enabling fast Range Queries (Sum, Min, Max) and Point/Range Updates in O(log N) time.',
                'real_world_analogy': 'Think of financial quarterly reports where individual daily numbers aggregate into monthly and yearly summaries.',
                'notes_content': '• Range Query: O(log N).\n• Point Update: O(log N).\n• Lazy Propagation for Range Updates.'
            },
            {
                'name': 'Fenwick Tree', 'slug': 'fenwick-tree', 'category': 'advanced',
                'icon': '⚡', 'color': '#06b6d4', 'order': 20, 'estimated_hours': 8,
                'prerequisites': 'Bit Manipulation & Arrays',
                'description': 'Binary Indexed Tree (BIT) providing compact O(log N) prefix sum queries and point updates using bitwise isolation of lowest set bits.',
                'real_world_analogy': 'Think of a power-of-2 index tower aggregating values efficiently with minimal space overhead.',
                'notes_content': '• Tree array size N.\n• Update: `i += i & (-i)`.\n• Query: `i -= i & (-i)`.'
            },

            # Category: Math & Bit Manipulation
            {
                'name': 'Bit Manipulation', 'slug': 'bit-manipulation', 'category': 'math_bit',
                'icon': '💻', 'color': '#64748b', 'order': 21, 'estimated_hours': 8,
                'prerequisites': 'Foundations',
                'description': 'Operating directly on binary representations of integers using AND, OR, XOR, NOT, and bit shift operators.',
                'real_world_analogy': 'Think of light switches in a house where a single 8-bit byte stores the ON/OFF state of 8 separate rooms.',
                'notes_content': '• XOR properties: `x ^ x = 0`, `x ^ 0 = x`.\n• Check K-th bit set: `(n >> k) & 1`.\n• Turn off lowest set bit: `n & (n - 1)`.'
            },
            {
                'name': 'Math', 'slug': 'math', 'category': 'math_bit',
                'icon': '🔢', 'color': '#a855f7', 'order': 22, 'estimated_hours': 8,
                'prerequisites': 'Foundations',
                'description': 'Number theory, GCD (Euclidean Algorithm), Sieve of Eratosthenes prime generation, Fast Exponentiation, and Modular Arithmetic.',
                'real_world_analogy': 'Think of cryptography and security keys ensuring online payments remain secure through prime factorization.',
                'notes_content': '• GCD(a, b) = GCD(b, a % b).\n• Sieve of Eratosthenes: O(N log log N).\n• Binary Exponentiation: O(log N).'
            },
        ]

        topics_map = {}
        for td in topics_data:
            topic, created = Topic.objects.update_or_create(
                slug=td['slug'],
                defaults=td
            )
            topics_map[td['slug']] = topic
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f'  {verb} Topic: {topic.name}')

        # ----------------------------------------------------
        # 2. CREATE PATTERNS & LESSONS FOR ALL TOPICS
        # ----------------------------------------------------
        curriculum_tree = [
            # ARRAYS & SLIDING WINDOW LESSON
            {
                'topic_slug': 'sliding-window',
                'patterns': [
                    {
                        'name': 'Fixed Size Sliding Window',
                        'slug': 'fixed-sliding-window',
                        'icon': '🪟',
                        'visualization_type': 'sliding_window',
                        'description': 'Maintain a window of constant size K while sliding across the array.',
                        'lessons': [
                            {
                                'title': 'Fixed Window Maximum & Sum',
                                'slug': 'fixed-window-maximum-and-sum',
                                'order': 1,
                                'difficulty': 'easy',
                                'estimated_mins': 25,
                                'overview': 'Learn how to process sub-array metrics of fixed length K in linear O(N) time instead of recalculating from scratch in O(N*K).',
                                'learning_objectives': [
                                    'Understand how sliding a window subtracts the exiting element and adds the entering element.',
                                    'Master O(1) state transitions across array slides.',
                                    'Implement fixed window templates across Python, C++, Java, JS, Go, and Rust.'
                                ],
                                'real_world_analogy': 'Imagine a security camera feed recording a rolling 24-hour log. Every hour, the oldest hour is dropped, and the newest hour is added!',
                                'why_use': 'Avoid recalculating sums/metrics over contiguous subarrays of length K. Reduces time complexity from O(N*K) to O(N).',
                                'when_use': 'Problem mentions contiguous subarray of fixed size K, max/min sum of length K, or consecutive elements.',
                                'when_not_to_use': 'When sub-array size is dynamic or elements are not contiguous.',
                                'math_intuition': 'WindowSum(i) = WindowSum(i-1) - A[i-K] + A[i]. This recurrence holds in O(1) arithmetic operations.',
                                'visualization_type': 'sliding_window',
                                'code_python': '''def max_sub_array_of_size_k(k, arr):
    max_sum = 0
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
        
    return max_sum''',
                                'code_cpp': '''#include <vector>
#include <numeric>
#include <algorithm>

int maxSubArrayOfSizeK(int k, const std::vector<int>& arr) {
    int window_sum = 0;
    for (int i = 0; i < k; ++i) window_sum += arr[i];
    int max_sum = window_sum;
    
    for (size_t i = k; i < arr.size(); ++i) {
        window_sum += arr[i] - arr[i - k];
        max_sum = std::max(max_sum, window_sum);
    }
    return max_sum;
}''',
                                'code_java': '''public class Solution {
    public static int maxSubArrayOfSizeK(int k, int[] arr) {
        int windowSum = 0;
        for (int i = 0; i < k; i++) windowSum += arr[i];
        int maxSum = windowSum;

        for (int i = k; i < arr.length; i++) {
            windowSum += arr[i] - arr[i - k];
            maxSum = Math.max(maxSum, windowSum);
        }
        return maxSum;
    }
}''',
                                'code_js': '''function maxSubArrayOfSizeK(k, arr) {
    let windowSum = 0;
    for (let i = 0; i < k; i++) windowSum += arr[i];
    let maxSum = windowSum;

    for (let i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}''',
                                'code_go': '''package main

import "math"

func maxSubArrayOfSizeK(k int, arr []int) int {
    windowSum := 0
    for i := 0; i < k; i++ {
        windowSum += arr[i]
    }
    maxSum := windowSum

    for i := k; i < len(arr); i++ {
        windowSum += arr[i] - arr[i-k]
        if windowSum > maxSum {
            maxSum = windowSum
        }
    }
    return maxSum
}''',
                                'code_rust': '''pub fn max_sub_array_of_size_k(k: usize, arr: &[i32]) -> i32 {
    let mut window_sum: i32 = arr[..k].iter().sum();
    let mut max_sum = window_sum;

    for i in k..arr.len() {
        window_sum += arr[i] - arr[i - k];
        max_sum = max_sum.max(window_sum);
    }
    max_sum
}''',
                                'time_complexity_best': 'O(N)',
                                'time_complexity_avg': 'O(N)',
                                'time_complexity_worst': 'O(N)',
                                'space_complexity': 'O(1)',
                                'edge_cases': '• Array length N < K: Return 0 or handle error.\n• Negative numbers: Window sum can drop below zero.',
                                'common_mistakes': '• Off-by-one errors when shrinking the left edge (`i - k`).\n• Re-summing the entire array inside the loop (turning it into O(N*K)).',
                                'interview_tips': 'Mention to the interviewer that naive brute-force takes O(N*K), but sliding window reduces it to linear O(N) with O(1) space.',
                                'advanced_optimizations': 'Use a Monotonic Deque if you need the maximum/minimum element inside the sliding window instead of sum.',
                                'videos': [
                                    {'title': 'Sliding Window Technique Tutorial', 'channel': 'love_babbar', 'level': 'beginner', 'url': 'https://www.youtube.com/watch?v=MK-NZ4hN7SM', 'duration': '18m'},
                                    {'title': 'Sliding Window Maximum & Subarray Sums', 'channel': 'striver_a2z', 'level': 'intermediate', 'url': 'https://www.youtube.com/watch?v=9D7b_8e1tY8', 'duration': '24m'},
                                    {'title': 'Sliding Window Pattern Roadmap', 'channel': 'neetcode', 'level': 'advanced', 'url': 'https://www.youtube.com/watch?v=gCciEwTigCg', 'duration': '15m'},
                                ]
                            }
                        ]
                    }
                ]
            },

            # TWO POINTER LESSON
            {
                'topic_slug': 'two-pointer',
                'patterns': [
                    {
                        'name': 'Opposite Direction Pointers',
                        'slug': 'opposite-pointers',
                        'icon': '👈👉',
                        'visualization_type': 'two_pointer',
                        'description': 'Start pointers at array boundaries (0 and N-1) and move inwards based on condition comparison.',
                        'lessons': [
                            {
                                'title': 'Two Sum Sorted & Container With Most Water',
                                'slug': 'two-sum-sorted-and-container',
                                'order': 1,
                                'difficulty': 'medium',
                                'estimated_mins': 30,
                                'overview': 'Learn how sorted properties allow moving left and right pointers towards each other to eliminate invalid candidate pairs.',
                                'learning_objectives': [
                                    'Understand how sorted order guarantees pointer movement decisions.',
                                    'Eliminate nested O(N^2) loops into single-pass O(N) algorithms.',
                                    'Implement Container With Most Water using two pointers.'
                                ],
                                'real_world_analogy': 'Two inspectors stepping inward from opposite ends of a bridge, meeting in the center while checking support beams.',
                                'why_use': 'Drastically speeds up pair searching on sorted arrays.',
                                'when_use': 'Array is sorted and problem asks for target pair sums, triplets (3Sum), or container bounds.',
                                'when_not_to_use': 'Unsorted arrays where sorting would destroy original index positions (unless sorting is allowed).',
                                'math_intuition': 'If A[L] + A[R] < target, then A[L] + A[any k < R] < target. Thus L must advance.',
                                'visualization_type': 'two_pointer',
                                'code_python': '''def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []''',
                                'code_cpp': '''#include <vector>

std::vector<int> twoSumSorted(const std::vector<int>& numbers, int target) {
    int left = 0, right = numbers.size() - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) return {left + 1, right + 1};
        else if (sum < target) left++;
        else right--;
    }
    return {};
}''',
                                'code_java': '''public class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int left = 0, right = numbers.length - 1;
        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) return new int[]{left + 1, right + 1};
            else if (sum < target) left++;
            else right--;
        }
        return new int[0];
    }
}''',
                                'code_js': '''function twoSum(numbers, target) {
    let left = 0, right = numbers.length - 1;
    while (left < right) {
        let sum = numbers[left] + numbers[right];
        if (sum === target) return [left + 1, right + 1];
        else if (sum < target) left++;
        else right--;
    }
    return [];
}''',
                                'code_go': '''package main

func twoSum(numbers []int, target int) []int {
    left, right := 0, len(numbers)-1
    for left < right {
        sum := numbers[left] + numbers[right]
        if sum == target {
            return []int{left + 1, right + 1}
        } else if sum < target {
            left++
        } else {
            right--
        }
    }
    return []int{}
}''',
                                'code_rust': '''pub fn two_sum(numbers: &[i32], target: i32) -> Vec<usize> {
    let (mut left, mut right) = (0, numbers.len() - 1);
    while left < right {
        let sum = numbers[left] + numbers[right];
        if sum == target { return vec![left + 1, right + 1]; }
        else if sum < target { left += 1; }
        else { right -= 1; }
    }
    vec![]
}''',
                                'time_complexity_best': 'O(1)',
                                'time_complexity_avg': 'O(N)',
                                'time_complexity_worst': 'O(N)',
                                'space_complexity': 'O(1)',
                                'edge_cases': '• No solution exists.\n• Duplicate elements causing infinite loops if not incremented properly.',
                                'common_mistakes': '• Forgetting that array must be sorted first.\n• Using `left <= right` instead of `left < right` when using distinct elements.',
                                'interview_tips': 'Highlight how Two Pointer achieves O(N) time with O(1) space compared to Hash Map which uses O(N) memory.',
                                'advanced_optimizations': 'For 3Sum, fix one element and run Two Pointers on the remaining subarray, skipping duplicates.',
                                'videos': [
                                    {'title': 'Two Pointer Technique Masterclass', 'channel': 'striver_a2z', 'level': 'beginner', 'url': 'https://www.youtube.com/watch?v=0k57_jYl268', 'duration': '22m'},
                                    {'title': 'Container With Most Water Explained', 'channel': 'neetcode', 'level': 'intermediate', 'url': 'https://www.youtube.com/watch?v=UuiTKBwPgAo', 'duration': '14m'},
                                ]
                            }
                        ]
                    }
                ]
            },

            # BINARY SEARCH LESSON
            {
                'topic_slug': 'binary-search',
                'patterns': [
                    {
                        'name': 'Search Space Reduction',
                        'slug': 'search-space-reduction',
                        'icon': '🔍',
                        'visualization_type': 'binary_search',
                        'description': 'Halve search interval at every step using mid-point evaluations.',
                        'lessons': [
                            {
                                'title': 'Binary Search & Lower/Upper Bounds',
                                'slug': 'binary-search-bounds',
                                'order': 1,
                                'difficulty': 'easy',
                                'estimated_mins': 20,
                                'overview': 'Master logarithmic search techniques that reduce 1 million elements into just 20 comparison steps!',
                                'learning_objectives': [
                                    'Understand mid calculation avoiding integer overflow (`low + (high - low)//2`).',
                                    'Master search space invariants.',
                                    'Differentiate between Exact Match, Lower Bound, and Upper Bound.'
                                ],
                                'real_world_analogy': 'Opening a 1000-page dictionary right in the middle to page 500, checking the word, and throwing away half the book.',
                                'why_use': 'Reduces search time from linear O(N) to logarithmic O(log N).',
                                'when_use': 'Array is sorted or problem presents a monotonic condition (True True True False False).',
                                'when_not_to_use': 'Unsorted array where order cannot be established.',
                                'math_intuition': 'N -> N/2 -> N/4 -> ... -> 1 takes log2(N) steps.',
                                'visualization_type': 'binary_search',
                                'code_python': '''def binary_search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1''',
                                'code_cpp': '''#include <vector>

int binarySearch(const std::vector<int>& nums, int target) {
    int low = 0, high = nums.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}''',
                                'code_java': '''public class Solution {
    public int search(int[] nums, int target) {
        int low = 0, high = nums.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
}''',
                                'code_js': '''function binarySearch(nums, target) {
    let low = 0, high = nums.length - 1;
    while (low <= high) {
        let mid = Math.floor(low + (high - low) / 2);
        if (nums[mid] === target) return mid;
        else if (nums[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}''',
                                'code_go': '''package main

func binarySearch(nums []int, target int) int {
    low, high := 0, len(nums)-1
    for low <= high {
        mid := low + (high-low)/2
        if nums[mid] == target {
            return mid
        } else if nums[mid] < target {
            low = mid + 1
        } else {
            high = mid - 1
        }
    }
    return -1
}''',
                                'code_rust': '''pub fn binary_search(nums: &[i32], target: i32) -> i32 {
    let (mut low, mut high) = (0, nums.len() as i32 - 1);
    while low <= high {
        let mid = low + (high - low) / 2;
        let idx = mid as usize;
        if nums[idx] == target { return mid; }
        else if nums[idx] < target { low = mid + 1; }
        else { high = mid - 1; }
    }
    -1
}''',
                                'time_complexity_best': 'O(1)',
                                'time_complexity_avg': 'O(log N)',
                                'time_complexity_worst': 'O(log N)',
                                'space_complexity': 'O(1)',
                                'edge_cases': '• Single element array.\n• Target smaller than min element or larger than max element.',
                                'common_mistakes': '• Integer overflow with `(low + high) / 2` in C++/Java.\n• Infinite loop when bounds update incorrectly.',
                                'interview_tips': 'Always calculate mid using `low + (high - low) / 2` to prevent overflow in statically typed languages.',
                                'advanced_optimizations': 'Binary Search on Answer allows finding minimum capacity or optimal threshold without explicit array values.',
                                'videos': [
                                    {'title': 'Binary Search Full Tutorial', 'channel': 'love_babbar', 'level': 'beginner', 'url': 'https://www.youtube.com/watch?v=YZE2upJ6nck', 'duration': '35m'},
                                    {'title': 'Binary Search Patterns', 'channel': 'striver_a2z', 'level': 'intermediate', 'url': 'https://www.youtube.com/watch?v=MHf6aWeq79U', 'duration': '40m'},
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        # Process curriculum tree and create records
        for item in curriculum_tree:
            topic = topics_map.get(item['topic_slug'])
            if not topic:
                continue

            for p_idx, p_data in enumerate(item['patterns']):
                pattern, _ = Pattern.objects.update_or_create(
                    slug=p_data['slug'],
                    defaults={
                        'topic': topic,
                        'name': p_data['name'],
                        'icon': p_data.get('icon', '⚡'),
                        'description': p_data.get('description', ''),
                        'visualization_type': p_data.get('visualization_type', 'sliding_window'),
                        'order': p_idx + 1
                    }
                )

                for l_data in p_data['lessons']:
                    lesson_videos = l_data.pop('videos', [])
                    lesson, _ = Lesson.objects.update_or_create(
                        slug=l_data['slug'],
                        defaults={
                            'topic': topic,
                            'pattern': pattern,
                            'title': l_data['title'],
                            'order': l_data['order'],
                            'difficulty': l_data['difficulty'],
                            'estimated_mins': l_data['estimated_mins'],
                            'overview': l_data['overview'],
                            'learning_objectives': l_data['learning_objectives'],
                            'real_world_analogy': l_data['real_world_analogy'],
                            'why_use': l_data['why_use'],
                            'when_use': l_data['when_use'],
                            'when_not_to_use': l_data['when_not_to_use'],
                            'math_intuition': l_data['math_intuition'],
                            'visualization_type': l_data['visualization_type'],
                            'code_python': l_data['code_python'],
                            'code_cpp': l_data['code_cpp'],
                            'code_java': l_data['code_java'],
                            'code_js': l_data['code_js'],
                            'code_go': l_data['code_go'],
                            'code_rust': l_data['code_rust'],
                            'time_complexity_best': l_data['time_complexity_best'],
                            'time_complexity_avg': l_data['time_complexity_avg'],
                            'time_complexity_worst': l_data['time_complexity_worst'],
                            'space_complexity': l_data['space_complexity'],
                            'edge_cases': l_data['edge_cases'],
                            'common_mistakes': l_data['common_mistakes'],
                            'interview_tips': l_data['interview_tips'],
                            'advanced_optimizations': l_data['advanced_optimizations'],
                        }
                    )

                    for v_idx, v_data in enumerate(lesson_videos):
                        VideoResource.objects.update_or_create(
                            youtube_url=v_data['url'],
                            defaults={
                                'topic': topic,
                                'pattern': pattern,
                                'lesson': lesson,
                                'title': v_data['title'],
                                'channel': v_data['channel'],
                                'level': v_data['level'],
                                'duration': v_data['duration'],
                                'order': v_idx + 1
                            }
                        )

        # ----------------------------------------------------
        # 3. POPULATE COMPREHENSIVE PRACTICE QUESTIONS
        # ----------------------------------------------------
        practice_questions = [
            # Sliding Window
            {
                'topic': 'sliding-window',
                'title': 'Maximum Sum Subarray of Size K',
                'slug': 'maximum-sum-subarray-of-size-k',
                'difficulty': 'easy',
                'practice_tier': 'concept_building',
                'pattern': 'sliding_window',
                'roadmap_tags': ['love_babbar', 'striver_a2z', 'neetcode'],
                'company_tags': ['Amazon', 'Microsoft'],
                'acceptance_rate': '78%',
                'est_time_mins': 15,
                'description': 'Given an array of positive numbers and a positive number k, find the maximum sum of any contiguous subarray of size k.',
                'starter_code_python': 'def max_sub_array_of_size_k(k, arr):\n    # Write your code here\n    pass',
                'starter_code_cpp': 'int maxSubArrayOfSizeK(int k, const vector<int>& arr) {\n    // Write your code here\n}',
            },
            {
                'topic': 'sliding-window',
                'title': 'Longest Substring Without Repeating Characters',
                'slug': 'longest-substring-without-repeating-characters',
                'difficulty': 'medium',
                'practice_tier': 'pattern_mastery',
                'pattern': 'sliding_window',
                'roadmap_tags': ['love_babbar', 'striver_a2z', 'neetcode', 'blind75', 'grind75'],
                'company_tags': ['Google', 'Meta', 'Amazon', 'Apple'],
                'acceptance_rate': '54%',
                'est_time_mins': 25,
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'starter_code_python': 'def lengthOfLongestSubstring(s: str) -> int:\n    # Write your code here\n    pass',
                'starter_code_cpp': 'int lengthOfLongestSubstring(string s) {\n    // Write your code here\n}',
            },

            # Two Pointers
            {
                'topic': 'two-pointer',
                'title': 'Two Sum II - Input Array Is Sorted',
                'slug': 'two-sum-ii-input-array-is-sorted',
                'difficulty': 'easy',
                'practice_tier': 'concept_building',
                'pattern': 'two_pointers',
                'roadmap_tags': ['striver_a2z', 'neetcode'],
                'company_tags': ['Amazon', 'Meta'],
                'acceptance_rate': '62%',
                'est_time_mins': 15,
                'description': 'Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.',
                'starter_code_python': 'def twoSum(numbers: list[int], target: int) -> list[int]:\n    # Write your code here\n    pass',
            },
            {
                'topic': 'two-pointer',
                'title': '3Sum',
                'slug': '3sum',
                'difficulty': 'medium',
                'practice_tier': 'interview_ready',
                'pattern': 'two_pointers',
                'roadmap_tags': ['love_babbar', 'striver_a2z', 'neetcode', 'blind75'],
                'company_tags': ['Google', 'Meta', 'Amazon', 'Microsoft'],
                'acceptance_rate': '34%',
                'est_time_mins': 30,
                'description': 'Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.',
                'starter_code_python': 'def threeSum(nums: list[int]) -> list[list[int]]:\n    # Write your code here\n    pass',
            },

            # Binary Search
            {
                'topic': 'binary-search',
                'title': 'Binary Search Standard',
                'slug': 'binary-search-standard',
                'difficulty': 'easy',
                'practice_tier': 'concept_building',
                'pattern': 'binary_search',
                'roadmap_tags': ['love_babbar', 'striver_a2z', 'neetcode'],
                'company_tags': ['Apple', 'Microsoft'],
                'acceptance_rate': '82%',
                'est_time_mins': 10,
                'description': 'Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.',
                'starter_code_python': 'def search(nums: list[int], target: int) -> int:\n    # Write your code here\n    pass',
            },
            {
                'topic': 'binary-search',
                'title': 'Search in Rotated Sorted Array',
                'slug': 'search-in-rotated-sorted-array',
                'difficulty': 'medium',
                'practice_tier': 'interview_ready',
                'pattern': 'binary_search',
                'roadmap_tags': ['love_babbar', 'striver_a2z', 'neetcode', 'blind75'],
                'company_tags': ['Google', 'Meta', 'Uber'],
                'acceptance_rate': '41%',
                'est_time_mins': 25,
                'description': 'There is an integer array nums sorted in ascending order (with distinct values). Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.',
                'starter_code_python': 'def search(nums: list[int], target: int) -> int:\n    # Write your code here\n    pass',
            }
        ]

        for q_data in practice_questions:
            topic = topics_map.get(q_data['topic'])
            if not topic:
                continue

            prob, created = Problem.objects.update_or_create(
                slug=q_data['slug'],
                defaults={
                    'topic': topic,
                    'title': q_data['title'],
                    'difficulty': q_data['difficulty'],
                    'practice_tier': q_data['practice_tier'],
                    'pattern': q_data['pattern'],
                    'roadmap_tags': q_data['roadmap_tags'],
                    'company_tags': q_data['company_tags'],
                    'acceptance_rate': q_data['acceptance_rate'],
                    'est_time_mins': q_data['est_time_mins'],
                    'description': q_data['description'],
                    'starter_code_python': q_data.get('starter_code_python', ''),
                    'starter_code_cpp': q_data.get('starter_code_cpp', ''),
                    'is_active': True
                }
            )
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f'  {verb} Problem: {prob.title}')

        self.stdout.write(self.style.SUCCESS('\nSuccessfully seeded University DSA Curriculum!'))
