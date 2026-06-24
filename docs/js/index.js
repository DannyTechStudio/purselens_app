const headline = document.getElementById("dynamic-headline");

const headlineTexts = [
    "Take control of every cedi you earn and spend",
    "Track your finances with clarity and simplicity",
    "Discover insights that impact your spending habits",
    "Plan budgets that help you achieve your financial goals",
    "Monitor income, expenses, and savings all in one place",
    "Make smarter money decisions with powerful financial insights",
    "Everything you need for better personal financial management"
];

let currentIndex = 0;

headline.textContent = headlineTexts[currentIndex];
headline.classList.add("animate-text");

headline.addEventListener("animationiteration", () => {
    setTimeout(() => {
        currentIndex = (currentIndex + 1) % headlineTexts.length;
        headline.textContent = headlineTexts[currentIndex];
    }, 2500);
});

