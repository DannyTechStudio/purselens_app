document.addEventListener('DOMContentLoaded', () => {
    // Modal Functionality
    // Category Modal Functionalities
    function displayCategoryModal() {
        const categoryBtn = document.getElementById('category-btn');
        const categoryModal = document.getElementById('category-modal-overlay');
        const categoryCloseModalBtn = document.getElementById('category-close-modal-btn');
        const categoryCancelBtn = document.getElementById('category-modal-cancel-btn');

        categoryBtn.addEventListener('click', () => {
            categoryModal.style.display = 'flex';
        });

        categoryCloseModalBtn.addEventListener('click', () => {
            categoryModal.style.display = 'none';
        });

        categoryCancelBtn.addEventListener('click', () => {
            categoryModal.style.display = 'none';
        });
    };

    displayCategoryModal();
});