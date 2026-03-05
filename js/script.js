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
