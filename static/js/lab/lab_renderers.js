/**
 * AI Visual Code Execution Lab — Lab Renderers
 * Pure SVG & Canvas rendering engine for all Data Structures & Animations:
 * Arrays, Sorting Bars, Linked Lists, Stacks, Queues, Binary Trees, Graphs,
 * Heaps, Hash Maps, DP Tables, and Recursion Call Stack.
 */

class VisualLabRenderers {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    /**
     * Main Draw Dispatcher
     */
    render(stepData) {
        if (!this.container) return;
        this.container.innerHTML = '';

        if (!stepData || !stepData.dataStructures) {
            this.renderEmptyState();
            return;
        }

        const ds = stepData.dataStructures;

        // Priority 1: Arrays / Sorting
        if (ds.arrays && ds.arrays.length > 0) {
            ds.arrays.forEach(arrObj => {
                // If larger unsorted array, draw bar chart or cell grid based on length
                if (arrObj.values.length > 12) {
                    this.renderBarChart(arrObj);
                } else {
                    this.renderArrayGrid(arrObj);
                }
            });
        }

        // Priority 2: Stacks / Queues
        if (ds.stacks && ds.stacks.length > 0) {
            ds.stacks.forEach(stk => this.renderStack(stk));
        }

        // Priority 3: DP Tables
        if (ds.dpTables && ds.dpTables.length > 0) {
            ds.dpTables.forEach(dp => this.renderDPTable(dp));
        }

        // Priority 4: Hash Maps
        if (ds.hashMaps && ds.hashMaps.length > 0) {
            ds.hashMaps.forEach(hm => this.renderHashMap(hm));
        }

        // Fallback: If no visual structure found
        if (this.container.children.length === 0) {
            this.renderMemoryCards(stepData.variables);
        }
    }

    renderEmptyState() {
        this.container.innerHTML = `
            <div class="lab-empty-visual">
                <i data-lucide="cpu" class="icon-xl" style="color: var(--primary-light); opacity: 0.6;"></i>
                <h4 style="color: var(--text-bright); margin-top: 10px;">Visual Execution Canvas Ready</h4>
                <p style="color: var(--text-muted); font-size: 0.8rem; max-width: 320px; margin-top: 4px;">
                    Paste code and click "Visual Execute" to observe memory, pointers, and array operations step-by-step.
                </p>
            </div>
        `;
        if (window.lucide) lucide.createIcons();
    }

    /**
     * 1. Array Grid Renderer with Animated Pointers & Highlight Boxes
     */
    renderArrayGrid(arrObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper array-ds-wrapper';

        const header = document.createElement('div');
        header.className = 'ds-header';
        header.innerHTML = `
            <span class="ds-title">📊 Array Structure: <strong>${arrObj.name}</strong></span>
            <span class="ds-meta font-mono">${arrObj.values.length} elements</span>
        `;
        wrapper.appendChild(header);

        const gridContainer = document.createElement('div');
        gridContainer.className = 'array-grid-container';

        arrObj.values.forEach((val, idx) => {
            const cellBox = document.createElement('div');
            cellBox.className = 'array-cell-box';

            // Check pointer matches
            const activePointers = [];
            if (arrObj.pointers) {
                for (let [pName, pVal] of Object.entries(arrObj.pointers)) {
                    if (pVal === idx) activePointers.push(pName);
                }
            }

            // Highlights
            if (arrObj.highlights && arrObj.highlights.includes(idx)) {
                cellBox.classList.add('highlighted');
            }
            if (arrObj.compareIndices && arrObj.compareIndices.includes(idx)) {
                cellBox.classList.add('comparing');
            }
            if (arrObj.swapIndices && arrObj.swapIndices.includes(idx)) {
                cellBox.classList.add('swapping');
            }
            if (activePointers.length > 0) {
                cellBox.classList.add('has-pointer');
            }

            // Value & Index
            cellBox.innerHTML = `
                <div class="cell-index font-mono">[${idx}]</div>
                <div class="cell-value font-mono">${val !== undefined ? val : 'ø'}</div>
                ${activePointers.map(p => `<div class="pointer-tag pointer-${p}">${p}</div>`).join('')}
            `;

            gridContainer.appendChild(cellBox);
        });

        wrapper.appendChild(gridContainer);
        this.container.appendChild(wrapper);
    }

    /**
     * 2. Sorting Bar Chart Renderer
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
     * 3. Stack Renderer
     */
    renderStack(stkObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper stack-ds-wrapper';

        wrapper.innerHTML = `
            <div class="ds-header">
                <span class="ds-title">🥞 Stack: <strong>${stkObj.name || 'CallStack'}</strong></span>
                <span class="ds-meta font-mono">TOP = ${stkObj.values ? stkObj.values.length - 1 : 0}</span>
            </div>
            <div class="stack-container">
                ${(stkObj.values || []).slice().reverse().map((item, idx) => `
                    <div class="stack-frame-item ${idx === 0 ? 'top-frame' : ''}">
                        <span class="font-mono">${item}</span>
                        ${idx === 0 ? '<span class="badge badge-easy text-2xs">TOP</span>' : ''}
                    </div>
                `).join('')}
            </div>
        `;
        this.container.appendChild(wrapper);
    }

    /**
     * 4. 2D DP Table Matrix Renderer
     */
    renderDPTable(dpObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper dp-table-wrapper';

        const matrix = dpObj.matrix || [];
        let html = `
            <div class="ds-header">
                <span class="ds-title">🧩 Dynamic Programming Table: <strong>${dpObj.name}</strong></span>
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
     * 5. Hash Map Renderer
     */
    renderHashMap(hmObj) {
        const wrapper = document.createElement('div');
        wrapper.className = 'ds-wrapper hashmap-wrapper';

        let html = `
            <div class="ds-header">
                <span class="ds-title">🗂 Hash Map: <strong>${hmObj.name}</strong></span>
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
     * Fallback Memory Grid Renderer
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
                </div>
            `;
        }

        html += '</div>';
        wrapper.innerHTML = html;
        this.container.appendChild(wrapper);
    }
}

window.VisualLabRenderers = VisualLabRenderers;
