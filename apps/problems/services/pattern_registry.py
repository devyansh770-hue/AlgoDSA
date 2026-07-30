import json
from apps.problems.models import Topic, Pattern

def init_patterns():
    # Only run if topics exist
    arrays_topic = Topic.objects.filter(slug='arrays').first()
    if not arrays_topic:
        return

    # Array Patterns Data
    array_patterns = [
        {
            "name": "Sliding Window",
            "slug": "sliding-window",
            "icon": "🖼️",
            "description": "Used to process sequential elements in arrays or strings. Instead of recomputing results for every subset, we slide a window over the data.",
            "order": 1,
            "content_json": {
                "introduction": "The Sliding Window pattern is used to perform operations on a specific window size of a given array or string. A 'window' is formed over some part of data, and this window can slide over the data to capture different portions.",
                "real_life_analogy": "Imagine you are in a moving train looking out of a window. As the train moves, the window stays the same size, but the scenery you see changes. The scenery entering on the right is added to your view, and the scenery leaving on the left is removed.",
                "visualization": {
                    "type": "array",
                    "data": [1, 3, -1, -3, 5, 3, 6, 7],
                    "steps": [
                        {"pointers": {"L": 0, "R": 2}, "highlight": [0,1,2], "desc": "Initial window of size 3."},
                        {"pointers": {"L": 1, "R": 3}, "highlight": [1,2,3], "desc": "Window slides to the right by 1."}
                    ]
                },
                "when_to_use": [
                    "The problem input is a linear data structure like an Array, String, or Linked List.",
                    "You're asked to find the longest/shortest substring, subarray, or a desired value.",
                    "The problem involves a contiguous sequence of elements."
                ],
                "when_not_to_use": [
                    "When the problem asks for non-contiguous subsequences (e.g., Longest Increasing Subsequence).",
                    "When dealing with trees, graphs, or completely unsorted data where order doesn't dictate the answer."
                ],
                "core_idea": "Avoid redundant work. Instead of recalculating the sum (or product, etc.) of a subarray from scratch for every possible subarray, we reuse the calculation from the previous subarray by subtracting the element that left the window and adding the element that entered the window.",
                "algorithm": [
                    "Initialize two pointers, left and right, to represent the window boundaries.",
                    "Expand the window by moving the right pointer and updating the window state.",
                    "If the window condition is violated, shrink the window by moving the left pointer until the condition is satisfied again.",
                    "Update the global answer (e.g., max length, min sum) during the process."
                ],
                "pseudocode": "function slidingWindow(arr):\n  left = 0\n  ans = 0\n  window_state = 0\n  \n  for right from 0 to arr.length - 1:\n    # add arr[right] to window_state\n    \n    while (window is invalid):\n      # remove arr[left] from window_state\n      left += 1\n      \n    # update ans based on valid window\n    \n  return ans",
                "code": {
                    "python": "def max_sum_subarray(arr, k):\n    max_sum = float('-inf')\n    current_sum = 0\n    left = 0\n    \n    for right in range(len(arr)):\n        current_sum += arr[right]\n        \n        if right >= k - 1:\n            max_sum = max(max_sum, current_sum)\n            current_sum -= arr[left]\n            left += 1\n            \n    return max_sum",
                    "cpp": "int maxSumSubarray(vector<int>& arr, int k) {\n    int maxSum = INT_MIN, currentSum = 0, left = 0;\n    for(int right = 0; right < arr.size(); right++) {\n        currentSum += arr[right];\n        if (right >= k - 1) {\n            maxSum = max(maxSum, currentSum);\n            currentSum -= arr[left];\n            left++;\n        }\n    }\n    return maxSum;\n}",
                    "javascript": "function maxSumSubarray(arr, k) {\n    let maxSum = -Infinity;\n    let currentSum = 0;\n    let left = 0;\n    for (let right = 0; right < arr.length; right++) {\n        currentSum += arr[right];\n        if (right >= k - 1) {\n            maxSum = Math.max(maxSum, currentSum);\n            currentSum -= arr[left];\n            left++;\n        }\n    }\n    return maxSum;\n}",
                    "java": "public int maxSumSubarray(int[] arr, int k) {\n    int maxSum = Integer.MIN_VALUE;\n    int currentSum = 0;\n    int left = 0;\n    for (int right = 0; right < arr.length; right++) {\n        currentSum += arr[right];\n        if (right >= k - 1) {\n            maxSum = Math.max(maxSum, currentSum);\n            currentSum -= arr[left];\n            left++;\n        }\n    }\n    return maxSum;\n}"
                },
                "dry_run": [
                    {"iteration": 1, "right": 0, "left": 0, "window": "[2]", "sum": 2, "max_sum": "-inf"},
                    {"iteration": 2, "right": 1, "left": 0, "window": "[2, 1]", "sum": 3, "max_sum": "-inf"},
                    {"iteration": 3, "right": 2, "left": 0, "window": "[2, 1, 5]", "sum": 8, "max_sum": 8, "note": "Window size k=3 reached. Left moves next."},
                    {"iteration": 4, "right": 3, "left": 1, "window": "[1, 5, 1]", "sum": 7, "max_sum": 8}
                ],
                "complexity": {
                    "time": "O(N)",
                    "time_reasoning": "Both the left and right pointers move forward at most N times. Each element is added to the window once and removed from the window once. Thus, 2N operations, which simplifies to O(N).",
                    "space": "O(1)",
                    "space_reasoning": "We only use a few variables (left, right, current_sum, max_sum) regardless of the input size N.",
                    "matrix": [
                        {"operation": "Best Time", "value": "O(N)"},
                        {"operation": "Worst Time", "value": "O(N)"},
                        {"operation": "Space", "value": "O(1)"}
                    ]
                },
                "common_mistakes": [
                    "Forgetting to update the global max/min BEFORE shrinking the window.",
                    "Off-by-one errors in window size calculation (using `right - left` instead of `right - left + 1`).",
                    "Not removing the `arr[left]` value before incrementing `left` pointer."
                ],
                "edge_cases": [
                    "Window size `k` is greater than array length (should return 0 or error).",
                    "Array contains all negative numbers.",
                    "Window size `k` is 0."
                ],
                "interview_tips": [
                    "If a problem asks for 'longest/shortest contiguous subarray/substring', immediately mention Sliding Window.",
                    "Clarify with the interviewer if the array contains negative numbers (important for variable-size sliding window)."
                ],
                "comparison": "Sliding Window vs Two Pointers: Sliding Window always maintains a contiguous 'window' or range between the two pointers. Two Pointers can start at opposite ends and move towards each other.",
                "cheat_sheet": "Fixed Window: Expand `right` until `right - left + 1 == k`, update ans, subtract `arr[left]`, `left++`.\nVariable Window: Expand `right`, `while (invalid) { subtract arr[left], left++ }`, update ans.",
                "quiz": [
                    {
                        "question": "What is the time complexity of the Sliding Window technique?",
                        "options": ["O(N^2)", "O(N)", "O(log N)", "O(N log N)"],
                        "answer": 1,
                        "explanation": "O(N). Both the left and right pointers iterate through the array at most once, meaning each element is processed a constant number of times."
                    },
                    {
                        "question": "Which keywords in a problem statement strongly suggest using Sliding Window?",
                        "options": ["Contiguous, longest, subarray", "Sorted, pairs, combinations", "Shortest path, nodes", "Permutations, all possibilities"],
                        "answer": 0,
                        "explanation": "Sliding window operates on contiguous subarrays/substrings to find optimal (longest/shortest) properties."
                    },
                    {
                        "question": "What happens when the window size condition (k) is violated in a variable sliding window?",
                        "options": ["Return the current answer", "Move the right pointer", "Move the left pointer until it's valid", "Reset both pointers to 0"],
                        "answer": 2,
                        "explanation": "We shrink the window by moving the left pointer (and updating the window state) until the window becomes valid again."
                    }
                ]
            }
        },
        {
            "name": "Two Pointers",
            "slug": "two-pointers",
            "icon": "👉👈",
            "description": "Used to search for pairs in a sorted array, or reverse arrays. Two pointers iterate through the data structure in tandem until one or both hit a certain condition.",
            "order": 2,
            "content_json": {
                "introduction": "The Two Pointers pattern involves using two variables (pointers) to iterate through a data structure, typically an array or string. One pointer usually starts from the beginning, and the other starts from the end. They move towards each other based on certain conditions.",
                "real_life_analogy": "Imagine looking for a specific word in a physical dictionary. You don't read every page. You open the middle, and depending on alphabetical order, you ignore half the book. Two pointers is like having your left hand on the first page and right hand on the last page, narrowing down the search.",
                "visualization": {
                    "type": "array",
                    "data": [1, 2, 3, 4, 6],
                    "steps": [
                        {"pointers": {"L": 0, "R": 4}, "highlight": [0,4], "desc": "Target is 6. 1 + 6 = 7 (Too big, move R left)"},
                        {"pointers": {"L": 0, "R": 3}, "highlight": [0,3], "desc": "1 + 4 = 5 (Too small, move L right)"}
                    ]
                },
                "when_to_use": [
                    "The array is sorted and you need to find a pair of elements.",
                    "You need to reverse an array or string.",
                    "You need to compare elements from the start and end of an array."
                ],
                "when_not_to_use": [
                    "When the array is unsorted and you cannot sort it (e.g., you need original indices).",
                    "When the problem asks for contiguous subarrays (use Sliding Window instead)."
                ],
                "core_idea": "By starting at opposite ends of a sorted array, we can eliminate a vast number of possibilities at each step. If the sum of elements at the pointers is too large, moving the right pointer left is the ONLY way to decrease the sum.",
                "algorithm": [
                    "Initialize `left` pointer at index 0 and `right` pointer at `array.length - 1`.",
                    "While `left < right`:",
                    "Evaluate the condition based on `arr[left]` and `arr[right]`.",
                    "If the condition is met, return the result.",
                    "If the value is too small, increment `left`.",
                    "If the value is too large, decrement `right`."
                ],
                "pseudocode": "function twoPointers(arr, target):\n  left = 0\n  right = arr.length - 1\n  \n  while left < right:\n    current_sum = arr[left] + arr[right]\n    \n    if current_sum == target:\n      return [left, right]\n    else if current_sum < target:\n      left += 1\n    else:\n      right -= 1\n      \n  return [-1, -1]",
                "code": {
                    "python": "def two_sum_sorted(arr, target):\n    left, right = 0, len(arr) - 1\n    while left < right:\n        current = arr[left] + arr[right]\n        if current == target:\n            return [left, right]\n        elif current < target:\n            left += 1\n        else:\n            right -= 1\n    return [-1, -1]",
                    "cpp": "vector<int> twoSumSorted(vector<int>& arr, int target) {\n    int left = 0, right = arr.size() - 1;\n    while (left < right) {\n        int current = arr[left] + arr[right];\n        if (current == target) return {left, right};\n        if (current < target) left++;\n        else right--;\n    }\n    return {-1, -1};\n}",
                    "javascript": "function twoSumSorted(arr, target) {\n    let left = 0, right = arr.length - 1;\n    while (left < right) {\n        let current = arr[left] + arr[right];\n        if (current === target) return [left, right];\n        if (current < target) left++;\n        else right--;\n    }\n    return [-1, -1];\n}",
                    "java": "public int[] twoSumSorted(int[] arr, int target) {\n    int left = 0, right = arr.length - 1;\n    while (left < right) {\n        int current = arr[left] + arr[right];\n        if (current == target) return new int[]{left, right};\n        if (current < target) left++;\n        else right--;\n    }\n    return new int[]{-1, -1};\n}"
                },
                "dry_run": [
                    {"iteration": 1, "left": 0, "right": 4, "arr[L]": 1, "arr[R]": 6, "sum": 7, "note": "Sum > Target(6). Move right--."},
                    {"iteration": 2, "left": 0, "right": 3, "arr[L]": 1, "arr[R]": 4, "sum": 5, "note": "Sum < Target(6). Move left++."},
                    {"iteration": 3, "left": 1, "right": 3, "arr[L]": 2, "arr[R]": 4, "sum": 6, "note": "Target found! Return."}
                ],
                "complexity": {
                    "time": "O(N)",
                    "time_reasoning": "The pointers only move inwards and never cross or reset, meaning they scan each element at most once.",
                    "space": "O(1)",
                    "space_reasoning": "Only two integer pointers are used.",
                    "matrix": [
                        {"operation": "Time Complexity", "value": "O(N)"},
                        {"operation": "Space Complexity", "value": "O(1)"}
                    ]
                },
                "common_mistakes": [
                    "Using `left <= right` instead of `left < right` when distinct elements are required (could use same element twice).",
                    "Forgetting to sort the array first if it isn't already sorted."
                ],
                "edge_cases": [
                    "Array with fewer than 2 elements.",
                    "Multiple pairs with the same sum (depends on problem requirements)."
                ],
                "interview_tips": [
                    "If you see a sorted array and a target value, Two Pointers should be your first thought.",
                    "You can optimize O(N^2) naive loops into O(N) using this pattern."
                ],
                "comparison": "Two Pointers (Opposite Ends) vs Fast/Slow Pointers: Opposite ends are for searching sorted arrays. Fast/Slow is for detecting cycles in linked lists or arrays.",
                "cheat_sheet": "1. Sort array (if needed). 2. left = 0, right = n-1. 3. while(left < right). 4. If sum < target: left++. If sum > target: right--. Else: found.",
                "quiz": [
                    {
                        "question": "What is the primary requirement for the Two Pointers (opposite ends) pattern to work correctly for searching sums?",
                        "options": ["The array must contain positive integers.", "The array must be sorted.", "The array must have an even length.", "The array must not contain duplicates."],
                        "answer": 1,
                        "explanation": "The logic of moving left++ (to increase sum) or right-- (to decrease sum) only works if the array is sorted."
                    }
                ]
            }
        }
    ]

    for p_data in array_patterns:
        pattern, created = Pattern.objects.update_or_create(
            topic=arrays_topic,
            slug=p_data['slug'],
            defaults={
                'name': p_data['name'],
                'icon': p_data['icon'],
                'description': p_data['description'],
                'order': p_data['order'],
                'content_json': p_data['content_json']
            }
        )
        print(f"[{'CREATED' if created else 'UPDATED'}] Pattern: {pattern.name}")
