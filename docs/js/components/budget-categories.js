document.addEventListener("DOMContentLoaded", () => {

    const msgDisplay = document.querySelector('.message-display');
    const budgetCatSelect = document.getElementById("budget-cat-select");

    /*---------------------------------------------------
            RENDER BUDGET CATEGORIES
    ---------------------------------------------------*/
    function renderBudgetsCategoryData(data) {
        const categories = data;

        if (!categories || categories.length === 0) {
            budgetCatSelect.innerHTML = `
                <option value="">No categories available</option>
            `;
            return;
        }

        categories.forEach(category => {
            const selectOption = document.createElement('option');

            selectOption.value = category.id;
            selectOption.textContent = category.name;

            budgetCatSelect.append(
                selectOption,
            );
        });
    }

    /*-------------------------------------------------------
            RENDERING TRANSACTION CATEGORIES
    -------------------------------------------------------*/
    async function loadBudgetsCategories() {
        try {

            const response = await apiGet('/categories/');
            renderBudgetsCategoryData(response.data.results);

        } catch (e) {

            msgDisplay.textContent = e.message;
            msgDisplay.classList.add('error');
            msgDisplay.style.display = "flex";
            
            setTimeout(() => {
                msgDisplay.textContent = "";
                msgDisplay.classList.remove('error');
                msgDisplay.style.display = "none";
            }, 3000);
        }
    }

    loadBudgetsCategories()
});

