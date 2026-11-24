document.addEventListener("DOMContentLoaded", () => {

    const descriptionInput = document.getElementById("description-input");
    const descriptionWordCounter = document.getElementById("word-counter");
    
    const MAX_DESCRIPTION_WORDS = 10;
    
    
    function countWords(text) {
        return text.trim().split(/\s+/).filter(Boolean).length;
    }
    
    
    function updateDescriptionCounter() {
        const wordCount = countWords(descriptionInput.value);
        
        descriptionWordCounter.textContent = `${wordCount}/${MAX_DESCRIPTION_WORDS} words`;
        
        descriptionWordCounter.classList.toggle(
            "limit-reached",
            wordCount >= MAX_DESCRIPTION_WORDS
        );
    }
    
    
    descriptionInput.addEventListener("beforeinput", (event) => {
        // Allow deletion and other editing operations
        if (event.inputType.startsWith("delete")) return;
        
        const start = descriptionInput.selectionStart;
        const end = descriptionInput.selectionEnd;
    
        const currentValue = descriptionInput.value;
    
        // Determine what the text that would result from the user's input.
        const insertedText = event.data ?? "";
        
        const updatedValue =
            currentValue.slice(0, start) +
            insertedText +
            currentValue.slice(end);
        
        // Prevent input if it would exceed the word limit
        if (countWords(updatedValue) > MAX_DESCRIPTION_WORDS) {
            event.preventDefault();
        }
        
    });
    
    
    descriptionInput.addEventListener("input", updateDescriptionCounter);
    // descriptionInput.addEventListener("input", updateDescriptionCounter());
    
    // Initialize the counter
    updateDescriptionCounter();
    
    
});