document.addEventListener("DOMContentLoaded", () => {
    
    const budgetPerfCardWrapper = document.querySelector(".budget-perf-card-wrapper");
    
    const budgetPerfStartCount = document.getElementById("budget-perf-start-count");
    const budgetPerfStopCount = document.getElementById("budget-perf-stop-count");
    const budgetPerfTotalCount = document.getElementById("budget-perf-total-count");

    const budgetPerfPagPrevBtn = document.getElementById("perf-prev-paginate-btn");
    const budgetPerfPagNextBtn = document.getElementById("perf-next-paginate-btn");


    /*-------------------------------------------------------
            TRACk PAGINATION STATE
    -------------------------------------------------------*/
    const paginationState = {
        currentPage: 1,
        pagesize: 5,
        totalCount: 0,
        nextUrl: null,
        previousUrl: null,
    };


    /*-------------------------------------------------------
            UPDATE PAGINATION UI
    -------------------------------------------------------*/
    function updatePaginationUI() {
        const {
            currentPage,
            pagesize,
            totalCount,
            nextUrl,
            previousUrl
        } = paginationState;

        const startIndex = totalCount === 0 ? 0 : (currentPage - 1) * pagesize + 1;
        const endIndex = Math.min(currentPage * pagesize, totalCount);

        budgetPerfStartCount.textContent = startIndex;
        budgetPerfStopCount.textContent = endIndex;
        budgetPerfTotalCount.textContent = totalCount;

        budgetPerfPagPrevBtn.disabled = !previousUrl;
        budgetPerfPagNextBtn.disabled = !nextUrl
    }


    /*-------------------------------------------------------
            FORMAT PERIOD START & END DATES
    --------------------------------------------------------*/
    function formatDate(startDate, endDate) {
        const start = new Date(`${startDate}T00:00:00`);
        const end = new Date(`${endDate}T00:00:00`);

        const formattedStartDate = start.toLocaleDateString("en-US", {
            month: "short",
            day: "numeric"
        });

        const formattedEndDate = end.toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric"
        });

        return `${formattedStartDate} - ${formattedEndDate}`;
    }

    /*------------------------------------------------------
           RENDER BUDGETS PERFORMANCE DATA
    ------------------------------------------------------*/
    function renderBudgetPerformanceData(data) {
        const budgetPerformances = data;

        budgetPerfCardWrapper.innerHTML = "";

        if (!budgetPerformances || budgetPerformances.length === 0) {
            budgetPerfCardWrapper.innerHTML = `
                <div class="empty-budget-perf-state">
                    <p class="empty-budget-perf-text">
                        No budget performance data available.
                    </p>
                </div>
            `;
            return;
        }

        budgetPerformances.forEach(performance => {
            
            const budgetPerfCard = document.createElement("div");
            
            const cardTitleWrapper = document.createElement("div");
            
            const catWrapper = document.createElement("div");
            
            const cardTitle = document.createElement("h3");
            cardTitle.textContent = performance.budget_title;

            const budgetStatus = document.createElement("small");

            if (performance.status === "on_track") {

                budgetStatus.textContent = ("On track");
                budgetStatus.classList.add("on-track");
            }
            
            if (performance.status === "at_risk") {

                budgetStatus.textContent = ("At risk");
                budgetStatus.classList.add("at-risk");
            }
            
            if (performance.status === "exceeded") {

                budgetStatus.textContent = ("Exceeded");
                budgetStatus.classList.add("exceeded");
            }
            
            const catTitleWrapper = document.createElement("div");
            const catNameSupText = document.createElement("span");
            
            const catNameVal = document.createElement("span");
            catNameVal.textContent = performance.category_name
                
            const progWrapper = document.createElement("div");
            
            const spentAmtWrapper = document.createElement("div");
            
            const spentWrapper = document.createElement("div");
            
            const spentVal = document.createElement("span");
            spentVal.textContent = performance.spent;

            const spentValSupText = document.createElement("span");
            spentValSupText.textContent = "spent"
            
            const totalWrapper = document.createElement("div");
            const totalValSupText = document.createElement("span");
            
            const totalVal = document.createElement("span");
            totalVal.textContent = performance.budget_amount;

            const progressBar = document.createElement("progress");
            progressBar.value = performance.spent;
            progressBar.max = performance.budget_amount;

            if (performance.status === "on_track") {
                progressBar.classList.add("on-track");
            }
            
            if (performance.status === "at_risk") {
                progressBar.classList.add("at-risk");
            }
            
            if (performance.status === "exceeded") {
                progressBar.classList.add("exceeded");
            }
            
            const spentAmtWrapper2 = document.createElement("div");
            
            const remainWrapper = document.createElement("div");
            
            const remainVal = document.createElement("span");
            remainVal.textContent = performance.remaining;

            const remainValSupText = document.createElement("span");
            remainValSupText.textContent = " remaining";

            const remainWrapper2 = document.createElement("div");
            
            const percentVal = document.createElement("span");
            percentVal.textContent = `${performance.utilization}%`;

            const percentValSupText = document.createElement("span");
            
            const periodWrapper = document.createElement("div");
            
            const typeWrapper = document.createElement("div");
            const periodTypeSupText = document.createElement("span");
            
            const periodTypeVal = document.createElement("span");
            periodTypeVal.textContent = performance.period.period_type;

            const durationWrapper = document.createElement("div");
            const durationValSupText = document.createElement("span");

            const formattedDates = formatDate(
                performance.period.start_date, performance.period.end_date
            );
            
            const durationVal = document.createElement("span");
            durationVal.textContent = formattedDates;

            cardTitleWrapper.append(cardTitle, catTitleWrapper);
            catTitleWrapper.append(catWrapper, budgetStatus);
            catWrapper.append(catNameSupText, catNameVal);

            progWrapper.append(spentAmtWrapper, progressBar, spentAmtWrapper2);
            
            spentAmtWrapper.append(spentWrapper, totalWrapper);
            spentWrapper.append(spentVal, spentValSupText);
            totalWrapper.append(totalValSupText, totalVal);
            
            spentAmtWrapper2.append(remainWrapper, remainWrapper2);
            remainWrapper.append(remainVal, remainValSupText);
            remainWrapper2.append(percentValSupText, percentVal);

            periodWrapper.append(typeWrapper, durationWrapper);
            typeWrapper.append(periodTypeSupText, periodTypeVal);
            durationWrapper.append(durationValSupText, durationVal);

            budgetPerfCard.append(
                cardTitleWrapper,
                progWrapper,
                periodWrapper,
            );

            budgetPerfCardWrapper.append(budgetPerfCard);

            budgetPerfCard.classList.add("budget-perf-card");
            
            cardTitleWrapper.classList.add("card-title-wrapper");
            
            catWrapper.classList.add("cat-wrapper");
            cardTitle.id = "budget-title";
            
            budgetStatus.classList.add("budget-status");
            budgetStatus.id = "budget-status";

            catTitleWrapper.classList.add("category-title-wrapper");
            catNameSupText.classList.add("faded");
            catNameSupText.innerText = "Category: ";
            catNameVal.classList.add("not-faded");
            catNameVal.id = "category-name";
            
            progWrapper.classList.add("progress-wrapper");
            
            spentAmtWrapper.classList.add("spent-amount-wrapper");
            
            spentWrapper.classList.add("spent-wrapper");
            spentVal.classList.add("not-faded");
            spentVal.id = "spent-value";
            spentValSupText.classList.add("faded");
            
            totalWrapper.classList.add("total-wrapper");
            totalValSupText.classList.add("faded");
            totalValSupText.innerText = "of";
            totalVal.classList.add("not-faded");
            totalVal.id = "total-value";
            
            progressBar.id = "utilization-progress";
            
            spentAmtWrapper2.classList.add("spent-amount-wrapper");
            
            remainWrapper.classList.add("remain-wrapper");
            remainVal.classList.add("not-faded");
            remainVal.id = "remaining";
            remainValSupText.classList.add("faded");
            
            remainWrapper2.classList.add("remain-wrapper");
            percentVal.classList.add("not-faded");
            percentVal.id = "util-percent";
            percentValSupText.classList.add("faded");
            
            periodWrapper.classList.add("period-wrapper");
            
            typeWrapper.classList.add("type-wrapper");
            periodTypeSupText.classList.add("faded");
            periodTypeSupText.textContent = "Period Type:";
            periodTypeVal.classList.add("not-faded");
            periodTypeVal.id = "period-type";
            
            durationWrapper.classList.add("duration-wrapper");
            durationValSupText.classList.add("faded");
            durationValSupText.textContent = "Duration:";
            durationVal.classList.add("not-faded");
            durationVal.id = "period-duration";

        });
    }


    /*------------------------------------------------------
           RENDER BUDGETS DATA
    ------------------------------------------------------*/
    async function loadBudgetPerformance(url = '/budget-performance/') {
        try {

            const response = await apiGet(url);

            paginationState.totalCount = response.data.count;
            paginationState.nextUrl = response.data.next;
            paginationState.previousUrl = response.data.previous;

            const requestedUrl = new URL(url, API_BASE_URL);

            paginationState.currentPage = Number(
                requestedUrl.searchParams.get("page") || 1
            );

            renderBudgetPerformanceData(response.data.results);

            updatePaginationUI();

            if (
                paginationState.nextUrl === null &&
                paginationState.previousUrl !== null
            ) {
                budgetPerfPagPrevBtn.disabled = true;
                budgetPerfPagPrevBtn.style.cursor = "not-allowed";

                budgetPerfPagNextBtn.disabled = false;
                budgetPerfPagNextBtn.style.cursor = "pointer";
            }

            if (
                paginationState.previousUrl === null &&
                paginationState.nextUrl !== null
            ) {
                budgetPerfPagPrevBtn.disabled = true;
                budgetPerfPagPrevBtn.style.cursor = "not-allowed";

                budgetPerfPagNextBtn.disabled = false;
                budgetPerfPagNextBtn.style.cursor = "pointer";
            }

        } catch (e) {

            budgetPerfCardWrapper.innerHTML = `
                <div class="empty-budget-perf-state">
                    <p class="error-budget-perf-text">
                        ${e.message}
                    </p>
                </div>
            `;
        }
    }

    loadBudgetPerformance()

    /*-------------------------------------------------------
            PAGINATION BUTTONS FUNCTIONALITIES
    -------------------------------------------------------*/
    budgetPerfPagNextBtn.addEventListener("click", () => {

        if (paginationState.nextUrl) {

            loadBudgetPerformance(paginationState.nextUrl);

        }
    });
    
    
    budgetPerfPagPrevBtn.addEventListener("click", () => {

        if (paginationState.previousUrl) {

            loadBudgetPerformance(paginationState.previousUrl);

        }
    });

});