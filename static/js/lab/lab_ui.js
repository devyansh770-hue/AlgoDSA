/**
 * AI Visual Code Execution Lab — Alpine.js Controller
 * Coordinates Monaco Editor, Step Engine, Renderers, Timeline, Inspector, and AI Teacher.
 */

function visualLabController() {
    return {
        // State
        selectedLanguage: 'python',
        selectedPreset: 'binary_search',
        customInput: '',
        code: '',
        monacoEditor: null,
        deltaDecorations: [],

        // Execution Engine
        engine: null,
        renderers: null,
        traceSteps: [],
        currentStepIndex: 0, // 0-indexed internally
        isPlaying: false,
        playInterval: null,
        playbackSpeed: 1, // 0.25x, 0.5x, 1x, 2x, 4x

        // Inspector & UI Tabs
        activeTab: 'variables', // 'variables', 'breakdown', 'stack', 'edge_cases', 'ai_teacher'
        currentStep: null,
        edgeCaseReport: [],
        aiReport: null,

        // Lifecycle Init
        init() {
            this.engine = new CodeExecutionEngine();
            this.loadPresetCode();
            this.initMonaco();
            this.$nextTick(() => {
                this.renderers = new VisualLabRenderers('visualization-canvas');
            });
        },

        /**
         * Preset loader
         */
        loadPresetCode() {
            const presets = this.engine.presetTemplates[this.selectedLanguage] || {};
            this.code = presets[this.selectedPreset] || presets['binary_search'] || '# Write code here\n';
            if (this.monacoEditor) {
                this.monacoEditor.setValue(this.code);
            }
        },

        onLanguageChange() {
            const presets = this.engine.presetTemplates[this.selectedLanguage] || {};
            const keys = Object.keys(presets);
            if (keys.length > 0) {
                this.selectedPreset = keys[0];
            }
            this.loadPresetCode();
            if (this.monacoEditor) {
                const monacoLangMap = { python: 'python', javascript: 'javascript', cpp: 'cpp', java: 'java' };
                monaco.editor.setModelLanguage(this.monacoEditor.getModel(), monacoLangMap[this.selectedLanguage] || 'python');
            }
        },

        /**
         * Initialize Monaco Editor
         */
        initMonaco() {
            if (typeof require === 'undefined') return;
            require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
            require(['vs/editor/editor.main'], () => {
                monaco.editor.defineTheme('algodsa-lab-dark', {
                    base: 'vs-dark',
                    inherit: true,
                    rules: [
                        { token: 'comment', foreground: '6a737d', fontStyle: 'italic' },
                        { token: 'keyword', foreground: '818cf8' },
                        { token: 'string', foreground: '06b6d4' },
                        { token: 'number', foreground: 'f59e0b' },
                        { token: 'type', foreground: '10b981' }
                    ],
                    colors: {
                        'editor.background': '#0d0d12',
                        'editor.foreground': '#e2e8f0',
                        'editor.lineHighlightBackground': '#1a1a26',
                        'editor.selectionBackground': '#6366f140',
                        'editorCursor.foreground': '#6366f1',
                        'editorLineNumber.foreground': '#4a5568',
                        'editorLineNumber.activeForeground': '#94a3b8',
                    }
                });

                const container = document.getElementById('monaco-lab-editor');
                if (!container) return;

                this.monacoEditor = monaco.editor.create(container, {
                    value: this.code,
                    language: this.selectedLanguage === 'cpp' ? 'cpp' : (this.selectedLanguage === 'java' ? 'java' : (this.selectedLanguage === 'javascript' ? 'javascript' : 'python')),
                    theme: 'algodsa-lab-dark',
                    fontSize: 13,
                    fontFamily: "'JetBrains Mono', monospace",
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    lineNumbers: 'on',
                    padding: { top: 12 }
                });

                this.monacoEditor.onDidChangeModelContent(() => {
                    this.code = this.monacoEditor.getValue();
                });
            });
        },

        /**
         * Primary Action: Run Visual Execution
         */
        executeVisualCode() {
            this.pausePlayback();
            const currentCode = this.monacoEditor ? this.monacoEditor.getValue() : this.code;
            
            // Generate full trace
            this.traceSteps = this.engine.generateTrace(currentCode, this.selectedLanguage, this.customInput);
            this.edgeCaseReport = this.engine.analyzeEdgeCases(currentCode, this.selectedLanguage);
            this.aiReport = this.engine.generateAITeacherReport(currentCode, this.selectedLanguage, this.traceSteps);

            this.currentStepIndex = 0;
            this.jumpToStep(0);
        },

        /**
         * Timeline & Step Navigation Controls
         */
        jumpToStep(index) {
            if (this.traceSteps.length === 0) return;
            if (index < 0) index = 0;
            if (index >= this.traceSteps.length) index = this.traceSteps.length - 1;

            this.currentStepIndex = index;
            this.currentStep = this.traceSteps[index];

            // 1. Highlight line in Monaco Editor
            this.highlightLineInEditor(this.currentStep.line);

            // 2. Render Data Structure Visualization
            if (this.renderers) {
                this.renderers.render(this.currentStep);
            }

            // Refresh icons if lucide available
            this.$nextTick(() => {
                if (window.lucide) lucide.createIcons();
            });
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

        startPlayback() {
            if (this.traceSteps.length === 0) {
                this.executeVisualCode();
            }
            if (this.currentStepIndex >= this.traceSteps.length - 1) {
                this.currentStepIndex = 0;
            }
            this.isPlaying = true;
            const delayMs = Math.round(1000 / this.playbackSpeed);

            this.playInterval = setInterval(() => {
                if (this.currentStepIndex < this.traceSteps.length - 1) {
                    this.stepForward();
                } else {
                    this.pausePlayback();
                }
            }, delayMs);
        },

        pausePlayback() {
            this.isPlaying = false;
            if (this.playInterval) {
                clearInterval(this.playInterval);
                this.playInterval = null;
            }
        },

        setSpeed(speed) {
            this.playbackSpeed = speed;
            if (this.isPlaying) {
                this.pausePlayback();
                this.startPlayback();
            }
        },

        /**
         * Highlight executing line in Monaco
         */
        highlightLineInEditor(lineNum) {
            if (!this.monacoEditor) return;
            this.deltaDecorations = this.monacoEditor.deltaDecorations(this.deltaDecorations, [
                {
                    range: new monaco.Range(lineNum, 1, lineNum, 1),
                    options: {
                        isWholeLine: true,
                        className: 'monaco-executing-line-bg',
                        glyphMarginClassName: 'monaco-executing-glyph'
                    }
                }
            ]);
            this.monacoEditor.revealLineInCenter(lineNum);
        },

        /**
         * Export Features
         */
        exportReport() {
            const jsonStr = JSON.stringify({
                code: this.code,
                language: this.selectedLanguage,
                totalSteps: this.traceSteps.length,
                trace: this.traceSteps,
                aiSummary: this.aiReport
            }, null, 2);

            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `execution_trace_${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }
    };
}

window.visualLabController = visualLabController;
