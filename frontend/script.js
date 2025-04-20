const el = id => document.getElementById(id);

document.addEventListener('DOMContentLoaded', () => {
    async function checkSession() {
        try {
            const res = await fetch('http://localhost:5000/check-session', { credentials: 'include' });
            const data = await res.json();
            if (res.ok && data.logged_in) {
                showDashboard(data.username);
            } else {
                showLogin();
            }
        } catch {
            showLogin();
        }
    }

    async function loginUser(username, password) {
        try {
            const res = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            if (res.ok) {
                showDashboard(data.username);
            } else {
                el('login-error').innerText = data.message;
            }
        } catch {
            el('login-error').innerText = 'Server error.';
        }
    }

    async function logoutUser() {
        await fetch('http://localhost:5000/logout', { method: 'POST', credentials: 'include' });
        showLogin();
    }

    function showDashboard(username) {
        el('login-screen').style.display = 'none';
        el('dashboard').style.display = 'block';
        el('welcome-username').innerText = username;
    }

    function showLogin() {
        el('login-screen').style.display = 'block';
        el('dashboard').style.display = 'none';
    }

    el('login-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const username = el('username').value.trim();
        const password = el('password').value.trim();
        if (username && password) {
            loginUser(username, password);
        }
    });

    el('logout-btn').addEventListener('click', logoutUser);

    checkSession();
});