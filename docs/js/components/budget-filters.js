document.addEventListener("DOMContentLoaded", () => {

    const msgDisplay = document.querySelector('.message-display');
    const filterForm = document.getElementById("filter-form");

    if (!filterForm) return;

    /*-------------------------------------------------------
            HANDLE BUDGET FILTER SUBMISSION
    -------------------------------------------------------*/
    filterForm.addEventListener("submit", async (event) => {

        // Prevent default browser form submission
        event.preventDefault();

        // Capture selected filter values
        const formData = new FormData(filterForm);

        const filters = {
            type: formData.get("type"),
            category: formData.get("category"),
            start_date: formData.get("start_date"),
            end_date: formData.get("end_date"),
            min_amount: formData.get("min_amount"),
            max_amount: formData.get("max_amount"),
        };

        /*-------------------------------------------------------
            VALIDATE FILTER VALUES
        -------------------------------------------------------*/
        
        // Validate transaction date range
        if (filters.start_date &&
            filters.end_date &&
            filters.start_date > filters.end_date
        ) {
            // alert("The end date must be on or after the start date.");
            msgDisplay.textContent = "The end date must be on or after the start date.";
            msgDisplay.classList.add('error');
            msgDisplay.style.display = "flex";
            
            setTimeout(() => {
                msgDisplay.textContent = "";
                msgDisplay.classList.remove('error');
                msgDisplay.style.display = "none";
            }, 3000);

            return;
        }

        // Validate amount range
        const minAmount = filters.min_amount !== "" ? Number(filters.min_amount) : null;
        const maxAmount = filters.max_amount !== "" ? Number(filters.max_amount) : null;

        if (minAmount !== null && 
            maxAmount !== null && 
            minAmount > maxAmount
        ) {
            msgDisplay.textContent = "Maximum amount must be greater than or equal to minimum amount.";
            msgDisplay.classList.add('error');
            msgDisplay.style.display = "flex";
            
            setTimeout(() => {
                msgDisplay.textContent = "";
                msgDisplay.classList.remove('error');
                msgDisplay.style.display = "none";
            }, 3000);

            return;
        }


        /*-------------------------------------------------------
            CONSTRUCT FILTER QUERY PARAMETERS
        -------------------------------------------------------*/
        const queryParams = new URLSearchParams();

        Object.entries(filters).forEach(([key, value]) => {

            // Ignore empty values and 'all' budget type
            if (
                value !== "" &&
                value !== null &&
                value !== "all"
            ) {
                queryParams.append(key, value);
            }
        });

        // Construct the API endpoint
        const queryString = queryParams.toString();

        const endpoint = queryString ? `/budgets/?${queryString}` : "/budgets/";
        
        await window.loadBudgets(endpoint);
    });


    /*-------------------------------------------------------
            HANDLE TRANSACTION FILTER RESET
    -------------------------------------------------------*/
    filterForm.addEventListener("reset", () => {

        // Wait for the browser to reset the form controls
        setTimeout(() => {

            // Fetch all budgets without filtering parameters
            window.loadBudgets("/budgets/");
        }, 0);
    });
    
});