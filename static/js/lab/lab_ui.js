/**
 * AlgoDSA — Educational Visual Code Execution Lab Controller v5.0
 *
 * ARCHITECTURE:
 * - Visual Execute sends code to /api/trace/ (Django backend, sys.settrace)
 * - Backend returns JSON frames array (never freezes browser)
 * - Frontend iterates frames via requestAnimationFrame (never blocks UI thread)
 * - currentStep is NEVER null after init (defensive default object)
 */

// ── SAFE DEFAULT STEP (prevents ALL null reference errors in Alpine) ──────────
const EMPTY_STEP = {
    step: 0,
    line: 0,
    variables: {},
    callStack: [],
    explanation: '',
    complexity: { opCount: 0, comparisons: 0, swaps: 0, depth: 0 }
};

function visualLabController() {
    return {
        // ── State ──────────────────────────────────────────────────────────────
        selectedLanguage: 'python',
        selectedPreset:   'binary_search',
        customInput:      '',
        code:             '',
        monacoEditor:     null,
        deltaDecorations: [],

        // ── Playback ───────────────────────────────────────────────────────────
        renderers:        null,
        traceSteps:       [],
        currentStepIndex: 0,
        isPlaying:        false,
        isLoading:        false,
        playLoop:         null,
        lastFrameTime:    0,
        playbackSpeed:    1,

        // ── Inspector / Tabs ───────────────────────────────────────────────────
        activeTab:       'variables',
        currentStep:      { ...EMPTY_STEP },   // ← NEVER null
        edgeCaseReport:  [],
        aiReport:        null,

        // ── Preset Code Templates ──────────────────────────────────────────────
        presetTemplates: {
            python: {
                binary_search: `# Binary Search Example
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
result = binary_search(arr, target)`,
                bubble_sort: `# Bubble Sort Example
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
bubble_sort(numbers)`,
                two_pointer: `# Two Pointer - Pair Sum
def two_sum_sorted(arr, target):
    left = 0
    right = len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return [-1, -1]

arr = [1, 2, 4, 6, 8, 11, 15]
target = 10
res = two_sum_sorted(arr, target)`,
                recursion_fib: `# Fibonacci with Memoization
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

result = fib(8)`
            },
            javascript: {
                binary_search: `// JavaScript Binary Search
function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    while (left <= right) {
        let mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
const arr = [10, 20, 30, 40, 50, 60, 70];
binarySearch(arr, 50);`
            },
            cpp: {
                binary_search: `// C++ — backend tracing not yet supported\n// Please use Python 3 for live tracing.`
            },
            java: {
                binary_search: `// Java — backend tracing not yet supported\n// Please use Python 3 for live tracing.`
            }
        },

        // ── Init ───────────────────────────────────────────────────────────────
        init() {
            this.loadPresetCode();
            this.initMonaco();
            this.$nextTick(() => {
                this.renderers = new VisualLabRenderers('visualization-canvas');
                this.setupKeyboardShortcuts();
            });
        },

        loadPresetCode() {
            const presets = this.presetTemplates[this.selectedLanguage] || {};
            this.code = presets[this.selectedPreset] || presets['binary_search'] || '# Write your Python code here\n';
            if (this.monacoEditor) {
                this.monacoEditor.setValue(this.code);
            }
        },

        onLanguageChange() {
            const presets = this.presetTemplates[this.selectedLanguage] || {};
            const keys = Object.keys(presets);
            if (keys.length > 0) this.selectedPreset = keys[0];
            this.loadPresetCode();
            if (this.monacoEditor) {
                const langMap = { python: 'python', javascript: 'javascript', cpp: 'cpp', java: 'java' };
                monaco.editor.setModelLanguage(this.monacoEditor.getModel(), langMap[this.selectedLanguage] || 'python');
            }
        },

        // ── Monaco Editor ──────────────────────────────────────────────────────
        initMonaco() {
            if (typeof require === 'undefined') return;
            require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
            require(['vs/editor/editor.main'], () => {
                monaco.editor.defineTheme('algodsa-lab-dark', {
                    base: 'vs-dark',
                    inherit: true,
                    rules: [
                        { token: 'comment',  foreground: '6a737d', fontStyle: 'italic' },
                        { token: 'keyword',  foreground: '818cf8' },
                        { token: 'string',   foreground: '06b6d4' },
                        { token: 'number',   foreground: 'f59e0b' },
                        { token: 'type',     foreground: '10b981' }
                    ],
                    colors: {
                        'editor.background':               '#0d0d12',
                        'editor.foreground':               '#e2e8f0',
                        'editor.lineHighlightBackground':  '#1a1a26',
                        'editor.selectionBackground':      '#6366f140',
                        'editorCursor.foreground':         '#6366f1',
                        'editorLineNumber.foreground':     '#4a5568',
                        'editorLineNumber.activeForeground': '#94a3b8',
                    }
                });

                const container = document.getElementById('monaco-lab-editor');
                if (!container) return;

                this.monacoEditor = monaco.editor.create(container, {
                    value:               this.code,
                    language:            this.selectedLanguage === 'cpp'  ? 'cpp'
                                       : this.selectedLanguage === 'java' ? 'java'
                                       : this.selectedLanguage === 'javascript' ? 'javascript' : 'python',
                    theme:               'algodsa-lab-dark',
                    fontSize:            13,
                    fontFamily:          "'JetBrains Mono', monospace",
                    minimap:             { enabled: false },
                    scrollBeyondLastLine: false,
                    automaticLayout:     true,
                    lineNumbers:         'on',
                    padding:             { top: 12 }
                });

                this.monacoEditor.onDidChangeModelContent(() => {
                    this.code = this.monacoEditor.getValue();
                });
            });
        },

        // ── Visual Execute ─────────────────────────────────────────────────────
        // Fetches execution trace from Django backend (never runs code in browser)
        async executeVisualCode() {
            this.pausePlayback();
            this.isLoading        = true;
            this.traceSteps       = [];
            this.currentStepIndex = 0;
            this.currentStep      = { ...EMPTY_STEP };   // ← reset to safe default
            this.aiReport         = null;
            this.edgeCaseReport   = [];

            const currentCode = this.monacoEditor ? this.monacoEditor.getValue() : this.code;

            // Read CSRF token from Django cookie so the POST is not rejected
            const csrfToken = this._getCookie('csrftoken');

            try {
                const response = await fetch('/api/trace/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken':  csrfToken || ''
                    },
                    body: JSON.stringify({
                        code:     currentCode,
                        language: this.selectedLanguage,
                        preset:   this.selectedPreset
                    })
                });

                // If we got redirected to login, response is HTML — detect it
                const contentType = response.headers.get('content-type') || '';
                if (!contentType.includes('application/json')) {
                    throw new Error('Session expired — please refresh the page and log in again.');
                }

                const data = await response.json();

                if (data.error) {
                    // Show error gracefully inside the step explanation instead of alert
                    this.currentStep = {
                        ...EMPTY_STEP,
                        explanation: '❌ ' + data.error
                    };
                    this.isLoading = false;
                    return;
                }

                this.traceSteps = data.frames || [];

                this.aiReport = {
                    summary:             `Traced ${this.traceSteps.length} steps on the backend via sys.settrace.`,
                    timeComplexity:      'Depends on algorithm',
                    spaceComplexity:     'Depends on algorithm',
                    keyMistakesToAvoid:  ['Off-by-one errors', 'Infinite loops', 'Incorrect base cases for recursion']
                };

                if (this.traceSteps.length > 0) {
                    this.jumpToStep(0);
                } else {
                    this.currentStep = { ...EMPTY_STEP, explanation: 'Code executed with no traceable steps.' };
                }

            } catch (err) {
                this.currentStep = {
                    ...EMPTY_STEP,
                    explanation: '❌ Execution Failed: ' + err.message
                };
            } finally {
                this.isLoading = false;
            }
        },

        // ── Step Navigation ────────────────────────────────────────────────────
        jumpToStep(index) {
            if (this.traceSteps.length === 0) return;
            index = Math.max(0, Math.min(index, this.traceSteps.length - 1));

            this.currentStepIndex = index;

            // Merge frame with EMPTY_STEP to guarantee all keys always exist
            const raw = this.traceSteps[index] || {};
            this.currentStep = {
                ...EMPTY_STEP,
                ...raw,
                complexity: { ...EMPTY_STEP.complexity, ...(raw.complexity || {}) },
                variables:  raw.variables  || {},
                callStack:  raw.callStack  || []
            };

            // Highlight executing line in Monaco (backend returns .line, not .currentLine)
            this.highlightLineInEditor(this.currentStep.line);

            // Update visualization canvas (non-blocking, only swaps innerHTML once)
            if (this.renderers) {
                this.renderers.render(this.currentStep);
            }
        },

        stepForward() {
            if (this.currentStepIndex < this.traceSteps.length - 1) {
                this.jumpToStep(this.currentStepIndex + 1);
            } else {
                this.pausePlayback();
            }
        },

        stepBackward() {
            if (this.currentStepIndex > 0) {
                this.jumpToStep(this.currentStepIndex - 1);
            }
        },

        togglePlayPause() {
            if (this.isPlaying) {
                this.pausePlayback();
            } else {
                this.startPlayback();
            }
        },

        // ── Playback via requestAnimationFrame (never blocks UI thread) ─────────
        startPlayback() {
            if (this.traceSteps.length === 0) {
                this.executeVisualCode();
                return;
            }
            if (this.currentStepIndex >= this.traceSteps.length - 1) {
                this.currentStepIndex = 0;
            }
            this.isPlaying     = true;
            this.lastFrameTime = performance.now();
            this.playLoop      = requestAnimationFrame(this._playbackTick.bind(this));
        },

        // Called every animation frame — steps forward only when enough time has elapsed
        _playbackTick(timestamp) {
            if (!this.isPlaying) return;

            const delayMs = Math.round(900 / this.playbackSpeed);
            if (timestamp - this.lastFrameTime >= delayMs) {
                if (this.currentStepIndex < this.traceSteps.length - 1) {
                    this.stepForward();
                    this.lastFrameTime = timestamp;
                } else {
                    this.pausePlayback();
                    return;
                }
            }
            // Schedule next tick — not a recursive call; rAF is async
            this.playLoop = requestAnimationFrame(this._playbackTick.bind(this));
        },

        pausePlayback() {
            this.isPlaying = false;
            if (this.playLoop) {
                cancelAnimationFrame(this.playLoop);
                this.playLoop = null;
            }
        },

        setSpeed(speed) {
            this.playbackSpeed = speed;
            if (this.isPlaying) {
                this.pausePlayback();
                this.startPlayback();
            }
        },

        // ── Monaco Line Highlight ──────────────────────────────────────────────
        highlightLineInEditor(lineNum) {
            if (!this.monacoEditor || !lineNum || lineNum < 1) return;
            this.deltaDecorations = this.monacoEditor.deltaDecorations(
                this.deltaDecorations,
                [{
                    range: new monaco.Range(lineNum, 1, lineNum, 1),
                    options: {
                        isWholeLine:            true,
                        className:              'monaco-executing-line-bg',
                        glyphMarginClassName:   'monaco-executing-glyph'
                    }
                }]
            );
            this.monacoEditor.revealLineInCenter(lineNum);
        },

        // ── Keyboard Shortcuts ─────────────────────────────────────────────────
        setupKeyboardShortcuts() {
            window.addEventListener('keydown', (e) => {
                if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
                if (e.code === 'Space')       { e.preventDefault(); this.togglePlayPause(); }
                else if (e.code === 'ArrowRight') { e.preventDefault(); this.stepForward(); }
                else if (e.code === 'ArrowLeft')  { e.preventDefault(); this.stepBackward(); }
            });
        },

        // ── Export ────────────────────────────────────────────────────────────
        exportReport() {
            const jsonStr = JSON.stringify({
                code:       this.code,
                language:   this.selectedLanguage,
                totalSteps: this.traceSteps.length,
                trace:      this.traceSteps,
                aiSummary:  this.aiReport
            }, null, 2);

            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url  = URL.createObjectURL(blob);
            const a    = document.createElement('a');
            a.href     = url;
            a.download = `execution_trace_${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        },

        // ── Utility: Read a cookie by name ────────────────────────────────────
        _getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
            return null;
        }
    };
}

window.visualLabController = visualLabController;
