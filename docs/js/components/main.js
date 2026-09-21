document.addEventListener('DOMContentLoaded', () => {
    
    // Category Modal Functionalities
    function displayCategoryModal() {
        const categoryBtn = document.getElementById('category-btn');
        
        if (!categoryBtn) return; // skip — element not found in DOM
        
        const categoryModal = document.getElementById('category-modal-overlay');
        const categoryCloseModalBtn = document.getElementById('category-close-modal-btn');
        const categoryCancelBtn = document.getElementById('category-modal-cancel-btn');
        
        categoryBtn.addEventListener('click', () => {
            categoryModal.style.display = 'flex';
            document.body.classList.add("modal-open");
        });
        
        categoryCloseModalBtn.addEventListener('click', () => {
            categoryModal.style.display = 'none';
            document.body.classList.remove("modal-open");
        });
        
        categoryCancelBtn.addEventListener('click', () => {
            categoryModal.style.display = 'none';
            document.body.classList.remove("modal-open");
        });
    };


    // Budget Modal Functionality
    function displayBudgetModal() {
        const budgetBtn = document.getElementById('budget-btn');
        
        if (!budgetBtn) return; // skip — element not found in DOM

        const budgetModal = document.getElementById('budget-modal-overlay');
        const budgetCloseModalBtn = document.getElementById('budget-close-modal-btn');
        const budgetCancelBtn = document.getElementById('budget-modal-cancel-btn');
        
        budgetBtn.addEventListener('click', () => {
            budgetModal.style.display = 'flex';
            document.body.classList.add("modal-open");
        });
        
        budgetCloseModalBtn.addEventListener('click', () => {
            budgetModal.style.display = 'none';
            document.body.classList.remove("modal-open");
        });
        
        budgetCancelBtn.addEventListener('click', () => {
            budgetModal.style.display = 'none';
            document.body.classList.remove("modal-open");
        });
    };

    
    
    // Transaction Modal Functionality
    function displayTransactionModal() {
        const transactionBtn = document.getElementById('transaction-btn');
        
        if (!transactionBtn) return; // skip — element not found in DOM

        const transactionModal = document.getElementById('transaction-modal-overlay');
        const transactionCloseModalBtn = document.getElementById('transaction-close-modal-btn');
        const transactionCancelBtn = document.getElementById('transaction-modal-cancel-btn');
        
        transactionBtn.addEventListener('click', () => {
            transactionModal.style.display = 'flex';
            document.body.classList.add("modal-open");
        });
        
        transactionCloseModalBtn.addEventListener('click', () => {
            transactionModal.style.display = 'none';
            document.body.classList.remove("modal-open");
        });
        
        transactionCancelBtn.addEventListener('click', () => {
            transactionModal.style.display = 'none';
            document.body.classList.remove("modal-open");
        });
    };
    
    

    // Functions Calls
    displayCategoryModal();
    displayBudgetModal();
    displayTransactionModal();
});    



