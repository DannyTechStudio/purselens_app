document.addEventListener('DOMContentLoaded', () => {

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
