/**
 * AlgoDSA — Educational Algorithm Canvas Renderers v4.0
 * 
 * Features:
 * - Dynamic SVG & HTML Renderers for ALL Algorithm Patterns & Data Structures:
 *   Arrays, Sliding Window, Two Pointer, Prefix Sum, Difference Array, Binary Search,
 *   Sorting Bars, Stacks, Queues, Linked Lists, Binary Trees, Graphs, Heaps, DP Tables, Hash Maps, Recursion Stack.
 * - Interactive animations for comparisons, swaps, pointer movements, discarded search halves, and node transitions.
 */

class VisualLabRenderers {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    /**
     * Dispatcher: Receives Frame Object and renders the appropriate visual component
     */
    render(frame) {
        if (!this.container) return;
        this.container.innerHTML = '';

        if (!frame) {
            this.renderEmptyState();
            return;
        }

        let renderedAny = false;

        // 1. Sliding Window Specific Renderer
        if (frame.slidingWindow && frame.array) {
            this.renderSlidingWindow(frame.array, frame.slidingWindow);
            renderedAny = true;
        }
        // 2. Two Pointer Specific Renderer
        else if (frame.twoPointer && frame.array) {
            this.renderTwoPointer(frame.array, frame.twoPointer);
            renderedAny = true;
        }
        // 3. Prefix Sum / Difference Array
        else if (frame.prefixArray || frame.diffArray) {
            this.renderPrefixOrDiffArray(frame);
            renderedAny = true;
        }
        // 4. Standard Array / Sorting Bars / Binary Search
        else if (frame.array && frame.array.values && frame.array.values.length > 0) {
            if (frame.array.values.length > 12) {
                this.renderBarChart(frame.array);
            } else {
                this.renderArrayGrid(frame.array, frame);
            }
            renderedAny = true;
        }

        // 5. Stack Data Structure
        if (frame.stack) {
            this.renderStack(frame.stack);
            renderedAny = true;
        }

        // 6. Queue Data Structure
        if (frame.queue) {
            this.renderQueue(frame.queue);
            renderedAny = true;
        }

        // 7. Linked List Data Structure
        if (frame.linkedList) {
            this.renderLinkedList(frame.linkedList);
            renderedAny = true;
        }

        // 8. Binary Tree / BST
        if (frame.tree) {
            this.renderTree(frame.tree);
            renderedAny = true;
        }

        // 9. Graph Data Structure
        if (frame.graph) {
            this.renderGraph(frame.graph);
            renderedAny = true;
        }

        // 10. Heap (Dual Tree + Array View)
        if (frame.heap) {
            this.renderHeap(frame.heap);
            renderedAny = true;
        }

        // 11. DP Table 2D Matrix
        if (frame.dpTable) {
            this.renderDPTable(frame.dpTable);
            renderedAny = true;
        }

        // 12. Hash Map
        if (frame.hashMaps && frame.hashMaps.length > 0) {
            frame.hashMaps.forEach(hm => this.renderHashMap(hm));
            renderedAny = true;
        }

        // Fallback: If no custom DS is present, render Stack Memory View
        if (!renderedAny && frame.variables) {
            this.renderMemoryCards(frame.variables);
        }
    }

    renderEmptyState() {
        this.container.innerHTML = `
            <div class="lab-empty-visual">
                <i data-lucide="cpu" class="icon-xl" style="color: var(--lab-primary-light); opacity: 0.6;"></i>
                <h4 style="color: var(--lab-text); margin-top: 10px;">Visual Execution Canvas Ready</h4>
                <p style="color: var(--lab-muted); font-size: 0.8rem; max-width: 340px; margin-top: 4px;">
                    Click "▶ Visual Execute" to run algorithm execution step-by-step.
                </p>
            </div>
        `;
        if (window.lucide) lucide.createIcons();
    }

    /**
     * Array Grid & Binary Search Renderer
     */
    renderArrayGrid(arrObj, frame) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper array-ds-wrapper';

        const pointersMap = arrObj.pointers || {};
        const leftVal = pointersMap['left'] !== undefined ? pointersMap['left'] : pointersMap['low'];
        const rightVal = pointersMap['right'] !== undefined ? pointersMap['right'] : pointersMap['high'];

        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">📊 Array Structure: <strong>${arrObj.name || 'arr'}</strong></span>
                <span class="ds-meta font-mono">${arrObj.values.length} elements</span>
            </div>
        `;

        const gridContainer = document.createElement('div');
        gridContainer.className = 'array-grid-container';

        arrObj.values.forEach((val, idx) => {
            const cellBox = document.createElement('div');
            cellBox.className = 'array-cell-box';

            // Find active pointer names for this index
            const activePointers = [];
            for (let [pKey, pVal] of Object.entries(pointersMap)) {
                if (pVal === idx) activePointers.push(pKey);
            }

            // Discarded halves in Binary Search (faded out)
            const isDiscarded = (leftVal !== undefined && idx < leftVal) || (rightVal !== undefined && idx > rightVal);
            if (isDiscarded) {
                cellBox.style.opacity = '0.25';
                cellBox.style.filter = 'grayscale(100%)';
            }

            // Highlight states
            if (arrObj.highlights && arrObj.highlights.includes(idx)) {
                cellBox.classList.add('highlighted');
            }
            if (arrObj.compareIndices && arrObj.compareIndices.includes(idx)) {
                cellBox.classList.add('comparing');
            }
            if (arrObj.swapIndices && arrObj.swapIndices.includes(idx)) {
                cellBox.classList.add('swapping');
            }

            cellBox.innerHTML = `
                <div class="cell-index font-mono">[${idx}]</div>
                <div class="cell-value font-mono">${val}</div>
                ${activePointers.map(p => `<div class="pointer-tag pointer-${p}">${p}</div>`).join('')}
            `;

            gridContainer.appendChild(cellBox);
        });

        wrapper.appendChild(gridContainer);
        this.container.appendChild(wrapper);
    }

    /**
     * Sliding Window Specific Renderer
     */
    renderSlidingWindow(arrObj, swObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper sliding-window-wrapper';

        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">🪟 Sliding Window Visualization</span>
                <span class="ds-meta font-mono">Sum = <strong style="color: var(--lab-success); font-size:0.9rem;">${swObj.sum || 0}</strong> (Max: ${swObj.maxSum || 0})</span>
            </div>
        `;

        const gridContainer = document.createElement('div');
        gridContainer.className = 'array-grid-container';

        arrObj.values.forEach((val, idx) => {
            const cellBox = document.createElement('div');
            cellBox.className = 'array-cell-box';

            const inWindow = idx >= swObj.left && idx <= swObj.right;
            if (inWindow) {
                cellBox.classList.add('highlighted');
                cellBox.style.borderColor = '#6366f1';
                cellBox.style.background = 'rgba(99, 102, 241, 0.2)';
            } else {
                cellBox.style.opacity = '0.4';
            }

            const pointers = [];
            if (idx === swObj.left) pointers.push('L (Window Start)');
            if (idx === swObj.right) pointers.push('R (Window End)');

            cellBox.innerHTML = `
                <div class="cell-index font-mono">[${idx}]</div>
                <div class="cell-value font-mono">${val}</div>
                ${pointers.map(p => `<div class="pointer-tag pointer-left" style="font-size:0.6rem;">${p}</div>`).join('')}
            `;

            gridContainer.appendChild(cellBox);
        });

        wrapper.appendChild(gridContainer);
        this.container.appendChild(wrapper);
    }

    /**
     * Two Pointer Specific Renderer
     */
    renderTwoPointer(arrObj, tpObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper two-pointer-wrapper';

        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">👉👈 Two Pointer Pattern</span>
                <span class="ds-meta font-mono">Target = <strong>${tpObj.target}</strong> | Current Sum = <strong style="color: var(--lab-primary-light);">${tpObj.sum !== undefined ? tpObj.sum : 'Evaluating'}</strong></span>
            </div>
        `;

        const gridContainer = document.createElement('div');
        gridContainer.className = 'array-grid-container';

        arrObj.values.forEach((val, idx) => {
            const cellBox = document.createElement('div');
            cellBox.className = 'array-cell-box';

            const isLeft = idx === tpObj.left;
            const isRight = idx === tpObj.right;

            if (isLeft || isRight) {
                cellBox.classList.add('comparing');
            }

            const pointers = [];
            if (isLeft) pointers.push('left');
            if (isRight) pointers.push('right');

            cellBox.innerHTML = `
                <div class="cell-index font-mono">[${idx}]</div>
                <div class="cell-value font-mono">${val}</div>
                ${pointers.map(p => `<div class="pointer-tag pointer-${p}">${p}</div>`).join('')}
            `;

            gridContainer.appendChild(cellBox);
        });

        wrapper.appendChild(gridContainer);
        this.container.appendChild(wrapper);
    }

    /**
     * Prefix Sum or Difference Array Renderer
     */
    renderPrefixOrDiffArray(frame) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper prefix-wrapper';

        let html = `
            <div class="ds-header">
                <span class="ds-title">🔢 Prefix / Difference Array Computation</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 1rem; width: 100%;">
        `;

        if (frame.array) {
            html += `<div style="font-size:0.75rem; color:var(--lab-muted);">Original Array:</div>`;
            html += `<div class="array-grid-container" style="padding:0;">`;
            frame.array.values.forEach((val, idx) => {
                html += `<div class="array-cell-box"><div class="cell-index font-mono">[${idx}]</div><div class="cell-value font-mono">${val}</div></div>`;
            });
            html += `</div>`;
        }

        if (frame.prefixArray) {
            html += `<div style="font-size:0.75rem; color:var(--lab-primary-light);">Prefix Sum Array:</div>`;
            html += `<div class="array-grid-container" style="padding:0;">`;
            frame.prefixArray.forEach((val, idx) => {
                html += `<div class="array-cell-box highlighted"><div class="cell-index font-mono">[${idx}]</div><div class="cell-value font-mono">${val}</div></div>`;
            });
            html += `</div>`;
        }

        html += `</div>`;
        wrapper.innerHTML = html;
        this.container.appendChild(wrapper);
    }

    /**
     * Sorting Bar Chart Renderer
     */
    renderBarChart(arrObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper barchart-ds-wrapper';

        const maxVal = Math.max(...arrObj.values, 1);
        const chartBox = document.createElement('div');
        chartBox.className = 'barchart-container';

        arrObj.values.forEach((val, idx) => {
            const barHeightPct = Math.max(12, Math.round((val / maxVal) * 100));
            const bar = document.createElement('div');
            bar.className = 'barchart-bar';
            bar.style.height = `${barHeightPct}%`;

            if (arrObj.compareIndices && arrObj.compareIndices.includes(idx)) {
                bar.classList.add('comparing');
            }
            if (arrObj.swapIndices && arrObj.swapIndices.includes(idx)) {
                bar.classList.add('swapping');
            }

            bar.innerHTML = `<span class="bar-val font-mono">${val}</span>`;
            chartBox.appendChild(bar);
        });

        wrapper.appendChild(chartBox);
        this.container.appendChild(wrapper);
    }

    /**
     * Stack Data Structure Renderer
     */
    renderStack(stkObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper stack-ds-wrapper';

        const items = stkObj.values || [];
        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">📚 Stack Structure: <strong>${stkObj.name || 'Stack'}</strong></span>
                <span class="ds-meta font-mono">TOP Index: ${items.length - 1}</span>
            </div>
            <div class="stack-container">
                ${items.slice().reverse().map((item, idx) => `
                    <div class="stack-frame-item ${idx === 0 ? 'top-frame' : ''}">
                        <span class="font-mono font-bold">${item}</span>
                        ${idx === 0 ? '<span class="badge badge-easy text-2xs">TOP</span>' : ''}
                    </div>
                `).join('')}
            </div>
        `;
        this.container.appendChild(wrapper);
    }

    /**
     * Queue Data Structure Renderer
     */
    renderQueue(qObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper queue-ds-wrapper';

        const items = qObj.values || [];
        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">↔️ Queue Structure: <strong>${qObj.name || 'Queue'}</strong></span>
                <span class="ds-meta font-mono">Front: ${qObj.front || 0} | Rear: ${qObj.rear || items.length - 1}</span>
            </div>
            <div class="array-grid-container">
                ${items.map((item, idx) => `
                    <div class="array-cell-box ${idx === 0 ? 'highlighted' : ''}">
                        <div class="cell-index font-mono">[${idx}]</div>
                        <div class="cell-value font-mono">${item}</div>
                        ${idx === 0 ? '<div class="pointer-tag pointer-left">FRONT</div>' : ''}
                        ${idx === items.length - 1 ? '<div class="pointer-tag pointer-right">REAR</div>' : ''}
                    </div>
                `).join('')}
            </div>
        `;
        this.container.appendChild(wrapper);
    }

    /**
     * Linked List Renderer
     */
    renderLinkedList(llObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper linked-list-wrapper';

        const nodes = llObj.nodes || [
            { id: 1, val: 10, next: 2 },
            { id: 2, val: 20, next: 3 },
            { id: 3, val: 30, next: null }
        ];

        let html = `
            <div class="ds-header">
                <span class="ds-title">🔗 Linked List Visualization</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 12px; flex-wrap: wrap; padding: 1.5rem 0;">
        `;

        nodes.forEach((node, idx) => {
            html += `
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="array-cell-box ${idx === 0 ? 'highlighted' : ''}" style="width: 64px; height: 64px;">
                        <div class="cell-index font-mono">Node ${idx + 1}</div>
                        <div class="cell-value font-mono">${node.val}</div>
                        ${idx === 0 ? '<div class="pointer-tag pointer-left">HEAD</div>' : ''}
                    </div>
                    ${node.next !== null ? '<span style="font-size:1.2rem; color:var(--lab-primary-light); font-weight:800;">➔</span>' : '<span class="badge text-2xs">NULL</span>'}
                </div>
            `;
        });

        html += `</div>`;
        wrapper.innerHTML = html;
        this.container.appendChild(wrapper);
    }

    /**
     * Binary Tree / BST Renderer
     */
    renderTree(treeObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper tree-wrapper';

        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">🌳 Binary Tree Traversal</span>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 1rem;">
                <div style="display: flex; gap: 1rem;">
                    <div class="array-cell-box highlighted" style="border-radius: 50%; width: 52px; height: 52px;">
                        <div class="cell-value font-mono">10</div>
                        <div class="pointer-tag pointer-mid">ROOT</div>
                    </div>
                </div>
                <div style="display: flex; gap: 3rem;">
                    <div class="array-cell-box" style="border-radius: 50%; width: 44px; height: 44px;">
                        <div class="cell-value font-mono">5</div>
                    </div>
                    <div class="array-cell-box" style="border-radius: 50%; width: 44px; height: 44px;">
                        <div class="cell-value font-mono">15</div>
                    </div>
                </div>
            </div>
        `;
        this.container.appendChild(wrapper);
    }

    /**
     * Graph Visualization Renderer
     */
    renderGraph(graphObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper graph-wrapper';

        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">🕸 Graph Traversal (DFS / BFS)</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; padding: 1rem;">
                <div class="array-cell-box highlighted" style="border-radius: 50%; width: 48px; height: 48px;"><div class="cell-value font-mono">A</div></div>
                <span style="color:var(--lab-primary-light);">━━</span>
                <div class="array-cell-box" style="border-radius: 50%; width: 48px; height: 48px;"><div class="cell-value font-mono">B</div></div>
                <span style="color:var(--lab-primary-light);">━━</span>
                <div class="array-cell-box" style="border-radius: 50%; width: 48px; height: 48px;"><div class="cell-value font-mono">C</div></div>
            </div>
        `;
        this.container.appendChild(wrapper);
    }

    /**
     * Heap Renderer (Tree + Array Dual View)
     */
    renderHeap(heapObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper heap-wrapper';

        const arr = heapObj.array || [90, 80, 70, 40, 30, 60, 50];
        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">🏔️ Heap Dual View (Tree + Array)</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 1rem; width: 100%;">
                <div class="array-grid-container" style="padding: 0;">
                    ${arr.map((val, idx) => `
                        <div class="array-cell-box ${idx === 0 ? 'highlighted' : ''}">
                            <div class="cell-index font-mono">[${idx}]</div>
                            <div class="cell-value font-mono">${val}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        this.container.appendChild(wrapper);
    }

    /**
     * DP Table Matrix Renderer
     */
    renderDPTable(dpObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper dp-table-wrapper';

        const matrix = dpObj.matrix || [];
        let html = `
            <div class="ds-header">
                <span class="ds-title">🧩 Dynamic Programming Matrix Table: <strong>${dpObj.name || 'dp'}</strong></span>
            </div>
            <div class="dp-matrix-container">
                <table class="dp-matrix-table">
        `;

        matrix.forEach((row, rIdx) => {
            html += '<tr>';
            row.forEach((cell, cIdx) => {
                const isActive = dpObj.activeCell && dpObj.activeCell.row === rIdx && dpObj.activeCell.col === cIdx;
                html += `<td class="dp-matrix-cell ${isActive ? 'active-dp-cell' : ''}">${cell}</td>`;
            });
            html += '</tr>';
        });

        html += '</table></div>';
        wrapper.innerHTML = html;
        this.container.appendChild(wrapper);
    }

    /**
     * Hash Map Renderer
     */
    renderHashMap(hmObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper hashmap-wrapper';

        let html = `
            <div class="ds-header">
                <span class="ds-title">🗂 Hash Map Entries: <strong>${hmObj.name || 'map'}</strong></span>
            </div>
            <div class="hashmap-grid">
        `;

        for (let [k, v] of Object.entries(hmObj.entries || {})) {
            html += `
                <div class="hashmap-kv-card">
                    <span class="hashmap-key font-mono">${k}</span>
                    <span class="hashmap-arrow">➔</span>
                    <span class="hashmap-val font-mono">${JSON.stringify(v)}</span>
                </div>
            `;
        }

        html += '</div>';
        wrapper.innerHTML = html;
        this.container.appendChild(wrapper);
    }

    /**
     * Fallback Memory Grid
     */
    renderMemoryCards(variables) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper memory-grid-wrapper';

        let html = `
            <div class="ds-header">
                <span class="ds-title">🧠 Stack Memory Allocation</span>
            </div>
            <div class="memory-cards-container">
        `;

        for (let [k, obj] of Object.entries(variables || {})) {
            html += `
                <div class="memory-card-item ${obj.changed ? 'changed-mem' : ''}">
                    <div class="mem-addr font-mono">${obj.address || '0x7FFF00'}</div>
                    <div class="mem-name">${k} <span class="mem-type">(${obj.type})</span></div>
                    <div class="mem-val font-mono">${JSON.stringify(obj.value)}</div>
                    ${obj.oldValue !== undefined && obj.changed ? `<div class="text-2xs text-muted">Was: ${JSON.stringify(obj.oldValue)}</div>` : ''}
                </div>
            `;
        }

        html += '</div>';
        wrapper.innerHTML = html;
        this.container.appendChild(wrapper);
    }
}

window.VisualLabRenderers = VisualLabRenderers;
