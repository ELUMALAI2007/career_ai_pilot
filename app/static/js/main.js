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
