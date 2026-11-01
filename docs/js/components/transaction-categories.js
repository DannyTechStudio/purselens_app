document.addEventListener("DOMContentLoaded", () => {

    const msgDisplay = document.querySelector('.message-display');
    const transCatFilterSelect = document.getElementById("category-filter");

    /*-------------------------------------------------------
            RENDER TRANSACTION CATEGORIES
    -------------------------------------------------------*/
    function renderTranscategoryData(data) {
        const categories = data;

        if (!categories || categories.length === 0) {
            transCatFilterSelect.innerHTML = `
                <option value="">No categories available</option>
            `;
            return;
        }

        categories.forEach(category => {
            const selectOption = document.createElement('option');

            selectOption.value = category.id;
            selectOption.textContent = category.name;

            transCatFilterSelect.append(
                selectOption,
            );
        });
    }

    /*-------------------------------------------------------
            RENDERING TRANSACTION CATEGORIES
    -------------------------------------------------------*/
    async function loadTransCategories() {
        try {

            const response = await apiGet('/categories/');
            renderTranscategoryData(response.data.results);

        } catch (e) {
            console.error(e.message);

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

    loadTransCategories();

});