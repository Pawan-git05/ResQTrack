// CTA Story Modal Interception and UI Enhancements
(function() {
    const storiesByAction = {
        donate: {
            title: 'Your Donation Heals — Animal Aid Unlimited, Udaipur',
            image: 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?q=80&w=1600&auto=format&fit=crop',
            text: 'Donations funded life-saving treatment for an injured cow. Your support pays for medication, transport, and shelter care so rescues can recover fully.',
            credit: 'Story inspired by Animal Aid Unlimited, Udaipur',
        },
        report: {
            title: 'A Report That Saved a Life — RESQ Trust, Pune',
            image: 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop',
            text: 'A citizen report alerted responders to a buffalo hit by traffic. Rapid coordination ensured safe transport to a hospital for treatment.',
            credit: 'Story inspired by RESQ Charitable Trust, Pune',
        },
        hero: {
            title: 'Become a Hero — People for Animals (PFA)',
            image: 'https://images.unsplash.com/photo-1583336663277-620dc1996580?q=80&w=1600&auto=format&fit=crop',
            text: 'PFA volunteers help goats, dogs, and other animals with pickups, first aid, and fostering. Join the network and make a direct impact.',
            credit: 'Story inspired by People for Animals (PFA)',
        },
    };

    function setupCtaInterception() {
        const modalEl = document.getElementById('storyModal');
        if (!modalEl) return;
        const bsModal = new bootstrap.Modal(modalEl);
        const title = document.getElementById('storyModalTitle');
        const img = document.getElementById('storyModalImage');
        const text = document.getElementById('storyModalText');
        const credit = document.getElementById('storyModalCredit');
        const continueBtn = document.getElementById('storyContinue');
        const backBtn = document.getElementById('storyBack');

        let pendingHref = '#';

        document.querySelectorAll('.cta-intercept').forEach((el) => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                const action = el.getAttribute('data-action');
                const story = storiesByAction[action];
                pendingHref = el.getAttribute('data-target') || el.getAttribute('href') || '#';
                if (story) {
                    title.textContent = story.title;
                    img.src = story.image;
                    img.alt = story.title;
                    text.textContent = story.text;
                    credit.textContent = story.credit;
                }
                continueBtn.setAttribute('href', pendingHref);
                bsModal.show();
            });
        });

        backBtn.addEventListener('click', () => {
            bsModal.hide();
        });
    }

    function animateCounters() {
        const targets = window.__resqCounters || { rescues: 0, ngos: 0, volunteers: 0, adoptions: 0 };
        const els = {
            rescues: document.getElementById('count-rescues'),
            ngos: document.getElementById('count-ngos'),
            volunteers: document.getElementById('count-volunteers'),
            adoptions: document.getElementById('count-adoptions'),
        };
        const duration = 1200;
        const start = performance.now();
        function step(now) {
            const progress = Math.min(1, (now - start) / duration);
            Object.entries(els).forEach(([key, el]) => {
                if (!el) return;
                const val = Math.floor(progress * targets[key]);
                el.textContent = String(val);
            });
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    function setupRevealOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
    }

    document.addEventListener('DOMContentLoaded', () => {
        setupRevealOnScroll();
        animateCounters();
    });
})();


// UI/UX Utilities
(function() {
    function ensureToastContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    class ToastManagerClass {
        constructor() {
            this.container = ensureToastContainer();
        }
        show(type, message, duration = 5000) {
            const toast = this._createToast(type, message);
            this.container.appendChild(toast);
            if (duration > 0) {
                setTimeout(() => this._removeToast(toast), duration);
            }
            return toast;
        }
        success(message, duration) { return this.show('success', message, duration); }
        error(message, duration) { return this.show('error', message, duration); }
        info(message, duration) { return this.show('info', message, duration); }
        _createToast(type, message) {
            const el = document.createElement('div');
            el.className = `toast toast-${type}`;
            el.innerHTML = `<span>${message}</span><button class="toast-close" aria-label="Close">×</button>`;
            el.querySelector('.toast-close').addEventListener('click', () => this._removeToast(el));
            return el;
        }
        _removeToast(el) {
            el.style.animation = 'fadeOut .2s ease forwards';
            el.addEventListener('animationend', () => el.remove(), { once: true });
        }
    }

    const LoadingOverlay = {
        _el: null,
        _create() {
            if (this._el) return this._el;
            const overlay = document.createElement('div');
            overlay.className = 'loading-overlay';
            const spinner = document.createElement('div');
            spinner.className = 'loading-spinner';
            overlay.appendChild(spinner);
            this._el = overlay;
            return this._el;
        },
        show() {
            const el = this._create();
            if (!document.body.contains(el)) document.body.appendChild(el);
        },
        hide() {
            if (!this._el) return;
            this._el.style.animation = 'fadeOut .2s ease forwards';
            this._el.addEventListener('animationend', () => {
                this._el.remove();
                this._el = null;
            }, { once: true });
        },
    };

    class FormValidatorClass {
        validateRequired(value) { return String(value ?? '').trim().length > 0; }
        validateEmail(email) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).trim()); }
        validatePhone(phone) { return /\d{10,}/.test(String(phone).replace(/\D/g, '')); }
        validateNumber(value) { return !Number.isNaN(Number(value)); }
        validateField(field) {
            const rules = (field.getAttribute('data-validate') || '').split('|').map(r => r.trim()).filter(Boolean);
            if (rules.length === 0) return true;
            let valid = true; let message = '';
            const value = field.value;
            for (const rule of rules) {
                if (rule === 'required' && !this.validateRequired(value)) { valid = false; message = 'This field is required.'; break; }
                if (rule === 'email' && value && !this.validateEmail(value)) { valid = false; message = 'Enter a valid email.'; break; }
                if (rule === 'phone' && !this.validatePhone(value)) { valid = false; message = 'Enter a valid phone number.'; break; }
                if (rule === 'number' && !this.validateNumber(value)) { valid = false; message = 'Enter a valid number.'; break; }
            }
            if (valid) this.showFieldSuccess(field); else this.showFieldError(field, message);
            return valid;
        }
        showFieldError(field, message) {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            const feedback = field.nextElementSibling && field.nextElementSibling.classList.contains('invalid-feedback') ? field.nextElementSibling : null;
            if (feedback) feedback.textContent = message || 'Invalid value.';
        }
        showFieldSuccess(field) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            const feedback = field.nextElementSibling && field.nextElementSibling.classList.contains('invalid-feedback') ? field.nextElementSibling : null;
            if (feedback) feedback.textContent = '';
        }
        clearFieldValidation(field) {
            field.classList.remove('is-valid', 'is-invalid');
            const feedback = field.nextElementSibling && field.nextElementSibling.classList.contains('invalid-feedback') ? field.nextElementSibling : null;
            if (feedback) feedback.textContent = '';
        }
        attachRealTimeValidation(form) {
            const fields = form.querySelectorAll('[data-validate]');
            fields.forEach((field) => {
                field.addEventListener('input', () => {
                    if (field.getAttribute('data-validate').includes('email') && !field.value) {
                        this.clearFieldValidation(field);
                        return;
                    }
                    this.validateField(field);
                });
                field.addEventListener('blur', () => this.validateField(field));
            });
        }
    }

    const ButtonLoader = {
        setLoading(button, isLoading) {
            if (!button) return;
            if (isLoading) {
                button.setAttribute('disabled', 'true');
                button.classList.add('btn-loading');
                if (!button.querySelector('.spinner-inline')) this._addSpinner(button);
            } else {
                button.removeAttribute('disabled');
                button.classList.remove('btn-loading');
                this._removeSpinner(button);
            }
        },
        _addSpinner(button) {
            const span = document.createElement('span');
            span.className = 'spinner-inline';
            button.insertBefore(span, button.firstChild);
        },
        _removeSpinner(button) {
            const s = button.querySelector('.spinner-inline');
            if (s) s.remove();
        }
    };

    window.ToastManager = window.ToastManager || new ToastManagerClass();
    window.LoadingOverlay = window.LoadingOverlay || LoadingOverlay;
    window.FormValidator = window.FormValidator || new FormValidatorClass();
    window.ButtonLoader = window.ButtonLoader || ButtonLoader;

    window.addEventListener('unhandledrejection', (event) => {
        const msg = (event && event.reason && (event.reason.message || event.reason)) || 'Unexpected error occurred.';
        if (window.ToastManager) window.ToastManager.error(String(msg));
    });
})();
