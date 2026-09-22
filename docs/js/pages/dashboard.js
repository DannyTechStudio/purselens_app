document.addEventListener('DOMContentLoaded', () => {
    /*---------------------------------------
            DOM ELEMENTS
    ----------------------------------------*/
    const msgDisplay = document.querySelector(".message-display");

    const greetingsOutput = document.getElementById("greeting-output");
    const userNameDis = document.getElementById("user-first-name");
    const ttlIncomeVal = document.getElementById("total-income-value");
    const ttlExpenseVal = document.getElementById("total-expenses-value");
    const balanceVal = document.getElementById("balance-value");

    const dateDisplay = document.getElementById("date-display");

    const budgetTtlVal = document.getElementById("total-budget-value");
    const budgeTtlSpentVal = document.getElementById("total-spent-value");
    const remainlVal = document.getElementById("remain-value");
    
    const spentPercent = document.getElementById("spent-percent");
    const RemainlPercent = document.getElementById("remain-percent");

    const utilizationProg = document.getElementById("utilization-progress");
    const ttlBudgetAmtSpent = document.getElementById("ttl-budget-amt-spent");
    const ttlBudgetAmt = document.getElementById("ttl-budget-amt");
    const budgetAmtRemain = document.getElementById("budget-amt-remain");

    const budgetOnTrack = document.getElementById("budget-on-track");
    const budgetAtTrack = document.getElementById("budget-at-risk");
    const budgetExceeded = document.getElementById("budget-exceeded");

    
    /*-----------------------------------------------
        SUPPORTING METHODS/FUNCTIONS
    -----------------------------------------------*/

    // Render Greetings
    function getGreeting() {
        const currentHour = new Date().getHours();

        if (currentHour < 12) {
            greetingsOutput.textContent = 'Good Morning';

        } else if (12 < currentHour < 18) {
            greetingsOutput.textContent = 'Good Afternoon';
            
        } else {
            greetingsOutput.textContent = 'Good Evening';
        }
    }

    getGreeting();


    // User Info Rendering
    function renderUserFirstName(data) {
        userInfo = data.user;
        userNameDis.textContent = userInfo.first_name;
    }


    // Rendering Financial Summary
    function renderFinancialSummary(data) {
        const financial_overview = data.financial_overview;

        ttlIncomeVal.textContent = `$${financial_overview.total_income}`;
        ttlExpenseVal.textContent = `$${financial_overview.total_expense}`;
        balanceVal.textContent = `$${financial_overview.balance}`;

        return;
    }


    // Rendering Budget Overview
    function renderBudgetOverview(data) {
        const budgetOverview = data.budgets_overview;

        const totalBudget = Number(budgetOverview.total_budget_amount);
        const totalSpent = Number(budgetOverview.total_spent);
        const totalRemaining = Number(budgetOverview.total_remaining);

        dateDisplay.textContent = budgetOverview.period;

        budgetTtlVal.textContent = `$${totalBudget.toFixed(2)}`;
        budgeTtlSpentVal.textContent = `$${totalSpent.toFixed(2)}`;
        remainlVal.textContent = `$${budgetOverview.total_remaining}`;

        // Calculate Percentage
        let spentPercentValue = 0;
        let remainingPercentValue = 0;

        if (totalBudget > 0) {

            spentPercentValue = (totalSpent / totalBudget) * 100;

            remainingPercentValue = (totalRemaining / totalBudget) * 100;
        }

        spentPercent.textContent = `${spentPercentValue.toFixed(2)}%`;
        RemainlPercent.textContent = `${remainingPercentValue.toFixed(2)}%`;
        
        // Progress Bar
        utilizationProg.value = totalSpent;
        utilizationProg.max = totalBudget;
        
        // Budgets Amounts
        ttlBudgetAmtSpent.textContent = `$${totalSpent.toFixed(2)}`;
        ttlBudgetAmt.textContent = `$${totalBudget.toFixed(2)}`;
        budgetAmtRemain.textContent = `$${totalRemaining.toFixed(2)}`;
        
        // Budgets Status Counts
        budgetOnTrack.textContent = budgetOverview.budgets_on_track;
        budgetAtTrack.textContent = budgetOverview.budgets_at_risk;
        budgetExceeded.textContent = budgetOverview.budgets_exceeded;
    }


    // Rendering Top Categories
    function renderTopCategories(data) {
        const topCategories = data.top_categories;
        const categoryRankWrapper = document.querySelector('.category-rank-wrapper');

        categoryRankWrapper.innerHTML = '';

        if (!topCategories || topCategories.length === 0) {
            categoryRankWrapper.innerHTML = `
                <p class="top-cat-empty-state">No expense category available</p>
            `;
            return;
        }

        topCategories.forEach(category => {
            
            const categoryRankCard = document.createElement('div');
            categoryRankCard.dataset.categoryId = category.category_id;

            const rankCardHeadingWrapper = document.createElement('div');
            const rankCardTitle = document.createElement('span');
            const titleCardVal = document.createElement('span');
            const rankCardBottomWrapper = document.createElement('div');
            const rankCardBottomTitle = document.createElement('span');
            const rankCardBottomTitleVal = document.createElement('span');
            
            categoryRankCard.classList.add('category-rank-card');
            rankCardHeadingWrapper.classList.add('rank-card-heading-wrapper');

            rankCardTitle.classList.add('rank-card-title');
            rankCardTitle.textContent = category.category_name;

            titleCardVal.classList.add('title-card-val');
            titleCardVal.textContent = `$${Number(category.total_spent).toFixed(2)}`;

            rankCardBottomWrapper.classList.add('rank-card-bottom-wrapper');

            rankCardBottomTitle.classList.add('rank-card-bot-title');
            rankCardBottomTitle.textContent =
                `${category.transaction_count} transaction${category.transaction_count === 1 ? '' : 's'}`;
            
            rankCardBottomTitleVal.classList.add('rank-card-bot-title-val');
            rankCardBottomTitleVal.textContent =
                `${Math.floor(category.transaction_percentage)}%`;
            
            rankCardHeadingWrapper.appendChild(rankCardTitle);
            rankCardHeadingWrapper.appendChild(titleCardVal);

            rankCardBottomWrapper.appendChild(rankCardBottomTitle);
            rankCardBottomWrapper.appendChild(rankCardBottomTitleVal);

            categoryRankCard.appendChild(rankCardHeadingWrapper);
            categoryRankCard.appendChild(rankCardBottomWrapper);

            categoryRankWrapper.appendChild(categoryRankCard);
        });
    }


    // Rendering Recent Transactions
    function renderRecentTransactions(data) {
        const recentTransactions = data.recent_transactions;
        const transactionTableBody = document.querySelector('.table-body');

        transactionTableBody.innerHTMl = '';

        if (!recentTransactions || recentTransactions.length === 0) {
            transactionTableBody.innerHTML = `
                <p class="empty-transaction-state">No transactions available.</p>
            `;
            return;
        }

        recentTransactions.forEach(transaction => {
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

            transactionTypeVal.textContent = transaction.type
            transactionTitle.textContent = transaction.title
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
                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
                </svg>
            `;

            deleteTransBtn.title = 'Delete transaction';
            deleteTransBtn.classList.add('btn-icon');
            deleteTransBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                    <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5" />
                </svg>
            `;

            transactionActions.appendChild(editTransBtn);
            transactionActions.appendChild(deleteTransBtn);

            transactionRow.appendChild(transactionType);
            transactionRow.appendChild(transactionDes);
            transactionRow.appendChild(transactionTitle);
            transactionRow.appendChild(transactionCategory);
            transactionRow.appendChild(transactionDate);
            transactionRow.appendChild(transactionAmt);
            transactionRow.appendChild(transactionActions);

            transactionTableBody.appendChild(transactionRow);
            
        });
    }
    

    // Rendering Insights
    function renderInsights(data) {
        const renderInsights = data.insights;
        const insightsContainer = document.querySelector('.insight-container');

        insightsContainer.innerHTML = '';

        renderInsights.forEach(insight => {
            const insightBlock = document.createElement('div');
            const insightLabel = document.createElement('span');
            const insightMsg = document.createElement('p');

            insightBlock.classList.add('insight-block');

            insightLabel.classList.add('insight-label');
            insightLabel.textContent = insight.type;
            
            insightMsg.textContent = insight.message
            insightMsg.classList.add('insight-message');

            if (insightLabel.textContent === 'info') {
                insightBlock.classList.add('info');
            }
            
            if (insightLabel.textContent === 'success') {
                insightBlock.classList.add('success');
            }

            if (insightLabel.textContent === 'warning') {
                insightBlock.classList.add('warning');
            }

            if (insightLabel.textContent === 'danger') {
                insightBlock.classList.add('danger');
            }

            insightBlock.appendChild(insightLabel);
            insightBlock.appendChild(insightMsg);

            insightsContainer.appendChild(insightBlock);
        });
    }


    // Mother Function Rendering Dashboard Data
    function renderDashboardData(data) {

        renderUserFirstName(data);
        renderFinancialSummary(data);
        renderBudgetOverview(data);
        renderInsights(data);
        renderTopCategories(data);
        renderRecentTransactions(data);

    }

    /*-------------------------------------------------------
            DASHBOARD API CALL
    -------------------------------------------------------*/
    async function loadDashboard() {

        try {
            
            const response = await apiGet('/dashboard/');
            renderDashboardData(response.data);

            msgDisplay.textContent = response.message;
            msgDisplay.classList.add('success');
            msgDisplay.style.display = "flex";
            
            setTimeout(() => {
                msgDisplay.textContent = "";
                msgDisplay.classList.remove('success');
                msgDisplay.style.display = "none";
            }, 3000);
            
        } catch (error) {
            
            console.error("Dashboard error:", error);
            
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

    loadDashboard()
});    




