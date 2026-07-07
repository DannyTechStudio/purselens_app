document.addEventListener('DOMContentLoaded', () => {

    // Budget Modal Functionality
    function displayBudgetModal() {
        const budgetBtn = document.getElementById('budget-btn');
        const budgetModal = document.getElementById('budget-modal-overlay');
        const budgetCloseModalBtn = document.getElementById('budget-close-modal-btn');
        const budgetCancelBtn = document.getElementById('budget-modal-cancel-btn');

        budgetBtn.addEventListener('click', () => {
            budgetModal.style.display = 'flex';
        });

        budgetCloseModalBtn.addEventListener('click', () => {
            budgetModal.style.display = 'none';
        });

        budgetCancelBtn.addEventListener('click', () => {
            budgetModal.style.display = 'none';
        });
    };

    displayBudgetModal();

});
