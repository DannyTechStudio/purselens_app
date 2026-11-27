document.addEventListener("DOMContentLoaded", async () => {
    
    /*------------------------------------------------------------------
        RECURRING FIELDS DISPLAY HANDLING
    -------------------------------------------------------------------*/
    const recurringCheckbox = document.getElementById("transaction-is-recurring-checkbox");
    const recurringFieldsWrapper = document.getElementById("recurring-fields-wrapper");
    const frequencyInput = document.getElementById('transaction-frequency-select');
    const nextDueDateInput = document.getElementById('transaction-next-due-date-input');
    

    function toggleRecurringFields() {
        const isRecurring = recurringCheckbox.checked;

        // Toggle recurring fields
        recurringFieldsWrapper.hidden = !isRecurring;

        // Make fields required only when recurring is enabled
        frequencyInput.required = isRecurring;
        nextDueDateInput.required = isRecurring;

        // Clear values when recurring is disabled
        if (!isRecurring) {
            
            frequencyInput.value = '';
            nextDueDateInput.value = '';
        }
    }


    // Handle checkbox change
    recurringCheckbox.addEventListener("change", toggleRecurringFields);
    

    // Set the initial state
    toggleRecurringFields();



    /*------------------------------------------------------------------
        DOM ELEMENTS
    -------------------------------------------------------------------*/
    const form = document.getElementById("transaction-form");
    const transactionBtn = document.getElementById("transaction-btn");
    const transactionBtnText = document.getElementById("transaction-btn-text");
    const transactionModal = document.getElementById("transaction-modal-overlay");
    const loader = document.getElementById("loader");
    const msgDisplay = document.querySelector(".message-display");
    
    
    /*------------------------------------------------------------------
        HANDLING FORM SUBMISSION
    -------------------------------------------------------------------*/
    form.addEventListener("submit", async (event) => {
        
        event.preventDefault();

        clearError();

        const transactionTitle = document.getElementById("transaction-title-input").value.trim();
        
        const transactionAmt = document.getElementById("transaction-amount-input").value;
        
        const transactionType = form.querySelector('input[name="type"]:checked')?.value;
        
        const categorySelectOption = document.getElementById("transaction-cat-select").value;
        
        const transactionDesc = document.getElementById("description-input").value.trim();
        
        const transactionDate = document.getElementById("transaction-date-input").value;
        
        const recurringCheckbox = document.getElementById("transaction-is-recurring-checkbox");
        
        const isRecurring = recurringCheckbox.checked;
        
        const transactionFreqSelect = frequencyInput.value;
        
        const nextDueDateValue = nextDueDateInput.value;

        //--------- Required fields validation
        if (!transactionTitle ||
            !transactionAmt ||
            !transactionType ||
            !categorySelectOption ||
            !transactionDate
        ) {
            
            showError("Please fill out all required fields.");

            setTimeout(clearError, 3000);

            return;
        }


        //--------- Recurring fields validations
        if (
            isRecurring &&
            (!transactionFreqSelect || !nextDueDateValue)
        ) {
            
            showError("Please fill out all required recurring transaction fields.");
            
            setTimeout(clearError, 3000);
            
            return;
        }
        
        
        //--------- Preparing transaction payload
        const transactionData = {

            title: transactionTitle,
            amount: transactionAmt,
            type: transactionType,
            category_id: categorySelectOption,
            description: transactionDesc,
            transaction_date: transactionDate,

            is_recurring: isRecurring,

            // Include these fields only when recurring is enabled/ckecked
            ...(isRecurring && {
                frequency: transactionFreqSelect,
                next_due_date: nextDueDateValue
            })
        };


        //----------- Loading state
        setLoadingState(true);

        
        try {

            const response = await apiPost(
                form.getAttribute("action"),
                transactionData
            );

            
            //----------- Reset form fields
            form.reset();

            
            //----------- Restore recurring fields to their initial state
            toggleRecurringFields();


            //----------- Display success message
            msgDisplay.textContent = response.message;

            msgDisplay.style.display = "flex";

            msgDisplay.classList.remove("error");
            msgDisplay.classList.add("success");


            setTimeout(clearError, 3000);


            //-------- Close modal
            transactionModal.style.display = "none";

            document.body.classList.remove("modal-open");
            
        } catch (error) {
            
            showError(error.message);

            setTimeout(clearError, 5000);

        } finally {
            
            setLoadingState(false);
        }

    });



    /*------------------------------------
        Error display handler
    -------------------------------------*/
    function showError(message) {

        msgDisplay.textContent = message;

        msgDisplay.style.display = "flex";

        msgDisplay.classList.remove("succes");
        msgDisplay.classList.add("error");
        
    }

    /*------------------------------------
        Error removal handler
    -------------------------------------*/
    function clearError() {
        
        msgDisplay.textContent = "";
        
        msgDisplay.style.display = "none";
        
        msgDisplay.classList.remove("error");
        

    }

    /*------------------------------------
        Loading state handler
    -------------------------------------*/
    function setLoadingState(isLoading) {
        
        transactionBtn.disabled = isLoading;

        if (isLoading) {

            // Add loading animation - no text
            loader.style.display = "block";

            transactionBtnText.textContent = "";
            
        } else {
            
            loader.style.display = "none";

            transactionBtnText.textContent = "Create Transaction";

        }
    }

});