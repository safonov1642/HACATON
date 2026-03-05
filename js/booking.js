document.addEventListener('DOMContentLoaded', () => {
    const bookingsList = document.getElementById('bookingsList');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const modal = document.getElementById('bookingModal');
    const closeModal = document.querySelector('.close-modal');
    const bookingForm = document.getElementById('bookingForm');
    const quickBookBtn = document.getElementById('quickBookBtn');
    const zoneSelect = document.getElementById('modalZoneSelect');

    let currentStatus = 'active';

    // Заполнить select зонами
    function populateZoneSelect() {
        const zones = getZones();
        zoneSelect.innerHTML = '<option value="">Выберите зону</option>';
        zones.forEach(zone => {
            const option = document.createElement('option');
            option.value = zone.id;
            option.textContent = `${zone.name} (${zone.pricePerHour} баллов/час)`;
            zoneSelect.appendChild(option);
        });
    }

    // Отобразить брони по статусу
    function renderBookings() {
        const bookings = getBookings();
        const filtered = bookings.filter(b => b.status === currentStatus);
        bookingsList.innerHTML = '';

        if (filtered.length === 0) {
            bookingsList.innerHTML = '<p style="text-align: center; color: rgba(255,255,255,0.6);">Нет бронирований</p>';
            return;
        }

        filtered.forEach(booking => {
            const item = document.createElement('div');
            item.className = 'booking-item';
            item.innerHTML = `
                <div class="booking-info">
                    <h4><i class="fas fa-gamepad"></i> ${booking.zoneName}</h4>
                    <p><i class="fas fa-calendar-day"></i> ${booking.date}</p>
                    <p><i class="fas fa-clock"></i> ${booking.startTime} — ${booking.endTime}</p>
                    <p><i class="fas fa-users"></i> Участники: ${booking.participants.join(', ')}</p>
                    <div class="extensions">
                        <span class="ext-tag"><i class="fas fa-bell"></i> Напомнить</span>
                        <span class="ext-tag"><i class="fas fa-hourglass-half"></i> Продлить</span>
                        <span class="ext-tag"><i class="fas fa-exclamation-triangle"></i> Штраф за неявку: 50</span>
                        <span class="ext-tag"><i class="fas fa-clock"></i> Лимит: 10ч/нед</span>
                    </div>
                </div>
                <div class="booking-actions">
                    ${booking.status === 'active' ? `
                        <button class="icon-btn cancel-booking" data-id="${booking.id}" title="Отменить"><i class="fas fa-times-circle"></i></button>
                        <button class="icon-btn" title="Продлить"><i class="fas fa-hourglass-start"></i></button>
                        <button class="icon-btn" title="Напомнить"><i class="fas fa-bell"></i></button>
                    ` : ''}
                </div>
            `;
            bookingsList.appendChild(item);
        });

        // Обработчики отмены
        document.querySelectorAll('.cancel-booking').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.currentTarget.dataset.id);
                if (confirm('Отменить бронь?')) {
                    updateBookingStatus(id, 'cancelled');
                    renderBookings();
                }
            });
        });
    }

    // Фильтрация
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentStatus = btn.dataset.status;
            renderBookings();
        });
    });

    // Открыть модалку бронирования
    

    closeModal.addEventListener('click', () => modal.classList.remove('active'));
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
    });

    // Обработка формы бронирования
    bookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const zoneId = parseInt(zoneSelect.value);
        if (!zoneId) {
            alert('Выберите зону');
            return;
        }
        const zone = getZones().find(z => z.id === zoneId);
        const date = document.getElementById('bookingDate').value;
        const start = document.getElementById('bookingStart').value;
        const duration = parseInt(document.getElementById('bookingDuration').value);
        const participants = document.getElementById('bookingParticipants').value.split(',').map(s => s.trim()).filter(s => s);

        if (!date || !start) {
            alert('Заполните дату и время');
            return;
        }

        const [hours, minutes] = start.split(':').map(Number);
        const startDate = new Date(date + 'T' + start);
        const endDate = new Date(startDate.getTime() + duration * 60 * 60 * 1000);
        const end = `${endDate.getHours().toString().padStart(2, '0')}:${endDate.getMinutes().toString().padStart(2, '0')}`;

        // Проверка доступности
        if (!isSlotAvailable(zoneId, date, start, end)) {
            alert('Это время уже занято. Выберите другой слот.');
            return;
        }

        const newBooking = {
            zoneId,
            zoneName: zone.name,
            date,
            startTime: start,
            endTime: end,
            status: 'active',
            participants: participants.length ? participants : ['user@example.com']
        };

        addBooking(newBooking);
        alert('Бронь создана!');
        modal.classList.remove('active');
        bookingForm.reset();
        renderBookings();
    });

    // Инициализация
    renderBookings();
});