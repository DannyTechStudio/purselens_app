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
        const emailInput = document.getElementById("email-input");
        const passwordInput = document.getElementById("password-input");
        
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

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
                redirectAfterLogin();
                
            }, 2000);

            emailInput.value = "";
            passwordInput.value = "";

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


    function redirectAfterLogin() {
        const redirectURL = sessionStorage.getItem("redirect_after_login");

        sessionStorage.removeItem("redirect_after_login");

        if (redirectURL) {
            const url = new URL(redirectURL, window.location.origin);

            if (url.origin === window.location.origin) {

                window.location.href = url.href;

                return;
            }
        }

        window.location.href = "../../pages/dashboard/dashboard.html";
    }


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

