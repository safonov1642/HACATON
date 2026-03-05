// Инициализация тестовых данных в localStorage
function initStorage() {
    if (!localStorage.getItem('zones')) {
        const zones = [
            {
                id: 1,
                name: 'Игровая зона A',
                type: 'gaming',
                capacity: 5,
                equipment: ['PC', 'PS5', 'Xbox'],
                pricePerHour: 50,
                ageRestriction: 12,
                description: 'Мощные ПК и новейшие консоли'
            },
            {
                id: 2,
                name: 'Тренировочная зона B',
                type: 'training',
                capacity: 10,
                equipment: ['Симуляторы', 'VR'],
                pricePerHour: 30,
                ageRestriction: 10,
                description: 'Место для отработки навыков'
            },
            {
                id: 3,
                name: 'Командная зона C',
                type: 'team',
                capacity: 6,
                equipment: ['Большой экран', 'ПК'],
                pricePerHour: 80,
                ageRestriction: 14,
                description: 'Для командных соревнований'
            }
        ];
        localStorage.setItem('zones', JSON.stringify(zones));
    }

    if (!localStorage.getItem('bookings')) {
        const bookings = [
            {
                id: 1,
                zoneId: 1,
                zoneName: 'Игровая зона A',
                date: '2025-03-15',
                startTime: '14:00',
                endTime: '16:00',
                status: 'active',
                participants: ['user@example.com']
            },
            {
                id: 2,
                zoneId: 2,
                zoneName: 'Тренировочная зона B',
                date: '2025-03-14',
                startTime: '10:00',
                endTime: '12:00',
                status: 'completed',
                participants: ['user@example.com']
            }
        ];
        localStorage.setItem('bookings', JSON.stringify(bookings));
    }
}

// Получить все зоны
function getZones() {
    return JSON.parse(localStorage.getItem('zones')) || [];
}

// Получить все брони
function getBookings() {
    return JSON.parse(localStorage.getItem('bookings')) || [];
}

// Сохранить брони
function saveBookings(bookings) {
    localStorage.setItem('bookings', JSON.stringify(bookings));
}

// Добавить новую бронь
function addBooking(booking) {
    const bookings = getBookings();
    const newId = bookings.length ? Math.max(...bookings.map(b => b.id)) + 1 : 1;
    const newBooking = { id: newId, ...booking };
    bookings.push(newBooking);
    saveBookings(bookings);
    return newBooking;
}

// Обновить статус брони (отмена и т.д.)
function updateBookingStatus(bookingId, status) {
    const bookings = getBookings();
    const index = bookings.findIndex(b => b.id === bookingId);
    if (index !== -1) {
        bookings[index].status = status;
        saveBookings(bookings);
        return true;
    }
    return false;
}

// Проверка доступности слота (без пересечений)
function isSlotAvailable(zoneId, date, startTime, endTime) {
    const bookings = getBookings().filter(b => b.status === 'active');
    const newStart = new Date(date + 'T' + startTime);
    const newEnd = new Date(date + 'T' + endTime);
    return !bookings.some(b => 
        b.zoneId === zoneId &&
        b.date === date &&
        !(newEnd <= new Date(date + 'T' + b.startTime) || newStart >= new Date(date + 'T' + b.endTime))
    );
}

initStorage();