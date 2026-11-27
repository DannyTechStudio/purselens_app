document.addEventListener("DOMContentLoaded", () => {

    /*---------------------------------------------------
            DOM ELEMENTS
    ---------------------------------------------------*/

    const form = document.getElementById("category-form");
    const categoryBtn = document.getElementById("add-category-btn");
    const categoryBtnText = document.getElementById("category-btn-text");
    const categoryModal = document.getElementById("category-modal-overlay");
    const loader = document.getElementById("loader");
    const msgDisplay = document.querySelector(".message-display");


    /*------------------------------------------------------------------
        HANDLING FORM SUBMISSION
    -------------------------------------------------------------------*/
    form.addEventListener("submit", async (event) => {
        
        event.preventDefault();

        clearError();

        
        const categoryName = document.getElementById("category-name-input").value.trim();
        
        const categoryTypeSelect = document.getElementById("category-type-dropdown").value;
        
        const categoryDescription = document.getElementById("description-input").value.trim();


        if (!categoryName || !categoryTypeSelect) {
            
            showError("Please fill out all required fields.");

            setTimeout(clearError, 3000);

            return;
        }


        //--------- Preparing category payload
        const categoryData = {

            name: categoryName,
            type: categoryTypeSelect,
            short_description: categoryDescription,
        };


        
        //---------- Loading state
        setLoadingState(true);


        try {

            const response = await apiPost(
                form.getAttribute("action"),
                categoryData
            );


            //----------- Reset form fields
            form.reset();


            //----------- Display success message 
            msgDisplay.textContent = response.message;

            msgDisplay.style.display = "flex";

            msgDisplay.classList.add("success");

            setTimeout(clearError, 3000);

            //-------- Close modal
            categoryModal.style.display = "none";

            document.body.classList.remove("modal-open");

            
        } catch (error) {
            
            showError(error.message);

            setTimeout(clearError, 3000);

        } finally {
            
            setLoadingState(false);
        }

    });


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
        
        categoryBtn.disabled = isLoading;

        if (isLoading) {

            // Add loading animation - no text
            loader.style.display = "block";
            categoryBtnText.textContent = "";
            
        } else {
            
            loader.style.display = "none";
            categoryBtnText.textContent = "Create Category";

        }
    }


});