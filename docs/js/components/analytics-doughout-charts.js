document.addEventListener("DOMContentLoaded", () => {
    const doughnutChart = document.getElementById("doughnut-chart");
    const categoryList = document.getElementById("category-list");

    /*-------------------------------------------------------
            Chart center text plugin
    -------------------------------------------------------*/
    const centerTextPlugin = {
        id: "centerText",

        afterDraw(chart, args, options) {

            const { ctx, chartArea } = chart;

            if (!chartArea) return;

            // Retrieve custom plugin configuration
            const pluginOptions = chart.options.plugins.centerText;

            const totalExpense = Number(pluginOptions.totalExpense);
            const periodLabel = pluginOptions.periodLabel;

            const centerX = (chartArea.left + chartArea.right) / 2;
            const centerY = (chartArea.top + chartArea.bottom) / 2;

            ctx.save();

            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            // Total spending label
            ctx.font = "12px Arial";
            ctx.fillStyle = "#9aa0a6";

            ctx.fillText(
                "TOTAL SPENDING",
                centerX,
                centerY - 20
            );

            // Total spending amount
            ctx.font = "bold 24px Arial";
            ctx.fillStyle = "#292b51";

            ctx.fillText(
                `$${totalExpense.toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                })}`,
                centerX,
                centerY
            );

            // Period label
            ctx.font = "12px Arial";
            ctx.fillStyle = "#292b51";

            const maxWidth = 150;
            const words = periodLabel.split(" ");
            const lines = [];
            let currentLine = "";

            words.forEach(word => {
            
                const testLine = currentLine
                    ? `${currentLine} ${word}`
                    : word;
            
                const textWidth = ctx.measureText(testLine).width;
            
                if (textWidth > maxWidth && currentLine) {
                    lines.push(currentLine);
                    currentLine = word;
                } else {
                    currentLine = testLine;
                }
            
            });

            if (currentLine) {
                lines.push(currentLine);
            }

            // Display wrapped text
            lines.forEach((line, index) => {
            
                ctx.fillText(
                    line,
                    centerX,
                    centerY + 23 + (index * 15)
                );
            
            });

            ctx.restore();
        }
    };


    /*-------------------------------------------------------
            Chart center text plugin
    -------------------------------------------------------*/
    function generateChartColors(count) {
        const colors = [];

        for (let i = 0; i < count; i++) {
            const hue = (i * 360 / count) % 360;

            const saturation = 75;
            const lightness = 48;

            colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
        }

        return colors;
    }


    let categoryBreakdownChart = null;

    /*-------------------------------------------------------
            Monthly Summary API call
    -------------------------------------------------------*/
    async function loadCategoryBreakDown(url = 'http://127.0.0.1:8000/api/category-breakdown/') {
        try {

            const response = await apiGet(url);

            const categoryBreakdowns = response.data.categories || [];

            if (categoryBreakdowns.length === 0) {

                categoryList.innerHTML = `
                    <li class="faded">No spending data available for this period.</li>
                `;
                return;
            }

            // Extract category spending names
            const categoryNames = categoryBreakdowns.map(
                category => category.category_name
            );
            
            // Extract category spending amounts
            const categoryAmounts = categoryBreakdowns.map(
                category => category.amount
            );

            // Extract category spending percentages
            const spendingPercentages = categoryBreakdowns.map(
                category => category.spending_percentage
            );

            // Chart colors
            const chartColors = generateChartColors(categoryBreakdowns.length);

            if (categoryBreakdownChart) {
                categoryBreakdownChart.destroy();
            }

            // Create doughnut chart
            categoryBreakdownChart = new Chart(doughnutChart, {

                type: 'doughnut',

                data: {
                    labels: categoryNames,

                    datasets: [
                        {
                            data: categoryAmounts,
                            backgroundColor: chartColors,
                            borderWidth: 0,
                            hoverOffset: 4,
                            weight: 1
                        }
                    ]
                },

                plugins: [centerTextPlugin],

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    radius: "100%",

                    cutout: "80%",

                    plugins: {
                        legend: {
                            display: false
                        },
                        centerText: {
                            totalExpense: Number(response.data.total_expense),
                            periodLabel: response.data.period.label
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {

                                    const amount = context.raw;

                                    return `$${amount.toLocaleString("en-US", {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    })}`;
                                }
                            }
                        }
                    }
                }
            });

            // Populate category details list
            categoryList.innerHTML = categoryBreakdowns.map(
                (category, index) => {
                    const amount = Number(category.amount);

                    const percentage = Number(spendingPercentages[index]);
                    
                    const color = chartColors[index];

                    return `
                        <li class="category-item">
                            <div class="cat-indicator-wrapper">
                                <span
                                    class="category-indicator"
                                    style="background-color: ${color}">
                                </span>

                                <span class="category-name">
                                    ${category.category_name}
                                </span>
                            </div>
                                
                            <div class="cat-percent-amt-wrapper">
                                <span class="category-amount">
                                    $${amount.toLocaleString("en-US", {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    })}
                                </span>

                                <span class="category-percentage">
                                    ${percentage.toFixed(1)}%
                                </span>
                            </div>

                        </li>
                    `;
                }
            ).join("");

        } catch (e) {

            categoryList.innerHTML = `
                <li class="faded">
                    Failed to load your category breakdown:<br> ${e.message}
                </li>
            `;
            categoryList.classList.add('empty-state');
        }
    }

    loadCategoryBreakDown();


    /*-------------------------------------------------------
            Filtering form functionality
    -------------------------------------------------------*/
    const filterForm = document.getElementById("period-filter");

    if (!filterForm) return;

    filterForm.querySelector("select").addEventListener("change", (event) => {
        
        const formData = new FormData(filterForm);

        // Retrieve selected filtering period
        const selectedPeriod = formData.get('period');

        // Construct query parameters
        const queryParams = new URLSearchParams()

        queryParams.append('period', selectedPeriod);

        const API_BASE_URL = "http://127.0.0.1:8000/api";

        const endpoint = `${API_BASE_URL}/category-breakdown/?${queryParams.toString()}`;

        loadCategoryBreakDown(endpoint);

    });
});