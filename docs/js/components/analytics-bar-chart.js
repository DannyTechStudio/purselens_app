document.addEventListener("DOMContentLoaded", () => {
    async function loadMonthlySummaries() {
        
        const barChartCanvas = document.getElementById("bar-chart");

        const emptyStateEle = document.getElementById("empty-monthly-summary-state");

        const monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        try {
            const response = await apiGet('/monthly-summary/');
            
            const monthlySummaries = response.data || [];

            if (monthlySummaries.length === 0) {

                emptyStateEle.style.display = "block";
                emptyStateEle.textContent = 'No monthly summaries data available yet.';
                return;
            }

            const monthData = new Map(
                monthlySummaries.map(summary => [summary.month, summary])
            );

            const incomeData = monthLabels.map(month => {
                const summary = monthData.get(month);
                return summary ? Number(summary.income) : null;
            });
            
            const expenseData = monthLabels.map(month => {
                const summary = monthData.get(month);
                return summary ? Number(summary.expense) : null;
            });
            
            const balanceData = monthLabels.map(month => {
                const summary = monthData.get(month);
                return summary ? Number(summary.balance) : null;
            });


            new Chart(barChartCanvas, {
                type: 'bar',

                data: {
                    labels: monthLabels,

                    datasets: [
                        {
                            label: 'Income',
                            data: incomeData,

                            backgroundColor: '#2ECC71',
                        },

                        {
                            label: 'Expense',
                            data: expenseData,

                            backgroundColor: '#E74C3C',
                        },

                        {
                            label: 'Balance',
                            data: balanceData,

                            backgroundColor: '#256bb1',
                        },
                    ]
                },

                plugins: {
                    legend: {
                        labels: {
                            color: '#374151',

                            font: {
                                family: 'Nunito',
                                size: 13,
                                weight: '700'
                            },

                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'cross'
                        }
                    }
                },

                options: {
                    responsive: true,

                    interaction: {
                        mode: 'index',
                        intersect: false
                    },

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                },
            });

        } catch (error) {

            emptyStateEle.style.display = "block";
            emptyStateEle.innerHTML = `Failed to load monthly summary:<br> ${error.message}`;
        }
    }

    loadMonthlySummaries();
});