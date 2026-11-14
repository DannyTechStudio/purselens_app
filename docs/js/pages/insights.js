// document.addEventListener("DOMContentLoaded", () => {
// });



const allInsightCount = document.getElementById("all-insight-count");
const infoCount = document.getElementById("info-count");
const successCount = document.getElementById("success-count");
const warningCount = document.getElementById("warning-count");
const criticalCount = document.getElementById("critical-count");

const insightWrapper = document.getElementById("insight-wrapper");
const insightEmptyState = document.querySelector(".empty-insight-state");

/*-------------------------------------------------------
        RENDERING FINANCIAL INSIGHTS
-------------------------------------------------------*/
function renderInsights(data) {
    const insights = data;

    insightWrapper.innerHTML = "";

    if (!insights || insights.length === 0) {
        insightWrapper.innerHTML = `
            <p>No insights yet.<br> Start tracking your spending to see trends.</p>
        `;
        return;
    }

    insights.forEach(insight => {
        const insightCard = document.createElement('div');
        const insightTypeWrap = document.createElement('div');
        const insightTitle = document.createElement('h2');
        const insightMsg = document.createElement('p');
        
        insightCard.classList.add("insight-card");
        insightCard.dataset.category = insight.type

        insightTypeWrap.classList.add("insight-type-wrap");
        insightTitle.classList.add("insight-heading");
        insightMsg.classList.add("insight-message");
        
        if (insight.type === "success") {
            insightTypeWrap.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-check preview-icon">
                    <circle cx="12" cy="12" r="10"/><path d="m16 9-5.5 5.5L8 12"/>
                </svg>
                <span style="font-weight: 600";>Success</span>
            `;
            insightCard.classList.add("success-type");
            insightTypeWrap.classList.add("success-type");
        }
        
        if (insight.type === "info") {
            insightTypeWrap.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bell preview-icon">
                    <path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>
                </svg>
                <span style="font-weight: 600";>Informational</span>
            `;
            insightCard.classList.add("info-type");
            insightTypeWrap.classList.add("info-type");
        }
        
        if (insight.type === "warning") {
            insightTypeWrap.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-triangle-exclamation-point preview-icon"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>
                    <path d="M12 9v4"/><path d="M12 17h.01"/>
                </svg>
                <span style="font-weight: 600";>Warning</span>
            `;
            insightCard.classList.add("warning-type");
            insightTypeWrap.classList.add("warning-type");
        }
        
        if (insight.type === "critical") {
            insightTypeWrap.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-octagon-exclamation-point preview-icon"><path d="M12 16h.01"/><path d="M12 8v4"/>
                    <path d="M15.312 2a2 2 0 0 1 1.414.586l4.688 4.688A2 2 0 0 1 22 8.688v6.624a2 2 0 0 1-.586 1.414l-4.688 4.688a2 2 0 0 1-1.414.586H8.688a2 2 0 0 1-1.414-.586l-4.688-4.688A2 2 0 0 1 2 15.312V8.688a2 2 0 0 1 .586-1.414l4.688-4.688A2 2 0 0 1 8.688 2z"/>
                </svg>
                <span style="font-weight: 600";>Critical</span>
            `;
            insightCard.classList.add("critical-type");
            insightTypeWrap.classList.add("critical-type");
        }
        
        insightTitle.textContent = insight.title;
        insightMsg.textContent = insight.message;

        insightCard.append(
            insightTypeWrap,
            insightTitle,
            insightMsg
        );
        
        insightWrapper.append(insightCard);
        
    });
}


/*-------------------------------------------------------
        FINANCIAL INSIGHTS API CALL
-------------------------------------------------------*/
async function loadFinancialInsights(url = '/insights/') {
    try {
        const response = await apiGet(url);
        
        const insights = response.data;

        let i_count = 0;
        let s_count = 0;
        let w_count = 0;
        let c_count = 0;

        allInsightCount.textContent = `(${insights.length})`;

        insights.forEach(insight => {

            if (insight.type === "info") {
                i_count++;
            }
            
            if (insight.type === "success") {
                s_count++;
            }
            
            if (insight.type === "warning") {
                w_count++;
            }

            if (insight.type === "warning") {
                c_count++;
            }
            
        });

        infoCount.textContent = `(${i_count})`;
        successCount.textContent = `(${s_count})`;
        warningCount.textContent = `(${w_count})`;
        criticalCount.textContent = `(${c_count})`;
        
        renderInsights(insights);

    } catch (error) {
        insightWrapper.innerHTML = `
            <p class="error-state">Oop! Something went wrong.<br> ${error.message}.</p>
        `;
    }
}

loadFinancialInsights();

window.loadInsights = loadFinancialInsights;


/*-------------------------------------------------------
        INSIGHT CARD FILTERING FUNCTIONALITY
-------------------------------------------------------*/
const insightFilterBtns = document.querySelectorAll(".insight-metrics-filter-btn");

insightFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {

        insightFilterBtns.forEach(b => b.classList.remove('in-use'));
        btn.classList.add('in-use');
        
        const filter = btn.dataset.filter;
        
        // Get the currently available insight cards
        const insightCards = document.querySelectorAll(".insight-card");

        let visibleCards = 0;

        insightCards.forEach(card => {
            const match = filter === 'all' || card.dataset.category === filter;

            if (match) {
                visibleCards++;
                 
                card.classList.remove('hidden');
                
                setTimeout(() => {
                    card.style.display = 'flex';
                }, 100);

            } else {
                card.classList.add('hidden');

                setTimeout(() => {
                    if (card.classList.contains('hidden')) {
                        card.style.display = 'none';
                    }
                }, 100);

            }
        });
        
         // Handle empty state
        if (visibleCards === 0) {
            insightWrapper.style.display = 'none';
            insightEmptyState.classList.remove('hidden');
        } else {
            insightWrapper.style.display = 'grid';
            insightEmptyState.classList.add('hidden');
        }
    });
});






