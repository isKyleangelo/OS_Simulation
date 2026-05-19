(() => {
    const API = '/api';
    const HOME = '/home/pusoy';

    const apps = {
        dashboard: { name: 'Dashboard', icon: 'dashboard', color: '#2f7df6', singleton: true, desktop: true },
        filemanager: { name: 'File Manager', icon: 'folder', color: '#e6a21a', singleton: true, desktop: true },
        texteditor: { name: 'Text Editor', icon: 'text', color: '#2563eb', singleton: false, desktop: true },
        imageviewer: { name: 'Image Viewer', icon: 'image', color: '#14a37f', singleton: false, desktop: true },
        pdfviewer: { name: 'PDF Viewer', icon: 'pdf', color: '#d92d20', singleton: false, desktop: true },
        mediaplayer: { name: 'Media Player', icon: 'music', color: '#bd3f83', singleton: false, desktop: true },
        printer: { name: 'Print Queue', icon: 'printer', color: '#4b647f', singleton: true, desktop: true },
        taskmanager: { name: 'Task Manager', icon: 'activity', color: '#0f9f6e', singleton: true, desktop: true },
        terminal: { name: 'Terminal', icon: 'terminal', color: '#111827', singleton: true, desktop: true },
        settings: { name: 'Settings', icon: 'settings', color: '#677589', singleton: true, desktop: true }
    };

    const backendApps = {
        dashboard: 'dashboard',
        filemanager: 'filemanager',
        settings: 'settings',
        taskmanager: 'taskmanager',
        terminal: 'terminal',
        printer: 'printer',
        texteditor: 'texteditor',
        imageviewer: 'imageviewer',
        pdfviewer: 'pdfviewer',
        mediaplayer: 'mediaplayer'
    };

    const backendToDesktop = {
        dashboard: 'dashboard',
        filemanager: 'filemanager',
        settings: 'settings',
        taskmanager: 'taskmanager',
        terminal: 'terminal',
        printer: 'printer',
        texteditor: 'texteditor',
        imageviewer: 'imageviewer',
        pdfviewer: 'pdfviewer',
        mediaplay: 'mediaplayer',
        mediaplayer: 'mediaplayer',
        vscode: 'texteditor'
    };

    const icons = {
        dashboard: '<path d="M3 13h8V3H3z"></path><path d="M13 21h8V11h-8z"></path><path d="M13 3h8v6h-8z"></path><path d="M3 21h8v-6H3z"></path>',
        folder: '<path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H9l2 2h7.5A2.5 2.5 0 0 1 21 9.5v7A2.5 2.5 0 0 1 18.5 19h-13A2.5 2.5 0 0 1 3 16.5z"></path>',
        text: '<path d="M6 3h8l4 4v14H6z"></path><path d="M14 3v5h4"></path><path d="M8 13h8"></path><path d="M8 17h6"></path>',
        image: '<rect x="3" y="5" width="18" height="14" rx="2"></rect><circle cx="8.5" cy="10.5" r="1.5"></circle><path d="m21 15-5-5L5 19"></path>',
        pdf: '<path d="M6 3h8l4 4v14H6z"></path><path d="M14 3v5h4"></path><path d="M8 17h8"></path><path d="M8 13h8"></path>',
        music: '<path d="M9 18V5l11-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="17" cy="16" r="3"></circle>',
        printer: '<path d="M6 9V3h12v6"></path><path d="M6 17H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2"></path><path d="M6 14h12v7H6z"></path>',
        activity: '<path d="M3 12h4l3-8 4 16 3-8h4"></path>',
        terminal: '<path d="m4 7 5 5-5 5"></path><path d="M12 19h8"></path>',
        settings: '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2 2-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V20h-3v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1-2-2 .1-.1A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.5-1H3v-3h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1 2-2 .1.1A1.7 1.7 0 0 0 8.2 5a1.7 1.7 0 0 0 1-1.5V3h3v.5a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1 2 2-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.7v3h-.7a1.7 1.7 0 0 0-1.5 1z"></path>',
        save: '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><path d="M17 21v-8H7v8"></path><path d="M7 3v5h8"></path>',
        open: '<path d="M14 3h7v7"></path><path d="M10 14 21 3"></path><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"></path>',
        trash: '<path d="M4 7h16"></path><path d="M10 11v6"></path><path d="M14 11v6"></path><path d="M6 7l1 14h10l1-14"></path><path d="M9 7V4h6v3"></path>',
        edit: '<path d="M12 20h9"></path><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"></path>',
        plus: '<path d="M12 5v14"></path><path d="M5 12h14"></path>',
        layout: '<rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M12 4v16"></path><path d="M3 10h18"></path>',
        minimize: '<path d="M5 12h14"></path>',
        close: '<path d="M6 6l12 12"></path><path d="M18 6 6 18"></path>',
        up: '<path d="m18 15-6-6-6 6"></path>',
        search: '<circle cx="11" cy="11" r="7"></circle><path d="m21 21-4.3-4.3"></path>',
        play: '<path d="M8 5v14l11-7z"></path>',
        pause: '<path d="M8 5h4v14H8z"></path><path d="M16 5h4v14h-4z"></path>',
        refresh: '<path d="M20 12a8 8 0 1 1-2.3-5.7"></path><path d="M20 4v6h-6"></path>',
        info: '<circle cx="12" cy="12" r="9"></circle><path d="M12 10v6"></path><path d="M12 7h.01"></path>'
    };

    const state = {
        windows: new Map(),
        counter: 0,
        z: 120,
        activePid: null,
        currentPath: HOME,
        selectedPath: null,
        selectedEntry: null,
        fileView: localStorage.getItem('pusoy_file_view') || 'grid',
        fileSearch: '',
        taskSort: localStorage.getItem('pusoy_task_sort') || 'pid',
        taskSearch: '',
        taskTimer: null,
        menuActions: new Map(),
        terminalOutput: 'PusoyShell ready.\nType help, ps, top, ls, printer, or clear.\n\n',
        media: new Map(),
        shellMetrics: null,
        printState: null
    };

    const $ = (selector, root = document) => root.querySelector(selector);
    const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

    function icon(name) {
        return `<span class="icon"><svg viewBox="0 0 24 24" aria-hidden="true">${icons[name] || icons.info}</svg></span>`;
    }

    function glyph(meta, cls = 'app-tile') {
        return `<span class="${cls}" style="background:${meta.color || '#64748b'}"><svg viewBox="0 0 24 24" aria-hidden="true">${icons[meta.icon] || icons.info}</svg></span>`;
    }

    function getLaunchableApps() {
        return Object.entries(apps)
            .filter(([appId, meta]) => meta.desktop && backendApps[appId])
            .map(([appId, meta]) => ({ app_id: appId, ...meta }))
            .sort((left, right) => left.name.localeCompare(right.name));
    }

    function getWindowByPid(pid) {
        const numericPid = Number(pid);
        if (!numericPid) return null;
        return [...state.windows.values()].find(win => Number(win.dataset.pid || 0) === numericPid) || null;
    }

    function getWindowByAppId(appId) {
        if (!appId) return null;
        return [...state.windows.values()].find(win => win.dataset.appId === appId) || null;
    }

    function emitPrintChange(detail = {}) {
        document.dispatchEvent(new CustomEvent('os:print-change', { detail }));
    }

    function hasActivePrintJobs(data) {
        return (data?.jobs || []).some(job => ['Waiting', 'Printing', 'Error'].includes(job.status));
    }

    function buildPrinterCard(printer) {
        return `
            <div class="card">
                <h3>${esc(printer.name)}</h3>
                <p class="muted">${esc(printer.driver)} - ${esc(printer.location)}</p>
                <p><span class="status-pill ${statusClass(printer.status)}" data-role="printer-status-${attr(printer.id)}">${esc(printer.status)}</span></p>
                <button class="btn" data-printer-toggle="${attr(printer.id)}" data-next-status="${printer.status === 'Offline' ? 'Online' : 'Offline'}">
                    Set ${printer.status === 'Offline' ? 'online' : 'offline'}
                </button>
            </div>`;
    }

    function buildPrinterRows(jobs = []) {
        return jobs.map(job => `
            <tr data-job-id="${attr(job.id)}">
                <td><b>#${job.id}</b><br><span class="muted">${esc(job.document_name)}</span></td>
                <td>${esc(job.printer_name)}</td>
                <td><span class="status-pill ${statusClass(job.status)}">${esc(job.status)}</span></td>
                <td>
                    <div class="progress ${job.status === 'Printing' ? 'is-printing' : ''}">
                        <div style="width:${Math.max(0, Math.min(100, Number(job.progress || 0)))}%"></div>
                    </div>
                </td>
                <td>${job.pages} page(s), ${job.copies} copy</td>
                <td>
                    ${job.status === 'Error' ? `<button class="btn" data-retry-job="${job.id}">Retry</button>` : ''}
                    ${['Waiting', 'Printing', 'Error'].includes(job.status) ? `<button class="btn danger" data-cancel-job="${job.id}">Cancel</button>` : ''}
                </td>
            </tr>`).join('');
    }

    function buildPrinterHistory(history = []) {
        return history.slice(0, 8).map(item => `
            <p><b>${esc(item.event)}</b> #${item.job_id} ${esc(item.document_name)}<br><span class="muted">${esc(item.message)} - ${new Date(item.timestamp).toLocaleTimeString()}</span></p>
        `).join('');
    }

    async function refreshPrinterManagerView(win, snapshot = null) {
        if (!document.body.contains(win)) return;
        const data = snapshot || await api(`${API}/print-system`);
        state.printState = data;
        const pending = (data.jobs || []).filter(job => job.status === 'Waiting').length;
        const printing = (data.jobs || []).filter(job => job.status === 'Printing').length;
        const completed = (data.jobs || []).filter(job => job.status === 'Completed').length;

        const pendingNode = $('[data-role="printer-pending"]', win);
        const printingNode = $('[data-role="printer-printing"]', win);
        const completedNode = $('[data-role="printer-completed"]', win);
        const printersHost = $('[data-role="printer-printers"]', win);
        const rowsHost = $('[data-role="printer-table-body"]', win);
        const historyHost = $('[data-role="printer-history"]', win);

        if (pendingNode) pendingNode.textContent = String(pending);
        if (printingNode) printingNode.textContent = String(printing);
        if (completedNode) completedNode.textContent = String(completed);
        if (printersHost) printersHost.innerHTML = (data.printers || []).map(buildPrinterCard).join('');
        if (rowsHost) rowsHost.innerHTML = buildPrinterRows(data.jobs || []);
        if (historyHost) historyHost.innerHTML = buildPrinterHistory(data.history || []);
        win.dataset.printActive = hasActivePrintJobs(data) ? 'true' : 'false';
        if (!hasActivePrintJobs(data)) {
            stopPrinterSync(win);
        }
    }

    function startPrinterSync(win) {
        if (win._printerSyncTimer || win.classList.contains('is-minimized')) return;
        const tick = async () => {
            if (!document.body.contains(win)) {
                stopPrinterSync(win);
                return;
            }
            if (win.classList.contains('is-minimized')) return;
            try {
                const data = await api(`${API}/print-system`);
                await refreshPrinterManagerView(win, data);
                if (!hasActivePrintJobs(data)) {
                    stopPrinterSync(win);
                }
            } catch (error) {
                console.warn('[printer] sync failed', error);
            }
        };
        win._printerSyncTimer = setInterval(tick, 650);
        tick();
    }

    function stopPrinterSync(win) {
        if (win._printerSyncTimer) {
            clearInterval(win._printerSyncTimer);
            win._printerSyncTimer = null;
        }
    }

    function emitProcessChange(detail = {}) {
        document.dispatchEvent(new CustomEvent('os:process-change', { detail }));
    }

    function windowsForProcess(appId, pid, instanceId = null) {
        const numericPid = Number(pid || 0);
        if (instanceId) {
            return [...state.windows.values()].filter(win => win.dataset.instanceId === instanceId);
        }
        if (numericPid) {
            return [...state.windows.values()].filter(win => Number(win.dataset.pid || 0) === numericPid);
        }
        return [...state.windows.values()].filter(win => {
            const sameApp = appId && win.dataset.appId === appId;
            return sameApp;
        });
    }

    function getWindowStateSummary(appId, pid, instanceId = null) {
        const related = windowsForProcess(appId, pid, instanceId);
        const visible = related.filter(win => !win.classList.contains('is-minimized'));
        const active = related.some(win => win.classList.contains('is-active') && !win.classList.contains('is-minimized'));
        let windowState = 'closed';
        if (visible.length) {
            windowState = visible.some(win => win.classList.contains('is-maximized')) ? 'maximized' : 'open';
        } else if (related.length) {
            windowState = 'minimized';
        }
        return {
            app_id: appId,
            instance_id: instanceId || null,
            pid: Number(pid || 0) || null,
            window_state: windowState,
            window_count: related.length,
            active
        };
    }

    function syncWindowState(winOrAppId, pid = null, instanceId = null) {
        const appId = typeof winOrAppId === 'string' ? winOrAppId : winOrAppId?.dataset.appId;
        const processPid = pid ?? (typeof winOrAppId === 'string' ? null : winOrAppId?.dataset.pid);
        const appInstanceId = instanceId ?? (typeof winOrAppId === 'string' ? null : winOrAppId?.dataset.instanceId);
        if (!appId) return;
        const payload = getWindowStateSummary(appId, processPid, appInstanceId);
        api(`${API}/app-window-state`, 'POST', payload).catch(() => {});
        emitProcessChange({ type: 'window-state', ...payload });
    }

    function isNearBottom(element, threshold = 48) {
        return element.scrollHeight - element.scrollTop - element.clientHeight <= threshold;
    }

    function updateTerminalScroll(win, stickToBottom) {
        const output = $('[data-role="terminal-output"]', win);
        if (!output) return;
        if (stickToBottom) {
            requestAnimationFrame(() => {
                output.scrollTo({ top: output.scrollHeight, behavior: 'smooth' });
            });
        }
    }

    function appendTerminalOutput(win, text, replace = false) {
        const output = $('[data-role="terminal-output"]', win);
        const shouldStick = output ? isNearBottom(output) : true;
        if (replace) {
            state.terminalOutput = text;
        } else {
            state.terminalOutput += text;
        }
        if (output) {
            output.textContent = state.terminalOutput;
        }
        updateTerminalScroll(win, shouldStick);
        const input = $('input[name="command"]', win);
        input?.focus({ preventScroll: true });
    }

    function taskKey(task) {
        return task.pid ? `pid-${task.pid}` : `app-${task.instance_id || task.app_id || task.name}`;
    }

    function taskWindowLabel(task) {
        const count = Number(task.window_count || 0);
        const stateLabel = task.window_state || 'unknown';
        return count > 1 ? `${stateLabel} (${count})` : stateLabel;
    }

    function taskRowHtml(task) {
        const active = task.active ? '<span class="muted"> - active</span>' : '';
        return `
            <td><b>${esc(task.name)}</b><br><span class="muted">${esc(task.type)} ${task.app_id ? `- ${esc(task.app_id)}` : ''}${task.instance_id ? ` - ${esc(task.instance_id)}` : ''}${active}</span></td>
            <td>${task.pid || '-'}</td>
            <td><span class="status-pill">${esc(displayTaskState(task.state))}</span></td>
            <td class="muted">${task.opened_at ? new Date(task.opened_at).toLocaleTimeString() : '-'}</td>
            <td><span class="status-pill ${task.window_state === 'open' || task.window_state === 'maximized' ? 'good' : task.window_state === 'hidden' || task.window_state === 'minimized' ? 'warn' : 'danger'}">${esc(taskWindowLabel(task))}</span></td>
            <td>${Math.round(task.cpu_usage || 0)}%</td>
            <td>${task.memory} MB</td>
            <td>${task.can_end ? `<button class="btn danger" data-end-pid="${task.pid || 0}" data-end-app="${attr(task.app_id || '')}" data-end-instance="${attr(task.instance_id || '')}">End</button>` : ''}</td>
        `;
    }

    function reconcileTaskRows(tbody, tasks) {
        const emptyKey = 'empty';
        const expectedKeys = new Set();
        const rows = new Map([...tbody.querySelectorAll('tr[data-task-key]')].map(row => [row.dataset.taskKey, row]));

        if (!tasks.length) {
            expectedKeys.add(emptyKey);
            let row = rows.get(emptyKey);
            const html = '<td colspan="8" class="muted">No tasks.</td>';
            if (!row) {
                row = document.createElement('tr');
                row.dataset.taskKey = emptyKey;
                tbody.appendChild(row);
            }
            if (row.dataset.hash !== html) {
                row.innerHTML = html;
                row.dataset.hash = html;
            }
        } else {
            for (const task of tasks) {
                const key = taskKey(task);
                expectedKeys.add(key);
                let row = rows.get(key);
                const html = taskRowHtml(task);
                if (!row) {
                    row = document.createElement('tr');
                    row.dataset.taskKey = key;
                }
                row.classList.toggle('is-active', Boolean(task.pid && Number(task.pid) === state.activePid));
                if (row.dataset.hash !== html) {
                    row.innerHTML = html;
                    row.dataset.hash = html;
                }
                tbody.appendChild(row);
            }
        }

        rows.forEach((row, key) => {
            if (!expectedKeys.has(key)) row.remove();
        });
    }

    async function refreshTaskManagerView(win, snapshot = null) {
        if (!document.body.contains(win) || win.classList.contains('is-minimized')) return;
        const tm = snapshot || await api(`${API}/task-manager`);
        const tasks = sortTasks((tm.tasks || []).filter(task => matchesTaskSearch(task, state.taskSearch)), state.taskSort);
        const tbody = $('[data-role="task-table-body"]', win);
        const runningApps = $('[data-role="task-running-apps"]', win);
        const cpuStat = $('[data-role="task-cpu"]', win);
        const memStat = $('[data-role="task-memory"]', win);
        const memDetail = $('[data-role="task-memory-detail"]', win);
        const appCount = tm.statistics?.running_apps || 0;
        const cpuUtil = Math.round(tm.statistics?.cpu_utilization || 0);
        const memUtil = Math.round(tm.statistics?.memory_utilization || 0);
        if (runningApps) runningApps.textContent = appCount;
        if (cpuStat) cpuStat.textContent = `${cpuUtil}%`;
        if (memStat) memStat.textContent = `${memUtil}%`;
        if (memDetail) memDetail.textContent = `${tm.statistics?.memory_used || 0}/${tm.statistics?.memory_total || 0} MB`;
        if (tbody) reconcileTaskRows(tbody, tasks);
    }

    function esc(value) {
        return String(value ?? '').replace(/[&<>"']/g, ch => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        })[ch]);
    }

    function attr(value) {
        return esc(value).replace(/`/g, '&#96;');
    }

    async function api(path, method = 'GET', body = null) {
        const options = { method, headers: {} };
        if (body !== null) {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(body);
        }
        const response = await fetch(path, options);
        const data = await response.json().catch(() => ({}));
        if (!response.ok || data.success === false) {
            throw new Error(data.error || data.message || `Request failed: ${response.status}`);
        }
        return data;
    }

    function toast(title, message = '', kind = 'info') {
        const stack = $('#toastStack');
        const item = document.createElement('div');
        item.className = 'toast';
        item.innerHTML = `<strong>${esc(title)}</strong>${message ? `<div class="muted">${esc(message)}</div>` : ''}`;
        if (kind === 'error') item.style.borderColor = 'rgba(217,45,32,.45)';
        stack.appendChild(item);
        setTimeout(() => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(-6px)';
            setTimeout(() => item.remove(), 180);
        }, 3600);
    }

    function applyPreferences() {
        const theme = localStorage.getItem('pusoy_theme') || 'dark';
        const wallpaper = localStorage.getItem('pusoy_wallpaper') || 'aurora';
        const accent = localStorage.getItem('pusoy_accent') || '#2f7df6';
        document.documentElement.dataset.theme = theme;
        document.documentElement.style.setProperty('--accent', accent);
        document.body.classList.remove('wallpaper-aurora', 'wallpaper-slate', 'wallpaper-light', 'wallpaper-graphite');
        document.body.classList.add(`wallpaper-${wallpaper}`);
    }

    async function openApp(type, payload = {}, options = {}) {
        hidePanels();
        hideMenus();
        const meta = apps[type] || apps.dashboard;
        const singleton = options.singleton ?? meta.singleton;
        const id = singleton ? type : `${type}-${++state.counter}`;
        if (singleton && state.windows.has(id)) {
            const existing = state.windows.get(id);
            focusWindow(existing);
            if (payload && Object.keys(payload).length) await renderWindow(existing, payload);
            return existing;
        }

        let launchResult = null;
        if (backendApps[type]) {
            try {
                launchResult = await api(`${API}/launch-app`, 'POST', {
                    app_id: backendApps[type],
                    instance_id: id,
                    singleton
                });
                console.debug('[app] launch', type, launchResult.process?.pid ?? 'n/a');
            } catch (error) {
                console.error('[app] launch failed', type, error);
                toast('Could not launch app', error.message, 'error');
                return null;
            }
        }

        const win = createWindow(id, type, meta, options.title || meta.name);
        if (launchResult?.process?.pid) {
            win.dataset.pid = String(launchResult.process.pid);
            win.dataset.appId = backendApps[type];
            win.dataset.instanceId = launchResult.app?.instance_id || id;
        }
        if (launchResult?.success) {
            emitProcessChange({
                type: 'launch',
                appId: backendApps[type] || type,
                instanceId: launchResult.app?.instance_id || id,
                pid: launchResult.process?.pid || null
            });
        }
        await renderWindow(win, payload);
        focusWindow(win);
        syncWindowState(win);
        renderTaskbar();
        return win;
    }

    function createWindow(id, type, meta, title) {
        const layer = $('#windowLayer');
        const offset = state.windows.size * 24;
        const win = document.createElement('section');
        win.id = `window-${id}`;
        win.className = 'window is-opening';
        win.dataset.id = id;
        win.dataset.type = type;
        win.dataset.title = title;
        win.dataset.dirty = 'false';
        win.dataset.pid = '';
        win.dataset.appId = '';
        win.dataset.instanceId = id;
        win.style.left = `${70 + offset}px`;
        win.style.top = `${42 + offset}px`;
        win.style.zIndex = ++state.z;
        win.innerHTML = `
            <div class="titlebar">
                <div class="titlebar-title">${glyph(meta, 'small-icon')}<span class="title-text">${esc(title)}</span></div>
                <div class="window-controls">
                    <button class="window-control" data-window-action="minimize" title="Minimize">${icon('minimize')}</button>
                    <button class="window-control" data-window-action="maximize" title="Maximize">${icon('layout')}</button>
                    <button class="window-control close" data-window-action="close" title="Close">${icon('close')}</button>
                </div>
            </div>
            <div class="window-body"></div>
            <div class="resize-handle" aria-hidden="true"></div>
        `;
        layer.appendChild(win);
        state.windows.set(id, win);
        bindWindowFrame(win);
        requestAnimationFrame(() => win.classList.remove('is-opening'));
        return win;
    }

    function bindWindowFrame(win) {
        win.addEventListener('pointerdown', event => {
            if (event.target.closest('button, input, textarea, select, option, a, [contenteditable="true"]')) return;
            focusWindow(win);
        });
        win.querySelector('.window-controls').addEventListener('click', event => {
            const button = event.target.closest('[data-window-action]');
            if (!button) return;
            const action = button.dataset.windowAction;
            if (action === 'minimize') minimizeWindow(win);
            if (action === 'maximize') maximizeWindow(win);
            if (action === 'close') closeWindow(win);
        });

        const titlebar = win.querySelector('.titlebar');
        titlebar.addEventListener('pointerdown', event => {
            if (event.target.closest('button') || win.classList.contains('is-maximized')) return;
            const startX = event.clientX;
            const startY = event.clientY;
            const rect = win.getBoundingClientRect();
            titlebar.setPointerCapture(event.pointerId);
            const move = moveEvent => {
                win.style.left = `${Math.max(0, rect.left + moveEvent.clientX - startX)}px`;
                win.style.top = `${Math.max(0, rect.top + moveEvent.clientY - startY)}px`;
            };
            const up = () => {
                titlebar.removeEventListener('pointermove', move);
                titlebar.removeEventListener('pointerup', up);
            };
            titlebar.addEventListener('pointermove', move);
            titlebar.addEventListener('pointerup', up);
        });

        const handle = win.querySelector('.resize-handle');
        handle.addEventListener('pointerdown', event => {
            if (win.classList.contains('is-maximized')) return;
            event.preventDefault();
            const startX = event.clientX;
            const startY = event.clientY;
            const rect = win.getBoundingClientRect();
            handle.setPointerCapture(event.pointerId);
            const move = moveEvent => {
                win.style.width = `${Math.max(360, rect.width + moveEvent.clientX - startX)}px`;
                win.style.height = `${Math.max(260, rect.height + moveEvent.clientY - startY)}px`;
            };
            const up = () => {
                handle.removeEventListener('pointermove', move);
                handle.removeEventListener('pointerup', up);
            };
            handle.addEventListener('pointermove', move);
            handle.addEventListener('pointerup', up);
        });
    }

    function startTaskManagerSync(win) {
        if (win._taskSyncTimer || win.classList.contains('is-minimized')) return;
        const tick = () => {
            if (!document.body.contains(win)) {
                stopTaskManagerSync(win);
                return;
            }
            if (win.classList.contains('is-minimized')) return;
            refreshTaskManagerView(win).catch(error => console.warn('[task-manager] sync failed', error));
        };
        win._taskSyncTimer = setInterval(tick, 1000);
        tick();
    }

    function stopTaskManagerSync(win) {
        if (win?._taskSyncTimer) {
            clearInterval(win._taskSyncTimer);
            win._taskSyncTimer = null;
        }
    }

    function focusWindow(win) {
        if (!win) return;
        const previouslyActive = [...state.windows.values()].filter(item => item.classList.contains('is-active') && item !== win);
        state.windows.forEach(item => item.classList.remove('is-active'));
        win.classList.remove('is-minimized');
        win.classList.add('is-active');
        state.activePid = Number(win.dataset.pid || 0) || null;
        if (win.dataset.type === 'printer' && hasActivePrintJobs(state.printState)) {
            startPrinterSync(win);
        }
        if (win.dataset.type === 'taskmanager') {
            startTaskManagerSync(win);
        }
        win.style.zIndex = ++state.z;
        console.debug('[window] focus', win.dataset.type, win.dataset.id);
        previouslyActive.forEach(item => syncWindowState(item));
        syncWindowState(win);
        renderTaskbar();
    }

    function minimizeWindow(win) {
        if (win.dataset.type === 'printer') {
            stopPrinterSync(win);
        }
        if (win.dataset.type === 'taskmanager') {
            stopTaskManagerSync(win);
        }
        win.classList.add('is-minimized');
        win.classList.remove('is-active');
        syncWindowState(win);
        renderTaskbar();
    }

    function maximizeWindow(win) {
        win.classList.toggle('is-maximized');
        focusWindow(win);
        syncWindowState(win);
    }

    async function closeWindow(win, options = {}) {
        if (!win) return;
        if (win.dataset.dirty === 'true' && !confirm('This document has unsaved changes. Close it anyway?')) {
            return;
        }
        const id = win.dataset.id;
        const type = win.dataset.type;
        const media = state.media.get(id);
        if (media?.timer) clearInterval(media.timer);
        state.media.delete(id);
        if (type === 'taskmanager' && state.taskTimer) {
            clearInterval(state.taskTimer);
            state.taskTimer = null;
        }
        if (type === 'taskmanager') {
            stopTaskManagerSync(win);
        }
        if (type === 'printer') {
            stopPrinterSync(win);
            if (win._printChangeHandler) {
                document.removeEventListener('os:print-change', win._printChangeHandler);
                win._printChangeHandler = null;
            }
        }
        if (type === 'taskmanager' && win._processChangeHandler) {
            document.removeEventListener('os:process-change', win._processChangeHandler);
            win._processChangeHandler = null;
        }
        const appId = backendApps[type] || win.dataset.appId || type;
        const pid = Number(win.dataset.pid || 0) || null;
        const instanceId = win.dataset.instanceId || null;
        if (backendApps[type] && !options.skipBackend) {
            api(`${API}/close-app`, 'POST', {
                app_id: backendApps[type],
                instance_id: instanceId,
                pid,
                force: false
            }).catch(() => {});
        }
        console.debug('[window] close', type, id);
        win.style.opacity = '0';
        win.style.transform = 'scale(.97)';
        setTimeout(() => win.remove(), 150);
        state.windows.delete(id);
        if (state.activePid && Number(win.dataset.pid || 0) === state.activePid) {
            state.activePid = null;
        }
        if (!options.skipBackend) {
            syncWindowState(appId, pid, instanceId);
        }
        emitProcessChange({ type: 'close', appId, instanceId, pid });
        renderTaskbar();
    }

    function setWindowTitle(win, title) {
        win.dataset.title = title;
        const text = win.querySelector('.title-text');
        if (text) text.textContent = title;
        renderTaskbar();
    }

    async function renderWindow(win, payload = {}) {
        const type = win.dataset.type;
        const body = win.querySelector('.window-body');
        body.innerHTML = '<div class="content muted">Loading...</div>';
        try {
            const html = await renderers[type](win, payload);
            body.innerHTML = html;
            binders[type]?.(win, payload);
        } catch (error) {
            body.innerHTML = `<div class="content"><div class="card"><h3>App error</h3><p>${esc(error.message)}</p></div></div>`;
            console.error(error);
        }
    }

    function renderTaskbar() {
        const bar = $('#taskbarApps');
        bar.innerHTML = [...state.windows.values()].map(win => {
            const meta = apps[win.dataset.type] || apps.dashboard;
            return `
                <button class="taskbar-app ${win.classList.contains('is-active') ? 'is-active' : ''} ${win.classList.contains('is-minimized') ? 'is-minimized' : ''}"
                    data-window-id="${attr(win.dataset.id)}" title="${attr(win.dataset.title)}">
                    ${glyph(meta, 'small-icon')}<span>${esc(win.dataset.title)}</span>
                </button>`;
        }).join('');
    }

    function metricCard(label, value, detail) {
        return `<div class="card"><h3>${esc(label)}</h3><div class="metric">${esc(value)}</div><div class="muted">${esc(detail)}</div></div>`;
    }

    const renderers = {
        dashboard: renderDashboard,
        filemanager: renderFileManager,
        texteditor: renderTextEditor,
        imageviewer: renderImageViewer,
        pdfviewer: renderPdfViewer,
        mediaplayer: renderMediaPlayer,
        printer: renderPrinterManager,
        taskmanager: renderTaskManager,
        terminal: renderTerminal,
        settings: renderSettings
    };

    const binders = {
        filemanager: bindFileManager,
        texteditor: bindTextEditor,
        imageviewer: bindImageViewer,
        pdfviewer: bindPdfViewer,
        mediaplayer: bindMediaPlayer,
        printer: bindPrinterManager,
        taskmanager: bindTaskManager,
        terminal: bindTerminal,
        settings: bindSettings,
        dashboard: bindDashboard
    };

    async function renderDashboard() {
        const [metricsData, health, fs, print] = await Promise.all([
            api(`${API}/system-metrics`),
            api(`${API}/system-health`),
            api(`${API}/fs/list?path=${encodeURIComponent(HOME)}`),
            api(`${API}/print-system`)
        ]);
        const metrics = metricsData.metrics || {};
        const activePrints = print.jobs.filter(job => ['Waiting', 'Printing'].includes(job.status)).length;
        return `
            <div class="app-surface">
                <div class="toolbar">
                    <button class="btn primary" data-open-app="filemanager">${icon('folder')}Files</button>
                    <button class="btn" data-open-app="printer">${icon('printer')}Print Queue</button>
                    <button class="btn" data-open-app="taskmanager">${icon('activity')}Task Manager</button>
                    <button class="btn" data-action="step">${icon('refresh')}Step CPU</button>
                </div>
                <div class="content grid">
                    <div class="grid three">
                        ${metricCard('CPU', `${Math.round(metrics.cpu_utilization || 0)}%`, `${metrics.running_processes || 0} running processes`)}
                        ${metricCard('Memory', `${Math.round(metrics.memory_utilization || 0)}%`, `${metrics.memory_used || 0}/${metrics.memory_total || 0} MB used`)}
                        ${metricCard('Health', health.status || 'GOOD', (health.issues || []).join(', ') || 'No active issues')}
                    </div>
                    <div class="grid three">
                        ${metricCard('Files', fs.count, `${fs.path} ready`)}
                        ${metricCard('Print Jobs', activePrints, 'Waiting or printing')}
                        ${metricCard('Uptime', `${Math.floor((metrics.uptime_seconds || 0) / 60)}m`, 'Simulated desktop session')}
                    </div>
                    <div class="card">
                        <h3>Connected workflow</h3>
                        <p class="muted">Files open in their associated apps, Text Editor can print, and Printer Manager tracks the queue and history.</p>
                    </div>
                </div>
            </div>`;
    }

    function bindDashboard(win) {
        win.querySelector('.window-body').addEventListener('click', async event => {
            const appButton = event.target.closest('[data-open-app]');
            if (appButton) openApp(appButton.dataset.openApp, {}, { singleton: true });
            if (event.target.closest('[data-action="step"]')) {
                await api(`${API}/step`, 'POST', {});
                toast('CPU stepped');
                renderWindow(win);
            }
        });
    }

    async function renderFileManager(win) {
        setWindowTitle(win, 'File Manager');
        const data = await api(`${API}/fs/list?path=${encodeURIComponent(state.currentPath)}&search=${encodeURIComponent(state.fileSearch)}`);
        const shortcuts = [
            ['Home', HOME],
            ['Desktop', `${HOME}/Desktop`],
            ['Documents', `${HOME}/Documents`],
            ['Pictures', `${HOME}/Pictures`],
            ['Music', `${HOME}/Music`],
            ['Downloads', `${HOME}/Downloads`],
            ['System', `${HOME}/System`]
        ];
        const entries = state.fileView === 'grid'
            ? `<div class="file-grid">${data.entries.map(fileGridEntry).join('') || emptyState('This folder is empty')}</div>`
            : `<div class="file-list">${data.entries.map(fileListEntry).join('') || emptyState('This folder is empty')}</div>`;
        return `
            <div class="file-manager">
                <aside class="sidebar">
                    <div class="sidebar-title">Places</div>
                    ${shortcuts.map(([label, path]) => `
                        <button class="nav-item ${data.path === path ? 'is-active' : ''}" data-nav="${attr(path)}">${icon(pathIcon(path))}${esc(label)}</button>
                    `).join('')}
                </aside>
                <section class="file-pane">
                    <div class="toolbar no-wrap">
                        <button class="btn" data-action="up" ${data.parent ? '' : 'disabled'}>${icon('up')}Up</button>
                        <button class="btn" data-action="toggle-view">${icon('layout')}${state.fileView === 'grid' ? 'List' : 'Grid'}</button>
                        <input class="field" data-action="search" style="flex:1" value="${attr(state.fileSearch)}" placeholder="Search this folder">
                        <button class="btn primary" data-action="new-file">${icon('plus')}File</button>
                        <button class="btn" data-action="new-folder">${icon('folder')}Folder</button>
                        <button class="btn" data-action="rename" ${state.selectedPath ? '' : 'disabled'}>${icon('edit')}Rename</button>
                        <button class="btn danger" data-action="delete" ${state.selectedPath ? '' : 'disabled'}>${icon('trash')}Delete</button>
                    </div>
                    <div class="breadcrumbs">
                        ${data.breadcrumbs.map(crumb => `<button class="breadcrumb" data-nav="${attr(crumb.path)}">${esc(crumb.name)}</button>`).join('<span class="muted">/</span>')}
                    </div>
                    ${entries}
                </section>
            </div>`;
    }

    function fileGridEntry(entry) {
        const selected = state.selectedPath === entry.path ? 'is-selected' : '';
        return `
            <button class="file-entry ${selected}" draggable="true"
                data-entry-path="${attr(entry.path)}" data-entry-type="${attr(entry.type)}"
                data-entry-name="${attr(entry.name)}" data-entry-association="${attr(entry.association)}">
                ${fileGlyph(entry)}
                <span class="file-entry-name">${esc(entry.name)}</span>
            </button>`;
    }

    function fileListEntry(entry) {
        const selected = state.selectedPath === entry.path ? 'is-selected' : '';
        return `
            <button class="list-row ${selected}" draggable="true"
                data-entry-path="${attr(entry.path)}" data-entry-type="${attr(entry.type)}"
                data-entry-name="${attr(entry.name)}" data-entry-association="${attr(entry.association)}">
                ${fileGlyph(entry)}
                <span style="text-align:left">${esc(entry.name)}</span>
                <span class="muted">${entry.type === 'folder' ? 'Folder' : `${entry.size || 0} B`}</span>
                <span class="muted modified-cell">${entry.modified_at ? new Date(entry.modified_at).toLocaleString() : ''}</span>
            </button>`;
    }

    function fileGlyph(entry) {
        const colors = {
            folder: '#e6a21a',
            texteditor: '#2563eb',
            imageviewer: '#14a37f',
            pdfviewer: '#d92d20',
            mediaplayer: '#bd3f83'
        };
        const iconName = entry.type === 'folder' ? 'folder' : (apps[entry.association]?.icon || 'text');
        return `<span class="file-glyph" style="background:${colors[entry.type === 'folder' ? 'folder' : entry.association] || '#64748b'}"><svg viewBox="0 0 24 24" aria-hidden="true">${icons[iconName] || icons.text}</svg></span>`;
    }

    function pathIcon(path) {
        if (path.includes('Pictures')) return 'image';
        if (path.includes('Music')) return 'music';
        if (path.includes('System')) return 'settings';
        return 'folder';
    }

    function emptyState(text) {
        return `<div class="empty-state">${esc(text)}</div>`;
    }

    function bindFileManager(win) {
        const body = win.querySelector('.window-body');
        let searchTimer = null;
        body.addEventListener('click', async event => {
            const nav = event.target.closest('[data-nav]');
            if (nav) {
                state.currentPath = nav.dataset.nav;
                state.selectedPath = null;
                state.selectedEntry = null;
                renderWindow(win);
                return;
            }

            const entryEl = event.target.closest('[data-entry-path]');
            if (entryEl) {
                selectEntry(entryEl);
                return;
            }

            const action = event.target.closest('[data-action]')?.dataset.action;
            if (!action) return;
            if (action === 'up') {
                state.currentPath = state.currentPath.split('/').slice(0, -1).join('/') || HOME;
                if (!state.currentPath.startsWith(HOME)) state.currentPath = HOME;
                state.selectedPath = null;
                renderWindow(win);
            }
            if (action === 'toggle-view') {
                state.fileView = state.fileView === 'grid' ? 'list' : 'grid';
                localStorage.setItem('pusoy_file_view', state.fileView);
                renderWindow(win);
            }
            if (action === 'new-file') await createFileInManager(win);
            if (action === 'new-folder') await createFolderInManager(win);
            if (action === 'rename') await renameSelected(win);
            if (action === 'delete') await deleteSelected(win);
        });

        body.addEventListener('dblclick', event => {
            const entryEl = event.target.closest('[data-entry-path]');
            if (entryEl) openEntry(entryEl.dataset.entryPath, entryEl.dataset.entryType);
        });

        body.addEventListener('contextmenu', event => {
            const entryEl = event.target.closest('[data-entry-path]');
            if (!entryEl) return;
            event.preventDefault();
            selectEntry(entryEl);
            showFileContext(event.clientX, event.clientY);
        });

        body.addEventListener('input', event => {
            if (event.target.matches('[data-action="search"]')) {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(() => {
                    state.fileSearch = event.target.value;
                    renderWindow(win);
                }, 180);
            }
        });

        body.addEventListener('dragstart', event => {
            const entryEl = event.target.closest('[data-entry-path]');
            if (!entryEl) return;
            event.dataTransfer.setData('text/plain', entryEl.dataset.entryPath);
        });

        body.addEventListener('dragover', event => {
            const target = event.target.closest('[data-entry-type="folder"]');
            if (target) {
                event.preventDefault();
                target.classList.add('drop-target');
            }
        });

        body.addEventListener('dragleave', event => {
            event.target.closest('[data-entry-type="folder"]')?.classList.remove('drop-target');
        });

        body.addEventListener('drop', async event => {
            const target = event.target.closest('[data-entry-type="folder"]');
            if (!target) return;
            event.preventDefault();
            target.classList.remove('drop-target');
            const source = event.dataTransfer.getData('text/plain');
            if (!source || source === target.dataset.entryPath) return;
            await api(`${API}/fs/move`, 'POST', { source_path: source, destination_folder: target.dataset.entryPath });
            toast('Moved item');
            renderWindow(win);
            renderDesktop();
        });
    }

    function selectEntry(entryEl) {
        state.selectedPath = entryEl.dataset.entryPath;
        state.selectedEntry = {
            path: entryEl.dataset.entryPath,
            type: entryEl.dataset.entryType,
            name: entryEl.dataset.entryName,
            association: entryEl.dataset.entryAssociation
        };
        $$('.file-entry,.list-row').forEach(el => el.classList.remove('is-selected'));
        entryEl.classList.add('is-selected');
        $$('[data-action="rename"],[data-action="delete"]').forEach(button => {
            button.disabled = false;
        });
    }

    async function openEntry(path, type) {
        try {
            if (type === 'folder') {
                state.currentPath = path;
                state.selectedPath = null;
                state.selectedEntry = null;
                const manager = state.windows.get('filemanager');
                if (manager) renderWindow(manager);
                return;
            }
            await openFile(path);
        } catch (error) {
            console.error('[file] open failed', path, error);
            toast('Failed to open file', error.message, 'error');
        }
    }

    async function openFile(path) {
        const file = await api(`${API}/fs/open`, 'POST', { path });
        await openApp(file.entry.association, { entry: file.entry, content: file.content, path: file.entry.path }, { title: file.entry.name });
    }

    async function createFileInManager(win) {
        try {
            const name = prompt('File name', 'untitled.txt');
            if (!name) return;
            await api(`${API}/fs/create-file`, 'POST', { directory: state.currentPath, name, content: '' });
            console.debug('[file] create', state.currentPath, name);
            toast('File created', name);
            state.selectedEntry = null;
            state.selectedPath = null;
            await renderWindow(win);
            await renderDesktop();
        } catch (error) {
            console.error('[file] create failed', error);
            toast('File creation failed', error.message, 'error');
        }
    }

    async function createFolderInManager(win) {
        try {
            const name = prompt('Folder name', 'New Folder');
            if (!name) return;
            await api(`${API}/fs/create-folder`, 'POST', { directory: state.currentPath, name });
            console.debug('[file] folder create', state.currentPath, name);
            toast('Folder created', name);
            state.selectedEntry = null;
            state.selectedPath = null;
            await renderWindow(win);
            await renderDesktop();
        } catch (error) {
            console.error('[file] folder create failed', error);
            toast('Folder creation failed', error.message, 'error');
        }
    }

    async function renameSelected(win) {
        try {
            if (!state.selectedEntry) return toast('Select an item first', '', 'error');
            const name = prompt('New name', state.selectedEntry.name);
            if (!name) return;
            await api(`${API}/fs/rename`, 'POST', { path: state.selectedEntry.path, new_name: name });
            console.debug('[file] rename', state.selectedEntry.path, name);
            toast('Item renamed');
            state.selectedEntry = null;
            state.selectedPath = null;
            await renderWindow(win);
            await renderDesktop();
        } catch (error) {
            console.error('[file] rename failed', error);
            toast('Rename failed', error.message, 'error');
        }
    }

    async function deleteSelected(win) {
        try {
            if (!state.selectedEntry) return toast('Select an item first', '', 'error');
            if (!confirm(`Delete ${state.selectedEntry.name}?`)) return;
            await api(`${API}/fs/delete`, 'POST', { path: state.selectedEntry.path });
            console.debug('[file] delete', state.selectedEntry.path);
            toast('Item deleted');
            state.selectedEntry = null;
            state.selectedPath = null;
            await renderWindow(win);
            await renderDesktop();
        } catch (error) {
            console.error('[file] delete failed', error);
            toast('Delete failed', error.message, 'error');
        }
    }

    async function renderTextEditor(win, payload = {}) {
        let entry = payload.entry || null;
        let content = payload.content ?? '';
        if (payload.path && !entry) {
            const file = await api(`${API}/fs/open`, 'POST', { path: payload.path });
            entry = file.entry;
            content = file.content;
        }
        const title = entry?.name || 'Untitled.txt';
        win.dataset.filePath = entry?.path || '';
        win.dataset.dirty = 'false';
        setWindowTitle(win, `Text Editor - ${title}`);
        return `
            <div class="editor-shell">
                <div class="toolbar">
                    <button class="btn" data-action="open">${icon('open')}Open</button>
                    <button class="btn primary" data-action="save">${icon('save')}Save</button>
                    <button class="btn" data-action="save-as">Save As</button>
                    <button class="btn" data-action="print">${icon('printer')}Print</button>
                    <span class="muted">${esc(win.dataset.filePath || 'New unsaved file')}</span>
                </div>
                <textarea class="editor-text" spellcheck="false">${esc(content)}</textarea>
                <div class="statusbar"><span data-role="dirty">Saved</span><span data-role="count">${content.length} characters</span></div>
            </div>`;
    }

    function bindTextEditor(win) {
        const body = win.querySelector('.window-body');
        const text = $('.editor-text', body);
        const dirty = $('[data-role="dirty"]', body);
        const count = $('[data-role="count"]', body);
        text.addEventListener('input', () => {
            win.dataset.dirty = 'true';
            dirty.textContent = 'Unsaved changes';
            count.textContent = `${text.value.length} characters`;
        });
        body.addEventListener('click', async event => {
            const action = event.target.closest('[data-action]')?.dataset.action;
            if (action === 'save') await saveEditor(win);
            if (action === 'save-as') await saveEditorAs(win);
            if (action === 'open') await openTextPicker(win);
            if (action === 'print') await openPrintDialog(win);
        });
    }

    async function saveEditor(win) {
        const text = $('.editor-text', win);
        let path = win.dataset.filePath;
        if (!path) {
            const name = prompt('Save as', 'untitled.txt');
            if (!name) return;
            path = name.includes('/') ? name : `${HOME}/Documents/${name}`;
        }
        const result = await api(`${API}/fs/save`, 'POST', { path, content: text.value });
        win.dataset.filePath = result.entry.path;
        win.dataset.dirty = 'false';
        setWindowTitle(win, `Text Editor - ${result.entry.name}`);
        $('[data-role="dirty"]', win).textContent = 'Saved';
        toast('File saved', result.entry.name);
        renderDesktop();
    }

    async function saveEditorAs(win) {
        const current = win.dataset.filePath || `${HOME}/Documents/untitled.txt`;
        const path = prompt('Save as path', current);
        if (!path) return;
        win.dataset.filePath = path;
        await saveEditor(win);
    }

    async function openTextPicker(win) {
        if (win.dataset.dirty === 'true' && !confirm('Discard unsaved changes and open another file?')) return;
        const data = await api(`${API}/files`);
        const textFiles = (data.entries || []).filter(entry => entry.association === 'texteditor');
        showModal('Open text file', `
            <div class="grid">
                ${textFiles.map(entry => `
                    <button class="nav-item" data-picker-path="${attr(entry.path)}">${fileGlyph(entry)}${esc(entry.path.replace(`${HOME}/`, ''))}</button>
                `).join('') || emptyState('No text files found')}
            </div>
        `, modal => {
            modal.addEventListener('click', async event => {
                const row = event.target.closest('[data-picker-path]');
                if (!row) return;
                const file = await api(`${API}/fs/open`, 'POST', { path: row.dataset.pickerPath });
                hideModal();
                await renderWindow(win, { entry: file.entry, content: file.content, path: file.entry.path });
            });
        });
    }

    async function openPrintDialog(win, options = {}) {
        const text = options.content ?? $('.editor-text', win)?.value ?? '';
        const documentName = options.documentName || (win.dataset.filePath ? win.dataset.filePath.split('/').pop() : 'Untitled.txt');
        const sourceApp = options.sourceApp || 'Text Editor';
        const printState = await api(`${API}/print-system`);
        showModal('Print document', `
            <form id="printForm" class="grid">
                <label>Printer<br><select class="select" name="printer_id" style="width:100%">
                    ${printState.printers.map(printer => `<option value="${attr(printer.id)}">${esc(printer.name)} (${esc(printer.status)})</option>`).join('')}
                </select></label>
                <div class="grid two">
                    <label>Copies<br><input class="field" name="copies" type="number" min="1" value="1" style="width:100%"></label>
                    <label>Page size<br><select class="select" name="page_size" style="width:100%"><option>Letter</option><option>A4</option><option>Legal</option></select></label>
                    <label>Orientation<br><select class="select" name="orientation" style="width:100%"><option>Portrait</option><option>Landscape</option></select></label>
                    <label>Color<br><select class="select" name="color_mode" style="width:100%"><option>Black and white</option><option>Color</option></select></label>
                </div>
                <div>
                    <strong>Print preview</strong>
                    <div class="print-preview">${esc(text.slice(0, 1200) || '(blank document)')}</div>
                </div>
                <div class="toolbar" style="border:0;padding:0;justify-content:flex-end">
                    <button class="btn" type="button" data-modal-close>Cancel</button>
                    <button class="btn primary" type="submit">${icon('printer')}Print</button>
                </div>
            </form>
        `, modal => {
            $('#printForm', modal).addEventListener('submit', async event => {
                event.preventDefault();
                const form = new FormData(event.currentTarget);
                const payload = Object.fromEntries(form.entries());
                payload.document_name = documentName;
                payload.content = text;
                payload.source_app = sourceApp;
                const result = await api(`${API}/print-jobs`, 'POST', payload);
                hideModal();
                toast('Print job submitted', documentName);
                emitPrintChange({
                    type: 'submitted',
                    job: result.job,
                    snapshot: result.print_system
                });
                const printerWin = state.windows.get('printer');
                if (printerWin) {
                    await refreshPrinterManagerView(printerWin, result.print_system);
                    focusWindow(printerWin);
                    startPrinterSync(printerWin);
                } else {
                    await openApp('printer', { printSystem: result.print_system }, { singleton: true });
                }
            });
        });
    }

    async function renderImageViewer(win, payload = {}) {
        const file = payload.entry ? payload : await api(`${API}/fs/open`, 'POST', { path: payload.path });
        const entry = payload.entry || file.entry;
        const content = payload.content ?? file.content;
        win.dataset.filePath = entry.path;
        win.dataset.zoom = win.dataset.zoom || '1';
        setWindowTitle(win, `Image Viewer - ${entry.name}`);
        const src = String(content).startsWith('data:image') ? content : makeSvgData(entry.name);
        return `
            <div class="app-surface">
                <div class="toolbar">
                    <button class="btn" data-action="prev">Previous</button>
                    <button class="btn" data-action="next">Next</button>
                    <button class="btn" data-action="zoom-out">Zoom out</button>
                    <button class="btn" data-action="zoom-in">Zoom in</button>
                    <span class="muted">${esc(entry.path)}</span>
                </div>
                <div class="viewer-stage"><img src="${attr(src)}" alt="${attr(entry.name)}" style="transform:scale(${attr(win.dataset.zoom)})"></div>
            </div>`;
    }

    function bindImageViewer(win) {
        win.querySelector('.window-body').addEventListener('click', async event => {
            const action = event.target.closest('[data-action]')?.dataset.action;
            if (!action) return;
            if (action === 'zoom-in' || action === 'zoom-out') {
                const current = Number(win.dataset.zoom || 1);
                win.dataset.zoom = String(Math.min(3, Math.max(0.3, current + (action === 'zoom-in' ? 0.15 : -0.15))));
                $('img', win).style.transform = `scale(${win.dataset.zoom})`;
            }
            if (action === 'prev' || action === 'next') await navigateSiblingFile(win, ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'], action);
        });
    }

    function makeSvgData(name) {
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 430"><rect width="700" height="430" fill="#14213d"/><rect x="50" y="50" width="600" height="330" rx="18" fill="#f8fafc"/><path d="M80 340 255 200 365 296 460 230 620 340Z" fill="#2f7df6"/><circle cx="190" cy="150" r="52" fill="#e6a21a"/><text x="350" y="96" text-anchor="middle" font-family="Segoe UI,Arial" font-size="28" fill="#182235">${esc(name)}</text></svg>`;
        return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
    }

    async function navigateSiblingFile(win, extensions, direction) {
        const path = win.dataset.filePath;
        const parent = path.split('/').slice(0, -1).join('/');
        const data = await api(`${API}/fs/list?path=${encodeURIComponent(parent)}`);
        const files = data.entries.filter(entry => entry.type === 'file' && extensions.includes(entry.extension));
        const index = files.findIndex(entry => entry.path === path);
        if (index === -1 || !files.length) return;
        const next = files[(index + (direction === 'next' ? 1 : -1) + files.length) % files.length];
        const file = await api(`${API}/fs/open`, 'POST', { path: next.path });
        await renderWindow(win, { entry: file.entry, content: file.content, path: file.entry.path });
    }

    async function renderPdfViewer(win, payload = {}) {
        const file = payload.entry ? payload : await api(`${API}/fs/open`, 'POST', { path: payload.path });
        const entry = payload.entry || file.entry;
        const content = payload.content ?? file.content;
        win.dataset.filePath = entry.path;
        win.dataset.fileContent = String(content || '');
        win.dataset.zoom = win.dataset.zoom || '1';
        setWindowTitle(win, `PDF Viewer - ${entry.name}`);
        const page = String(content).startsWith('data:application/pdf')
            ? `<iframe title="${attr(entry.name)}" src="${attr(content)}" style="width:100%;height:100%;border:0;background:#fff"></iframe>`
            : `<article class="pdf-page" style="transform:scale(${attr(win.dataset.zoom)});transform-origin:top center"><h1>${esc(entry.name)}</h1><p>${esc(String(content)).replace(/\n/g, '</p><p>')}</p></article>`;
        return `
            <div class="app-surface">
                <div class="toolbar">
                    <button class="btn" data-action="zoom-out">Zoom out</button>
                    <button class="btn" data-action="zoom-in">Zoom in</button>
                    <button class="btn primary" data-action="print">${icon('printer')}Print</button>
                    <span class="muted">${esc(entry.path)}</span>
                </div>
                <div class="pdf-stage">${page}</div>
            </div>`;
    }

    function bindPdfViewer(win) {
        const body = win.querySelector('.window-body');
        body.addEventListener('click', event => {
            const action = event.target.closest('[data-action]')?.dataset.action;
            if (!action) return;
            if (action === 'print') {
                openPrintDialog(win, {
                    documentName: win.dataset.filePath ? win.dataset.filePath.split('/').pop() : 'Document.pdf',
                    content: win.dataset.fileContent || $('.pdf-page', win)?.innerText || win.dataset.filePath || '',
                    sourceApp: 'PDF Viewer'
                });
                return;
            }
            const current = Number(win.dataset.zoom || 1);
            win.dataset.zoom = String(Math.min(2, Math.max(0.55, current + (action === 'zoom-in' ? 0.1 : -0.1))));
            const page = $('.pdf-page', win);
            if (page) page.style.transform = `scale(${win.dataset.zoom})`;
        });
    }

    async function renderMediaPlayer(win, payload = {}) {
        const file = payload.entry ? payload : (payload.path ? await api(`${API}/fs/open`, 'POST', { path: payload.path }) : null);
        const entry = payload.entry || file?.entry || { name: 'No track loaded', path: '' };
        const content = payload.content ?? file?.content ?? '';
        const duration = Number(String(content).match(/duration=(\d+)/)?.[1] || 90);
        let media = state.media.get(win.dataset.id);
        if (!media || media.path !== entry.path) {
            if (media?.timer) clearInterval(media.timer);
            media = { path: entry.path, title: entry.name, duration, current: 0, playing: false, volume: 70, timer: null };
            state.media.set(win.dataset.id, media);
        }
        win.dataset.filePath = entry.path;
        setWindowTitle(win, `Media Player - ${entry.name}`);
        return `
            <div class="media-stage">
                <div class="media-card">
                    <div class="album-art">${glyph(apps.mediaplayer)}</div>
                    <div>
                        <h3>${esc(entry.name)}</h3>
                        <div class="muted">${esc(entry.path || 'Open an audio file from File Manager')}</div>
                    </div>
                    <div class="progress"><div data-role="media-progress" style="width:${(media.current / media.duration) * 100}%"></div></div>
                    <div class="statusbar"><span data-role="media-time">${formatTime(media.current)} / ${formatTime(media.duration)}</span><span>Volume ${media.volume}%</span></div>
                    <div class="toolbar" style="border:0;padding:0">
                        <button class="btn primary" data-action="play">${icon(media.playing ? 'pause' : 'play')}${media.playing ? 'Pause' : 'Play'}</button>
                        <button class="btn" data-action="stop">Stop</button>
                        <label class="muted">Volume <input type="range" min="0" max="100" value="${media.volume}" data-action="volume"></label>
                    </div>
                </div>
            </div>`;
    }

    function bindMediaPlayer(win) {
        const body = win.querySelector('.window-body');
        body.addEventListener('click', event => {
            const action = event.target.closest('[data-action]')?.dataset.action;
            if (action === 'play') toggleMedia(win);
            if (action === 'stop') stopMedia(win);
        });
        body.addEventListener('input', event => {
            if (event.target.matches('[data-action="volume"]')) {
                const media = state.media.get(win.dataset.id);
                media.volume = Number(event.target.value);
                renderWindow(win, { path: win.dataset.filePath });
            }
        });
    }

    function toggleMedia(win) {
        const media = state.media.get(win.dataset.id);
        media.playing = !media.playing;
        if (media.playing && !media.timer) {
            media.timer = setInterval(() => {
                media.current += 1;
                if (media.current >= media.duration) {
                    media.current = media.duration;
                    media.playing = false;
                    clearInterval(media.timer);
                    media.timer = null;
                }
                updateMediaUi(win);
            }, 1000);
        }
        if (!media.playing && media.timer) {
            clearInterval(media.timer);
            media.timer = null;
        }
        renderWindow(win, { path: win.dataset.filePath });
    }

    function stopMedia(win) {
        const media = state.media.get(win.dataset.id);
        if (media.timer) clearInterval(media.timer);
        media.timer = null;
        media.playing = false;
        media.current = 0;
        renderWindow(win, { path: win.dataset.filePath });
    }

    function updateMediaUi(win) {
        const media = state.media.get(win.dataset.id);
        const progress = $('[data-role="media-progress"]', win);
        const time = $('[data-role="media-time"]', win);
        if (progress) progress.style.width = `${(media.current / media.duration) * 100}%`;
        if (time) time.textContent = `${formatTime(media.current)} / ${formatTime(media.duration)}`;
    }

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
    }

    async function renderPrinterManager(win, payload = {}) {
        const data = payload.printSystem || payload.print_system || await api(`${API}/print-system`);
        state.printState = data;
        const rows = buildPrinterRows(data.jobs || []);
        const printerCards = (data.printers || []).map(buildPrinterCard).join('');
        const history = buildPrinterHistory(data.history || []);
        const pending = (data.jobs || []).filter(job => job.status === 'Waiting').length;
        const printing = (data.jobs || []).filter(job => job.status === 'Printing').length;
        const completed = (data.jobs || []).filter(job => job.status === 'Completed').length;
        return `
            <div class="app-surface">
                <div class="toolbar">
                    <button class="btn" data-action="refresh">${icon('refresh')}Refresh</button>
                    <button class="btn primary" data-action="install">${icon('plus')}Install printer</button>
                </div>
                <div class="content grid">
                    <div class="grid three">
                        <div class="card"><h3>Waiting</h3><div class="metric"><span data-role="printer-pending">${pending}</span></div><div class="muted">Queued jobs</div></div>
                        <div class="card"><h3>Printing</h3><div class="metric"><span data-role="printer-printing">${printing}</span></div><div class="muted">Jobs in progress</div></div>
                        <div class="card"><h3>Completed</h3><div class="metric"><span data-role="printer-completed">${completed}</span></div><div class="muted">Finished jobs</div></div>
                    </div>
                    <div class="grid two" data-role="printer-printers">${printerCards}</div>
                    <div class="card">
                        <h3>Queue</h3>
                        <table class="table">
                            <thead><tr><th>Document</th><th>Printer</th><th>Status</th><th>Progress</th><th>Settings</th><th>Actions</th></tr></thead>
                            <tbody data-role="printer-table-body">${rows || '<tr><td colspan="6" class="muted">No print jobs yet.</td></tr>'}</tbody>
                        </table>
                    </div>
                    <div class="card">
                        <h3>History</h3>
                        <div data-role="printer-history">${history || '<p class="muted">No print history yet.</p>'}</div>
                    </div>
                </div>
            </div>`;
    }

    function statusClass(status) {
        if (['Completed', 'Online'].includes(status)) return 'good';
        if (['Waiting', 'Busy', 'Printing'].includes(status)) return 'warn';
        if (['Error', 'Cancelled', 'Offline'].includes(status)) return 'danger';
        return '';
    }

    function displayTaskState(state) {
        if (state === 'RUNNING') return 'Running';
        if (state === 'WAITING') return 'Suspended';
        if (state === 'TERMINATED') return 'Closed';
        if (state === 'READY') return 'Ready';
        return state || 'Unknown';
    }

    function matchesTaskSearch(task, query) {
        const needle = String(query || '').trim().toLowerCase();
        if (!needle) return true;
        return [task.name, task.app_id, task.instance_id, task.pid, task.state, task.window_state, task.type]
            .filter(Boolean)
            .some(value => String(value).toLowerCase().includes(needle));
    }

    function sortTasks(tasks, sortKey) {
        const sorted = [...tasks];
        if (sortKey === 'name') {
            sorted.sort((left, right) => String(left.name || '').localeCompare(String(right.name || '')) || Number(left.pid || 0) - Number(right.pid || 0));
        } else if (sortKey === 'memory') {
            sorted.sort((left, right) => Number(right.memory || 0) - Number(left.memory || 0) || Number(left.pid || 0) - Number(right.pid || 0));
        } else {
            sorted.sort((left, right) => Number(left.pid || 0) - Number(right.pid || 0));
        }
        return sorted;
    }

    async function closeTaskProcess(pid, appId = null, instanceId = null) {
        const targets = windowsForProcess(appId, pid, instanceId);
        for (const win of targets) {
            await closeWindow(win, { skipBackend: true });
        }
    }

    function bindPrinterManager(win) {
        if (win.dataset.printerManagerBound === 'true') return;
        win.dataset.printerManagerBound = 'true';
        const body = win.querySelector('.window-body');
        const syncFromState = () => {
            if (state.printState) refreshPrinterManagerView(win, state.printState).catch(() => {});
        };
        win._printChangeHandler = event => {
            const snapshot = event.detail?.snapshot || event.detail?.print_system || null;
            if (!document.body.contains(win) || win.classList.contains('is-minimized')) return;
            if (snapshot) {
                refreshPrinterManagerView(win, snapshot).catch(() => {});
            } else {
                refreshPrinterManagerView(win).catch(() => {});
            }
            if (hasActivePrintJobs(snapshot || state.printState)) {
                startPrinterSync(win);
            }
        };
        document.addEventListener('os:print-change', win._printChangeHandler);
        syncFromState();
        if (hasActivePrintJobs(state.printState)) startPrinterSync(win);
        body.addEventListener('click', async event => {
            const cancel = event.target.closest('[data-cancel-job]');
            const retry = event.target.closest('[data-retry-job]');
            const toggle = event.target.closest('[data-printer-toggle]');
            const action = event.target.closest('[data-action]')?.dataset.action;
            if (cancel) {
                const result = await api(`${API}/print-jobs/${cancel.dataset.cancelJob}/cancel`, 'POST', {});
                toast('Print job cancelled');
                emitPrintChange({ type: 'cancelled', job: result.job, snapshot: state.printState });
                await refreshPrinterManagerView(win).catch(() => {});
            }
            if (retry) {
                const result = await api(`${API}/print-jobs/${retry.dataset.retryJob}/retry`, 'POST', {});
                toast('Print job retried');
                emitPrintChange({ type: 'retry', job: result.job, snapshot: state.printState });
                await refreshPrinterManagerView(win).catch(() => {});
            }
            if (toggle) {
                const result = await api(`${API}/printers/${toggle.dataset.printerToggle}/status`, 'POST', { status: toggle.dataset.nextStatus });
                toast('Printer status updated');
                emitPrintChange({ type: 'printer-status', printer: result.printer, snapshot: state.printState });
                await refreshPrinterManagerView(win).catch(() => {});
            }
            if (action === 'refresh') await refreshPrinterManagerView(win).catch(() => {});
            if (action === 'install') openInstallPrinterDialog(win);
        });
    }

    function openInstallPrinterDialog(win) {
        showModal('Install printer driver', `
            <form id="installPrinterForm" class="grid">
                <label>Printer name<br><input class="field" name="name" value="Lab Printer" style="width:100%"></label>
                <label>Driver<br><input class="field" name="driver" value="Generic PusoyOS Driver" style="width:100%"></label>
                <label>Location<br><input class="field" name="location" value="CMSC Lab" style="width:100%"></label>
                <div class="toolbar" style="border:0;padding:0;justify-content:flex-end">
                    <button class="btn" type="button" data-modal-close>Cancel</button>
                    <button class="btn primary" type="submit">Install</button>
                </div>
            </form>
        `, modal => {
            $('#installPrinterForm', modal).addEventListener('submit', async event => {
                event.preventDefault();
                const result = await api(`${API}/printers/install`, 'POST', Object.fromEntries(new FormData(event.currentTarget).entries()));
                hideModal();
                toast('Printer installed');
                emitPrintChange({ type: 'printer-installed', printer: result.printer, snapshot: state.printState });
                await refreshPrinterManagerView(win).catch(() => {});
            });
        });
    }

    async function renderTaskManager() {
        const [tm, algorithms] = await Promise.all([
            api(`${API}/task-manager`),
            api(`${API}/scheduling-algorithms`),
        ]);
        const tasks = sortTasks((tm.tasks || []).filter(task => matchesTaskSearch(task, state.taskSearch)), state.taskSort);
        const launchableApps = getLaunchableApps();
        return `
            <div class="app-surface">
                <div class="toolbar">
                    <select class="select" data-action="launch-select">${launchableApps.map(app => `<option value="${attr(app.app_id)}">${esc(app.name)}</option>`).join('')}</select>
                    <button class="btn primary" data-action="launch">Run app</button>
                    <input class="field" data-role="process-name" placeholder="Process name" value="Background Task">
                    <input class="field" data-role="process-memory" type="number" value="64" min="1">
                    <button class="btn" data-action="process">New process</button>
                    <select class="select" data-action="algorithm">${(algorithms.algorithms || []).map(item => `<option value="${attr(item.id)}">${esc(item.name)}</option>`).join('')}</select>
                    <button class="btn" data-action="step">Step CPU</button>
                    <input class="field" data-role="task-search" placeholder="Search processes" value="${attr(state.taskSearch)}" style="min-width:180px;flex:1">
                    <select class="select" data-action="task-sort">
                        <option value="name" ${state.taskSort === 'name' ? 'selected' : ''}>Sort by name</option>
                        <option value="pid" ${state.taskSort === 'pid' ? 'selected' : ''}>Sort by PID</option>
                        <option value="memory" ${state.taskSort === 'memory' ? 'selected' : ''}>Sort by memory</option>
                    </select>
                </div>
                <div class="content grid">
                    <div class="grid three">
                        <div class="card"><h3>Apps</h3><div class="metric"><span data-role="task-running-apps">${tm.statistics.running_apps || 0}</span></div><div class="muted">Open application processes</div></div>
                        <div class="card"><h3>CPU</h3><div class="metric"><span data-role="task-cpu">${Math.round(tm.statistics.cpu_utilization || 0)}%</span></div><div class="muted">Scheduler load</div></div>
                        <div class="card"><h3>Memory</h3><div class="metric"><span data-role="task-memory">${Math.round(tm.statistics.memory_utilization || 0)}%</span></div><div class="muted"><span data-role="task-memory-detail">${tm.statistics.memory_used}/${tm.statistics.memory_total} MB</span></div></div>
                    </div>
                    <div class="card">
                        <table class="table">
                            <thead><tr><th>Name</th><th>PID</th><th>State</th><th>Opened</th><th>Window</th><th>CPU</th><th>Memory</th><th>Action</th></tr></thead>
                            <tbody data-role="task-table-body">${tasks.map(task => `
                                <tr data-task-key="${attr(taskKey(task))}" class="${task.pid && Number(task.pid) === state.activePid ? 'is-active' : ''}">
                                    ${taskRowHtml(task)}
                                </tr>
                            `).join('') || '<tr data-task-key="empty"><td colspan="8" class="muted">No tasks.</td></tr>'}</tbody>
                        </table>
                    </div>
                </div>
            </div>`;
    }

    function bindTaskManager(win) {
        if (win.dataset.taskManagerBound === 'true') return;
        win.dataset.taskManagerBound = 'true';
        const body = win.querySelector('.window-body');
        win._processChangeHandler = () => {
            if (!document.body.contains(win) || win.classList.contains('is-minimized')) return;
            refreshTaskManagerView(win).catch(() => {});
        };
        document.addEventListener('os:process-change', win._processChangeHandler);
        startTaskManagerSync(win);
        body.addEventListener('click', async event => {
            const action = event.target.closest('[data-action]')?.dataset.action;
            const end = event.target.closest('[data-end-pid]');
            if (action === 'launch') {
                const appId = $('[data-action="launch-select"]', body).value;
                let launched = false;
                if (backendToDesktop[appId]) {
                    launched = Boolean(await openApp(backendToDesktop[appId], {}, { singleton: apps[backendToDesktop[appId]]?.singleton }));
                } else {
                    const result = await api(`${API}/launch-app`, 'POST', { app_id: appId }).catch(() => null);
                    if (result?.success) {
                        launched = true;
                        emitProcessChange({ type: 'launch', appId, pid: result.process?.pid || null });
                    }
                }
                if (launched) toast('Application launched', appId);
                refreshTaskManagerView(win).catch(() => {});
            }
            if (action === 'process') {
                await api(`${API}/create-process`, 'POST', {
                    name: $('[data-role="process-name"]', body).value || 'Background Task',
                    memory: $('[data-role="process-memory"]', body).value || 64,
                    burst_time: 12,
                    io_ops: 1,
                    priority: 1
                });
                emitProcessChange({ type: 'create-process' });
                toast('Process created');
                refreshTaskManagerView(win).catch(() => {});
            }
            if (action === 'step') {
                await api(`${API}/step`, 'POST', {});
                emitProcessChange({ type: 'step' });
                refreshTaskManagerView(win).catch(() => {});
            }
            if (action === 'task-sort') {
                state.taskSort = $('[data-action="task-sort"]', body).value;
                localStorage.setItem('pusoy_task_sort', state.taskSort);
                await refreshTaskManagerView(win);
            }
            if (end) {
                await api(`${API}/task-action`, 'POST', {
                    action: 'end',
                    pid: Number(end.dataset.endPid),
                    app_id: end.dataset.endApp || null,
                    instance_id: end.dataset.endInstance || null
                });
                await closeTaskProcess(
                    Number(end.dataset.endPid),
                    end.dataset.endApp || null,
                    end.dataset.endInstance || null
                );
                console.debug('[task-manager] end task', end.dataset.endPid, end.dataset.endApp || 'process');
                toast('Task ended');
                refreshTaskManagerView(win).catch(() => {});
            }
        });
        body.addEventListener('change', async event => {
            if (event.target.matches('[data-action="algorithm"]')) {
                await api(`${API}/set-scheduling-algorithm`, 'POST', { algorithm: event.target.value });
                toast('Scheduler updated', event.target.value);
            }
            if (event.target.matches('[data-action="task-sort"]')) {
                state.taskSort = event.target.value;
                localStorage.setItem('pusoy_task_sort', state.taskSort);
                await refreshTaskManagerView(win);
            }
            if (event.target.matches('[data-role="task-search"]')) {
                state.taskSearch = event.target.value;
                refreshTaskManagerView(win).catch(() => {});
            }
        });
        body.addEventListener('input', event => {
            if (event.target.matches('[data-role="task-search"]')) {
                state.taskSearch = event.target.value;
                refreshTaskManagerView(win).catch(() => {});
            }
        });
    }

    async function renderTerminal() {
        return `
            <div class="terminal">
                <div class="terminal-output" data-role="terminal-output">${esc(state.terminalOutput)}</div>
                <form class="terminal-form">
                    <span>user@pusoy&gt;</span>
                    <input name="command" autocomplete="off" autofocus>
                    <button class="btn primary" type="submit">Run</button>
                </form>
            </div>`;
    }

    function bindTerminal(win) {
        const form = $('.terminal-form', win);
        const input = $('input[name="command"]', form);
        input.focus({ preventScroll: true });
        updateTerminalScroll(win, true);
        form.addEventListener('submit', async event => {
            event.preventDefault();
            const command = input.value.trim();
            if (!command) return;
            if (command === 'clear') {
                appendTerminalOutput(win, '', true);
            } else {
                const result = await api(`${API}/terminal-command`, 'POST', { command });
                appendTerminalOutput(win, `user@pusoy> ${command}\n${result.output}\n`);
                emitProcessChange({ type: 'terminal-command', command });
            }
            input.value = '';
            input.focus({ preventScroll: true });
        });
    }

    async function renderSettings() {
        const [settings, sys, memory] = await Promise.all([
            api(`${API}/system-settings`),
            api(`${API}/system-info`),
            api(`${API}/memory-info`)
        ]);
        const prefs = settings.settings || {};
        const system = sys.system || {};
        return `
            <div class="app-surface">
                <div class="toolbar">
                    <button class="btn primary" data-action="save">${icon('save')}Apply</button>
                </div>
                <div class="content grid two">
                    <div class="card">
                        <h3>Theme</h3>
                        <div class="toolbar" style="border:0;padding:0">
                            <button class="btn" data-theme-option="light">Light</button>
                            <button class="btn" data-theme-option="dark">Dark</button>
                        </div>
                    </div>
                    <div class="card">
                        <h3>Wallpaper</h3>
                        <div class="toolbar" style="border:0;padding:0">
                            <button class="btn" data-wallpaper-option="aurora">Aurora</button>
                            <button class="btn" data-wallpaper-option="slate">Slate grid</button>
                            <button class="btn" data-wallpaper-option="light">Light grid</button>
                            <button class="btn" data-wallpaper-option="graphite">Graphite</button>
                        </div>
                    </div>
                    <div class="card">
                        <h3>Accent</h3>
                        <input class="field" type="color" data-role="accent" value="${attr(localStorage.getItem('pusoy_accent') || prefs.accent || '#2f7df6')}">
                    </div>
                    <div class="card">
                        <h3>System information</h3>
                        <p>Host: <b>${esc(system.hostname)}</b></p>
                        <p>Version: <b>${esc(system.os_version)}</b></p>
                        <p>Kernel: <b>${esc(system.kernel)}</b></p>
                        <p>Memory: <b>${memory.allocated || memory.used || 0}/${memory.total || 0} MB</b></p>
                    </div>
                </div>
            </div>`;
    }

    function bindSettings(win) {
        const body = win.querySelector('.window-body');
        body.addEventListener('click', async event => {
            const theme = event.target.closest('[data-theme-option]')?.dataset.themeOption;
            const wallpaper = event.target.closest('[data-wallpaper-option]')?.dataset.wallpaperOption;
            if (theme) {
                localStorage.setItem('pusoy_theme', theme);
                applyPreferences();
                await api(`${API}/system-settings`, 'POST', { theme });
            }
            if (wallpaper) {
                localStorage.setItem('pusoy_wallpaper', wallpaper);
                applyPreferences();
                await api(`${API}/background-settings`, 'POST', { type: 'preset', value: wallpaper });
            }
            if (event.target.closest('[data-action="save"]')) {
                const accent = $('[data-role="accent"]', body).value;
                localStorage.setItem('pusoy_accent', accent);
                applyPreferences();
                await api(`${API}/system-settings`, 'POST', { accent });
                toast('Settings applied');
            }
        });
        body.addEventListener('input', event => {
            if (event.target.matches('[data-role="accent"]')) {
                localStorage.setItem('pusoy_accent', event.target.value);
                applyPreferences();
            }
        });
    }

    function showModal(title, content, binder) {
        $('#modalTitle').textContent = title;
        $('#modalBody').innerHTML = content;
        $('#modalBackdrop').classList.add('is-open');
        binder?.($('#modalBody'));
    }

    function hideModal() {
        $('#modalBackdrop').classList.remove('is-open');
        $('#modalBody').innerHTML = '';
    }

    async function renderDesktop() {
        const desktop = $('#desktop');
        const desktopFiles = await api(`${API}/fs/list?path=${encodeURIComponent(`${HOME}/Desktop`)}`).catch(() => ({ entries: [] }));
        const appIcons = Object.entries(apps).filter(([, meta]) => meta.desktop).map(([id, meta]) => `
            <button class="desktop-icon" data-desktop-app="${attr(id)}">
                ${glyph(meta)}
                <span>${esc(meta.name)}</span>
            </button>
        `).join('');
        const files = (desktopFiles.entries || []).map(entry => `
            <button class="desktop-icon" data-desktop-file="${attr(entry.path)}" data-entry-type="${attr(entry.type)}">
                ${fileGlyph(entry)}
                <span>${esc(entry.name)}</span>
            </button>
        `).join('');
        desktop.innerHTML = appIcons + files;
    }

    async function renderStart(query = '') {
        const grid = $('#startGrid');
        const q = query.trim().toLowerCase();
        const appItems = Object.entries(apps)
            .filter(([, meta]) => !q || meta.name.toLowerCase().includes(q))
            .map(([id, meta]) => `
                <button class="start-app" data-start-app="${attr(id)}">${glyph(meta, 'small-icon')}<span><b>${esc(meta.name)}</b><br><span class="muted">${esc(id)}</span></span></button>
            `);
        let fileItems = [];
        if (q) {
            const data = await api(`${API}/fs/list?path=${encodeURIComponent(HOME)}&search=${encodeURIComponent(query)}`).catch(() => ({ entries: [] }));
            fileItems = (data.entries || []).slice(0, 8).map(entry => `
                <button class="start-app" data-start-file="${attr(entry.path)}" data-entry-type="${attr(entry.type)}">${fileGlyph(entry)}<span><b>${esc(entry.name)}</b><br><span class="muted">${esc(entry.path.replace(`${HOME}/`, ''))}</span></span></button>
            `);
        }
        grid.innerHTML = [...appItems, ...fileItems].join('') || emptyState('No matches');
    }

    function showMenu(menu, x, y, items) {
        state.menuActions.clear();
        menu.innerHTML = items.map((item, index) => {
            if (item.separator) return '<div class="menu-separator"></div>';
            const id = `menu-${index}`;
            state.menuActions.set(id, item.action);
            return `<button class="menu-action" data-menu-id="${id}">${icon(item.icon || 'info')}${esc(item.label)}</button>`;
        }).join('');
        menu.style.left = `${Math.min(x, window.innerWidth - 220)}px`;
        menu.style.top = `${Math.min(y, window.innerHeight - 260)}px`;
        menu.classList.add('is-open');
    }

    function showDesktopContext(x, y) {
        showMenu($('#desktopMenu'), x, y, [
            { label: 'Open File Manager', icon: 'folder', action: () => openApp('filemanager', {}, { singleton: true }) },
            { label: 'New text document', icon: 'text', action: createDesktopTextFile },
            { separator: true },
            { label: 'Arrange windows', icon: 'layout', action: tileWindows },
            { label: 'Show desktop', icon: 'minimize', action: minimizeAll },
            { label: 'Settings', icon: 'settings', action: () => openApp('settings', {}, { singleton: true }) },
            { label: 'Refresh', icon: 'refresh', action: renderDesktop }
        ]);
    }

    function showFileContext(x, y) {
        showMenu($('#fileMenu'), x, y, [
            { label: 'Open', icon: 'open', action: () => state.selectedEntry && openEntry(state.selectedEntry.path, state.selectedEntry.type) },
            { label: 'Rename', icon: 'edit', action: () => renameSelected(state.windows.get('filemanager')) },
            { label: 'Delete', icon: 'trash', action: () => deleteSelected(state.windows.get('filemanager')) },
            { separator: true },
            { label: 'Properties', icon: 'info', action: showProperties }
        ]);
    }

    async function createDesktopTextFile() {
        const name = prompt('File name', 'New Document.txt');
        if (!name) return;
        await api(`${API}/fs/create-file`, 'POST', { directory: `${HOME}/Desktop`, name, content: '' });
        toast('Desktop file created', name);
        renderDesktop();
    }

    function showProperties() {
        if (!state.selectedEntry) return;
        showModal(`${state.selectedEntry.name} properties`, `
            <div class="grid">
                <div class="card">
                    <p><b>Name</b><br>${esc(state.selectedEntry.name)}</p>
                    <p><b>Path</b><br>${esc(state.selectedEntry.path)}</p>
                    <p><b>Type</b><br>${esc(state.selectedEntry.type)}</p>
                    <p><b>Opens with</b><br>${esc(apps[state.selectedEntry.association]?.name || 'File Manager')}</p>
                </div>
            </div>
        `);
    }

    function hideMenus() {
        $$('.context-menu').forEach(menu => menu.classList.remove('is-open'));
    }

    function hidePanels() {
        $('#startMenu').classList.remove('is-open');
        $('#quickPanel').classList.remove('is-open');
    }

    function minimizeAll() {
        state.windows.forEach(win => minimizeWindow(win));
    }

    function tileWindows() {
        const visible = [...state.windows.values()].filter(win => !win.classList.contains('is-minimized'));
        const width = Math.max(380, Math.floor((window.innerWidth - 28) / Math.max(1, visible.length)));
        visible.forEach((win, index) => {
            win.classList.remove('is-maximized');
            win.style.left = `${8 + index * width}px`;
            win.style.top = '8px';
            win.style.width = `${width - 8}px`;
            win.style.height = 'calc(100vh - 68px)';
        });
    }

    async function updateTray() {
        const now = new Date();
        $('#clock').textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        $('#dateText').textContent = now.toLocaleDateString([], { month: 'short', day: 'numeric' });
        try {
            const [metricsData, print] = await Promise.all([api(`${API}/system-metrics`), api(`${API}/print-system`)]);
            const metrics = metricsData.metrics || {};
            $('#trayCpu').textContent = `CPU ${Math.round(metrics.cpu_utilization || 0)}%`;
            $('#trayRam').textContent = `RAM ${Math.round(metrics.memory_utilization || 0)}%`;
            const activePrints = (print.jobs || []).filter(job => ['Waiting', 'Printing'].includes(job.status)).length;
            $('#trayPrint').textContent = `Print ${activePrints}`;
            $('#quickPanelBody').innerHTML = `
                ${metricCard('CPU', `${Math.round(metrics.cpu_utilization || 0)}%`, `${metrics.total_processes || 0} total processes`)}
                ${metricCard('Memory', `${Math.round(metrics.memory_utilization || 0)}%`, `${metrics.memory_used || 0}/${metrics.memory_total || 0} MB`)}
                ${metricCard('Print Queue', activePrints, 'Waiting or printing jobs')}
                <button class="btn primary" data-quick-open="printer">${icon('printer')}Open Print Queue</button>
            `;
        } catch (error) {
            console.warn(error);
        }
    }

    async function refreshLiveApps() {
        for (const win of state.windows.values()) {
            if (win.dataset.type === 'printer' && !win.classList.contains('is-minimized')) {
                renderWindow(win);
            }
        }
        updateTray();
    }

    function bindShell() {
        $('#startButton').addEventListener('click', async () => {
            $('#startMenu').classList.toggle('is-open');
            $('#quickPanel').classList.remove('is-open');
            await renderStart($('#globalSearch').value);
        });
        $('#trayButton').addEventListener('click', () => {
            $('#quickPanel').classList.toggle('is-open');
            $('#startMenu').classList.remove('is-open');
        });
        $('#taskbarApps').addEventListener('click', event => {
            const button = event.target.closest('[data-window-id]');
            if (!button) return;
            const win = state.windows.get(button.dataset.windowId);
            if (!win) return;
            if (win.classList.contains('is-active') && !win.classList.contains('is-minimized')) minimizeWindow(win);
            else focusWindow(win);
        });
        $('#desktop').addEventListener('dblclick', async event => {
            const appIcon = event.target.closest('[data-desktop-app]');
            const fileIcon = event.target.closest('[data-desktop-file]');
            if (appIcon) openApp(appIcon.dataset.desktopApp, {}, { singleton: apps[appIcon.dataset.desktopApp]?.singleton });
            if (fileIcon) openEntry(fileIcon.dataset.desktopFile, fileIcon.dataset.entryType);
        });
        $('#desktop').addEventListener('contextmenu', event => {
            event.preventDefault();
            showDesktopContext(event.clientX, event.clientY);
        });
        $('#desktop').addEventListener('click', event => {
            $$('.desktop-icon').forEach(iconEl => iconEl.classList.remove('is-selected'));
            event.target.closest('.desktop-icon')?.classList.add('is-selected');
        });
        $('#globalSearch').addEventListener('input', event => {
            $('#startMenu').classList.add('is-open');
            renderStart(event.target.value);
        });
        $('#startGrid').addEventListener('click', event => {
            const app = event.target.closest('[data-start-app]');
            const file = event.target.closest('[data-start-file]');
            if (app) openApp(app.dataset.startApp, {}, { singleton: apps[app.dataset.startApp]?.singleton });
            if (file) openEntry(file.dataset.startFile, file.dataset.entryType);
        });
        document.addEventListener('click', event => {
            if (event.target.closest('.context-menu')) {
                const actionId = event.target.closest('[data-menu-id]')?.dataset.menuId;
                if (actionId && state.menuActions.has(actionId)) state.menuActions.get(actionId)();
                hideMenus();
                return;
            }
            if (!event.target.closest('.panel') && !event.target.closest('#startButton') && !event.target.closest('#trayButton') && !event.target.closest('#globalSearch')) hidePanels();
            if (!event.target.closest('.context-menu')) hideMenus();
            if (event.target.closest('[data-modal-close]')) hideModal();
            const quick = event.target.closest('[data-quick-open]');
            if (quick) openApp(quick.dataset.quickOpen, {}, { singleton: true });
        });
        $('#modalClose').addEventListener('click', hideModal);
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape') {
                hideModal();
                hideMenus();
                hidePanels();
            }
            if (event.ctrlKey && event.key.toLowerCase() === 'm') {
                event.preventDefault();
                minimizeAll();
            }
        });
        document.addEventListener('os:print-change', () => {
            updateTray().catch(() => {});
        });
    }

    window.OS = {
        openApp,
        openFile,
        renderDesktop
    };

    async function boot() {
        applyPreferences();
        bindShell();
        await renderDesktop();
        await renderStart();
        await updateTray();
        setInterval(updateTray, 2500);
        await openApp('dashboard', {}, { singleton: true });
    }

    boot().catch(error => {
        console.error(error);
        toast('Boot error', error.message, 'error');
    });
})();
