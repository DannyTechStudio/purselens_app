// DOM Elements
const heading = document.querySelector(".card-title");
const iconWrapper = document.querySelector(".icon-wrapper");
const cardSubWrapper = document.querySelector(".card-sub-wrapper");
const userEmail = document.getElementById("user-email");
const cardNotice = document.querySelector(".card-notice");
const emailLink = document.querySelector(".email-link");
const resendWrapper = document.querySelector(".resend-wrapper");
const resendBtn = document.getElementById("resend-btn");
const cardSpam = document.querySelector(".card-spam");
const resendNotice = document.querySelector(".resend-notice");
const messageOutput = document.querySelector(".message-output");

// Click Event
resendBtn.addEventListener("click", async (event) => {
    
    console.log("Resend button clicked");
    
    const params = new URLSearchParams(window.location.search);
    
    const email = params.get("email");

    resendBtn.innerHTML = `
        <span class="loader-3"></span>
    `;
    
    try {

        const response = await resendVerificationEmail(
            email,
        );

        handleResendSuccess();

        setTimeout(() => {

            messageOutput.textContent = response.messsage;
            messageOutput.style.display = "flex";
            messageOutput.classList.add("success");
        }, 2000);
        
    } catch (error) {
        
        console.error(error);

        resendBtn.innerHTML = "Resend Verification Email";
        
        setTimeout(() => {
            
            messageOutput.textContent = error;
            messageOutput.style.display = "flex";
            messageOutput.classList.add("error");
        }, 2000);
        
    } finally {}
    
});
    

function handleResendSuccess() {

    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email");

    heading.textContent = "Resend Successful";

    userEmail.textContent = email;

    cardNotice.textContent = 
        "A new verification link has been sent to your email. Visit your email inbox to verify."

    emailLink.removeAttribute("href");
    emailLink.removeAttribute("target");
    emailLink.removeAttribute("rel");

    emailLink.style.display = "none";
    emailLink.setAttribute("aria-disabled", "true");
    emailLink.classList.add("disabled");

    emailLink.innerHTML = "";

    resendWrapper.style.display = "none";
}


function handleResendFailure() {

    heading.textContent = "Unable to Resend Verification Email";

    iconWrapper.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#f20b0b" class="bi bi-ban" viewBox="0 0 16 16">
            <path d="M15 8a6.97 6.97 0 0 0-1.71-4.584l-9.874 9.875A7 7 0 0 0 15
            8M2.71 12.584l9.874-9.875a7 7 0 0 0-9.874 9.874ZM16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0"/>
        </svg>
    `;

    iconWrapper.classList.add("failure");

    cardSubWrapper.style.display = "none";

    cardNotice.textContent =
        "We couldn't resend a new verification link. Please try again.";
    
    emailLink.removeAttribute("href");
    emailLink.removeAttribute("target");
    emailLink.removeAttribute("rel");

    emailLink.setAttribute("aria-disabled", "true");
    emailLink.classList.remove("disabled");

    emailLink.style.display = "none";

    resendWrapper.style.display = "flex";

    cardSpam.style.display = "none";

}

