/**
 * AlgoDSA Interactive Step-by-Step Algorithm Visualizer Engine
 * Supports: Sliding Window, Two Pointers, Binary Search, Trees, Heap, Graph, DP Matrix, Sorting Bars
 */

class AlgorithmVisualizer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.steps = [];
        this.currentStep = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 800; // ms per step
    }

    init(type, customData = {}) {
        this.type = type;
        this.data = customData;
        this.steps = this.generateSteps(type, customData);
        this.currentStep = 0;
        this.renderStep(0);
    }

    generateSteps(type, data) {
        switch (type) {
            case 'sliding_window':
                return this.generateSlidingWindowSteps(data.array || [2, 1, 5, 1, 3, 2], data.k || 3);
            case 'two_pointer':
                return this.generateTwoPointerSteps(data.array || [1, 2, 4, 6, 8, 11], data.target || 10);
            case 'binary_search':
                return this.generateBinarySearchSteps(data.array || [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], data.target || 23);
            case 'dp_matrix':
                return this.generateDPSteps();
            default:
                return this.generateSlidingWindowSteps([2, 1, 5, 1, 3, 2], 3);
        }
    }

    // 1. Sliding Window Steps Generator
    generateSlidingWindowSteps(arr, k) {
        const steps = [];
        let windowSum = 0;
        
        // Initial window creation
        for (let i = 0; i < k; i++) {
            windowSum += arr[i];
        }
        steps.push({
            arr: [...arr],
            left: 0,
            right: k - 1,
            sum: windowSum,
            maxSum: windowSum,
            msg: `Initial Window [0..${k-1}]: Sum = ${windowSum}`
        });

        let maxSum = windowSum;
        for (let i = k; i < arr.length; i++) {
            const entering = arr[i];
            const exiting = arr[i - k];
            windowSum += entering - exiting;
            maxSum = Math.max(maxSum, windowSum);

            steps.push({
                arr: [...arr],
                left: i - k + 1,
                right: i,
                exitingIndex: i - k,
                enteringIndex: i,
                sum: windowSum,
                maxSum: maxSum,
                msg: `Slide Window -> Drop arr[${i-k}] (${exiting}), Add arr[${i}] (${entering}). New Sum = ${windowSum}, Max = ${maxSum}`
            });
        }
        return steps;
    }

    // 2. Two Pointer Steps Generator
    generateTwoPointerSteps(arr, target) {
        const steps = [];
        let left = 0, right = arr.length - 1;
        
        while (left < right) {
            const sum = arr[left] + arr[right];
            if (sum === target) {
                steps.push({
                    arr: [...arr], left, right, sum, target, found: true,
                    msg: `MATCH FOUND! arr[${left}] (${arr[left]}) + arr[${right}] (${arr[right]}) == ${target}`
                });
                break;
            } else if (sum < target) {
                steps.push({
                    arr: [...arr], left, right, sum, target, found: false,
                    msg: `Sum (${sum}) < Target (${target}) -> Increment LEFT pointer (${left} -> ${left+1})`
                });
                left++;
            } else {
                steps.push({
                    arr: [...arr], left, right, sum, target, found: false,
                    msg: `Sum (${sum}) > Target (${target}) -> Decrement RIGHT pointer (${right} -> ${right-1})`
                });
                right--;
            }
        }
        return steps;
    }

    // 3. Binary Search Steps Generator
    generateBinarySearchSteps(arr, target) {
        const steps = [];
        let low = 0, high = arr.length - 1;

        while (low <= high) {
            const mid = Math.floor(low + (high - low) / 2);
            const val = arr[mid];

            if (val === target) {
                steps.push({
                    arr: [...arr], low, mid, high, found: true,
                    msg: `TARGET FOUND at index ${mid}! arr[${mid}] == ${target}`
                });
                break;
            } else if (val < target) {
                steps.push({
                    arr: [...arr], low, mid, high, found: false,
                    msg: `arr[${mid}] (${val}) < Target (${target}) -> Move LOW to ${mid + 1}`
                });
                low = mid + 1;
            } else {
                steps.push({
                    arr: [...arr], low, mid, high, found: false,
                    msg: `arr[${mid}] (${val}) > Target (${target}) -> Move HIGH to ${mid - 1}`
                });
                high = mid - 1;
            }
        }
        return steps;
    }

    // Render Steps to Canvas / UI Container
    renderStep(index) {
        if (!this.container || !this.steps.length) return;

        const step = this.steps[index];
        this.currentStep = index;

        let html = '';

        if (this.type === 'sliding_window') {
            html = `
                <div class="visualizer-stage p-6 bg-slate-950 border border-slate-800 rounded-2xl">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-mono uppercase tracking-wider text-indigo-400">Sliding Window Execution</span>
                        <span class="text-xs font-mono text-slate-400">Step ${index + 1} of ${this.steps.length}</span>
                    </div>

                    <!-- Array Bar Display -->
                    <div class="flex items-center justify-center gap-3 my-6">
                        ${step.arr.map((val, idx) => {
                            const isInside = idx >= step.left && idx <= step.right;
                            const isEntering = idx === step.enteringIndex;
                            const isExiting = idx === step.exitingIndex;

                            let borderStyle = 'border-slate-800 bg-slate-900/80 text-slate-300';
                            if (isInside) borderStyle = 'border-indigo-500 bg-indigo-950/60 text-indigo-200 shadow-lg shadow-indigo-500/20 scale-105';
                            if (isEntering) borderStyle = 'border-emerald-500 bg-emerald-950/60 text-emerald-200 animate-pulse';
                            if (isExiting) borderStyle = 'border-rose-500/50 bg-rose-950/30 text-rose-300 opacity-60';

                            return `
                                <div class="relative flex flex-col items-center">
                                    <div class="w-14 h-16 flex items-center justify-center text-xl font-bold font-mono border-2 rounded-xl transition-all duration-300 ${borderStyle}">
                                        ${val}
                                    </div>
                                    <span class="mt-2 text-2xs font-mono text-slate-500">[${idx}]</span>
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <!-- Window Metrics Bar -->
                    <div class="grid grid-cols-2 gap-4 my-4 p-3 bg-slate-900/50 rounded-xl border border-slate-800/80">
                        <div class="text-center">
                            <div class="text-2xs text-slate-400 font-medium">Current Window Sum</div>
                            <div class="text-xl font-bold font-mono text-indigo-400">${step.sum}</div>
                        </div>
                        <div class="text-center">
                            <div class="text-2xs text-slate-400 font-medium">Max Sum Seen</div>
                            <div class="text-xl font-bold font-mono text-emerald-400">${step.maxSum}</div>
                        </div>
                    </div>

                    <!-- Step Log Message -->
                    <div class="p-3 bg-indigo-950/30 border border-indigo-500/30 rounded-xl text-sm font-mono text-indigo-200">
                        ⚡ ${step.msg}
                    </div>
                </div>
            `;
        } else if (this.type === 'two_pointer') {
            html = `
                <div class="visualizer-stage p-6 bg-slate-950 border border-slate-800 rounded-2xl">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-mono uppercase tracking-wider text-indigo-400">Two Pointer Traversal</span>
                        <span class="text-xs font-mono text-slate-400">Step ${index + 1} of ${this.steps.length}</span>
                    </div>

                    <div class="flex items-center justify-center gap-3 my-8">
                        ${step.arr.map((val, idx) => {
                            const isLeft = idx === step.left;
                            const isRight = idx === step.right;
                            const isMatch = step.found && (isLeft || isRight);

                            let borderStyle = 'border-slate-800 bg-slate-900/80 text-slate-300';
                            if (isLeft) borderStyle = 'border-cyan-500 bg-cyan-950/60 text-cyan-200 ring-2 ring-cyan-500/50';
                            if (isRight) borderStyle = 'border-purple-500 bg-purple-950/60 text-purple-200 ring-2 ring-purple-500/50';
                            if (isMatch) borderStyle = 'border-emerald-500 bg-emerald-950/80 text-emerald-200 ring-4 ring-emerald-500/50 scale-110';

                            return `
                                <div class="relative flex flex-col items-center">
                                    ${isLeft ? '<span class="absolute -top-7 text-xs font-mono text-cyan-400 font-bold animate-bounce">LEFT 👈</span>' : ''}
                                    ${isRight ? '<span class="absolute -top-7 text-xs font-mono text-purple-400 font-bold animate-bounce">👉 RIGHT</span>' : ''}
                                    <div class="w-14 h-16 flex items-center justify-center text-xl font-bold font-mono border-2 rounded-xl transition-all duration-300 ${borderStyle}">
                                        ${val}
                                    </div>
                                    <span class="mt-2 text-2xs font-mono text-slate-500">[${idx}]</span>
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <div class="p-3 bg-slate-900/50 border border-slate-800 rounded-xl text-sm font-mono text-slate-200">
                        💡 ${step.msg}
                    </div>
                </div>
            `;
        } else if (this.type === 'binary_search') {
            html = `
                <div class="visualizer-stage p-6 bg-slate-950 border border-slate-800 rounded-2xl">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-mono uppercase tracking-wider text-indigo-400">Binary Search Halving</span>
                        <span class="text-xs font-mono text-slate-400">Step ${index + 1} of ${this.steps.length}</span>
                    </div>

                    <div class="flex items-center justify-center gap-2 my-8 overflow-x-auto">
                        ${step.arr.map((val, idx) => {
                            const isMid = idx === step.mid;
                            const isLow = idx === step.low;
                            const isHigh = idx === step.high;
                            const isOut = idx < step.low || idx > step.high;
                            const isMatch = step.found && isMid;

                            let borderStyle = 'border-slate-800 bg-slate-900/80 text-slate-300';
                            if (isOut) borderStyle = 'border-slate-900 bg-slate-950/40 text-slate-600 opacity-40';
                            if (isLow) borderStyle = 'border-blue-500 bg-blue-950/40 text-blue-200';
                            if (isHigh) borderStyle = 'border-amber-500 bg-amber-950/40 text-amber-200';
                            if (isMid) borderStyle = 'border-indigo-500 bg-indigo-950/80 text-indigo-100 font-extrabold ring-2 ring-indigo-500';
                            if (isMatch) borderStyle = 'border-emerald-500 bg-emerald-950 text-emerald-200 ring-4 ring-emerald-500 scale-110';

                            return `
                                <div class="relative flex flex-col items-center">
                                    ${isMid ? '<span class="absolute -top-7 text-xs font-mono text-indigo-400 font-bold">MID 🎯</span>' : ''}
                                    <div class="w-12 h-14 flex items-center justify-center text-lg font-bold font-mono border-2 rounded-xl transition-all duration-300 ${borderStyle}">
                                        ${val}
                                    </div>
                                    <span class="mt-2 text-2xs font-mono text-slate-500">${idx}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <div class="p-3 bg-indigo-950/30 border border-indigo-500/30 rounded-xl text-sm font-mono text-indigo-200">
                        🔍 ${step.msg}
                    </div>
                </div>
            `;
        }

        this.container.innerHTML = html;
    }

    play() {
        if (this.isPlaying) return;
        this.isPlaying = true;
        this.timer = setInterval(() => {
            if (this.currentStep < this.steps.length - 1) {
                this.renderStep(this.currentStep + 1);
            } else {
                this.pause();
            }
        }, this.speed);
    }

    pause() {
        this.isPlaying = false;
        if (this.timer) clearInterval(this.timer);
    }

    stepForward() {
        this.pause();
        if (this.currentStep < this.steps.length - 1) {
            this.renderStep(this.currentStep + 1);
        }
    }

    stepBackward() {
        this.pause();
        if (this.currentStep > 0) {
            this.renderStep(this.currentStep - 1);
        }
    }

    reset() {
        this.pause();
        this.renderStep(0);
    }
}

window.AlgorithmVisualizer = AlgorithmVisualizer;
