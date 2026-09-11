document.addEventListener("DOMContentLoaded", async () => {

    // DOM Elements
    const form = document.getElementById("login-form");
    const loginBtn = document.getElementById("login-btn");
    const loader = document.querySelector(".loader");
    const loginBtnText = document.querySelector(".text-span");
    const messageOutput = document.querySelector(".error-output");

    // Form Submission
    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        clearError();

        // Form Elements
        const email = document.getElementById("email-input").value.trim();
        const password = document.getElementById("password-input").value.trim();

        if (!email || !password) {

            showError("Please fill out all fields.");

            setTimeout(() => {

                clearError();
            }, 5000);

            return;
        }

        setLoadingState(true);

        try {

            const response = await login(

                email,
                password,
            );

            messageOutput.textContent = response.message;
            messageOutput.style.display = "flex";
            messageOutput.classList.add("success");

            setTimeout(() => {

                clearError();
            }, 2000);

            setTimeout(() => {

                window.location.href = "../../pages/dashboard/dashboard.html";
            }, 2000);

        } catch (error) {

            console.error(error);

            messageOutput.textContent = `${error}`;
            messageOutput.style.display = "flex";
            messageOutput.classList.add("error");

            setTimeout(() => {

                clearError();
            }, 5000);

        } finally {

            setLoadingState(false);
        }
    });


    function setLoadingState(isLoading) {

        
        loginBtn.disabled = isLoading;
        
        if (isLoading) {
            
            loader.style.display = "block";
            loginBtnText.textContent = "";

        } else {
            
            loader.style.display = "none";
            loginBtnText.textContent = "Sign In";
        }
    }


    function showError(message) {

        messageOutput.textContent = message;
        messageOutput.style.display = "flex";
        messageOutput.classList.add("error");
    }


    function clearError() {

        messageOutput.textContent = "";
        messageOutput.style.display = "none";
        messageOutput.classList.remove("error");
    }

});



// Toggle Password Input
function togglePassword(btn) {
    
    const input = btn.closest('.input-wrapper').querySelector('input');
    
    input.type = input.type === 'password' ? 'text' : 'password';
    
    const isVisible = input.type === 'text';

    const label = isVisible ? 'Hide password' : 'Show password';

    btn.setAttribute('aria-pressed', String(isVisible));
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
    
    input.focus();

}

