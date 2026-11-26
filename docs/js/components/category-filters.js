document.addEventListener("DOMContentLoaded", () => {

    const msgDisplay = document.querySelector(".message-display");
    const filterForm = document.getElementById("filter-form");

    
    if (!filterForm) return;


    /*-------------------------------------------------------
            HANDLE CATEGORY FILTER SUBMISSION
    -------------------------------------------------------*/
    filterForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const formData = new FormData(filterForm);

        const filters = {
            type: formData.get("type"),
        }


        const queryParams = new URLSearchParams();

        Object.entries(filters).forEach(([KeyboardEvent, value]) => {

            if (value !== "" && value !== null && value !== "all") {
                
                queryParams.append(KeyboardEvent, value);
            }
        });

        
        const queryString = queryParams.toString();

        const endpoint = queryString ? `/categories/?${queryString}` : '/categories/';

        await window.loadCats(endpoint);

    });



    /*-------------------------------------------------------
            HANDLE CATEGORY FILTER SUBMISSION
    -------------------------------------------------------*/
    filterForm.addEventListener("reset", () => {

        setTimeout(() => {

            window.loadCats('/categories/');
        }, 0);

    });

});