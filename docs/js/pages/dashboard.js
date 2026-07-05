document.addEventListener('DOMContentLoaded', () => {
    
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


    // Budget Modal Functionality
    function displayTransactionModal() {
        const transactionBtn = document.getElementById('transaction-btn');
        const transactionModal = document.getElementById('transaction-modal-overlay');
        const transactionCloseModalBtn = document.getElementById('transaction-close-modal-btn');
        const transactionCancelBtn = document.getElementById('transaction-modal-cancel-btn');
        
        transactionBtn.addEventListener('click', () => {
            transactionModal.style.display = 'flex';
        });
        
        transactionCloseModalBtn.addEventListener('click', () => {
            transactionModal.style.display = 'none';
        });
        
        transactionCancelBtn.addEventListener('click', () => {
            transactionModal.style.display = 'none';
        });
    };

    displayTransactionModal();
    
});    



