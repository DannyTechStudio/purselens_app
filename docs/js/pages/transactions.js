document.addEventListener('DOMContentLoaded', () => {
    const msgDisplay = document.querySelector('.message-display');
    const transactionTableBody = document.querySelector('.table-body');


    // Rendering Recent Transactions
    function renderTransactionsData(data) {
        const transactions = data.result;

        transactionTableBody.innerHTML = "";

        if (!transactions || transactions.length === 0) {
            transactionTableBody.innerHTML = `
                <p class="empty-transaction-state">No transactions available.</p>
            `;
            return;
        }

        transactions.forEach(transaction => {
            const transactionRow = document.createElement('tr');

            const transactionType = document.createElement('td');
            const transactionTypeVal = document.createElement('span');
            const transactionDes = document.createElement('td');
            const transactionTitle = document.createElement('td');
            const transactionCategory = document.createElement('td');
            const transactionDate = document.createElement('td');
            const transactionAmt = document.createElement('td');
            const transactionActions = document.createElement('td');
            
            const editTransBtn = document.createElement('button');
            const deleteTransBtn = document.createElement('button');

            transactionTypeVal.textContent = transaction.type;
            transactionTitle.textContent = transaction.title;
            transactionDes.textContent = transaction.description;
            transactionCategory.textContent = transaction.category_name;
            transactionDate.textContent = transaction.transaction_date;
            transactionAmt.textContent = transaction.amount;
            
            transactionTypeVal.classList.add('transaction-type');

            if (transactionTypeVal.textContent === 'transfer') {
                transactionTypeVal.classList.add('transfer');
            }

            if (transactionTypeVal.textContent === 'income') {
                transactionTypeVal.classList.add('income');
            }

            if (transactionTypeVal.textContent === 'expense') {
                transactionTypeVal.classList.add('expense');
            }
            
            transactionRow.classList.add('transaction-row');

            transactionType.classList.add('type-cell');
            transactionType.appendChild(transactionTypeVal);

            transactionTitle.classList.add('title-cell');
            transactionDes.classList.add('description-cell');
            transactionCategory.classList.add('category-cell');
            transactionDate.classList.add('date-cell');
            transactionAmt.classList.add('amount-cell');
            transactionActions.classList.add('actions-cell');

            editTransBtn.title = 'Edit transaction';
            editTransBtn.classList.add('btn-icon');
            editTransBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                    <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
                </svg>
            `;

            deleteTransBtn.title = 'Delete transaction';
            deleteTransBtn.classList.add('btn-icon');
            deleteTransBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentcolor" class="bi bi-trash3" viewBox="0 0 16 16">
                    <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5" />
                </svg>
            `;

            transactionActions.append(editTransBtn, deleteTransBtn);

            transactionRow.append(
                transactionType,
                transactionTitle,
                transactionDes,
                transactionCategory,
                transactionDate,
                transactionAmt,
                transactionActions
            );

            transactionTableBody.appendChild(transactionRow);
        });
    }


    /*-------------------------------------------------------
            TRANSACTION API CALL
    -------------------------------------------------------*/
    async function loadTransactions() {

        try {

            const response = await apiGet('/transactions/');
            renderTransactionsData(response.data);

            msgDisplay.textContent = response.message;
            msgDisplay.classList.add('success');
            msgDisplay.style.display = "flex";
            
            setTimeout(() => {
                msgDisplay.textContent = "";
                msgDisplay.classList.remove('success');
                msgDisplay.style.display = "none";
            }, 3000);

        } catch (error) {
            console.error("Transaction error:", error);

            transactionTableBody.innerHTML = `
                <p>Oops!, ${error.messgae}</p>
            `;
            
            msgDisplay.textContent = error.message;
            msgDisplay.classList.add('error');
            msgDisplay.style.display = "flex";
            
            setTimeout(() => {
                msgDisplay.textContent = "";
                msgDisplay.classList.remove('error');
                msgDisplay.style.display = "none";
            }, 3000);
        }
    }

    loadTransactions();

});
