document.addEventListener('DOMContentLoaded', () => {
    // Элементы DOM
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const zoneTypeButtons = document.getElementById('zoneTypeButtons');
    const backToZones = document.getElementById('backToZones');
    const resetBtn = document.getElementById('resetSelection');
    const confirmBtn = document.getElementById('confirmBookingBtn');
    const timeSlotsContainer = document.getElementById('timeSlots');
    const deviceRadios = document.querySelectorAll('input[name="device"]');
    const selectionPrompt = document.getElementById('timeSelectionPrompt');
    const dateInput = document.getElementById('bookingDate');

    // Переменные состояния
    let selectedZone = null;
    let selectedStart = null;        // выбранный час начала (число)
    let selectedEnd = null;          // выбранный час окончания (число)
    let zones = [];
    let selectedDate = new Date().toISOString().split('T')[0]; // сегодня YYYY-MM-DD

    // Инициализация даты в поле ввода
    if (dateInput) {
        dateInput.value = selectedDate;
        dateInput.addEventListener('change', (e) => {
            selectedDate = e.target.value;
            resetSelection();               // сброс выбранного интервала
            if (selectedZone) renderTimeSlots();
        });
    }

    // Загрузка зон из localStorage
    function loadZones() {
        zones = getZones();
    }

    // Получить все активные брони
    function getActiveBookings() {
        return getBookings().filter(b => b.status === 'active');
    }

    // Проверка доступности интервала для зоны на дату
    function isIntervalAvailable(zoneId, date, startHour, endHour) {
        const bookings = getActiveBookings().filter(b => b.zoneId === zoneId && b.date === date);
        for (let hour = startHour; hour < endHour; hour++) {
            const conflicting = bookings.some(b => {
                const bStart = parseInt(b.startTime.split(':')[0]);
                const bEnd = parseInt(b.endTime.split(':')[0]);
                return (hour < bEnd && hour + 1 > bStart);
            });
            if (conflicting) return false;
        }
        return true;
    }

    // Обработчик выбора типа зоны (кнопки в шаге 1)
    zoneTypeButtons.addEventListener('click', (e) => {
        const btn = e.target.closest('.filter-btn');
        if (!btn) return;

        const type = btn.dataset.type;
        const zone = zones.find(z => z.type === type);
        if (!zone) {
            alert('Зона этого типа временно недоступна');
            return;
        }
        selectedZone = zone;
        resetSelection();           // сброс выбранного интервала
        step1.style.display = 'none';
        step2.style.display = 'block';
        renderTimeSlots();
    });

    // Назад к выбору зоны
    backToZones.addEventListener('click', () => {
        step2.style.display = 'none';
        step1.style.display = 'block';
        resetSelection();
        selectedZone = null;
    });

    // Сброс выбора времени
    function resetSelection() {
        selectedStart = null;
        selectedEnd = null;
        resetBtn.style.display = 'none';
        confirmBtn.style.display = 'none';
        selectionPrompt.innerText = '👇 Выберите время начала';
        if (selectedZone) renderTimeSlots();
    }

    resetBtn.addEventListener('click', resetSelection);

    // Отрисовка слотов времени для выбранной зоны и даты
    function renderTimeSlots() {
        const zone = selectedZone;
        if (!zone) return;

        const date = selectedDate;   // используем выбранную дату
        const startHour = 9;
        const endHour = 23;

        let html = '';
        for (let hour = startHour; hour < endHour; hour++) {
            const isBooked = !isIntervalAvailable(zone.id, date, hour, hour + 1);
            let slotClass = 'time-slot';
            if (isBooked) {
                slotClass += ' booked';
            } else {
                slotClass += ' free';
            }

            // Визуализация выбранного интервала
            if (selectedStart !== null && selectedEnd !== null) {
                if (hour >= selectedStart && hour < selectedEnd) {
                    slotClass += ' selected-interval';
                } else if (hour === selectedStart) {
                    slotClass += ' selected-start';
                }
            } else if (selectedStart !== null && selectedEnd === null) {
                if (hour === selectedStart) {
                    slotClass += ' selected-start';
                }
            }

            html += `<div class="${slotClass}" data-hour="${hour}" data-zone-id="${zone.id}" data-date="${date}" ${isBooked ? '' : 'data-free'}>${hour}:00</div>`;
        }
        timeSlotsContainer.innerHTML = html;

        // Привязываем обработчики ко всем слотам
        document.querySelectorAll('.time-slot').forEach(slot => {
            slot.addEventListener('click', (e) => handleSlotClick(e.currentTarget));
        });
    }

    // Обработчик клика по слоту
    function handleSlotClick(slot) {
        if (!selectedZone) return;
        if (slot.classList.contains('booked')) return;

        const hour = parseInt(slot.dataset.hour);
        const zoneId = parseInt(slot.dataset.zoneId);
        // Дата в data-атрибуте уже актуальна, можно использовать её, но для единообразия будем брать selectedDate
        // (она совпадает с той, что в data-date, так как перерисовка происходит при изменении даты)
        const date = selectedDate;

        // Случай 1: ещё не выбрано начало
        if (selectedStart === null) {
            selectedStart = hour;
            selectionPrompt.innerText = '👇 Выберите время окончания (позже начала)';
            resetBtn.style.display = 'inline-block';
            renderTimeSlots();
            return;
        }

        // Случай 2: начало выбрано, конец ещё нет
        if (selectedStart !== null && selectedEnd === null) {
            if (hour <= selectedStart) {
                alert('Время окончания должно быть позже времени начала');
                return;
            }

            // Проверяем доступность интервала
            if (!isIntervalAvailable(zoneId, date, selectedStart, hour)) {
                alert('Этот интервал недоступен (какие-то часы уже заняты)');
                return;
            }

            // Сохраняем выбранный конец, показываем кнопку подтверждения
            selectedEnd = hour;
            selectionPrompt.innerText = `Выбран интервал ${selectedStart}:00 – ${selectedEnd}:00. Нажмите "Подтвердить" для бронирования.`;
            confirmBtn.style.display = 'inline-block';
            resetBtn.style.display = 'inline-block'; // оставляем кнопку сброса
            renderTimeSlots();
        }
    }

    // Подтверждение бронирования
    confirmBtn.addEventListener('click', () => {
        if (selectedStart === null || selectedEnd === null || !selectedZone) return;

        const device = document.querySelector('input[name="device"]:checked').value;
        const newBooking = {
            zoneId: selectedZone.id,
            zoneName: selectedZone.name,
            date: selectedDate,                    // используем выбранную дату
            startTime: `${selectedStart}:00`,
            endTime: `${selectedEnd}:00`,
            status: 'active',
            participants: ['user@example.com'],
            device
        };

        addBooking(newBooking);
        alert(`Бронь создана: ${selectedZone.name}, ${selectedDate} ${selectedStart}:00–${selectedEnd}:00, устройство: ${device === 'pc' ? 'ПК' : 'Консоль'}`);

        // Сброс после подтверждения
        resetSelection();
        renderTimeSlots(); // обновляем сетку (занятые слоты станут красными)
    });

    // Инициализация
    loadZones();
});