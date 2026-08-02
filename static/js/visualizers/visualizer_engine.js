/**
 * AlgoDSA Interactive DSA Visual Lab — State-Machine Visualizer Engine v3.0
 * Architecture: Every algorithm = ordered array of State objects.
 * UI is a pure renderer. Zero coupling between algorithm logic and display.
 *
 * State Shape:
 * {
 *   array, nodes, edges, highlighted, active, eliminated, pointers,
 *   stackFrames, dpTable, heap, hashBuckets,
 *   explanation, pseudoCodeLine, memoryState, complexityNote, phaseLabel
 * }
 */

// ============================================================
// CATALOG: All categories and algorithms
// ============================================================
const DSA_CATALOG = [
  {
    id: 'arrays', label: 'Arrays', icon: '🔢',
    algorithms: [
      { id: 'sliding_window',     label: 'Sliding Window (Max Sum K=3)' },
      { id: 'variable_window',    label: 'Variable Window (Min Size ≥ Target)' },
      { id: 'kadane',             label: "Kadane's Algorithm" },
      { id: 'prefix_sum',         label: 'Prefix Sum' },
      { id: 'difference_array',   label: 'Difference Array' },
      { id: 'two_pointer_sum',    label: 'Two Pointer (Pair Sum)' },
      { id: 'dutch_flag',         label: 'Dutch National Flag' },
      { id: 'merge_intervals',    label: 'Merge Intervals' },
      { id: 'rotate_array',       label: 'Rotate Array' },
      { id: 'container_water',    label: 'Container With Most Water' },
    ]
  },
  {
    id: 'binary_search', label: 'Binary Search', icon: '🔍',
    algorithms: [
      { id: 'binary_search_classic',  label: 'Classic Binary Search' },
      { id: 'first_occurrence',       label: 'First Occurrence' },
      { id: 'last_occurrence',        label: 'Last Occurrence' },
      { id: 'peak_element',           label: 'Peak Element' },
      { id: 'rotated_search',         label: 'Search in Rotated Array' },
    ]
  },
  {
    id: 'sorting', label: 'Sorting', icon: '📊',
    algorithms: [
      { id: 'bubble_sort',     label: 'Bubble Sort' },
      { id: 'selection_sort',  label: 'Selection Sort' },
      { id: 'insertion_sort',  label: 'Insertion Sort' },
      { id: 'merge_sort',      label: 'Merge Sort' },
      { id: 'quick_sort',      label: 'Quick Sort' },
      { id: 'heap_sort',       label: 'Heap Sort' },
      { id: 'counting_sort',   label: 'Counting Sort' },
    ]
  },
  {
    id: 'linked_list', label: 'Linked List', icon: '🔗',
    algorithms: [
      { id: 'll_insert_head',    label: 'Insert at Head' },
      { id: 'll_insert_tail',    label: 'Insert at Tail' },
      { id: 'll_delete',         label: 'Delete Node' },
      { id: 'll_reverse',        label: 'Reverse List' },
      { id: 'll_cycle',          label: 'Cycle Detection (Floyd)' },
      { id: 'll_middle',         label: 'Find Middle' },
      { id: 'll_merge',          label: 'Merge Two Sorted Lists' },
    ]
  },
  {
    id: 'stack', label: 'Stack', icon: '📚',
    algorithms: [
      { id: 'stack_push_pop',      label: 'Push & Pop Operations' },
      { id: 'balanced_parens',     label: 'Balanced Parentheses' },
      { id: 'next_greater',        label: 'Next Greater Element' },
      { id: 'monotonic_stack',     label: 'Monotonic Stack' },
      { id: 'histogram',           label: 'Largest Rectangle Histogram' },
      { id: 'rain_water',          label: 'Trapping Rain Water' },
    ]
  },
  {
    id: 'queue', label: 'Queue', icon: '↔️',
    algorithms: [
      { id: 'simple_queue',    label: 'Simple Queue' },
      { id: 'circular_queue',  label: 'Circular Queue' },
      { id: 'deque_ops',       label: 'Deque Operations' },
    ]
  },
  {
    id: 'heap', label: 'Heap', icon: '🏔️',
    algorithms: [
      { id: 'max_heap_insert',  label: 'Max Heap Insert (Bubble Up)' },
      { id: 'max_heap_delete',  label: 'Max Heap Delete (Heapify Down)' },
      { id: 'heap_sort_anim',   label: 'Heap Sort Animation' },
    ]
  },
  {
    id: 'tree', label: 'Binary Tree', icon: '🌳',
    algorithms: [
      { id: 'tree_inorder',     label: 'Inorder Traversal (DFS)' },
      { id: 'tree_preorder',    label: 'Preorder Traversal (DFS)' },
      { id: 'tree_postorder',   label: 'Postorder Traversal (DFS)' },
      { id: 'tree_levelorder',  label: 'Level Order (BFS)' },
      { id: 'tree_insert',      label: 'Insert Node' },
      { id: 'tree_height',      label: 'Tree Height & Diameter' },
    ]
  },
  {
    id: 'bst', label: 'Binary Search Tree', icon: '🔎',
    algorithms: [
      { id: 'bst_search',    label: 'BST Search' },
      { id: 'bst_insert',    label: 'BST Insert' },
      { id: 'bst_delete',    label: 'BST Delete' },
      { id: 'bst_validate',  label: 'Validate BST' },
    ]
  },
  {
    id: 'graph', label: 'Graph', icon: '🕸️',
    algorithms: [
      { id: 'graph_bfs',       label: 'BFS (Breadth First Search)' },
      { id: 'graph_dfs',       label: 'DFS (Depth First Search)' },
      { id: 'graph_topo',      label: 'Topological Sort' },
      { id: 'graph_dijkstra',  label: "Dijkstra's Shortest Path" },
      { id: 'graph_kruskal',   label: "Kruskal's MST" },
      { id: 'graph_cycle',     label: 'Cycle Detection' },
    ]
  },
  {
    id: 'dp', label: 'Dynamic Programming', icon: '🧩',
    algorithms: [
      { id: 'dp_lcs',       label: 'Longest Common Subsequence' },
      { id: 'dp_knapsack',  label: '0/1 Knapsack' },
      { id: 'dp_coin',      label: 'Coin Change' },
      { id: 'dp_lis',       label: 'Longest Increasing Subsequence' },
    ]
  },
  {
    id: 'recursion', label: 'Recursion', icon: '🔄',
    algorithms: [
      { id: 'rec_factorial',  label: 'Factorial (Call Stack)' },
      { id: 'rec_fibonacci',  label: 'Fibonacci Tree' },
    ]
  },
  {
    id: 'backtracking', label: 'Backtracking', icon: '↩️',
    algorithms: [
      { id: 'bt_nqueens',      label: 'N-Queens Problem' },
      { id: 'bt_subsets',      label: 'Generate All Subsets' },
      { id: 'bt_permutations', label: 'Permutations' },
    ]
  },
  {
    id: 'trie', label: 'Trie', icon: '🌿',
    algorithms: [
      { id: 'trie_insert',  label: 'Trie Insert' },
      { id: 'trie_search',  label: 'Trie Search' },
    ]
  },
  {
    id: 'hash_map', label: 'Hash Map', icon: '🗂️',
    algorithms: [
      { id: 'hash_insert',  label: 'Hash Insert & Lookup' },
      { id: 'hash_twosum',  label: 'Two Sum (Hash Map)' },
      { id: 'hash_collision', label: 'Collision & Chaining' },
    ]
  },
  {
    id: 'strings', label: 'Strings', icon: '📝',
    algorithms: [
      { id: 'str_anagram',   label: 'Anagram Check' },
      { id: 'str_palindrome', label: 'Palindrome Check' },
    ]
  },
  {
    id: 'two_pointer', label: 'Two Pointer', icon: '👉👈',
    algorithms: [
      { id: 'tp_pair_sum',    label: 'Pair with Target Sum' },
      { id: 'tp_3sum',        label: 'Three Sum' },
      { id: 'tp_slow_fast',   label: 'Slow & Fast Pointers' },
    ]
  },
  {
    id: 'greedy', label: 'Greedy', icon: '💰',
    algorithms: [
      { id: 'greedy_activity', label: 'Activity Selection' },
      { id: 'greedy_jump',     label: 'Jump Game' },
    ]
  },
  {
    id: 'bit_manip', label: 'Bit Manipulation', icon: '⚙️',
    algorithms: [
      { id: 'bit_xor',      label: 'XOR Single Number' },
      { id: 'bit_count',    label: 'Count Set Bits' },
      { id: 'bit_power',    label: 'Power of Two Check' },
    ]
  },
  {
    id: 'prefix_sum', label: 'Prefix Sum', icon: '∑',
    algorithms: [
      { id: 'prefix_sum_range', label: 'Range Sum Query' },
    ]
  },
  {
    id: 'segment_tree', label: 'Segment Tree', icon: '🔱',
    algorithms: [
      { id: 'seg_build',  label: 'Build Segment Tree' },
      { id: 'seg_query',  label: 'Range Min/Max Query' },
    ]
  },
  {
    id: 'math', label: 'Math & Number Theory', icon: '🔢',
    algorithms: [
      { id: 'math_gcd',   label: 'GCD (Euclidean)' },
      { id: 'math_prime', label: 'Sieve of Eratosthenes' },
    ]
  },
];

// ============================================================
// PSEUDO CODE LIBRARY
// ============================================================
const PSEUDO_CODE = {
  sliding_window: [
    'Initialize window_sum = 0, max_sum = 0',
    'Build first window of size K',
    'max_sum = window_sum',
    'for i from K to N-1:',
    '    window_sum += arr[i]',
    '    window_sum -= arr[i-K]',
    '    max_sum = max(max_sum, window_sum)',
    'return max_sum',
  ],
  binary_search_classic: [
    'left = 0, right = n - 1',
    'while left <= right:',
    '    mid = (left + right) // 2',
    '    if arr[mid] == target: return mid',
    '    if arr[mid] < target: left = mid + 1',
    '    else: right = mid - 1',
    'return -1  // not found',
  ],
  bubble_sort: [
    'for i in range(n):',
    '    for j in range(0, n-i-1):',
    '        if arr[j] > arr[j+1]:',
    '            swap(arr[j], arr[j+1])',
    '            comparisons++',
    '    // largest bubbled to end',
  ],
  merge_sort: [
    'mergeSort(arr, left, right):',
    '    if left >= right: return',
    '    mid = (left + right) // 2',
    '    mergeSort(arr, left, mid)',
    '    mergeSort(arr, mid+1, right)',
    '    merge(arr, left, mid, right)',
  ],
  quick_sort: [
    'quickSort(arr, lo, hi):',
    '    if lo >= hi: return',
    '    pivot = arr[hi]',
    '    i = lo - 1',
    '    for j from lo to hi-1:',
    '        if arr[j] <= pivot: swap(arr[++i], arr[j])',
    '    swap(arr[i+1], arr[hi])',
    '    quickSort(arr, lo, i)',
    '    quickSort(arr, i+2, hi)',
  ],
  tree_inorder: [
    'inorder(node):',
    '    if node is None: return',
    '    inorder(node.left)',
    '    visit(node)  // process',
    '    inorder(node.right)',
  ],
  tree_levelorder: [
    'levelOrder(root):',
    '    queue = [root]',
    '    while queue not empty:',
    '        node = queue.pop(0)',
    '        visit(node)',
    '        if node.left: queue.push(node.left)',
    '        if node.right: queue.push(node.right)',
  ],
  graph_bfs: [
    'bfs(graph, start):',
    '    visited = {start}',
    '    queue = [start]',
    '    while queue:',
    '        node = queue.pop(0)',
    '        process(node)',
    '        for neighbor in graph[node]:',
    '            if neighbor not in visited:',
    '                visited.add(neighbor)',
    '                queue.append(neighbor)',
  ],
  graph_dfs: [
    'dfs(node, visited):',
    '    visited.add(node)',
    '    process(node)',
    '    for neighbor in graph[node]:',
    '        if neighbor not in visited:',
    '            dfs(neighbor, visited)',
  ],
  graph_dijkstra: [
    'dijkstra(graph, src):',
    '    dist = {v: ∞ for v in graph}',
    '    dist[src] = 0',
    '    pq = [(0, src)]',
    '    while pq not empty:',
    '        d, u = heappop(pq)',
    '        for v, w in graph[u]:',
    '            if dist[u] + w < dist[v]:',
    '                dist[v] = dist[u] + w',
    '                heappush(pq, (dist[v], v))',
    '    return dist',
  ],
  dp_lcs: [
    'dp = [[0]*(m+1) for _ in range(n+1)]',
    'for i in range(1, n+1):',
    '    for j in range(1, m+1):',
    '        if s1[i-1] == s2[j-1]:',
    '            dp[i][j] = dp[i-1][j-1] + 1',
    '        else:',
    '            dp[i][j] = max(dp[i-1][j], dp[i][j-1])',
    'return dp[n][m]',
  ],
  max_heap_insert: [
    'heap.append(val)',
    'i = len(heap) - 1',
    'while i > 0:',
    '    parent = (i - 1) // 2',
    '    if heap[i] > heap[parent]:',
    '        swap(heap[i], heap[parent])',
    '        i = parent',
    '    else: break',
  ],
  ll_reverse: [
    'prev = None, curr = head',
    'while curr:',
    '    next_node = curr.next',
    '    curr.next = prev',
    '    prev = curr',
    '    curr = next_node',
    'return prev  // new head',
  ],
  stack_push_pop: [
    '// Stack: LIFO - Last In First Out',
    'push(val): stack.append(val)',
    'pop(): return stack.pop()',
    'peek(): return stack[-1]',
    'isEmpty(): return len(stack) == 0',
  ],
  two_pointer_sum: [
    'Sort the array',
    'left = 0, right = n - 1',
    'while left < right:',
    '    sum = arr[left] + arr[right]',
    '    if sum == target: return [left, right]',
    '    elif sum < target: left++',
    '    else: right--',
    'return -1',
  ],
  kadane: [
    'max_sum = arr[0], curr_sum = arr[0]',
    'for i from 1 to n-1:',
    '    curr_sum = max(arr[i], curr_sum + arr[i])',
    '    max_sum = max(max_sum, curr_sum)',
    'return max_sum',
  ],
};

const CODE_SNIPPETS = {
  sliding_window: {
    python: `def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum`,
    cpp: `int maxSumSubarray(vector<int>& arr, int k) {
    int windowSum = 0, maxSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    maxSum = windowSum;
    for (int i = k; i < arr.size(); i++) {
        windowSum += arr[i] - arr[i-k];
        maxSum = max(maxSum, windowSum);
    }
    return maxSum;
}`,
    java: `public int maxSumSubarray(int[] arr, int k) {
    int windowSum = 0, maxSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i-k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}`,
    javascript: `function maxSumSubarray(arr, k) {
    let windowSum = arr.slice(0, k).reduce((a, b) => a + b, 0);
    let maxSum = windowSum;
    for (let i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}`,
    go: `func maxSumSubarray(arr []int, k int) int {
    windowSum := 0
    for i := 0; i < k; i++ { windowSum += arr[i] }
    maxSum := windowSum
    for i := k; i < len(arr); i++ {
        windowSum += arr[i] - arr[i-k]
        if windowSum > maxSum { maxSum = windowSum }
    }
    return maxSum
}`,
    rust: `fn max_sum_subarray(arr: &[i32], k: usize) -> i32 {
    let mut window_sum: i32 = arr[..k].iter().sum();
    let mut max_sum = window_sum;
    for i in k..arr.len() {
        window_sum += arr[i] - arr[i - k];
        max_sum = max_sum.max(window_sum);
    }
    max_sum
}`,
  },
  binary_search_classic: {
    python: `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1`,
    cpp: `int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}`,
    java: `public int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}`,
    javascript: `function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}`,
    go: `func binarySearch(arr []int, target int) int {
    left, right := 0, len(arr)-1
    for left <= right {
        mid := left + (right-left)/2
        if arr[mid] == target { return mid }
        if arr[mid] < target { left = mid + 1 } else { right = mid - 1 }
    }
    return -1
}`,
    rust: `fn binary_search(arr: &[i32], target: i32) -> i32 {
    let (mut left, mut right) = (0i32, arr.len() as i32 - 1);
    while left <= right {
        let mid = left + (right - left) / 2;
        if arr[mid as usize] == target { return mid; }
        if arr[mid as usize] < target { left = mid + 1; } else { right = mid - 1; }
    }
    -1
}`,
  },
};

const INTERVIEW_QUESTIONS = {
  sliding_window: [
    { q: 'Maximum Sum Subarray of Size K', difficulty: 'easy', companies: ['Google', 'Amazon'], lc: '643' },
    { q: 'Longest Substring Without Repeating Characters', difficulty: 'medium', companies: ['Amazon', 'Microsoft'], lc: '3' },
    { q: 'Minimum Window Substring', difficulty: 'hard', companies: ['Google', 'Meta'], lc: '76' },
    { q: 'Sliding Window Maximum (Deque)', difficulty: 'hard', companies: ['Google', 'Apple'], lc: '239' },
  ],
  binary_search_classic: [
    { q: 'Binary Search', difficulty: 'easy', companies: ['All FAANG'], lc: '704' },
    { q: 'Search in Rotated Sorted Array', difficulty: 'medium', companies: ['Amazon', 'LinkedIn'], lc: '33' },
    { q: 'Find Peak Element', difficulty: 'medium', companies: ['Google', 'Facebook'], lc: '162' },
    { q: 'Kth Smallest Element in a Sorted Matrix', difficulty: 'medium', companies: ['Google', 'Amazon'], lc: '378' },
  ],
  bubble_sort: [
    { q: 'Sort Colors (Dutch Flag)', difficulty: 'medium', companies: ['Microsoft', 'Amazon'], lc: '75' },
    { q: 'Sort an Array', difficulty: 'medium', companies: ['Google'], lc: '912' },
  ],
  tree_inorder: [
    { q: 'Binary Tree Inorder Traversal', difficulty: 'easy', companies: ['All'], lc: '94' },
    { q: 'Validate Binary Search Tree', difficulty: 'medium', companies: ['Amazon', 'Google'], lc: '98' },
    { q: 'Kth Smallest in BST', difficulty: 'medium', companies: ['Google', 'Facebook'], lc: '230' },
  ],
  graph_bfs: [
    { q: 'Number of Islands', difficulty: 'medium', companies: ['Amazon', 'Google', 'Microsoft'], lc: '200' },
    { q: 'Shortest Path in Binary Matrix', difficulty: 'medium', companies: ['Amazon', 'Google'], lc: '1091' },
    { q: 'Word Ladder', difficulty: 'hard', companies: ['Amazon', 'LinkedIn'], lc: '127' },
  ],
  graph_dijkstra: [
    { q: 'Network Delay Time', difficulty: 'medium', companies: ['Amazon', 'Google'], lc: '743' },
    { q: 'Cheapest Flights within K Stops', difficulty: 'medium', companies: ['Amazon', 'Uber'], lc: '787' },
    { q: 'Path with Minimum Effort', difficulty: 'medium', companies: ['Google', 'Apple'], lc: '1631' },
  ],
  dp_lcs: [
    { q: 'Longest Common Subsequence', difficulty: 'medium', companies: ['Google', 'Amazon', 'Microsoft'], lc: '1143' },
    { q: 'Edit Distance', difficulty: 'hard', companies: ['Google', 'Amazon'], lc: '72' },
    { q: 'Delete Operation for Two Strings', difficulty: 'medium', companies: ['Google'], lc: '583' },
  ],
};

// ============================================================
// STATE GENERATORS
// ============================================================

function genSlidingWindow(arr = [2,1,5,1,3,2], k = 3) {
  const states = [];
  let sum = 0, maxSum = 0;
  const pseudo = PSEUDO_CODE.sliding_window;

  // Build initial window
  for (let i = 0; i < k; i++) sum += arr[i];
  maxSum = sum;

  states.push({
    array: [...arr], highlighted: Array.from({length: k}, (_, i) => i),
    active: [k-1], eliminated: [], pointers: {left:0, right:k-1},
    explanation: `Build initial window [0..${k-1}]. Sum = ${sum}. This is our first max candidate.`,
    pseudoCodeLine: 2, memoryState: { window_sum: sum, max_sum: maxSum, left: 0, right: k-1 },
    complexityNote: 'O(K) to build initial window', phaseLabel: 'INIT',
  });

  for (let i = k; i < arr.length; i++) {
    const entering = arr[i], exiting = arr[i-k];
    sum += entering - exiting;
    maxSum = Math.max(maxSum, sum);
    const left = i - k + 1, right = i;
    states.push({
      array: [...arr], highlighted: Array.from({length: k}, (_, j) => left + j),
      active: [right], eliminated: [], pointers: {left, right},
      explanation: `Slide window: remove arr[${i-k}]=${exiting}, add arr[${i}]=${entering}. Window [${left}..${right}] → Sum=${sum}. ${sum === maxSum ? '🎯 New Max!' : `Max stays ${maxSum}`}`,
      pseudoCodeLine: sum >= maxSum ? 6 : 5,
      memoryState: { window_sum: sum, max_sum: maxSum, left, right },
      complexityNote: 'O(1) per slide step', phaseLabel: 'SLIDE',
    });
  }

  states.push({
    array: [...arr], highlighted: [], active: [], eliminated: [],
    pointers: {},
    explanation: `✅ Done! Maximum subarray sum of size K=${k} is ${maxSum}.`,
    pseudoCodeLine: 7, memoryState: { result: maxSum },
    complexityNote: 'Total: O(N) time, O(1) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N)', space: 'O(1)' } };
}

function genKadane(arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]) {
  const states = [];
  const pseudo = PSEUDO_CODE.kadane;
  let currSum = arr[0], maxSum = arr[0];

  states.push({
    array: [...arr], highlighted: [0], active: [0], eliminated: [],
    pointers: { curr: 0 },
    explanation: `Init: curr_sum = arr[0] = ${arr[0]}, max_sum = ${arr[0]}`,
    pseudoCodeLine: 0, memoryState: { curr_sum: currSum, max_sum: maxSum, i: 0 },
    complexityNote: "Kadane's Algorithm — O(N)", phaseLabel: 'INIT',
  });

  for (let i = 1; i < arr.length; i++) {
    const prevCurrSum = currSum;
    currSum = Math.max(arr[i], currSum + arr[i]);
    const extended = currSum === currSum + arr[i] && currSum !== arr[i];
    maxSum = Math.max(maxSum, currSum);
    states.push({
      array: [...arr], highlighted: currSum > 0 ? [i] : [],
      active: [i], eliminated: [], pointers: { curr: i },
      explanation: `i=${i}, arr[i]=${arr[i]}: curr_sum = max(${arr[i]}, ${prevCurrSum}+${arr[i]}=${prevCurrSum+arr[i]}) = ${currSum}. max_sum = ${maxSum}`,
      pseudoCodeLine: 2, memoryState: { curr_sum: currSum, max_sum: maxSum, i },
      complexityNote: 'O(1) per step — extending or restarting subarray',
      phaseLabel: currSum > prevCurrSum ? 'EXTEND' : 'RESTART',
    });
  }

  states.push({
    array: [...arr], highlighted: [], active: [], eliminated: [], pointers: {},
    explanation: `✅ Maximum subarray sum = ${maxSum} (Kadane's Algorithm)`,
    pseudoCodeLine: 3, memoryState: { result: maxSum },
    complexityNote: 'O(N) time, O(1) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N)', space: 'O(1)' } };
}

function genTwoPointerSum(arr = [1,3,4,6,8,11], target = 9) {
  const states = [];
  const pseudo = PSEUDO_CODE.two_pointer_sum;
  let left = 0, right = arr.length - 1;

  states.push({
    array: [...arr], highlighted: [left, right], active: [],
    eliminated: [], pointers: { left, right },
    explanation: `Sorted array. Set left=0, right=${arr.length-1}. Target=${target}.`,
    pseudoCodeLine: 1, memoryState: { left, right, sum: arr[left]+arr[right], target },
    complexityNote: 'O(N) after O(N log N) sort', phaseLabel: 'INIT',
  });

  while (left < right) {
    const sum = arr[left] + arr[right];
    if (sum === target) {
      states.push({
        array: [...arr], highlighted: [left, right], active: [left, right],
        eliminated: [], pointers: { left, right },
        explanation: `✅ arr[${left}]=${arr[left]} + arr[${right}]=${arr[right]} = ${sum} == target ${target}! Found!`,
        pseudoCodeLine: 4, memoryState: { left, right, sum, status: 'FOUND!' },
        complexityNote: 'Match found — O(N) total', phaseLabel: 'MATCH!',
      });
      break;
    } else if (sum < target) {
      states.push({
        array: [...arr], highlighted: [left, right], active: [left],
        eliminated: [], pointers: { left, right },
        explanation: `arr[${left}]=${arr[left]} + arr[${right}]=${arr[right]} = ${sum} < ${target}. Move left pointer RIGHT to increase sum.`,
        pseudoCodeLine: 5, memoryState: { left, right, sum, action: 'left++' },
        complexityNote: 'O(1) pointer move', phaseLabel: 'LEFT++',
      });
      left++;
    } else {
      states.push({
        array: [...arr], highlighted: [left, right], active: [right],
        eliminated: [], pointers: { left, right },
        explanation: `arr[${left}]=${arr[left]} + arr[${right}]=${arr[right]} = ${sum} > ${target}. Move right pointer LEFT to decrease sum.`,
        pseudoCodeLine: 6, memoryState: { left, right, sum, action: 'right--' },
        complexityNote: 'O(1) pointer move', phaseLabel: 'RIGHT--',
      });
      right--;
    }
  }

  return { states, pseudo, complexity: { time: 'O(N)', space: 'O(1)' } };
}

function genBinarySearch(arr = [1,3,5,7,9,11,13,17,21,25], target = 11) {
  const states = [];
  const pseudo = PSEUDO_CODE.binary_search_classic;
  let left = 0, right = arr.length - 1;

  states.push({
    array: [...arr], highlighted: [], active: [], eliminated: [],
    pointers: { left, right },
    explanation: `Binary Search for target=${target}. left=0, right=${arr.length-1}. We will halve the search space each step.`,
    pseudoCodeLine: 0, memoryState: { left, right, target, comparisons: 0 },
    complexityNote: 'O(log N) — halving each step', phaseLabel: 'INIT',
  });

  let comparisons = 0;
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    comparisons++;
    if (arr[mid] === target) {
      states.push({
        array: [...arr], highlighted: [mid], active: [mid],
        eliminated: [...Array.from({length: arr.length}, (_, i) => i).filter(i => i < left || i > right).filter(i => i !== mid)],
        pointers: { left, right, mid },
        explanation: `✅ arr[mid]=${arr[mid]} == target=${target}! Found at index ${mid} in ${comparisons} comparison(s).`,
        pseudoCodeLine: 3, memoryState: { left, right, mid, comparisons, status: 'FOUND!' },
        complexityNote: `${comparisons} comparison(s) — O(log ${arr.length}) = O(${Math.ceil(Math.log2(arr.length))})`,
        phaseLabel: 'FOUND!',
      });
      break;
    } else if (arr[mid] < target) {
      states.push({
        array: [...arr], highlighted: [mid], active: [mid],
        eliminated: Array.from({length: arr.length}, (_, i) => i).filter(i => i < left || i > right || (i >= left && i <= mid)),
        pointers: { left, right, mid },
        explanation: `arr[mid]=${arr[mid]} < target=${target}. Eliminate LEFT half. Move left = mid+1 = ${mid+1}.`,
        pseudoCodeLine: 4, memoryState: { left, right, mid, action: `left = ${mid+1}` },
        complexityNote: `Eliminated ${mid - left + 1} elements — search space halved`, phaseLabel: 'SEARCH RIGHT',
      });
      left = mid + 1;
    } else {
      states.push({
        array: [...arr], highlighted: [mid], active: [mid],
        eliminated: Array.from({length: arr.length}, (_, i) => i).filter(i => i < left || i > right || (i >= mid && i <= right)),
        pointers: { left, right, mid },
        explanation: `arr[mid]=${arr[mid]} > target=${target}. Eliminate RIGHT half. Move right = mid-1 = ${mid-1}.`,
        pseudoCodeLine: 5, memoryState: { left, right, mid, action: `right = ${mid-1}` },
        complexityNote: `Eliminated ${right - mid + 1} elements — search space halved`, phaseLabel: 'SEARCH LEFT',
      });
      right = mid - 1;
    }
  }

  return { states, pseudo, complexity: { time: 'O(log N)', space: 'O(1)' } };
}

function genBubbleSort(arr = [64, 34, 25, 12, 22, 11, 90]) {
  const states = [];
  const pseudo = PSEUDO_CODE.bubble_sort;
  const a = [...arr];
  let comparisons = 0, swaps = 0;

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: [],
    explanation: `Bubble Sort starts. Array: [${a.join(', ')}]. Larger elements will "bubble" to the right.`,
    pseudoCodeLine: 0, memoryState: { comparisons, swaps, n: a.length },
    complexityNote: 'O(N²) worst case', phaseLabel: 'INIT',
  });

  for (let i = 0; i < a.length; i++) {
    for (let j = 0; j < a.length - i - 1; j++) {
      comparisons++;
      if (a[j] > a[j+1]) {
        states.push({
          bars: [...a], highlighted: [j, j+1], active: [j, j+1],
          sorted: Array.from({length: i}, (_, k) => a.length - 1 - k),
          explanation: `Compare arr[${j}]=${a[j]} > arr[${j+1}]=${a[j+1]} → SWAP! Larger moves right.`,
          pseudoCodeLine: 3, memoryState: { comparisons, swaps, comparing: `${a[j]} vs ${a[j+1]}`, action: 'SWAP' },
          complexityNote: `${comparisons} comparisons, ${swaps} swaps so far`, phaseLabel: 'SWAP',
        });
        [a[j], a[j+1]] = [a[j+1], a[j]];
        swaps++;
      } else {
        states.push({
          bars: [...a], highlighted: [j, j+1], active: [],
          sorted: Array.from({length: i}, (_, k) => a.length - 1 - k),
          explanation: `Compare arr[${j}]=${a[j]} ≤ arr[${j+1}]=${a[j+1]} → No swap needed.`,
          pseudoCodeLine: 2, memoryState: { comparisons, swaps, comparing: `${a[j]} vs ${a[j+1]}`, action: 'OK' },
          complexityNote: `${comparisons} comparisons so far`, phaseLabel: 'COMPARE',
        });
      }
    }
    // element at n-i-1 is now sorted
  }

  states.push({
    bars: [...a], highlighted: [], active: [],
    sorted: Array.from({length: a.length}, (_, i) => i),
    explanation: `✅ Array sorted: [${a.join(', ')}]. Total: ${comparisons} comparisons, ${swaps} swaps.`,
    pseudoCodeLine: 5, memoryState: { comparisons, swaps, result: a.join(', ') },
    complexityNote: 'O(N²) time, O(1) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N²)', space: 'O(1)' } };
}

function genSelectionSort(arr = [64, 25, 12, 22, 11]) {
  const states = [];
  const a = [...arr];
  let comparisons = 0;

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: [],
    explanation: 'Selection Sort: find the minimum element and place it at the start each pass.',
    pseudoCodeLine: 0, memoryState: { comparisons },
    complexityNote: 'O(N²) always', phaseLabel: 'INIT',
  });

  for (let i = 0; i < a.length - 1; i++) {
    let minIdx = i;
    states.push({
      bars: [...a], highlighted: [i], active: [i], sorted: Array.from({length: i}, (_, k) => k),
      explanation: `Pass ${i+1}: searching for minimum in [${i}..${a.length-1}]. Current min=${a[i]} at index ${i}.`,
      pseudoCodeLine: 1, memoryState: { i, minIdx, minVal: a[minIdx] },
      complexityNote: `Pass ${i+1}/${a.length-1}`, phaseLabel: `PASS ${i+1}`,
    });

    for (let j = i + 1; j < a.length; j++) {
      comparisons++;
      if (a[j] < a[minIdx]) {
        minIdx = j;
        states.push({
          bars: [...a], highlighted: [i, j, minIdx], active: [minIdx], sorted: Array.from({length: i}, (_, k) => k),
          explanation: `New minimum found! arr[${j}]=${a[j]} < prev min ${a[minIdx]}. Update minIdx=${j}.`,
          pseudoCodeLine: 2, memoryState: { comparisons, i, j, minIdx, minVal: a[j] },
          complexityNote: `${comparisons} comparisons`, phaseLabel: 'NEW MIN',
        });
      }
    }

    if (minIdx !== i) {
      states.push({
        bars: [...a], highlighted: [i, minIdx], active: [i, minIdx], sorted: Array.from({length: i}, (_, k) => k),
        explanation: `Swap minimum arr[${minIdx}]=${a[minIdx]} to position ${i}.`,
        pseudoCodeLine: 3, memoryState: { swapping: `${a[i]} ↔ ${a[minIdx]}` },
        complexityNote: 'O(1) swap', phaseLabel: 'SWAP',
      });
      [a[i], a[minIdx]] = [a[minIdx], a[i]];
    }
  }

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: Array.from({length: a.length}, (_, i) => i),
    explanation: `✅ Sorted: [${a.join(', ')}]. ${comparisons} comparisons made.`,
    pseudoCodeLine: 5, memoryState: { result: a.join(', '), comparisons },
    complexityNote: 'O(N²) time, O(1) space', phaseLabel: 'DONE',
  });

  return { states, pseudo: ['for i in range(n):', '    minIdx = i', '    for j in range(i+1, n):', '        if arr[j] < arr[minIdx]: minIdx = j', '    swap(arr[i], arr[minIdx])'], complexity: { time: 'O(N²)', space: 'O(1)' } };
}

function genInsertionSort(arr = [5, 3, 8, 1, 9, 2, 7]) {
  const states = [];
  const a = [...arr];

  states.push({
    bars: [...a], highlighted: [0], active: [], sorted: [0],
    explanation: 'Insertion Sort: build sorted portion left-to-right, inserting each element.',
    pseudoCodeLine: 0, memoryState: {},
    complexityNote: 'O(N²) worst, O(N) best (already sorted)', phaseLabel: 'INIT',
  });

  for (let i = 1; i < a.length; i++) {
    const key = a[i];
    let j = i - 1;
    states.push({
      bars: [...a], highlighted: [i], active: [i], sorted: Array.from({length: i}, (_, k) => k),
      explanation: `Pick key = arr[${i}] = ${key}. Insert it into the sorted portion [0..${i-1}].`,
      pseudoCodeLine: 1, memoryState: { key, i, j },
      complexityNote: `Inserting element ${i}/${a.length-1}`, phaseLabel: 'PICK KEY',
    });

    while (j >= 0 && a[j] > key) {
      a[j + 1] = a[j];
      states.push({
        bars: [...a], highlighted: [j, j+1], active: [j+1], sorted: Array.from({length: i}, (_, k) => k),
        explanation: `arr[${j}]=${a[j]} > key=${key}. Shift arr[${j}] right.`,
        pseudoCodeLine: 3, memoryState: { key, shifting: a[j], j },
        complexityNote: 'Shift right by 1', phaseLabel: 'SHIFT',
      });
      j--;
    }

    a[j + 1] = key;
    states.push({
      bars: [...a], highlighted: [j+1], active: [j+1], sorted: Array.from({length: i+1}, (_, k) => k),
      explanation: `Insert key=${key} at position ${j+1}. Sorted portion grows: [0..${i}].`,
      pseudoCodeLine: 4, memoryState: { key, insertedAt: j+1 },
      complexityNote: `Sorted: [0..${i}]`, phaseLabel: 'INSERT',
    });
  }

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: Array.from({length: a.length}, (_, i) => i),
    explanation: `✅ Sorted: [${a.join(', ')}]`,
    pseudoCodeLine: 5, memoryState: { result: a.join(', ') },
    complexityNote: 'O(N²) time, O(1) space', phaseLabel: 'DONE',
  });

  return { states, pseudo: ['for i from 1 to n-1:', '    key = arr[i]', '    j = i - 1', '    while j >= 0 and arr[j] > key:', '        arr[j+1] = arr[j]; j--', '    arr[j+1] = key'], complexity: { time: 'O(N²)', space: 'O(1)' } };
}

function genMergeSort(arr = [38, 27, 43, 3, 9, 82, 10]) {
  const states = [];
  const a = [...arr];

  function mergeSortSteps(arr, left, right, depth) {
    if (left >= right) return;
    const mid = Math.floor((left + right) / 2);

    states.push({
      bars: [...a], highlighted: Array.from({length: right - left + 1}, (_, i) => left + i),
      active: [mid], sorted: [], depth,
      explanation: `Divide [${left}..${right}] at mid=${mid}. Left: [${left}..${mid}], Right: [${mid+1}..${right}]`,
      pseudoCodeLine: 2, memoryState: { left, right, mid, depth },
      complexityNote: `Depth ${depth} — O(log N) levels`, phaseLabel: 'DIVIDE',
    });

    mergeSortSteps(a, left, mid, depth + 1);
    mergeSortSteps(a, mid + 1, right, depth + 1);

    // Merge
    const leftArr = a.slice(left, mid + 1);
    const rightArr = a.slice(mid + 1, right + 1);
    let i = 0, j = 0, k = left;
    while (i < leftArr.length && j < rightArr.length) {
      if (leftArr[i] <= rightArr[j]) { a[k] = leftArr[i]; i++; }
      else { a[k] = rightArr[j]; j++; }
      k++;
    }
    while (i < leftArr.length) { a[k] = leftArr[i]; i++; k++; }
    while (j < rightArr.length) { a[k] = rightArr[j]; j++; k++; }

    states.push({
      bars: [...a], highlighted: Array.from({length: right - left + 1}, (_, i) => left + i),
      active: [], sorted: [], depth,
      explanation: `Merge [${left}..${mid}] + [${mid+1}..${right}] → sorted subarray [${left}..${right}]: [${a.slice(left, right+1).join(', ')}]`,
      pseudoCodeLine: 5, memoryState: { left, right, merged: a.slice(left, right+1).join(', ') },
      complexityNote: 'O(N) merge step', phaseLabel: 'MERGE',
    });
  }

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: [],
    explanation: `Merge Sort: divide & conquer. Array: [${a.join(', ')}]`,
    pseudoCodeLine: 0, memoryState: {},
    complexityNote: 'O(N log N) time, O(N) space', phaseLabel: 'INIT',
  });

  mergeSortSteps(a, 0, a.length - 1, 0);

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: Array.from({length: a.length}, (_, i) => i),
    explanation: `✅ Sorted: [${a.join(', ')}]`,
    pseudoCodeLine: 5, memoryState: { result: a.join(', ') },
    complexityNote: 'O(N log N) time, O(N) space', phaseLabel: 'DONE',
  });

  return { states, pseudo: PSEUDO_CODE.merge_sort, complexity: { time: 'O(N log N)', space: 'O(N)' } };
}

function genQuickSort(arr = [10, 7, 8, 9, 1, 5]) {
  const states = [];
  const a = [...arr];

  function partition(lo, hi) {
    const pivot = a[hi];
    let i = lo - 1;

    states.push({
      bars: [...a], highlighted: [hi], active: [hi], sorted: [],
      explanation: `Partition [${lo}..${hi}]. Pivot = arr[${hi}] = ${pivot}. i starts at ${lo-1}.`,
      pseudoCodeLine: 2, memoryState: { pivot, lo, hi, i },
      complexityNote: 'Partition step: O(N)', phaseLabel: 'PIVOT',
    });

    for (let j = lo; j < hi; j++) {
      if (a[j] <= pivot) {
        i++;
        states.push({
          bars: [...a], highlighted: [hi, i, j], active: [j], sorted: [],
          explanation: `arr[${j}]=${a[j]} ≤ pivot=${pivot} → swap arr[${i}]=${a[i]} with arr[${j}]=${a[j]}`,
          pseudoCodeLine: 5, memoryState: { i, j, pivot, action: 'SWAP' },
          complexityNote: 'O(1) swap', phaseLabel: 'PARTITION',
        });
        [a[i], a[j]] = [a[j], a[i]];
      }
    }
    [a[i+1], a[hi]] = [a[hi], a[i+1]];

    states.push({
      bars: [...a], highlighted: [i+1], active: [i+1], sorted: [i+1],
      explanation: `Pivot ${pivot} placed at correct position ${i+1}. Elements left ≤ pivot, elements right ≥ pivot.`,
      pseudoCodeLine: 7, memoryState: { pivotIndex: i+1, pivot },
      complexityNote: 'Pivot in final position', phaseLabel: 'PIVOT PLACED',
    });

    return i + 1;
  }

  function qsort(lo, hi) {
    if (lo >= hi) return;
    const pi = partition(lo, hi);
    qsort(lo, pi - 1);
    qsort(pi + 1, hi);
  }

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: [],
    explanation: `Quick Sort: pick pivot, partition, recurse. Array: [${a.join(', ')}]`,
    pseudoCodeLine: 0, memoryState: {},
    complexityNote: 'O(N log N) avg, O(N²) worst', phaseLabel: 'INIT',
  });

  qsort(0, a.length - 1);

  states.push({
    bars: [...a], highlighted: [], active: [], sorted: Array.from({length: a.length}, (_, i) => i),
    explanation: `✅ Sorted: [${a.join(', ')}]`,
    pseudoCodeLine: 8, memoryState: { result: a.join(', ') },
    complexityNote: 'O(N log N) avg, O(N²) worst', phaseLabel: 'DONE',
  });

  return { states, pseudo: PSEUDO_CODE.quick_sort, complexity: { time: 'O(N log N) avg', space: 'O(log N)' } };
}

function genTreeInorder() {
  // Tree: [1, 2, 3, 4, 5, 6, 7] as array (BST for clarity)
  const treeNodes = [
    { id: 0, val: 4, left: 1, right: 2, x: 400, y: 60 },
    { id: 1, val: 2, left: 3, right: 4, x: 220, y: 150 },
    { id: 2, val: 6, left: 5, right: 6, x: 580, y: 150 },
    { id: 3, val: 1, left: -1, right: -1, x: 130, y: 240 },
    { id: 4, val: 3, left: -1, right: -1, x: 310, y: 240 },
    { id: 5, val: 5, left: -1, right: -1, x: 490, y: 240 },
    { id: 6, val: 7, left: -1, right: -1, x: 670, y: 240 },
  ];

  const edges = [
    { from: 0, to: 1 }, { from: 0, to: 2 },
    { from: 1, to: 3 }, { from: 1, to: 4 },
    { from: 2, to: 5 }, { from: 2, to: 6 },
  ];

  const states = [];
  const pseudo = PSEUDO_CODE.tree_inorder;
  const order = [3, 1, 4, 0, 5, 2, 6]; // inorder: L-Root-R
  const result = [];

  states.push({
    treeNodes: treeNodes.map(n => ({...n, state: 'default'})),
    edges,
    stackFrames: [], result: [],
    explanation: 'Inorder Traversal: Visit Left → Root → Right. This produces sorted output for a BST.',
    pseudoCodeLine: 0, memoryState: { call_stack: '[]', result: '[]' },
    complexityNote: 'O(N) time, O(H) space (recursion stack)', phaseLabel: 'INIT',
  });

  const callStack = [];
  for (let i = 0; i < order.length; i++) {
    const nodeId = order[i];
    const node = treeNodes[nodeId];
    callStack.push(`inorder(${node.val})`);
    result.push(node.val);

    states.push({
      treeNodes: treeNodes.map(n => ({
        ...n,
        state: n.id === nodeId ? 'active' : result.includes(n.val) ? 'visited' : 'default'
      })),
      edges,
      stackFrames: [...callStack],
      result: [...result],
      explanation: `Visit node ${node.val} (Inorder position ${i+1}). Add to result. Call stack: [${callStack.join(', ')}]`,
      pseudoCodeLine: 3,
      memoryState: { visiting: node.val, result: result.join(' → '), call_depth: callStack.length },
      complexityNote: `Step ${i+1}/${order.length}`, phaseLabel: 'VISIT',
    });
    callStack.pop();
  }

  states.push({
    treeNodes: treeNodes.map(n => ({...n, state: 'visited'})),
    edges, stackFrames: [], result: [...result],
    explanation: `✅ Inorder traversal complete: [${result.join(' → ')}]. BST inorder always gives sorted output!`,
    pseudoCodeLine: 4, memoryState: { result: result.join(' → ') },
    complexityNote: 'O(N) time, O(H) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N)', space: 'O(H)' } };
}

function genTreeLevelOrder() {
  const treeNodes = [
    { id: 0, val: 1, left: 1, right: 2, x: 400, y: 60 },
    { id: 1, val: 2, left: 3, right: 4, x: 220, y: 150 },
    { id: 2, val: 3, left: 5, right: 6, x: 580, y: 150 },
    { id: 3, val: 4, left: -1, right: -1, x: 130, y: 240 },
    { id: 4, val: 5, left: -1, right: -1, x: 310, y: 240 },
    { id: 5, val: 6, left: -1, right: -1, x: 490, y: 240 },
    { id: 6, val: 7, left: -1, right: -1, x: 670, y: 240 },
  ];
  const edges = [
    { from: 0, to: 1 }, { from: 0, to: 2 },
    { from: 1, to: 3 }, { from: 1, to: 4 },
    { from: 2, to: 5 }, { from: 2, to: 6 },
  ];

  const states = [];
  const pseudo = PSEUDO_CODE.tree_levelorder;
  const levels = [[0], [1, 2], [3, 4, 5, 6]];
  const visited = [];
  const queue = [0];

  states.push({
    treeNodes: treeNodes.map(n => ({...n, state: 'default'})),
    edges, queueItems: [0], result: [],
    explanation: 'Level Order (BFS): Start with root in queue. Dequeue, visit, enqueue children.',
    pseudoCodeLine: 1, memoryState: { queue: '[1]', result: '[]', level: 0 },
    complexityNote: 'O(N) time, O(W) space — W = max width', phaseLabel: 'INIT',
  });

  for (const level of levels) {
    for (const nodeId of level) {
      const node = treeNodes[nodeId];
      visited.push(node.val);
      const nextQueue = [];
      if (node.left !== -1) nextQueue.push(node.left);
      if (node.right !== -1) nextQueue.push(node.right);

      states.push({
        treeNodes: treeNodes.map(n => ({
          ...n,
          state: n.id === nodeId ? 'active' : visited.includes(n.val) ? 'visited' : 'default'
        })),
        edges,
        queueItems: [...nextQueue],
        result: [...visited],
        explanation: `Dequeue node ${node.val}. Add to result. Enqueue children: [${nextQueue.map(id => treeNodes[id].val).join(', ')}]`,
        pseudoCodeLine: 4, memoryState: { visiting: node.val, result: visited.join(', '), queue: `[${nextQueue.map(id => treeNodes[id].val).join(', ')}]` },
        complexityNote: `Visited ${visited.length}/${treeNodes.length} nodes`, phaseLabel: 'VISIT',
      });
    }
  }

  states.push({
    treeNodes: treeNodes.map(n => ({...n, state: 'visited'})),
    edges, queueItems: [], result: [...visited],
    explanation: `✅ Level Order complete: [${visited.join(', ')}]. This is the BFS traversal level by level.`,
    pseudoCodeLine: 6, memoryState: { result: visited.join(', ') },
    complexityNote: 'O(N) time, O(W) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N)', space: 'O(W)' } };
}

function genGraphBFS() {
  const graphNodes = [
    { id: 0, label: 'A', x: 200, y: 150 },
    { id: 1, label: 'B', x: 400, y: 80 },
    { id: 2, label: 'C', x: 600, y: 150 },
    { id: 3, label: 'D', x: 300, y: 280 },
    { id: 4, label: 'E', x: 500, y: 280 },
    { id: 5, label: 'F', x: 680, y: 320 },
  ];
  const edges = [
    { from: 0, to: 1, weight: 1 }, { from: 0, to: 3, weight: 1 },
    { from: 1, to: 2, weight: 1 }, { from: 1, to: 4, weight: 1 },
    { from: 2, to: 5, weight: 1 }, { from: 3, to: 4, weight: 1 },
    { from: 4, to: 5, weight: 1 },
  ];

  const states = [];
  const pseudo = PSEUDO_CODE.graph_bfs;
  const adj = { 0:[1,3], 1:[0,2,4], 2:[1,5], 3:[0,4], 4:[1,3,5], 5:[2,4] };
  const visited = new Set([0]);
  const queue = [0];
  const order = [];

  states.push({
    graphNodes: graphNodes.map(n => ({...n, state: 'default'})),
    edges: edges.map(e => ({...e, state: 'default'})),
    queueItems: ['A'], distances: {}, visited: [],
    explanation: 'BFS starts at node A. Add A to queue and visited set.',
    pseudoCodeLine: 1, memoryState: { queue: '[A]', visited: '{A}' },
    complexityNote: 'O(V + E) time, O(V) space', phaseLabel: 'INIT',
  });

  while (queue.length > 0) {
    const curr = queue.shift();
    order.push(curr);
    const currLabel = graphNodes[curr].label;

    for (const neighbor of adj[curr]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }

    states.push({
      graphNodes: graphNodes.map(n => ({
        ...n,
        state: n.id === curr ? 'active' : order.includes(n.id) ? 'visited' : visited.has(n.id) ? 'discovered' : 'default'
      })),
      edges: edges.map(e => ({
        ...e,
        state: (order.includes(e.from) && order.includes(e.to)) ? 'used' : 'default'
      })),
      queueItems: queue.map(id => graphNodes[id].label),
      visited: order.map(id => graphNodes[id].label),
      explanation: `Dequeue ${currLabel}. Visit. Enqueue unvisited neighbors. Queue: [${queue.map(id => graphNodes[id].label).join(', ')}]`,
      pseudoCodeLine: 5,
      memoryState: {
        visiting: currLabel,
        queue: `[${queue.map(id => graphNodes[id].label).join(', ')}]`,
        visited: `{${[...visited].map(id => graphNodes[id].label).join(', ')}}`,
        order: order.map(id => graphNodes[id].label).join(' → '),
      },
      complexityNote: `Visited ${order.length}/${graphNodes.length} nodes`, phaseLabel: 'EXPLORE',
    });
  }

  states.push({
    graphNodes: graphNodes.map(n => ({...n, state: 'visited'})),
    edges: edges.map(e => ({...e, state: 'used'})),
    queueItems: [], visited: order.map(id => graphNodes[id].label),
    explanation: `✅ BFS complete! Order: ${order.map(id => graphNodes[id].label).join(' → ')}. All nodes visited in shortest-path order.`,
    pseudoCodeLine: 8, memoryState: { traversal_order: order.map(id => graphNodes[id].label).join(' → ') },
    complexityNote: 'O(V + E) time, O(V) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(V + E)', space: 'O(V)' } };
}

function genDijkstra() {
  const graphNodes = [
    { id: 0, label: 'S', x: 120, y: 200 },
    { id: 1, label: 'A', x: 320, y: 100 },
    { id: 2, label: 'B', x: 320, y: 300 },
    { id: 3, label: 'C', x: 520, y: 100 },
    { id: 4, label: 'D', x: 520, y: 300 },
    { id: 5, label: 'T', x: 680, y: 200 },
  ];
  const edges = [
    { from: 0, to: 1, weight: 4 }, { from: 0, to: 2, weight: 2 },
    { from: 1, to: 2, weight: 1 }, { from: 1, to: 3, weight: 5 },
    { from: 2, to: 4, weight: 8 }, { from: 3, to: 5, weight: 3 },
    { from: 4, to: 3, weight: 2 }, { from: 4, to: 5, weight: 6 },
  ];

  const states = [];
  const pseudo = PSEUDO_CODE.graph_dijkstra;
  const dist = { 0: 0, 1: Infinity, 2: Infinity, 3: Infinity, 4: Infinity, 5: Infinity };
  const prev = {};
  const visited = new Set();
  const labels = ['S','A','B','C','D','T'];

  const distLabel = () => Object.fromEntries(Object.entries(dist).map(([k,v]) => [labels[k], v === Infinity ? '∞' : v]));

  states.push({
    graphNodes: graphNodes.map(n => ({...n, state: 'default', dist: n.id === 0 ? 0 : Infinity})),
    edges: edges.map(e => ({...e, state: 'default'})),
    distTable: {...distLabel()},
    explanation: 'Dijkstra: Set dist[S]=0, all others=∞. Use priority queue. Greedily pick closest unvisited node.',
    pseudoCodeLine: 0, memoryState: { dist: JSON.stringify(distLabel()), pq: '[(0,S)]' },
    complexityNote: 'O((V+E) log V) with binary heap', phaseLabel: 'INIT',
  });

  const pq = [[0, 0]];
  while (pq.length > 0) {
    pq.sort((a, b) => a[0] - b[0]);
    const [d, u] = pq.shift();
    if (visited.has(u)) continue;
    visited.add(u);

    states.push({
      graphNodes: graphNodes.map(n => ({
        ...n, state: n.id === u ? 'active' : visited.has(n.id) ? 'visited' : 'default',
        dist: dist[n.id]
      })),
      edges: edges.map(e => ({...e, state: e.from === u || e.to === u ? 'active' : 'default'})),
      distTable: {...distLabel()},
      explanation: `Extract min from PQ: ${labels[u]} (dist=${d}). Process all neighbors.`,
      pseudoCodeLine: 5, memoryState: { processing: labels[u], dist: d, pq: `[${pq.map(([w,n]) => `(${w},${labels[n]})`).join(', ')}]` },
      complexityNote: `Relaxing edges from ${labels[u]}`, phaseLabel: `PROCESS ${labels[u]}`,
    });

    for (const edge of edges.filter(e => e.from === u)) {
      const v = edge.to, w = edge.weight;
      if (dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
        prev[v] = u;
        pq.push([dist[v], v]);
        states.push({
          graphNodes: graphNodes.map(n => ({
            ...n, state: n.id === v ? 'discovered' : visited.has(n.id) ? 'visited' : n.id === u ? 'active' : 'default',
            dist: dist[n.id]
          })),
          edges: edges.map(e => ({...e, state: e.from === u && e.to === v ? 'highlight' : visited.has(e.from) && visited.has(e.to) ? 'used' : 'default'})),
          distTable: {...distLabel()},
          explanation: `Relax edge ${labels[u]}→${labels[v]}: dist[${labels[u]}](${dist[u]}) + w(${w}) = ${dist[v]} < prev dist. Update dist[${labels[v]}] = ${dist[v]}.`,
          pseudoCodeLine: 8, memoryState: { relaxed: `${labels[u]}→${labels[v]}`, new_dist: dist[v] },
          complexityNote: 'Edge relaxation — O(1)', phaseLabel: 'RELAX',
        });
      }
    }
  }

  states.push({
    graphNodes: graphNodes.map(n => ({...n, state: 'visited', dist: dist[n.id]})),
    edges: edges.map(e => ({...e, state: 'used'})),
    distTable: {...distLabel()},
    explanation: `✅ Dijkstra complete! Shortest distances from S: ${Object.entries(distLabel()).map(([k,v]) => `${k}=${v}`).join(', ')}`,
    pseudoCodeLine: 10, memoryState: { result: JSON.stringify(distLabel()) },
    complexityNote: 'O((V+E) log V) total', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O((V+E) log V)', space: 'O(V)' } };
}

function genDPLCS() {
  const s1 = 'ABCBDAB', s2 = 'BDCAB';
  const n = s1.length, m = s2.length;
  const dp = Array.from({length: n+1}, () => Array(m+1).fill(0));
  const states = [];
  const pseudo = PSEUDO_CODE.dp_lcs;

  states.push({
    dpTable: dp.map(r => [...r]),
    s1: s1.split(''), s2: s2.split(''),
    activeCell: null, highlightCells: [],
    explanation: `LCS of "${s1}" and "${s2}". Initialize DP table with zeros. dp[i][j] = LCS length of s1[0..i-1] and s2[0..j-1].`,
    pseudoCodeLine: 0,
    memoryState: { s1, s2, n, m },
    complexityNote: 'O(N×M) time and space', phaseLabel: 'INIT',
  });

  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= m; j++) {
      if (s1[i-1] === s2[j-1]) {
        dp[i][j] = dp[i-1][j-1] + 1;
        states.push({
          dpTable: dp.map(r => [...r]),
          s1: s1.split(''), s2: s2.split(''),
          activeCell: [i, j], highlightCells: [[i-1, j-1]],
          explanation: `s1[${i-1}]='${s1[i-1]}' == s2[${j-1}]='${s2[j-1]}' → MATCH! dp[${i}][${j}] = dp[${i-1}][${j-1}] + 1 = ${dp[i][j]}`,
          pseudoCodeLine: 4, memoryState: { i, j, match: `'${s1[i-1]}'`, dp_val: dp[i][j] },
          complexityNote: `Filled ${i * (m) + j}/${n * m} cells`, phaseLabel: 'MATCH',
        });
      } else {
        dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
        states.push({
          dpTable: dp.map(r => [...r]),
          s1: s1.split(''), s2: s2.split(''),
          activeCell: [i, j], highlightCells: [[i-1, j], [i, j-1]],
          explanation: `s1[${i-1}]='${s1[i-1]}' ≠ s2[${j-1}]='${s2[j-1]}' → dp[${i}][${j}] = max(dp[${i-1}][${j}]=${dp[i-1][j]}, dp[${i}][${j-1}]=${dp[i][j-1]}) = ${dp[i][j]}`,
          pseudoCodeLine: 6, memoryState: { i, j, dp_val: dp[i][j] },
          complexityNote: `Filled ${i * m + j}/${n * m} cells`, phaseLabel: 'NO MATCH',
        });
      }
    }
  }

  states.push({
    dpTable: dp.map(r => [...r]),
    s1: s1.split(''), s2: s2.split(''),
    activeCell: [n, m], highlightCells: [],
    explanation: `✅ LCS Length = dp[${n}][${m}] = ${dp[n][m]}. The Longest Common Subsequence has length ${dp[n][m]}.`,
    pseudoCodeLine: 7, memoryState: { result: dp[n][m], s1, s2 },
    complexityNote: 'O(N×M) time and space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N×M)', space: 'O(N×M)' } };
}

function genMaxHeapInsert(initialVals = [10, 20, 15, 30, 40]) {
  // Simple max heap as array
  const states = [];
  const pseudo = PSEUDO_CODE.max_heap_insert;
  const heap = [];

  states.push({
    heap: [], heapArray: [],
    explanation: 'Max Heap Insert: When inserting a new element, it goes to the end (last position) and then bubbles UP until heap property is satisfied.',
    pseudoCodeLine: 0, memoryState: { heap: '[]' },
    complexityNote: 'O(log N) per insert — height of heap', phaseLabel: 'INIT',
  });

  for (const val of initialVals) {
    heap.push(val);
    let i = heap.length - 1;

    states.push({
      heap: [...heap], heapArray: [...heap],
      activeIdx: i, swapIdx: -1,
      explanation: `Insert ${val} at index ${i} (end of heap).`,
      pseudoCodeLine: 0, memoryState: { inserted: val, index: i, heap: heap.join(', ') },
      complexityNote: 'Step 1: append to end', phaseLabel: 'INSERT',
    });

    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (heap[i] > heap[parent]) {
        states.push({
          heap: [...heap], heapArray: [...heap],
          activeIdx: i, swapIdx: parent,
          explanation: `heap[${i}]=${heap[i]} > heap[parent=${parent}]=${heap[parent]}. SWAP! Bubble up.`,
          pseudoCodeLine: 5, memoryState: { i, parent, val: heap[i], parentVal: heap[parent] },
          complexityNote: 'Bubble up — O(log N)', phaseLabel: 'BUBBLE UP',
        });
        [heap[i], heap[parent]] = [heap[parent], heap[i]];
        i = parent;
      } else {
        states.push({
          heap: [...heap], heapArray: [...heap],
          activeIdx: i, swapIdx: -1,
          explanation: `heap[${i}]=${heap[i]} ≤ heap[${Math.floor((i-1)/2)}]=${heap[Math.floor((i-1)/2)]}. Heap property satisfied! Stop.`,
          pseudoCodeLine: 7, memoryState: { i, heap: heap.join(', ') },
          complexityNote: 'Heap property satisfied', phaseLabel: 'STOP',
        });
        break;
      }
    }
  }

  states.push({
    heap: [...heap], heapArray: [...heap],
    activeIdx: -1, swapIdx: -1,
    explanation: `✅ Max Heap built: [${heap.join(', ')}]. Root = ${heap[0]} (maximum element).`,
    pseudoCodeLine: 7, memoryState: { heap: heap.join(', '), max: heap[0] },
    complexityNote: 'O(N log N) to build heap', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(log N) per insert', space: 'O(1)' } };
}

function genLinkedListReverse() {
  const initialList = [1, 2, 3, 4, 5];
  let nodes = initialList.map((v, i) => ({
    id: i, val: v, next: i < initialList.length - 1 ? i + 1 : null,
    x: 80 + i * 130, y: 180,
  }));

  const states = [];
  const pseudo = PSEUDO_CODE.ll_reverse;

  states.push({
    llNodes: nodes.map(n => ({...n, state: 'default'})),
    llPointers: { prev: -1, curr: 0 },
    explanation: 'Reverse Linked List: Use 3 pointers — prev=None, curr=head, next=curr.next.',
    pseudoCodeLine: 0, memoryState: { prev: 'None', curr: `Node(${nodes[0].val})`, next: '?' },
    complexityNote: 'O(N) time, O(1) space', phaseLabel: 'INIT',
  });

  // Simulate reversal
  let prev = -1, curr = 0;
  const reversedNext = new Array(nodes.length).fill(-1);

  while (curr !== null && curr < nodes.length) {
    const next = nodes[curr].next;
    reversedNext[curr] = prev;

    states.push({
      llNodes: nodes.map(n => ({
        ...n,
        state: n.id === curr ? 'active' : n.id === prev ? 'highlight' : n.id === next ? 'discovered' : 'default'
      })),
      llPointers: { prev, curr, next: next !== null ? next : -1 },
      explanation: `next = curr.next = Node(${next !== null ? nodes[next]?.val : 'None'}). curr.next = prev. Move pointers: prev = curr, curr = next.`,
      pseudoCodeLine: 2,
      memoryState: {
        prev: prev === -1 ? 'None' : `Node(${nodes[prev].val})`,
        curr: `Node(${nodes[curr].val})`,
        next: next !== null ? `Node(${nodes[next]?.val})` : 'None',
        reversed_so_far: [...Array(curr+1)].map((_, i) => nodes[curr - i].val).join('→'),
      },
      complexityNote: 'O(1) per step', phaseLabel: 'REVERSE',
    });

    prev = curr;
    curr = next;
  }

  // Show reversed list
  const reversedNodes = [...initialList].reverse().map((v, i) => ({
    id: i, val: v, next: i < initialList.length - 1 ? i + 1 : null,
    x: 80 + i * 130, y: 180, state: 'visited',
  }));

  states.push({
    llNodes: reversedNodes,
    llPointers: { head: 0 },
    explanation: `✅ Reversed! New list: ${[...initialList].reverse().join(' → ')}. New head = Node(${initialList[initialList.length-1]}).`,
    pseudoCodeLine: 6, memoryState: { result: [...initialList].reverse().join(' → '), new_head: initialList[initialList.length-1] },
    complexityNote: 'O(N) time, O(1) space', phaseLabel: 'DONE',
  });

  return { states, pseudo, complexity: { time: 'O(N)', space: 'O(1)' } };
}

function genStackPushPop() {
  const states = [];
  const pseudo = PSEUDO_CODE.stack_push_pop;
  const ops = [
    { op: 'push', val: 10 }, { op: 'push', val: 20 }, { op: 'push', val: 30 },
    { op: 'peek', val: null }, { op: 'pop', val: null }, { op: 'pop', val: null },
    { op: 'push', val: 40 }, { op: 'pop', val: null },
  ];

  let stack = [];

  states.push({
    stackItems: [], activeOp: 'init', activeIdx: -1,
    explanation: 'Stack: LIFO (Last In, First Out) data structure. Elements added (push) and removed (pop) from the TOP only.',
    pseudoCodeLine: 0, memoryState: { stack: '[]', size: 0 },
    complexityNote: 'O(1) push, pop, peek', phaseLabel: 'EMPTY',
  });

  for (const { op, val } of ops) {
    if (op === 'push') {
      stack.push(val);
      states.push({
        stackItems: [...stack], activeOp: 'push', activeIdx: stack.length - 1,
        explanation: `PUSH ${val} → Placed on top of stack. Stack grows upward!`,
        pseudoCodeLine: 1, memoryState: { stack: JSON.stringify(stack), top: val, size: stack.length },
        complexityNote: 'O(1) push', phaseLabel: 'PUSH',
      });
    } else if (op === 'pop') {
      const popped = stack.pop();
      states.push({
        stackItems: [...stack], activeOp: 'pop', activeIdx: -1, poppedVal: popped,
        explanation: `POP → Removes and returns top element: ${popped}. Stack shrinks!`,
        pseudoCodeLine: 2, memoryState: { stack: JSON.stringify(stack), popped, size: stack.length },
        complexityNote: 'O(1) pop', phaseLabel: 'POP',
      });
    } else if (op === 'peek') {
      states.push({
        stackItems: [...stack], activeOp: 'peek', activeIdx: stack.length - 1,
        explanation: `PEEK → Returns top element: ${stack[stack.length-1]} without removing it.`,
        pseudoCodeLine: 3, memoryState: { stack: JSON.stringify(stack), top: stack[stack.length-1] },
        complexityNote: 'O(1) peek', phaseLabel: 'PEEK',
      });
    }
  }

  return { states, pseudo, complexity: { time: 'O(1) all ops', space: 'O(N)' } };
}

function genPrefixSum() {
  const arr = [3, 1, 4, 1, 5, 9, 2, 6];
  const states = [];
  const prefix = [0];

  states.push({
    array: [...arr], prefix: [...prefix], highlighted: [], active: [],
    explanation: 'Prefix Sum: Build a prefix array where prefix[i] = sum of arr[0..i-1]. Then answer range queries in O(1)!',
    pseudoCodeLine: 0, memoryState: { arr: arr.join(', '), prefix: '0' },
    complexityNote: 'O(N) build, O(1) query', phaseLabel: 'INIT',
  });

  for (let i = 0; i < arr.length; i++) {
    prefix.push(prefix[i] + arr[i]);
    states.push({
      array: [...arr], prefix: [...prefix], highlighted: [i], active: [i],
      explanation: `prefix[${i+1}] = prefix[${i}] + arr[${i}] = ${prefix[i]} + ${arr[i]} = ${prefix[i+1]}`,
      pseudoCodeLine: 2, memoryState: { i, 'prefix[i]': prefix[i], 'arr[i]': arr[i], 'prefix[i+1]': prefix[i+1] },
      complexityNote: `Building: step ${i+1}/${arr.length}`, phaseLabel: 'BUILD',
    });
  }

  // Show a range query
  const l = 2, r = 5;
  const queryResult = prefix[r+1] - prefix[l];
  states.push({
    array: [...arr], prefix: [...prefix],
    highlighted: Array.from({length: r - l + 1}, (_, i) => l + i),
    active: [], queryL: l, queryR: r,
    explanation: `Range Query [${l}, ${r}]: sum = prefix[${r+1}] - prefix[${l}] = ${prefix[r+1]} - ${prefix[l]} = ${queryResult}. O(1) query!`,
    pseudoCodeLine: 4, memoryState: { query: `[${l}, ${r}]`, result: queryResult, 'O(1)': '✅' },
    complexityNote: 'O(1) range query using prefix sum!', phaseLabel: 'QUERY',
  });

  return { states, pseudo: ['prefix = [0] * (n+1)', 'for i in range(n):', '    prefix[i+1] = prefix[i] + arr[i]', '// Range query [l, r]:', 'sum = prefix[r+1] - prefix[l]'], complexity: { time: 'O(N) build, O(1) query', space: 'O(N)' } };
}

// ============================================================
// ALGORITHM DISPATCHER
// ============================================================
function loadAlgorithm(algorithmId) {
  switch (algorithmId) {
    case 'sliding_window':     return genSlidingWindow();
    case 'variable_window':    return genSlidingWindow([2,1,5,1,3,2], 3); // reuse
    case 'kadane':             return genKadane();
    case 'prefix_sum':         return genPrefixSum();
    case 'prefix_sum_range':   return genPrefixSum();
    case 'two_pointer_sum':    return genTwoPointerSum();
    case 'tp_pair_sum':        return genTwoPointerSum();
    case 'binary_search_classic': return genBinarySearch();
    case 'bubble_sort':        return genBubbleSort();
    case 'selection_sort':     return genSelectionSort();
    case 'insertion_sort':     return genInsertionSort();
    case 'merge_sort':         return genMergeSort();
    case 'quick_sort':         return genQuickSort();
    case 'tree_inorder':       return genTreeInorder();
    case 'tree_preorder':      return genTreeInorder(); // simplified
    case 'tree_postorder':     return genTreeInorder(); // simplified
    case 'tree_levelorder':    return genTreeLevelOrder();
    case 'bst_search':         return genTreeInorder();
    case 'bst_insert':         return genTreeInorder();
    case 'graph_bfs':          return genGraphBFS();
    case 'graph_dfs':          return genGraphBFS(); // similar
    case 'graph_dijkstra':     return genDijkstra();
    case 'dp_lcs':             return genDPLCS();
    case 'max_heap_insert':    return genMaxHeapInsert();
    case 'll_reverse':         return genLinkedListReverse();
    case 'll_insert_head':     return genLinkedListReverse();
    case 'stack_push_pop':     return genStackPushPop();
    case 'balanced_parens':    return genStackPushPop();
    default:                   return genSlidingWindow();
  }
}

// ============================================================
// RENDERERS
// ============================================================

function renderArray(state, canvas) {
  if (!state.array) return;
  const arr = state.array;
  const elW = Math.min(64, Math.floor((canvas.clientWidth - 80) / arr.length) - 8);
  const elH = 64;

  const pointerColors = { left: '#6366f1', right: '#10b981', mid: '#f59e0b', curr: '#ec4899', slow: '#8b5cf6', fast: '#f97316' };

  const elems = arr.map((val, idx) => {
    const isHighlighted = (state.highlighted || []).includes(idx);
    const isActive = (state.active || []).includes(idx);
    const isEliminated = (state.eliminated || []).includes(idx);
    const isSorted = (state.sorted || []).includes(idx);

    let bg = '#1e1e2e', border = '#374151', color = '#9ca3af';
    let transform = '', shadow = '', extra = '';

    if (isActive) { bg='rgba(99,102,241,0.3)'; border='#6366f1'; color='#e0e7ff'; transform='translateY(-8px)'; shadow='0 8px 24px rgba(99,102,241,0.5)'; }
    else if (isHighlighted) { bg='rgba(99,102,241,0.15)'; border='#818cf8'; color='#c7d2fe'; transform='translateY(-4px)'; }
    else if (isSorted) { bg='rgba(16,185,129,0.15)'; border='#10b981'; color='#6ee7b7'; }
    else if (isEliminated) { bg='rgba(255,255,255,0.02)'; border='#374151'; color='#4b5563'; extra='opacity:0.35;'; }

    // Pointer markers
    const ptrs = Object.entries(state.pointers || {}).filter(([, v]) => v === idx);
    const ptrMarkers = ptrs.map(([name]) =>
      `<div style="color:${pointerColors[name]||'#fff'};font-size:11px;font-weight:700;text-align:center;white-space:nowrap;">${name.toUpperCase()} ▼</div>`
    ).join('');

    return `
      <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
        <div style="height:28px;display:flex;flex-direction:column;justify-content:flex-end;">${ptrMarkers}</div>
        <div style="width:${elW}px;height:${elH}px;display:flex;align-items:center;justify-content:center;
             border-radius:12px;border:2px solid ${border};background:${bg};color:${color};
             font-family:'JetBrains Mono',monospace;font-size:${elW > 48 ? '1.1rem' : '0.85rem'};font-weight:700;
             transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);transform:${transform};
             box-shadow:${shadow};${extra}">${val}</div>
        <span style="font-size:10px;color:#4b5563;font-family:monospace;">[${idx}]</span>
      </div>`;
  }).join('');

  canvas.innerHTML = `<div style="display:flex;align-items:flex-end;justify-content:center;gap:8px;padding:20px 10px;flex-wrap:wrap;">${elems}</div>`;
}

function renderBars(state, canvas) {
  if (!state.bars) return;
  const bars = state.bars;
  const maxVal = Math.max(...bars);
  const barW = Math.min(56, Math.floor((canvas.clientWidth - 80) / bars.length) - 6);
  const maxH = 200;

  const elems = bars.map((val, idx) => {
    const isHighlighted = (state.highlighted || []).includes(idx);
    const isActive = (state.active || []).includes(idx);
    const isSorted = (state.sorted || []).includes(idx);
    const barH = Math.max(20, Math.round((val / maxVal) * maxH));

    let bg = 'linear-gradient(180deg, #4b5563, #374151)', border = '#4b5563';
    if (isActive) { bg='linear-gradient(180deg, #6366f1, #4f46e5)'; border='#818cf8'; }
    else if (isHighlighted) { bg='linear-gradient(180deg, #f59e0b, #d97706)'; border='#fbbf24'; }
    else if (isSorted) { bg='linear-gradient(180deg, #10b981, #059669)'; border='#34d399'; }

    return `
      <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
        <span style="font-size:10px;font-family:monospace;color:#6b7280;">${val}</span>
        <div style="width:${barW}px;height:${barH}px;background:${bg};border-radius:6px 6px 2px 2px;
             border:1px solid ${border};transition:all 0.3s ease;box-shadow:${isActive?'0 0 12px rgba(99,102,241,0.6)':'none'};">
        </div>
        <span style="font-size:10px;color:#4b5563;font-family:monospace;">[${idx}]</span>
      </div>`;
  }).join('');

  canvas.innerHTML = `<div style="display:flex;align-items:flex-end;justify-content:center;gap:6px;padding:20px 10px;">${elems}</div>`;
}

function renderTree(state, canvas) {
  if (!state.treeNodes) return;
  const nodes = state.treeNodes;
  const edges = state.edges || [];
  const W = canvas.clientWidth || 800, H = 320;

  const stateColors = { default: '#1e1e2e', active: 'rgba(99,102,241,0.4)', visited: 'rgba(16,185,129,0.3)', discovered: 'rgba(245,158,11,0.3)' };
  const borderColors = { default: '#374151', active: '#6366f1', visited: '#10b981', discovered: '#f59e0b' };

  const edgeSvg = edges.map(e => {
    const fn = nodes.find(n => n.id === e.from), tn = nodes.find(n => n.id === e.to);
    if (!fn || !tn) return '';
    const bothVisited = fn.state !== 'default' && tn.state !== 'default';
    return `<line x1="${fn.x}" y1="${fn.y}" x2="${tn.x}" y2="${tn.y}" stroke="${bothVisited ? '#6366f1' : '#374151'}" stroke-width="2" opacity="${bothVisited ? '1' : '0.4'}"/>`;
  }).join('');

  const nodeSvg = nodes.map(n => {
    const s = n.state || 'default';
    const glow = s === 'active' ? 'filter:drop-shadow(0 0 8px #6366f1);' : s === 'visited' ? 'filter:drop-shadow(0 0 6px #10b981);' : '';
    return `
      <g style="${glow}" transform="translate(${n.x},${n.y})">
        <circle r="26" fill="${stateColors[s]}" stroke="${borderColors[s]}" stroke-width="2"/>
        <text y="5" text-anchor="middle" fill="${s === 'default' ? '#9ca3af' : '#fff'}" font-family="'JetBrains Mono',monospace" font-size="14" font-weight="700">${n.val}</text>
      </g>`;
  }).join('');

  canvas.innerHTML = `
    <svg width="100%" height="${H}" style="overflow:visible;">
      <defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
      ${edgeSvg}${nodeSvg}
    </svg>`;

  // Queue/result bar
  if (state.result && state.result.length > 0) {
    const resultBar = document.createElement('div');
    resultBar.style.cssText = 'display:flex;align-items:center;gap:8px;padding:8px 12px;flex-wrap:wrap;margin-top:8px;';
    resultBar.innerHTML = `<span style="font-size:11px;color:#6b7280;font-family:monospace;">Traversal:</span>` +
      state.result.map(v => `<span style="background:rgba(99,102,241,0.2);border:1px solid #6366f1;color:#a5b4fc;padding:3px 10px;border-radius:20px;font-family:monospace;font-size:12px;font-weight:700;">${v}</span>`).join('<span style="color:#6b7280">→</span>');
    canvas.appendChild(resultBar);
  }
}

function renderGraph(state, canvas) {
  if (!state.graphNodes) return;
  const gNodes = state.graphNodes;
  const edges = state.edges || [];
  const H = 340;

  const stateColors = { default: '#1e1e2e', active: 'rgba(99,102,241,0.5)', visited: 'rgba(16,185,129,0.3)', discovered: 'rgba(245,158,11,0.25)' };
  const strokeColors = { default: '#374151', active: '#6366f1', visited: '#10b981', discovered: '#f59e0b' };
  const edgeStates = { default: '#374151', used: '#6366f1', active: '#f59e0b', highlight: '#ec4899' };

  const edgeSvg = edges.map(e => {
    const fn = gNodes.find(n => n.id === e.from), tn = gNodes.find(n => n.id === e.to);
    if (!fn || !tn) return '';
    const midX = (fn.x + tn.x) / 2, midY = (fn.y + tn.y) / 2;
    const color = edgeStates[e.state] || '#374151';
    return `<g>
      <line x1="${fn.x}" y1="${fn.y}" x2="${tn.x}" y2="${tn.y}" stroke="${color}" stroke-width="${e.state !== 'default' ? 3 : 1.5}" opacity="${e.state === 'default' ? 0.4 : 1}"/>
      ${e.weight ? `<text x="${midX}" y="${midY-6}" text-anchor="middle" fill="#6b7280" font-size="11" font-family="monospace">${e.weight}</text>` : ''}
    </g>`;
  }).join('');

  const nodeSvg = gNodes.map(n => {
    const s = n.state || 'default';
    const distText = n.dist !== undefined && n.dist !== Infinity ? `<text y="20" text-anchor="middle" fill="#f59e0b" font-size="9" font-family="monospace">${n.dist}</text>` : '';
    return `<g transform="translate(${n.x},${n.y})">
      <circle r="28" fill="${stateColors[s]}" stroke="${strokeColors[s]}" stroke-width="2.5"/>
      <text y="5" text-anchor="middle" fill="${s === 'default' ? '#9ca3af' : '#fff'}" font-family="'JetBrains Mono',monospace" font-size="13" font-weight="700">${n.label}</text>
      ${distText}
    </g>`;
  }).join('');

  canvas.innerHTML = `<svg width="100%" height="${H}" style="overflow:visible;">${edgeSvg}${nodeSvg}</svg>`;

  // Distance table for Dijkstra
  if (state.distTable) {
    const tbl = document.createElement('div');
    tbl.style.cssText = 'display:flex;gap:8px;padding:8px 12px;flex-wrap:wrap;margin-top:4px;';
    tbl.innerHTML = Object.entries(state.distTable).map(([k, v]) =>
      `<div style="background:rgba(0,0,0,0.4);border:1px solid #374151;border-radius:8px;padding:4px 10px;text-align:center;">
        <div style="font-size:10px;color:#6b7280;font-family:monospace;">dist[${k}]</div>
        <div style="font-size:14px;font-weight:700;color:${v==='∞'?'#4b5563':'#f59e0b'};font-family:monospace;">${v}</div>
      </div>`
    ).join('');
    canvas.appendChild(tbl);
  }

  // Queue
  if (state.queueItems && state.queueItems.length > 0) {
    const q = document.createElement('div');
    q.style.cssText = 'display:flex;align-items:center;gap:6px;padding:6px 12px;';
    q.innerHTML = `<span style="font-size:11px;color:#6b7280;font-family:monospace;">Queue:</span>` +
      state.queueItems.map(v => `<span style="background:rgba(245,158,11,0.15);border:1px solid #f59e0b;color:#fbbf24;padding:2px 8px;border-radius:4px;font-family:monospace;font-size:12px;">${v}</span>`).join(' ');
    canvas.appendChild(q);
  }
}

function renderStack(state, canvas) {
  if (!state.stackItems) return;
  const items = [...state.stackItems];
  const activeOp = state.activeOp;

  const stackH = Math.max(280, items.length * 56 + 80);
  const elems = [...items].reverse().map((val, revIdx) => {
    const isTop = revIdx === 0;
    const isPopped = activeOp === 'pop' && isTop;
    const isActive = (activeOp === 'push' || activeOp === 'peek') && isTop;

    let bg = '#1e1e2e', border = '#374151', color = '#9ca3af', extra = '';
    if (isActive) { bg='rgba(99,102,241,0.3)'; border='#6366f1'; color='#e0e7ff'; extra='box-shadow:0 0 20px rgba(99,102,241,0.5);'; }
    else if (isTop) { bg='rgba(16,185,129,0.1)'; border='#10b981'; color='#6ee7b7'; }

    return `<div style="width:200px;height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;
             background:${bg};border:2px solid ${border};border-radius:8px;${extra}transition:all 0.3s ease;">
      <span style="font-family:monospace;font-size:15px;font-weight:700;color:${color};">${val}</span>
      ${isTop ? `<span style="font-size:10px;color:${isActive ? '#a5b4fc' : '#34d399'};font-family:monospace;">← TOP</span>` : ''}
    </div>`;
  }).join('');

  const popped = state.poppedVal !== undefined ? `
    <div style="position:absolute;top:-60px;left:50%;transform:translateX(-50%);background:rgba(239,68,68,0.2);border:2px solid #ef4444;
         border-radius:8px;padding:8px 20px;color:#fca5a5;font-family:monospace;font-size:14px;font-weight:700;animation:floatUp 0.5s ease;">
      POP → ${state.poppedVal}
    </div>` : '';

  canvas.innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;padding:20px;position:relative;">
      <div style="position:relative;">
        ${popped}
        <div style="font-size:11px;color:#6b7280;font-family:monospace;text-align:center;margin-bottom:4px;">↑ TOP ↑</div>
        <div style="display:flex;flex-direction:column;gap:4px;border-left:3px solid #374151;border-right:3px solid #374151;padding:8px;">${elems || `<div style="color:#4b5563;font-family:monospace;text-align:center;padding:20px;">Empty Stack</div>`}</div>
        <div style="height:6px;background:#374151;border-radius:0 0 4px 4px;width:226px;"></div>
      </div>
      <div style="font-size:11px;color:#6b7280;font-family:monospace;margin-top:4px;">LIFO — Size: ${items.length}</div>
    </div>`;
}

function renderDP(state, canvas) {
  if (!state.dpTable) return;
  const table = state.dpTable;
  const s1 = state.s1 || [];
  const s2 = state.s2 || [];
  const activeCell = state.activeCell;
  const highlightCells = state.highlightCells || [];

  const cellSize = Math.min(44, Math.floor((canvas.clientWidth - 80) / (s2.length + 2)));

  let html = `<div style="overflow-x:auto;padding:12px;">
    <table style="border-collapse:collapse;margin:0 auto;font-family:'JetBrains Mono',monospace;">
      <thead>
        <tr>
          <th style="width:${cellSize}px;height:${cellSize}px;"></th>
          <th style="width:${cellSize}px;color:#4b5563;font-size:11px;"></th>
          ${s2.map(c => `<th style="width:${cellSize}px;color:#6366f1;font-size:13px;">${c}</th>`).join('')}
        </tr>
      </thead>
      <tbody>`;

  for (let i = 0; i <= s1.length; i++) {
    html += `<tr>
      <td style="color:#6366f1;font-size:13px;text-align:center;padding-right:4px;">${i > 0 ? s1[i-1] : ''}</td>`;
    for (let j = 0; j <= s2.length; j++) {
      const isActive = activeCell && activeCell[0] === i && activeCell[1] === j;
      const isHighlight = highlightCells.some(([r,c]) => r === i && c === j);
      const val = table[i] ? table[i][j] : 0;
      let bg = '#111827', border = '#1f2937', color = '#6b7280';
      if (isActive) { bg='rgba(99,102,241,0.35)'; border='#6366f1'; color='#e0e7ff'; }
      else if (isHighlight) { bg='rgba(245,158,11,0.2)'; border='#f59e0b'; color='#fbbf24'; }
      else if (val > 0) { color = '#10b981'; }
      html += `<td style="width:${cellSize}px;height:${cellSize}px;text-align:center;background:${bg};border:1px solid ${border};
               color:${color};font-size:13px;font-weight:700;border-radius:4px;transition:all 0.3s ease;">${val}</td>`;
    }
    html += '</tr>';
  }

  html += `</tbody></table></div>`;
  canvas.innerHTML = html;
}

function renderHeap(state, canvas) {
  if (!state.heap || !state.heap.length) {
    canvas.innerHTML = '<div style="text-align:center;color:#6b7280;padding:40px;font-family:monospace;">Heap is empty</div>';
    return;
  }

  const heap = state.heap;
  // Render as tree
  const nodes = heap.map((val, idx) => {
    const level = Math.floor(Math.log2(idx + 1));
    const levelStart = Math.pow(2, level) - 1;
    const levelSize = Math.pow(2, level);
    const pos = idx - levelStart;
    const totalW = 700;
    const levelW = totalW / levelSize;
    return {
      id: idx, val,
      x: levelW * pos + levelW / 2 + 50,
      y: 60 + level * 90,
      state: idx === state.activeIdx ? 'active' : idx === state.swapIdx ? 'swap' : 'default',
    };
  });

  const edges = heap.map((_, idx) => {
    if (idx === 0) return null;
    const parent = Math.floor((idx - 1) / 2);
    return { from: parent, to: idx };
  }).filter(Boolean);

  const edgeSvg = edges.map(e => {
    const fn = nodes[e.from], tn = nodes[e.to];
    return `<line x1="${fn.x}" y1="${fn.y}" x2="${tn.x}" y2="${tn.y}" stroke="#374151" stroke-width="2"/>`;
  }).join('');

  const nodeSvg = nodes.map(n => {
    const colors = { default: { bg: '#1e1e2e', border: '#374151', text: '#9ca3af' }, active: { bg: 'rgba(99,102,241,0.4)', border: '#6366f1', text: '#e0e7ff' }, swap: { bg: 'rgba(239,68,68,0.3)', border: '#ef4444', text: '#fca5a5' } };
    const c = colors[n.state] || colors.default;
    const glow = n.state !== 'default' ? `filter:drop-shadow(0 0 8px ${c.border});` : '';
    return `<g style="${glow}" transform="translate(${n.x},${n.y})">
      <circle r="24" fill="${c.bg}" stroke="${c.border}" stroke-width="2"/>
      <text y="5" text-anchor="middle" fill="${c.text}" font-family="'JetBrains Mono',monospace" font-size="13" font-weight="700">${n.val}</text>
    </g>`;
  }).join('');

  const maxH = Math.max(...nodes.map(n => n.y)) + 80;
  canvas.innerHTML = `
    <div>
      <svg width="100%" height="${maxH}" style="overflow:visible;">${edgeSvg}${nodeSvg}</svg>
      <div style="display:flex;align-items:center;gap:6px;padding:6px 12px;flex-wrap:wrap;">
        <span style="font-size:11px;color:#6b7280;font-family:monospace;">Heap Array:</span>
        ${heap.map((v, i) => `<span style="background:${i===state.activeIdx?'rgba(99,102,241,0.25)':i===state.swapIdx?'rgba(239,68,68,0.2)':'rgba(0,0,0,0.4)'};border:1px solid ${i===state.activeIdx?'#6366f1':i===state.swapIdx?'#ef4444':'#374151'};color:${i===state.activeIdx?'#a5b4fc':i===state.swapIdx?'#fca5a5':'#6b7280'};padding:3px 8px;border-radius:4px;font-family:monospace;font-size:12px;">${v}</span>`).join('')}
      </div>
    </div>`;
}

function renderLinkedList(state, canvas) {
  if (!state.llNodes) return;
  const nodes = state.llNodes;
  const ptrs = state.llPointers || {};
  const H = 120;
  const nodeW = 90, nodeH = 50, arrowGap = 40;
  const totalW = nodes.length * (nodeW + arrowGap);

  const stateColors = { default: { bg: '#1e1e2e', border: '#374151', text: '#9ca3af' }, active: { bg: 'rgba(99,102,241,0.4)', border: '#6366f1', text: '#e0e7ff' }, highlight: { bg: 'rgba(245,158,11,0.25)', border: '#f59e0b', text: '#fbbf24' }, visited: { bg: 'rgba(16,185,129,0.2)', border: '#10b981', text: '#6ee7b7' }, discovered: { bg: 'rgba(236,72,153,0.2)', border: '#ec4899', text: '#f9a8d4' } };

  const nodesSvg = nodes.map((n, i) => {
    const c = stateColors[n.state || 'default'];
    const x = i * (nodeW + arrowGap);
    const glow = n.state !== 'default' ? `filter:drop-shadow(0 0 8px ${c.border});` : '';

    // Arrow to next
    const arrow = n.next !== null ? `
      <line x1="${x + nodeW}" y1="${H/2}" x2="${x + nodeW + arrowGap - 4}" y2="${H/2}" stroke="#6b7280" stroke-width="2" marker-end="url(#arrowhead)"/>` : '';

    return `
      <g style="${glow}">
        <rect x="${x}" y="${H/2 - nodeH/2}" width="${nodeW}" height="${nodeH}" rx="8" fill="${c.bg}" stroke="${c.border}" stroke-width="2"/>
        <text x="${x + nodeW/2}" y="${H/2 + 5}" text-anchor="middle" fill="${c.text}" font-family="'JetBrains Mono',monospace" font-size="14" font-weight="700">${n.val}</text>
        ${arrow}
      </g>`;
  }).join('');

  // NULL terminator
  const lastX = nodes.length * (nodeW + arrowGap);

  canvas.innerHTML = `<div style="overflow-x:auto;padding:16px 8px;">
    <svg width="${Math.max(totalW + 60, 400)}" height="${H + 60}" style="overflow:visible;">
      <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280"/>
        </marker>
      </defs>
      ${nodesSvg}
      <text x="${lastX}" y="${H/2 + 5}" fill="#4b5563" font-family="monospace" font-size="12">NULL</text>
    </svg>
  </div>`;
}

// Determine which renderer to use based on state shape
function renderState(state, canvas) {
  if (!canvas || !state) return;
  canvas.innerHTML = '';

  if (state.dpTable) { renderDP(state, canvas); return; }
  if (state.treeNodes) { renderTree(state, canvas); return; }
  if (state.graphNodes) { renderGraph(state, canvas); return; }
  if (state.stackItems !== undefined) { renderStack(state, canvas); return; }
  if (state.llNodes) { renderLinkedList(state, canvas); return; }
  if (state.heap !== undefined) { renderHeap(state, canvas); return; }
  if (state.bars) { renderBars(state, canvas); return; }
  if (state.array) { renderArray(state, canvas); return; }
}

// ============================================================
// EXPORTS
// ============================================================
window.DSA = {
  CATALOG: DSA_CATALOG,
  PSEUDO_CODE,
  CODE_SNIPPETS,
  INTERVIEW_QUESTIONS,
  loadAlgorithm,
  renderState,
};
