document.addEventListener('DOMContentLoaded', () => {
    const burgerBtn = document.getElementById('burgerBtn');
    const menuOverlay = document.getElementById('menuOverlay');
    const closeMenu = document.getElementById('closeMenu');

    function openMenu() {
        menuOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // запрет прокрутки фона
    }

    function closeMenuFunc() {
        menuOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    burgerBtn.addEventListener('click', openMenu);

    closeMenu.addEventListener('click', closeMenuFunc);

    // Клик по оверлею (затемненной области) тоже закрывает меню
    menuOverlay.addEventListener('click', (e) => {
        if (e.target === menuOverlay) {
            closeMenuFunc();
        }
    });
});
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Получение токена из localStorage
function getToken() {
    return localStorage.getItem('access_token');
}

// Сохранение токена
function setToken(token) {
    localStorage.setItem('access_token', token);
}

// Удаление токена (выход)
function removeToken() {
    localStorage.removeItem('access_token');
}

// Базовый fetch с авторизацией
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const config = {
        ...options,
        headers,
    };
    const response = await fetch(url, config);
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Ошибка запроса');
    }
    return response.json();
}

// Примеры методов
async function getZones(type = '') {
    const query = type ? `?type=${type}` : '';
    return apiFetch(`/zones${query}`);
}

async function getZoneById(id) {
    return apiFetch(`/zones/${id}`);
}

async function createBooking(bookingData) {
    return apiFetch('/bookings', {
        method: 'POST',
        body: JSON.stringify(bookingData),
    });
}

async function getMyBookings(status = '') {
    const query = status ? `?status=${status}` : '';
    return apiFetch(`/bookings/my${query}`);
}

async function cancelBooking(bookingId) {
    return apiFetch(`/bookings/${bookingId}/cancel`, {
        method: 'PATCH',
    });
}

async function getSchedule(date) {
    return apiFetch(`/calendar/schedule?date=${date}`);
}

// Админские методы
async function adminGetAllBookings(filters = {}) {
    const params = new URLSearchParams(filters).toString();
    return apiFetch(`/admin/bookings?${params}`);
}

async function adminMarkNoShow(bookingId, userId) {
    return apiFetch(`/admin/bookings/${bookingId}/mark-no-show`, {
        method: 'POST',
        body: JSON.stringify({ user_id: userId }),
    });
}

async function adminGetRestrictions() {
    return apiFetch('/admin/restrictions');
}

async function adminCreateRestriction(data) {
    return apiFetch('/admin/restrictions', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

async function adminDeleteRestriction(id) {
    return apiFetch(`/admin/restrictions/${id}`, {
        method: 'DELETE',
    });
}

async function adminBlockUser(userId, blockUntil) {
    return apiFetch(`/admin/users/${userId}/block?block_until=${blockUntil}`, {
        method: 'POST',
    });
}

async function adminUnblockUser(userId) {
    return apiFetch(`/admin/users/${userId}/unblock`, {
        method: 'POST',
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const dateInput = document.getElementById('calendar-date');
    const prevBtn = document.getElementById('prev-day');
    const nextBtn = document.getElementById('next-day');
    const todayBtn = document.getElementById('today-btn');
    const container = document.getElementById('calendar-container');

    let currentDate = new Date();
    dateInput.value = formatDate(currentDate);
    await loadSchedule(currentDate);

    prevBtn.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() - 1);
        dateInput.value = formatDate(currentDate);
        loadSchedule(currentDate);
    });

    nextBtn.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() + 1);
        dateInput.value = formatDate(currentDate);
        loadSchedule(currentDate);
    });

    todayBtn.addEventListener('click', () => {
        currentDate = new Date();
        dateInput.value = formatDate(currentDate);
        loadSchedule(currentDate);
    });

    dateInput.addEventListener('change', () => {
        currentDate = new Date(dateInput.value + 'T00:00:00');
        loadSchedule(currentDate);
    });

    async function loadSchedule(date) {
        const dateStr = formatDate(date);
        const data = await getSchedule(dateStr);
        renderCalendar(data, dateStr);
    }

    function renderCalendar(data, dateStr) {
        // data = { zones: [{ zone_id, zone_name, bookings: [{start, end, user_name}] }], global_restrictions: [...] }
        const zones = data.zones;
        const restrictions = data.global_restrictions; // интервалы, когда вообще нельзя бронировать

        // Построим временные слоты с 8:00 до 23:00 с шагом 1 час
        const startHour = 8;
        const endHour = 23;
        const hours = [];
        for (let h = startHour; h < endHour; h++) {
            hours.push(`${h}:00`);
        }

        let html = '<div class="calendar-grid">';
        // Заголовки зон
        html += '<div class="time-column">Время</div>';
        zones.forEach(zone => {
            html += `<div class="zone-header">${zone.zone_name}</div>`;
        });

        // Строки времени
        hours.forEach((hour, index) => {
            const currentHour = startHour + index;
            html += `<div class="time-column">${hour}</div>`;
            zones.forEach(zone => {
                const cellStart = new Date(`${dateStr}T${currentHour}:00:00`);
                const cellEnd = new Date(`${dateStr}T${currentHour + 1}:00:00`);
                // Проверка на глобальные ограничения
                const isRestricted = restrictions.some(r => {
                    const rStart = new Date(r.start);
                    const rEnd = new Date(r.end);
                    return (cellStart < rEnd && cellEnd > rStart);
                });
                // Проверка на бронь
                const booking = zone.bookings.find(b => {
                    const bStart = new Date(b.start);
                    const bEnd = new Date(b.end);
                    return (cellStart < bEnd && cellEnd > bStart);
                });
                let cellClass = 'calendar-cell free';
                let title = 'Свободно';
                if (isRestricted) {
                    cellClass = 'calendar-cell restricted';
                    title = 'Занято (пары)';
                } else if (booking) {
                    cellClass = 'calendar-cell booked';
                    title = `Занято: ${booking.user_name} (${new Date(booking.start).getHours()}:00 - ${new Date(booking.end).getHours()}:00)`;
                }
                html += `<div class="${cellClass}" title="${title}" data-zone="${zone.zone_id}" data-start="${cellStart.toISOString()}" data-end="${cellEnd.toISOString()}" data-free="${!isRestricted && !booking}">${title}</div>`;
            });
        });
        html += '</div>';
        container.innerHTML = html;

        // Добавить обработчики клика на свободные ячейки
        document.querySelectorAll('.calendar-cell.free').forEach(cell => {
            cell.addEventListener('click', () => {
                const zoneId = cell.dataset.zone;
                const start = cell.dataset.start;
                // Переход на страницу создания брони
                window.location.href = `booking-new.html?zoneId=${zoneId}&start=${start}`;
            });
        });
    }

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
});q