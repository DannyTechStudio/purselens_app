document.addEventListener('DOMContentLoaded', () => {
    
    async function loadChartData() {
        
        const chartContainer = document.getElementById('line-chart');
        const chartEmptyState = document.getElementById('chart-empty-state');
        
        const monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        try {

            const response = await apiGet('/monthly-summary/');
            const monthlySummaries = response.data || [];

            if (monthlySummaries.length === 0) {
                
                chartContainer.style.display = 'none';
                chartEmptyState.style.display = 'flex';
                
                chartEmptyState.innerHTML = `
                    <p>No monthly data yet</p>
                    <span>
                        Add some income or expense transactions to see your trends over time.
                    </span>
                `;
                
                return;
            }
            

            chartContainer.style.display = 'block';
            chartEmptyState.style.display = 'none';

            const monthlyData = new Map(
                monthlySummaries.map(summary => [summary.month, summary])
            );

            const incomeData = monthLabels.map(month => {
                const summary = monthlyData.get(month);
                return summary ? Number(summary.income) : null;
            });

            const expenseData = monthLabels.map(month => {
                const summary = monthlyData.get(month);
                return summary ? Number(summary.expense) : null;
            });

            
            new Chart(chartContainer, {
                type: 'line',

                data: {
                    labels: monthLabels,

                    datasets: [
                        {
                            label: 'Income',
                            data: incomeData,

                            pointRadius: 1,
                            pointHoverRadius: 6,
                            borderWidth: 3,
                            borderColor: '#0077ff',
                            tension: 0.42
                        },

                        {
                            label: 'Expense',
                            data: expenseData,

                            pointRadius: 1,
                            pointHoverRadius: 6,
                            borderWidth: 3,
                            borderColor: '#ef4444',
                            tension: 0.42
                        }
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
                }
            });

        } catch (error) {
            console.error('Failed to load monthly summary:', error);

            chartContainer.style.display = 'none';
            chartEmptyState.style.display = 'flex';

            chartEmptyState.innerHTML = `
                <p>Falied to load monthly summary:<br> ${error.message}.</p>
            `;
        }

    }

    loadChartData();
});