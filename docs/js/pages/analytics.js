document.addEventListener("DOMContentLoaded", () => {

    const cashflowPrevArrow = document.getElementById("left-arrow");
    const monthDisplay = document.getElementById("month-display");
    const cashflowNextArrow = document.getElementById("right-arrow");

    const inflowValue = document.getElementById("inflow");
    const outflowValue = document.getElementById("outflow");
    const netflowValue = document.getElementById("netflow");

    const inflowPercentChangeVal = document.getElementById("inflow-percent-change-val");
    const outflowPercentChangeVal = document.getElementById("outflow-percent-change-val");
    const netflowPercentChangeVal = document.getElementById("netflow-percent-change-val");

    /*-------------------------------------------------------------
            Update Navigation buttons Style
    --------------------------------------------------------------*/
    function updateButtonState(button) {
        button.classList.toggle("not-disabled", !button.disabled);
        button.classList.toggle("disabled", button.disabled);
    }


    /*-------------------------------------------------------------
            Update Navigation buttons Style
    --------------------------------------------------------------*/
    function updatePercentIndicator(element, currentValue, previousValue) {
        // Remove previous styling
        element.classList.remove("increase", "decrease", "balanced");

        // Handle previous month having zero value
        if (previousValue === 0) {
            if (currentValue === 0) {
                element.textContent = "0.0% balanced";
                element.classList.add("balanced");
            } else {
                element.textContent = "No previous data";
            }

            return;
        }

        const difference = currentValue - previousValue;

        const percentage = (difference / Math.abs(previousValue)) * 100;

        // Determine direction
        if (percentage > 0) {
            
            element.textContent = `${Math.abs(percentage).toFixed(1)}% increase`;
            element.classList.add("increase");

        } else if (percentage < 0) {

            element.textContent = `${Math.abs(percentage).toFixed(1)}% decrease`;
            element.classList.add("decrease");

        } else {
            element.textContent = "0.0% balanced";
            element.classList.add("balanced");
        }
    }


    /*-------------------------------------------------------------
            Update Navigation buttons Style
    --------------------------------------------------------------*/
    function calculatePercentChange(data, currentIndex) {
        const prevIndex = currentIndex - 1;

        const indicators = [
            inflowPercentChangeVal,
            outflowPercentChangeVal,
            netflowPercentChangeVal
        ];

        // No previous month available
        if (prevIndex < 0) {
            indicators.forEach(indicator => {
                indicator.style.display = "none";
            });

            return;
        }

        // Show indicators
        indicators.forEach(indicator => {
            indicator.style.display = "";
        });


        const previous = data[prevIndex];
        const current = data[currentIndex];

        updatePercentIndicator(
            inflowPercentChangeVal,
            Number(current.inflow),
            Number(previous.inflow),
        );

        updatePercentIndicator(
            outflowPercentChangeVal,
            Number(current.outflow),
            Number(previous.outflow),
        );

        updatePercentIndicator(
            netflowPercentChangeVal,
            Number(current.net_flow),
            Number(previous.net_flow),
        );
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

            calculatePercentChange(cashflowData, dataIndex);
            
            cashflowPrevArrow.addEventListener("click", () => {
                if (dataIndex > 0) {
                    dataIndex -= 1;
                    
                    renderCashflowData(cashflowData, dataIndex);
                    calculatePercentChange(cashflowData, dataIndex);
                }
            });
            
            
            cashflowNextArrow.addEventListener("click", () => {
                if (dataIndex < cashflowData.length - 1) {
                    dataIndex += 1;
                    
                    renderCashflowData(cashflowData, dataIndex);
                    calculatePercentChange(cashflowData, dataIndex);
                }
            });
            
            console.log(response.message);
            
        } catch (error) {
           console.log(error.message);
        }
    }
    
    loadCashflowData();
    
});