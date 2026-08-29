/**
 * CareerPilot AI Client Engine
 * Theme management, password toggling, Bootstrap initializers, and interactivity.
 */

// Global Theme Switcher State & Handler
function setTheme(mode) {
    if (!['light', 'dark', 'system'].includes(mode)) return;
    localStorage.setItem('theme', mode);
    applyTheme(mode);
}

function applyTheme(mode) {
    const htmlEl = document.documentElement;
    const currentMode = mode || localStorage.getItem('theme') || 'system';

    if (currentMode === 'system') {
        htmlEl.setAttribute('data-theme', 'system');
        const isDarkOS = window.matchMedia('(prefers-color-scheme: dark)').matches;
        htmlEl.setAttribute('data-resolved-theme', isDarkOS ? 'dark' : 'light');
    } else {
        htmlEl.setAttribute('data-theme', currentMode);
        htmlEl.setAttribute('data-resolved-theme', currentMode);
    }

    // Sync Active State across UI Controls (Navbar / Settings)
    document.querySelectorAll('[data-theme-value]').forEach(btn => {
        const value = btn.getAttribute('data-theme-value');
        if (value === currentMode) {
            btn.classList.add('active');
            if (btn.querySelector('.fa-check')) {
                btn.querySelector('.fa-check').classList.remove('d-none');
            }
        } else {
            btn.classList.remove('active');
            if (btn.querySelector('.fa-check')) {
                btn.querySelector('.fa-check').classList.add('d-none');
            }
        }
    });
}

// Password Visibility Toggle Utility
function togglePasswordVisibility(inputFieldId, iconId) {
    const input = document.getElementById(inputFieldId);
    const icon = document.getElementById(iconId);

    if (input && icon) {
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }
}

// Render a small, safe Markdown subset for AI replies. Model output is always
// inserted as text nodes, never as HTML.
function renderAssistantReply(container, text) {
    container.replaceChildren();
    const lines = String(text || '').replace(/\r\n/g, '\n').split('\n');
    let list = null;
    let listType = null;
    const closeList = () => { list = null; listType = null; };

    function addInlineText(element, value) {
        value.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).forEach(part => {
            if (part.startsWith('**') && part.endsWith('**')) {
                const strong = document.createElement('strong');
                strong.textContent = part.slice(2, -2);
                element.appendChild(strong);
            } else if (part.startsWith('`') && part.endsWith('`')) {
                const code = document.createElement('code');
                code.textContent = part.slice(1, -1);
                element.appendChild(code);
            } else element.appendChild(document.createTextNode(part));
        });
    }

    lines.forEach(rawLine => {
        const line = rawLine.trim();
        const heading = line.match(/^#{1,3}\s+(.+)/);
        const ordered = line.match(/^\d+[.)]\s+(.+)/);
        const bullet = line.match(/^[-*•]\s+(.+)/);
        if (heading) {
            closeList();
            const title = document.createElement('h6');
            addInlineText(title, heading[1]);
            container.appendChild(title);
        } else if (ordered || bullet) {
            const type = ordered ? 'ol' : 'ul';
            if (!list || listType !== type) {
                list = document.createElement(type);
                listType = type;
                container.appendChild(list);
            }
            const item = document.createElement('li');
            addInlineText(item, (ordered || bullet)[1]);
            list.appendChild(item);
        } else if (line) {
            closeList();
            const paragraph = document.createElement('p');
            addInlineText(paragraph, line);
            container.appendChild(paragraph);
        } else closeList();
    });
}

window.renderAssistantReply = renderAssistantReply;

document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize Theme Preference
    const savedTheme = localStorage.getItem('theme') || 'system';
    applyTheme(savedTheme);

    // 2. Listen for System Preference Changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
        if (localStorage.getItem('theme') === 'system') {
            applyTheme('system');
        }
    });

    // 3. Initialize Bootstrap Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 4. Auto-dismiss Alert Messages after 6 seconds
    setTimeout(function () {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function (alert) {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                // Ignore if already closed
            }
        });
    }, 6000);

    console.log("CareerPilot AI Theme & Auth Engine initialized successfully.");
});
