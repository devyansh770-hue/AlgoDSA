/**
 * AlgoDSA Interactive DSA Visual Lab — Centralized Algorithm Registry & Engine v4.0
 * Architecture: Every algorithm is a completely independent, self-contained AlgorithmConfig object.
 *
 * AlgorithmConfig Shape:
 * {
 *   id, slug, category, title, subtitle, difficulty, description, intuition,
 *   when_to_use, when_not_to_use, pseudo_code, variables, complexities,
 *   code_examples: { python, cpp, java, javascript, go, rust },
 *   notes, interview_questions, common_mistakes,
 *   getAnimationSteps(customInput)
 * }
 */

const AlgorithmRegistry = {};

function registerAlgo(config) {
  AlgorithmRegistry[config.id] = config;
}

// ------------------------------------------------------------
// 1. SLIDING WINDOW (MAX SUM K=3)
// ------------------------------------------------------------
registerAlgo({
  id: 'sliding_window',
  slug: 'sliding-window-max-sum',
  category: 'arrays',
  title: 'Sliding Window',
  subtitle: 'Maximum Sum Subarray of Fixed Size K=3',
  difficulty: 'Easy',
  description: 'Maintain a contiguous window of size K and slide it across the array to find maximum sum in O(N) time.',
  intuition: 'Instead of re-summing K elements at every index (O(N*K)), subtract the element leaving the window and add the element entering the window in O(1).',
  when_to_use: 'Problems asking for min/max/count of contiguous subarrays or substrings of fixed or dynamic size.',
  when_not_to_use: 'Non-contiguous combinations, or arrays with negative numbers when using variable window conditions.',
  pseudo_code: [
    'window_sum = sum(arr[0..K-1])',
    'max_sum = window_sum',
    'for i from K to len(arr)-1:',
    '    window_sum += arr[i]',
    '    window_sum -= arr[i-K]',
    '    max_sum = max(max_sum, window_sum)',
    'return max_sum'
  ],
  variables: ['window_sum', 'max_sum', 'left', 'right', 'K'],
  complexities: { time: 'O(N)', space: 'O(1)' },
  code_examples: {
    python: `def max_sum_subarray(arr, k):\n    window_sum = sum(arr[:k])\n    max_sum = window_sum\n    for i in range(k, len(arr)):\n        window_sum += arr[i] - arr[i-k]\n        max_sum = max(max_sum, window_sum)\n    return max_sum`,
    cpp: `int maxSumSubarray(vector<int>& arr, int k) {\n    int windowSum = 0;\n    for (int i = 0; i < k; i++) windowSum += arr[i];\n    int maxSum = windowSum;\n    for (int i = k; i < arr.size(); i++) {\n        windowSum += arr[i] - arr[i-k];\n        maxSum = max(maxSum, windowSum);\n    }\n    return maxSum;\n}`,
    java: `public int maxSumSubarray(int[] arr, int k) {\n    int windowSum = 0;\n    for (int i = 0; i < k; i++) windowSum += arr[i];\n    int maxSum = windowSum;\n    for (int i = k; i < arr.length; i++) {\n        windowSum += arr[i] - arr[i-k];\n        maxSum = Math.max(maxSum, windowSum);\n    }\n    return maxSum;\n}`,
    javascript: `function maxSumSubarray(arr, k) {\n    let windowSum = arr.slice(0, k).reduce((a, b) => a + b, 0);\n    let maxSum = windowSum;\n    for (let i = k; i < arr.length; i++) {\n        windowSum += arr[i] - arr[i - k];\n        maxSum = Math.max(maxSum, windowSum);\n    }\n    return maxSum;\n}`,
    go: `func maxSumSubarray(arr []int, k int) int {\n    windowSum := 0\n    for i := 0; i < k; i++ { windowSum += arr[i] }\n    maxSum := windowSum\n    for i := k; i < len(arr); i++ {\n        windowSum += arr[i] - arr[i-k]\n        if windowSum > maxSum { maxSum = windowSum }\n    }\n    return maxSum\n}`,
    rust: `fn max_sum_subarray(arr: &[i32], k: usize) -> i32 {\n    let mut window_sum: i32 = arr[..k].iter().sum();\n    let mut max_sum = window_sum;\n    for i in k..arr.len() {\n        window_sum += arr[i] - arr[i - k];\n        max_sum = max_sum.max(window_sum);\n    }\n    max_sum\n}`
  },
  notes: 'Always ensure K <= N before running loop. Indices: left = i - K + 1, right = i.',
  common_mistakes: [
    'Off-by-one errors when subtracting arr[i-k]',
    'Forgetting to initialize max_sum to the first window sum',
    'Not handling cases where array length < K'
  ],
  interview_questions: [
    { q: 'Maximum Average Subarray I', difficulty: 'easy', companies: ['Google', 'Amazon'], lc: '643' },
    { q: 'Longest Substring Without Repeating Characters', difficulty: 'medium', companies: ['Amazon', 'Microsoft'], lc: '3' },
    { q: 'Minimum Window Substring', difficulty: 'hard', companies: ['Google', 'Meta'], lc: '76' }
  ],
  getAnimationSteps: function(arr = [2, 1, 5, 1, 3, 2], k = 3) {
    const states = [];
    let sum = 0, maxSum = 0;

    for (let i = 0; i < k; i++) sum += arr[i];
    maxSum = sum;

    states.push({
      array: [...arr], highlighted: Array.from({length: k}, (_, i) => i),
      active: [k-1], eliminated: [], pointers: {left: 0, right: k-1},
      explanation: `Step 1: Build initial window [0..${k-1}]. Window Sum = ${sum}. Max Sum initialized to ${maxSum}.`,
      currentPseudoLine: 0,
      memoryState: { window_sum: sum, max_sum: maxSum, left: 0, right: k-1, K: k },
      complexityNote: 'O(K) to build initial window', phaseLabel: 'INIT'
    });

    for (let i = k; i < arr.length; i++) {
      const entering = arr[i], exiting = arr[i-k];
      sum += entering - exiting;
      maxSum = Math.max(maxSum, sum);
      const left = i - k + 1, right = i;

      states.push({
        array: [...arr], highlighted: Array.from({length: k}, (_, j) => left + j),
        active: [right], eliminated: [], pointers: {left, right},
        explanation: `Slide window to [${left}..${right}]: Add arr[${right}] (${entering}), Subtract arr[${i-k}] (${exiting}). New Sum = ${sum}. ${sum === maxSum ? '🎯 New Max!' : `Max stays ${maxSum}`}`,
        currentPseudoLine: sum >= maxSum ? 5 : 4,
        memoryState: { window_sum: sum, max_sum: maxSum, left, right, K: k },
        complexityNote: 'O(1) slide step', phaseLabel: 'SLIDE'
      });
    }

    states.push({
      array: [...arr], highlighted: [], active: [], eliminated: [], pointers: {},
      explanation: `✅ Execution Finished! Maximum subarray sum of size K=${k} is ${maxSum}.`,
      currentPseudoLine: 6,
      memoryState: { result: maxSum, window_sum: sum, max_sum: maxSum },
      complexityNote: 'Total: O(N) time, O(1) space', phaseLabel: 'DONE'
    });

    return states;
  }
});

// ------------------------------------------------------------
// 2. KADANE'S ALGORITHM
// ------------------------------------------------------------
registerAlgo({
  id: 'kadane',
  slug: 'kadanes-algorithm',
  category: 'arrays',
  title: "Kadane's Algorithm",
  subtitle: 'Maximum Subarray Sum in Dynamic Range',
  difficulty: 'Medium',
  description: "Find the contiguous subarray with the largest sum in a single pass O(N) using dynamic programming / greedy choice.",
  intuition: "At each index i, decide: Should I extend the existing sum (curr_sum + arr[i]), or start fresh from arr[i]? If curr_sum drops below 0, it will only hurt future subarrays, so reset it.",
  when_to_use: "Finding maximum contiguous subarray sum with positive and negative numbers.",
  when_not_to_use: "Non-contiguous elements or circular arrays (requires modified 2-pass Kadane).",
  pseudo_code: [
    'curr_sum = arr[0]',
    'max_sum = arr[0]',
    'for i from 1 to len(arr)-1:',
    '    curr_sum = max(arr[i], curr_sum + arr[i])',
    '    max_sum = max(max_sum, curr_sum)',
    'return max_sum'
  ],
  variables: ['curr_sum', 'max_sum', 'i', 'arr[i]'],
  complexities: { time: 'O(N)', space: 'O(1)' },
  code_examples: {
    python: `def max_sub_array(nums):\n    curr_sum = max_sum = nums[0]\n    for x in nums[1:]:\n        curr_sum = max(x, curr_sum + x)\n        max_sum = max(max_sum, curr_sum)\n    return max_sum`,
    cpp: `int maxSubArray(vector<int>& nums) {\n    int currSum = nums[0], maxSum = nums[0];\n    for (size_t i = 1; i < nums.size(); i++) {\n        currSum = max(nums[i], currSum + nums[i]);\n        maxSum = max(maxSum, currSum);\n    }\n    return maxSum;\n}`,
    java: `public int maxSubArray(int[] nums) {\n    int currSum = nums[0], maxSum = nums[0];\n    for (int i = 1; i < nums.length; i++) {\n        currSum = Math.max(nums[i], currSum + nums[i]);\n        maxSum = Math.max(maxSum, currSum);\n    }\n    return maxSum;\n}`,
    javascript: `function maxSubArray(nums) {\n    let currSum = nums[0], maxSum = nums[0];\n    for (let i = 1; i < nums.length; i++) {\n        currSum = Math.max(nums[i], currSum + nums[i]);\n        maxSum = Math.max(maxSum, currSum);\n    }\n    return maxSum;\n}`,
    go: `func maxSubArray(nums []int) int {\n    currSum, maxSum := nums[0], nums[0]\n    for i := 1; i < len(nums); i++ {\n        if nums[i] > currSum+nums[i] { currSum = nums[i] } else { currSum += nums[i] }\n        if currSum > maxSum { maxSum = currSum }\n    }\n    return maxSum\n}`,
    rust: `fn max_sub_array(nums: &[i32]) -> i32 {\n    let mut curr_sum = nums[0];\n    let mut max_sum = nums[0];\n    for &x in &nums[1..] {\n        curr_sum = x.max(curr_sum + x);\n        max_sum = max_sum.max(curr_sum);\n    }\n    max_sum\n}`
  },
  notes: "Kadane's algorithm works even if all numbers are negative — it will return the least negative single number.",
  common_mistakes: [
    'Initializing curr_sum or max_sum to 0 instead of arr[0] (fails when all elements are negative)',
    'Forgetting that empty subarrays are usually disallowed'
  ],
  interview_questions: [
    { q: 'Maximum Subarray', difficulty: 'medium', companies: ['Amazon', 'Apple', 'Microsoft'], lc: '53' },
    { q: 'Maximum Product Subarray', difficulty: 'medium', companies: ['Google', 'LinkedIn'], lc: '152' },
    { q: 'Maximum Sum Circular Subarray', difficulty: 'medium', companies: ['Facebook'], lc: '918' }
  ],
  getAnimationSteps: function(arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]) {
    const states = [];
    let currSum = arr[0], maxSum = arr[0];

    states.push({
      array: [...arr], highlighted: [0], active: [0], eliminated: [],
      pointers: { curr: 0 },
      explanation: `Step 1: Initialize curr_sum = arr[0] = ${arr[0]}, max_sum = ${arr[0]}.`,
      currentPseudoLine: 0,
      memoryState: { curr_sum: currSum, max_sum: maxSum, i: 0, 'arr[i]': arr[0] },
      complexityNote: "Kadane's Initialization — O(1)", phaseLabel: 'INIT'
    });

    for (let i = 1; i < arr.length; i++) {
      const prevCurr = currSum;
      currSum = Math.max(arr[i], currSum + arr[i]);
      maxSum = Math.max(maxSum, currSum);
      const isReset = currSum === arr[i] && arr[i] > prevCurr + arr[i];

      states.push({
        array: [...arr], highlighted: currSum > 0 ? [i] : [],
        active: [i], eliminated: [], pointers: { curr: i },
        explanation: `i=${i} (val=${arr[i]}): curr_sum = max(${arr[i]}, ${prevCurr}+${arr[i]}) = ${currSum}. ${isReset ? '🔄 Reset window to curr element!' : '➕ Extended window!'} max_sum = ${maxSum}`,
        currentPseudoLine: 3,
        memoryState: { curr_sum: currSum, max_sum: maxSum, i: i, 'arr[i]': arr[i] },
        complexityNote: 'O(1) decision per element', phaseLabel: isReset ? 'RESET' : 'EXTEND'
      });
    }

    states.push({
      array: [...arr], highlighted: [], active: [], eliminated: [], pointers: {},
      explanation: `✅ Done! Maximum contiguous subarray sum is ${maxSum}.`,
      currentPseudoLine: 5,
      memoryState: { result: maxSum, max_sum: maxSum },
      complexityNote: 'Total: O(N) time, O(1) space', phaseLabel: 'DONE'
    });

    return states;
  }
});

// ------------------------------------------------------------
// 3. PREFIX SUM
// ------------------------------------------------------------
registerAlgo({
  id: 'prefix_sum',
  slug: 'prefix-sum',
  category: 'arrays',
  title: 'Prefix Sum',
  subtitle: 'Cumulative Precomputation for O(1) Range Queries',
  difficulty: 'Easy',
  description: 'Precompute an array where prefix[i] stores the sum of all elements from index 0 to i-1. Any range sum [L, R] is then calculated in O(1) via prefix[R+1] - prefix[L].',
  intuition: 'Range Sum(L..R) = Sum(0..R) - Sum(0..L-1). By storing Sum(0..i) ahead of time, range queries drop from O(N) to O(1).',
  when_to_use: 'Multiple static range sum queries on an array.',
  when_not_to_use: 'Dynamic arrays with frequent updates (use Segment Tree or Fenwick Tree instead for O(log N) updates).',
  pseudo_code: [
    'prefix = [0] * (N + 1)',
    'for i from 0 to N-1:',
    '    prefix[i+1] = prefix[i] + arr[i]',
    '// Range sum query [L..R]:',
    'return prefix[R+1] - prefix[L]'
  ],
  variables: ['prefix[i]', 'arr[i]', 'L', 'R', 'range_sum'],
  complexities: { time: 'O(N) build, O(1) query', space: 'O(N)' },
  code_examples: {
    python: `class NumArray:\n    def __init__(self, nums):\n        self.prefix = [0]\n        for x in nums:\n            self.prefix.append(self.prefix[-1] + x)\n    def sumRange(self, left, right):\n        return self.prefix[right + 1] - self.prefix[left]`,
    cpp: `class NumArray {\n    vector<int> prefix;\npublic:\n    NumArray(vector<int>& nums) {\n        prefix.assign(nums.size() + 1, 0);\n        for (size_t i = 0; i < nums.size(); i++) prefix[i+1] = prefix[i] + nums[i];\n    }\n    int sumRange(int left, int right) {\n        return prefix[right + 1] - prefix[left];\n    }\n};`,
    java: `class NumArray {\n    private int[] prefix;\n    public NumArray(int[] nums) {\n        prefix = new int[nums.length + 1];\n        for (int i = 0; i < nums.length; i++) prefix[i+1] = prefix[i] + nums[i];\n    }\n    public int sumRange(int left, int right) {\n        return prefix[right + 1] - prefix[left];\n    }\n}`,
    javascript: `class NumArray {\n    constructor(nums) {\n        this.prefix = [0];\n        for (let x of nums) this.prefix.push(this.prefix[this.prefix.length - 1] + x);\n    }\n    sumRange(left, right) {\n        return this.prefix[right + 1] - this.prefix[left];\n    }\n}`,
    go: `type NumArray struct { prefix []int }\nfunc Constructor(nums []int) NumArray {\n    p := make([]int, len(nums)+1)\n    for i, v := range nums { p[i+1] = p[i] + v }\n    return NumArray{prefix: p}\n}\nfunc (this *NumArray) SumRange(left int, right int) int {\n    return this.prefix[right+1] - this.prefix[left]\n}`,
    rust: `struct NumArray { prefix: Vec<i32> }\nimpl NumArray {\n    fn new(nums: Vec<i32>) -> Self {\n        let mut prefix = vec![0; nums.len() + 1];\n        for i in 0..nums.len() { prefix[i+1] = prefix[i] + nums[i]; }\n        Self { prefix }\n    }\n    fn sum_range(&self, left: usize, right: usize) -> i32 {\n        self.prefix[right + 1] - self.prefix[left]\n    }\n}`
  },
  notes: '1-indexed prefix array avoids boundary checks for left=0.',
  common_mistakes: [
    '0-indexed vs 1-indexed prefix array confusion',
    'Off-by-one error: writing prefix[right] - prefix[left-1] instead of prefix[right+1] - prefix[left]'
  ],
  interview_questions: [
    { q: 'Range Sum Query - Immutable', difficulty: 'easy', companies: ['Facebook', 'Amazon'], lc: '303' },
    { q: 'Subarray Sum Equals K', difficulty: 'medium', companies: ['Google', 'Meta'], lc: '560' },
    { q: 'Continuous Subarray Sum', difficulty: 'medium', companies: ['Facebook'], lc: '523' }
  ],
  getAnimationSteps: function(arr = [3, 1, 4, 1, 5, 9, 2, 6]) {
    const states = [];
    const prefix = [0];

    states.push({
      array: [...arr], prefix: [...prefix], highlighted: [], active: [],
      explanation: 'Step 1: Initialize 1-indexed prefix array with prefix[0] = 0.',
      currentPseudoLine: 0,
      memoryState: { arr: arr.join(', '), prefix: '0' },
      complexityNote: 'O(N) build phase', phaseLabel: 'INIT'
    });

    for (let i = 0; i < arr.length; i++) {
      prefix.push(prefix[i] + arr[i]);
      states.push({
        array: [...arr], prefix: [...prefix], highlighted: [i], active: [i],
        explanation: `prefix[${i+1}] = prefix[${i}] (${prefix[i]}) + arr[${i}] (${arr[i]}) = ${prefix[i+1]}.`,
        currentPseudoLine: 2,
        memoryState: { i, 'arr[i]': arr[i], 'prefix[i+1]': prefix[i+1] },
        complexityNote: `Building prefix step ${i+1}/${arr.length}`, phaseLabel: 'BUILD'
      });
    }

    const L = 2, R = 5;
    const querySum = prefix[R+1] - prefix[L];
    states.push({
      array: [...arr], prefix: [...prefix],
      highlighted: Array.from({length: R - L + 1}, (_, i) => L + i),
      active: [], pointers: { L, R },
      explanation: `🎯 Query Range [${L}..${R}]: Sum = prefix[${R+1}] (${prefix[R+1]}) - prefix[${L}] (${prefix[L]}) = ${querySum}. Executed in O(1) time!`,
      currentPseudoLine: 4,
      memoryState: { L, R, 'prefix[R+1]': prefix[R+1], 'prefix[L]': prefix[L], range_sum: querySum },
      complexityNote: 'O(1) range sum query complete!', phaseLabel: 'QUERY'
    });

    return states;
  }
});

// ------------------------------------------------------------
// 5. BINARY SEARCH (CLASSIC)
// ------------------------------------------------------------
registerAlgo({
  id: 'binary_search_classic',
  slug: 'binary-search',
  category: 'binary_search',
  title: 'Binary Search',
  subtitle: 'Logarithmic O(log N) Search in Sorted Array',
  difficulty: 'Easy',
  description: 'Repeatedly divide the search space in half by comparing the middle element with the target value.',
  intuition: 'If the array is sorted, comparing target with mid tells you with 100% certainty which half of the array target MUST reside in.',
  when_to_use: 'Sorted arrays, or monotonically increasing/decreasing functions (search space optimization).',
  when_not_to_use: 'Unsorted arrays, or linked lists (where random access O(1) mid is impossible).',
  pseudo_code: [
    'left = 0, right = len(arr) - 1',
    'while left <= right:',
    '    mid = left + (right - left) // 2',
    '    if arr[mid] == target: return mid',
    '    else if arr[mid] < target: left = mid + 1',
    '    else: right = mid - 1',
    'return -1  // target not found'
  ],
  variables: ['left', 'right', 'mid', 'arr[mid]', 'target'],
  complexities: { time: 'O(log N)', space: 'O(1)' },
  code_examples: {
    python: `def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1`,
    cpp: `int binarySearch(vector<int>& arr, int target) {\n    int left = 0, right = arr.size() - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}`,
    java: `public int binarySearch(int[] arr, int target) {\n    int left = 0, right = arr.length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}`,
    javascript: `function binarySearch(arr, target) {\n    let left = 0, right = arr.length - 1;\n    while (left <= right) {\n        const mid = Math.floor((left + right) / 2);\n        if (arr[mid] === target) return mid;\n        else if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}`,
    go: `func binarySearch(arr []int, target int) int {\n    left, right := 0, len(arr)-1\n    for left <= right {\n        mid := left + (right-left)/2\n        if arr[mid] == target { return mid }\n        if arr[mid] < target { left = mid + 1 } else { right = mid - 1 }\n    }\n    return -1\n}`,
    rust: `fn binary_search(arr: &[i32], target: i32) -> i32 {\n    let (mut left, mut right) = (0i32, arr.len() as i32 - 1);\n    while left <= right {\n        let mid = left + (right - left) / 2;\n        if arr[mid as usize] == target { return mid; }\n        if arr[mid as usize] < target { left = mid + 1; } else { right = mid - 1; }\n    }\n    -1\n}`
  },
  notes: 'Avoid integer overflow when calculating mid: use mid = left + (right - left) / 2 instead of (left + right) / 2.',
  common_mistakes: [
    'Using left < right instead of left <= right in while condition',
    'Integer overflow in (left + right) / 2',
    'Updating left = mid or right = mid instead of mid + 1 / mid - 1 (infinite loops)'
  ],
  interview_questions: [
    { q: 'Binary Search', difficulty: 'easy', companies: ['All FAANG'], lc: '704' },
    { q: 'Search in Rotated Sorted Array', difficulty: 'medium', companies: ['Amazon', 'LinkedIn'], lc: '33' },
    { q: 'Find First and Last Position in Sorted Array', difficulty: 'medium', companies: ['Google', 'Meta'], lc: '34' }
  ],
  getAnimationSteps: function(arr = [1, 3, 5, 7, 9, 11, 13, 17, 21, 25], target = 11) {
    const states = [];
    let left = 0, right = arr.length - 1;
    let comparisons = 0;

    states.push({
      array: [...arr], highlighted: [], active: [], eliminated: [],
      pointers: { left, right },
      explanation: `Step 1: Set left=0, right=${arr.length-1}. Target=${target}. Range length=${arr.length}.`,
      currentPseudoLine: 0,
      memoryState: { left, right, mid: '-', 'arr[mid]': '-', target, comparisons: 0 },
      complexityNote: 'O(log N) — Search space length 10', phaseLabel: 'INIT'
    });

    while (left <= right) {
      const mid = Math.floor((left + right) / 2);
      comparisons++;

      if (arr[mid] === target) {
        states.push({
          array: [...arr], highlighted: [mid], active: [mid],
          eliminated: Array.from({length: arr.length}, (_, i) => i).filter(i => i < left || i > right).filter(i => i !== mid),
          pointers: { left, right, mid },
          explanation: `🎯 arr[mid=${mid}] = ${arr[mid]} matches Target ${target}! Found in ${comparisons} comparison(s).`,
          currentPseudoLine: 3,
          memoryState: { left, right, mid, 'arr[mid]': arr[mid], target, comparisons, status: 'FOUND!' },
          complexityNote: `Found in ${comparisons} steps!`, phaseLabel: 'MATCH!'
        });
        break;
      } else if (arr[mid] < target) {
        states.push({
          array: [...arr], highlighted: [mid], active: [mid],
          eliminated: Array.from({length: arr.length}, (_, i) => i).filter(i => i < left || i > right || (i >= left && i <= mid)),
          pointers: { left, right, mid },
          explanation: `arr[mid=${mid}] = ${arr[mid]} < Target ${target}. Eliminate left half [${left}..${mid}]. Move left = mid + 1 = ${mid+1}.`,
          currentPseudoLine: 4,
          memoryState: { left: mid + 1, right, mid, 'arr[mid]': arr[mid], target, comparisons },
          complexityNote: `Eliminated ${mid - left + 1} elements`, phaseLabel: 'MOVE RIGHT'
        });
        left = mid + 1;
      } else {
        states.push({
          array: [...arr], highlighted: [mid], active: [mid],
          eliminated: Array.from({length: arr.length}, (_, i) => i).filter(i => i < left || i > right || (i >= mid && i <= right)),
          pointers: { left, right, mid },
          explanation: `arr[mid=${mid}] = ${arr[mid]} > Target ${target}. Eliminate right half [${mid}..${right}]. Move right = mid - 1 = ${mid-1}.`,
          currentPseudoLine: 5,
          memoryState: { left, right: mid - 1, mid, 'arr[mid]': arr[mid], target, comparisons },
          complexityNote: `Eliminated ${right - mid + 1} elements`, phaseLabel: 'MOVE LEFT'
        });
        right = mid - 1;
      }
    }

    return states;
  }
});

// Helper getter function
function getAlgorithmConfig(algoId) {
  return AlgorithmRegistry[algoId] || AlgorithmRegistry['sliding_window'];
}

// Catalog categories list
function getCatalog() {
  return [
    {
      id: 'arrays', label: 'Arrays', icon: '🔢',
      algorithms: [
        { id: 'sliding_window', label: 'Sliding Window (Max Sum K=3)' },
        { id: 'kadane', label: "Kadane's Algorithm" },
        { id: 'prefix_sum', label: 'Prefix Sum Range Query' }
      ]
    },
    {
      id: 'binary_search', label: 'Binary Search', icon: '🔍',
      algorithms: [
        { id: 'binary_search_classic', label: 'Classic Binary Search' }
      ]
    },
    {
      id: 'sorting', label: 'Sorting', icon: '📊',
      algorithms: [
        { id: 'bubble_sort', label: 'Bubble Sort' }
      ]
    }
  ];
}

// Global visualizer API
window.DSA = {
  Registry: AlgorithmRegistry,
  getAlgorithmConfig,
  registerAlgo,
  getCatalog,
  renderState: function(state, canvas) {
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
};

// Render Functions
function renderArray(state, canvas) {
  if (!state.array) return;
  const arr = state.array;
  const elW = Math.min(64, Math.floor((canvas.clientWidth - 80) / arr.length) - 8);
  const elH = 64;
  const pointerColors = { left: '#6366f1', right: '#10b981', mid: '#f59e0b', curr: '#ec4899', L: '#6366f1', R: '#10b981' };

  const elems = arr.map((val, idx) => {
    const isHighlighted = (state.highlighted || []).includes(idx);
    const isActive = (state.active || []).includes(idx);
    const isEliminated = (state.eliminated || []).includes(idx);

    let bg = '#1e1e2e', border = '#374151', color = '#9ca3af', transform = '', shadow = '', extra = '';

    if (isActive) { bg='rgba(99,102,241,0.3)'; border='#6366f1'; color='#e0e7ff'; transform='translateY(-8px)'; shadow='0 8px 24px rgba(99,102,241,0.5)'; }
    else if (isHighlighted) { bg='rgba(99,102,241,0.15)'; border='#818cf8'; color='#c7d2fe'; transform='translateY(-4px)'; }
    else if (isEliminated) { bg='rgba(255,255,255,0.02)'; border='#374151'; color='#4b5563'; extra='opacity:0.35;'; }

    const ptrs = Object.entries(state.pointers || {}).filter(([, v]) => v === idx);
    const ptrMarkers = ptrs.map(([name]) =>
      `<div style="color:${pointerColors[name]||'#fff'};font-size:11px;font-weight:700;text-align:center;">${name.toUpperCase()} ▼</div>`
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

  if (state.prefix) {
    const pArr = state.prefix;
    const pElems = pArr.map((v, i) =>
      `<div style="padding:4px 10px;background:rgba(16,185,129,0.15);border:1px solid #10b981;color:#34d399;font-family:monospace;font-size:12px;border-radius:6px;">p[${i}] = ${v}</div>`
    ).join('');
    canvas.innerHTML += `<div style="margin-top:16px;display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap;">${pElems}</div>`;
  }
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

function renderTree(state, canvas) {}
function renderGraph(state, canvas) {}
function renderStack(state, canvas) {}
function renderDP(state, canvas) {}
function renderHeap(state, canvas) {}
function renderLinkedList(state, canvas) {}
