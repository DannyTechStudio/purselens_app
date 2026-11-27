document.addEventListener("DOMContentLoaded", () => {
    
    /*-----------------------------------------------------
        DOM ELEMENTS
    -----------------------------------------------------*/

    const form = document.getElementById("budget-form");
    const budgetBtn = document.getElementById("add-budget-btn");
    const loader = document.getElementById("loader");
    const budgetBtnText = document.getElementById("budget-btn-text");
    const budgetModal = document.getElementById("budget-modal-overlay");
    const msgDisplay = document.querySelector(".message-display");


    /*-----------------------------------------------------
        DOM ELEMENTS
    -----------------------------------------------------*/

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        clearError
        
        
        const budgetTitle = document.getElementById("budget-title-input").value.trim();
        
        const budgetCategorySelect = document.getElementById("budget-category-select").value;
        
        const budgetAmount = document.getElementById("budget-amount-input").value.trim();
        
        const budgetPeriodType = document.getElementById("budget-period-type-select").value;
        
        const budgetStartDate = document.getElementById("budget-start-date-input").value;
        
        const budgetEndDate = document.getElementById("budget-end-date-input").value;
        

        //------------- Required fields validation
        if (!budgetTitle || 
            !budgetCategorySelect || 
            !budgetAmount || 
            !budgetPeriodType || 
            !budgetStartDate || 
            !budgetEndDate
        ) {
            showError("Please fill out all required fields.");

            setTimeout(clearError, 3000);
            
            return;
        }

        
        //-------- Preparing budget payload
        const budgetData = {

            title: budgetTitle,
            category_id: budgetCategorySelect,
            budget_amount: budgetAmount,
            period_type: budgetPeriodType,
            start_date: budgetStartDate,
            end_date: budgetEndDate,
        };
        
        
        //-------- Loading state
        setLoadingState(true);
        
        
        try {

            const response = await apiPost(
                form.getAttribute("action"),
                budgetData
            );
            
            
            //-------- Reset form fields
            form.reset();
            
            
            //-------- Display success message
            msgDisplay.textContent = response.message;

            msgDisplay.style.display = "flex";
            msgDisplay.classList.add("success");


            setTimeout(clearError, 3000);


            //-------- Close modal
            budgetModal.style.display = "none";

            document.body.classList.remove("modal-open");
            
            
        } catch (error) {
            
            showError(error.message);

            setTimeout(clearError, 3000);

        } finally {

            setLoadingState(false);
        }
        
    });


    /*-----------------------------------------------------
            HELPER METHODS
    -----------------------------------------------------*/

    //------------------- Error display handler
    function showError(message) {

        msgDisplay.textContent = message;
        msgDisplay.style.display = "flex";
        msgDisplay.classList.add("error");
        
    }


    //------------------- Error removal handler
    function clearError() {
        
        msgDisplay.textContent = "";
        msgDisplay.style.display = "none";
        msgDisplay.classList.remove("error");
    }


    //------------------- Loading state handler
    function setLoadingState(isLoading) {
        
        budgetBtn.disabled = isLoading;

        if (isLoading) {

            // Add loading animation - no text
            loader.style.display = "block";

            budgetBtnText.textContent = "";
            
        } else {
            
            loader.style.display = "none";

            budgetBtnText.textContent = "Create Budget";
        }
    }

});