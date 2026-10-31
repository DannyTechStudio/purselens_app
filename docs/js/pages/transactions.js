document.addEventListener('DOMContentLoaded', () => {
    const msgDisplay = document.querySelector('.message-display');
    const transactionTableBody = document.querySelector('.table-body');

    const transPaginationStartCount = document.getElementById("start-count");
    const transPaginationStopCount = document.getElementById("stop-count");
    const transPaginationTotalCount = document.getElementById("total-count");

    const prevPaginationBtn = document.getElementById("prev-paginate-btn");
    const nextPaginationBtn = document.getElementById("next-paginate-btn");

    /*-------------------------------------------------------
            TRACk PAGINATION STATE
    -------------------------------------------------------*/
    const paginationState = {
        currentPage: 1,
        pagesize: 10,
        totalCount: 0,
        nextUrl: null,
        previousUrl: null,
    };

    /*-------------------------------------------------------
            UPDATE PAGINATION UI
    -------------------------------------------------------*/
    function updatePaginationUI() {
        const {
            currentPage,
            pagesize,
            totalCount,
            nextUrl,
            previousUrl
        } = paginationState;

        const startIndex = totalCount === 0 ? 0 : (currentPage - 1) * pagesize + 1;
        const endIndex = Math.min(currentPage * pagesize, totalCount);

        transPaginationStartCount.textContent = startIndex;
        transPaginationStopCount.textContent = endIndex;
        transPaginationTotalCount.textContent = totalCount;

        prevPaginationBtn.disabled = !previousUrl;
        nextPaginationBtn.disabled = !nextUrl
        
    }


    /*-------------------------------------------------------
            RENDERING RECENT TRANSACTIONS
    -------------------------------------------------------*/
    function renderTransactionsData(data) {
        const transactions = data;

        transactionTableBody.innerHTML = "";

        if (!transactions || transactions.length === 0) {
            transactionTableBody.innerHTML = ` 
                <tr>
                    <td colspan="7">
                        <p id="message-display">No transactions available.</p>
                    </td>
                </tr> `;

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
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
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
    async function loadTransactions(url = '/transactions/') {
        try {
            const response = await apiGet(url);

            paginationState.totalCount = response.data.count;
            paginationState.nextUrl = response.data.next;
            paginationState.previousUrl = response.data.previous;

            const requestedUrl = new URL(url, API_BASE_URL);

            paginationState.currentPage = Number(
                requestedUrl.searchParams.get("page") || 1
            );

            // Render the returned transactions for the requested page
            renderTransactionsData(response.data.results);

            // Update the pagination controls
            updatePaginationUI()

            // Disabling Pagination buttons when previous or next URL are null
            if (
                paginationState.nextUrl === null &&
                paginationState.previousUrl !== null
            ) {
                nextPaginationBtn.disabled = true;
                nextPaginationBtn.style.cursor = "not-allowed";

                prevPaginationBtn.disabled = false;
                prevPaginationBtn.style.cursor = "pointer";
            }
            
            if (
                paginationState.previousUrl === null &&
                paginationState.nextUrl !== null
            ) {
                prevPaginationBtn.disabled = true;
                prevPaginationBtn.style.cursor = "not-allowed";

                nextPaginationBtn.disabled = false;
                nextPaginationBtn.style.cursor = "pointer";
            }
            
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
                <tr>
                    <td colspan="7">
                        <p id="message-display">Oops! ${error.message}</p>
                    </td>
                </tr>`;
            
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

    // Make the function accessible to other JavaScript files
    window.loadTransactions = loadTransactions;


    /*-------------------------------------------------------
            PAGINATION BUTTONS FUNCTIONALITIES
    -------------------------------------------------------*/
    nextPaginationBtn.addEventListener("click", () => {

        if (paginationState.nextUrl) {

            loadTransactions(paginationState.nextUrl);

            console.log(paginationState.nextUrl);
            
        }
    });
    
    
    prevPaginationBtn.addEventListener("click", () => {

        if (paginationState.previousUrl) {

            loadTransactions(paginationState.previousUrl);

            console.log(paginationState.previousUrl);

        }
    });
});
