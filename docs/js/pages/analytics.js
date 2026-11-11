document.addEventListener("DOMContentLoaded", () => {

    const cashflowPrevArrow = document.getElementById("left-arrow");
    const monthDisplay = document.getElementById("month-display");
    const cashflowNextArrow = document.getElementById("right-arrow");

    const inflowValue = document.getElementById("inflow");
    const outflowValue = document.getElementById("outflow");
    const netflowValue = document.getElementById("netflow");

    /*-------------------------------------------------------------
            Update Navigation buttons Style
    --------------------------------------------------------------*/
    function updateButtonState(button) {
        button.classList.toggle("not-disabled", !button.disabled);
        button.classList.toggle("disabled", button.disabled);
    }

    /*-------------------------------------------------------------
            Render Cashflow Data
    --------------------------------------------------------------*/
    function renderCashflowData(data, index) {
        const currentData = data[index];

        monthDisplay.textContent = `${currentData.month}, ${currentData.year}`;
        inflowValue.textContent = `$${currentData.inflow}`;
        outflowValue.textContent = `$${currentData.outflow}`;
        netflowValue.textContent = `$${currentData.net_flow}`;

        // Update previous button state
        cashflowPrevArrow.disabled = index === 0;
        updateButtonState(cashflowPrevArrow);
        
        // Update next button state
        cashflowNextArrow.disabled = index === data.length - 1;
        updateButtonState(cashflowNextArrow);
    }


    /*-------------------------------------------------------------
            Cashflow API call
    --------------------------------------------------------------*/
    async function loadCashflowData(url = '/cashflow/') {
        try {
            const response = await apiGet(url);
            
            const cashflowData = response.data;
            let dataIndex = cashflowData.length - 1;

            renderCashflowData(cashflowData, dataIndex);

            cashflowPrevArrow.addEventListener("click", () => {
                if (dataIndex > 0) {
                    dataIndex -= 1;

                    renderCashflowData(cashflowData, dataIndex);
                }
            });
            
            
            cashflowNextArrow.addEventListener("click", () => {
                if (dataIndex < cashflowData.length - 1) {
                    dataIndex += 1;
                    
                    renderCashflowData(cashflowData, dataIndex);
                }
            });
            
            console.log(response.message);
            
        } catch (error) {
           console.log(error.message);
        }
    }
    
    loadCashflowData();
    
});