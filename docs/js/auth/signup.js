document.addEventListener("DOMContentLoaded", async () => {
    
    // DOM Elements
    const form = document.getElementById("signup-form");
    const submitBtn = document.getElementById("submit-btn");
    const submitBtnText = document.querySelector(".text-span");
    const loader = document.querySelector(".loader");
    const messageOutput = document.querySelector(".message-output");
    

    // Form Submission
    form.addEventListener("submit", async (event) => {
        
        event.preventDefault();
        
        clearError();

        // Form Elements
        const firstName = document.getElementById("first-name").value.trim();
        const lastName = document.getElementById("last-name").value.trim();
        const email = document.getElementById("email-input").value.trim();
        const password = document.getElementById("password-input").value;

        if (!firstName || !lastName || !email || !password) {
            
            showError("Please fill out all fields.");

            setTimeout(() => {

                clearError();

            }, 5000);

            return
        }

        // Loading State
        setLoadingState(true);

        try {

            const response = await register({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password,
            });

            console.log("Registration successful:", response);

            messageOutput.textContent = response.message;
            messageOutput.style.display = "flex";
            messageOutput.classList.add("success");
            
            // Clear message after 5secs
            setTimeout(() => {
                
                clearError();
                
            }, 2000);
            
            // Redirect to verify page after 2secs
            setTimeout(() => {
                
                window.location.href = `../../pages/auth/verify_email.html?email=${encodeURIComponent(email)}`;
                
            }, 2000);

        } catch (error) {

            console.error(error);

            messageOutput.textContent = `${error}`;
            messageOutput.style.display = "flex",
            messageOutput.classList.add("error"); 
            
            handleRegistrationError(error);
            
            setTimeout(() => {

                clearError()
                
            }, 5000);

        } finally {

            setLoadingState(false);

        }
    });


    // Loading State
    function setLoadingState(isLoading) {
        
        submitBtn.disabled = isLoading;

        if (isLoading) {

            // Add loading animation - no text
            loader.style.display = "block";
            submitBtnText.textContent = "";
            
        } else {
            
            loader.style.display = "none";
            submitBtnText.textContent = "Create Account";

        }
    }


    // Error Handling
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


    function handleRegistrationError(error) {

        const data = error.data;

        if (!data) {

            showError(error.message);

            return;
        }

        if (data.email) {

            showError(
                Array.isArray(data.email)
                    ? data.email[0]
                    : data.email
            );

            return;
        }

        if (data.password) {

            showError(
                Array.isArray(data.password)
                    ? data.password[0]
                    : data.password
            );

            return;
        }

        if (data.first_name) {

            showError(
                Array.isArray(data.first_name)
                    ? data.first_name[0]
                    : data.first_name
            );

            return;
        }

        if (data.last_name) {

            showError(
                Array.isArray(data.last_name)
                    ? data.last_name[0]
                    : data.last_name
            );

            return;
        }

        showError(
            data.message ||
            data.detail ||
            error.message ||
            "Unable to create your account. Please try again."
        );
    }
    
});



// Toggle Password
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




