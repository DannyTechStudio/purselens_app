document.addEventListener("DOMContentLoaded", async () => {

    const userEmail = document.getElementById("user-email");
    const emailLink = document.querySelector(".email-link");

    const params = new URLSearchParams(window.location.search);

    const email = params.get("email");
    const token = params.get("token");


    if (email && !token) {
        userEmail.textContent = email;

        const providerUrl = getEmailProviderUrl(email);

        if (providerUrl) {
            
            emailLink.href = providerUrl;
            emailLink.target = "_blank";
            emailLink.rel = "noopener noreferrer";

        } else {

            emailLink.removeAttribute("href");
            emailLink.removeAttribute("target");
            emailLink.removeAttribute("rel");

            emailLink.textContent = "Open your email";

            setTimeout(() => {

                messageOutput.textContent =
                    "Please open your email provider and check your inbox for the PurseLens verification email.";
                
                messageOutput.style.display = "flex";
                messageOutput.classList.add("normal");

            }, 10000);
        }

        return;
    }


    if (!token) {
        
        messageOutput.textContent =
            "Verification token not found! Request a new verification email.";

        messageOutput.style.display = "flex";
        messageOutput.classList.add("error");

        return;
    }

    showVerifyingState();
    
    try {
        
        const response = await verifyEmail(token);

        console.log("Email verification successful:", response);

        showVerificationSuccess();
        
        setTimeout(() => {

            window.location.href = "../../pages/dashboard/dashboard.html";

        }, 2000);

    } catch (error) {

        console.error("Email verification failed:", error);
        showVerificationError();
    }

});


// DOM Elements
const heading = document.querySelector(".card-title");
const iconWrapper = document.querySelector(".icon-wrapper");
const cardSubWrapper = document.querySelector(".card-sub-wrapper");
const cardNotice = document.querySelector(".card-notice");
const emailLink = document.querySelector(".email-link");
const resendWrapper = document.querySelector(".resend-wrapper");
const cardSpam = document.querySelector(".card-spam");
const resendNotice = document.querySelector(".resend-notice");
const messageOutput = document.querySelector(".message-output");


// Email Provider
function getEmailProviderUrl(email) {
    const domain = email.split("@")[1]?.toLowerCase();

    if (domain === "gmail.com") {

        return "https://mail.google.com/";
    }

    if (domain === "outlook.com" ||
        domain === "hotmail.com" ||
        domain === "live.com"
    ) {

        return "https://outlook.live.com/mail/0/inbox";
    }

    if (domain === "yahoo.com") {

        return "https://mail.yahoo.com/";
    }

    return null
}


// Verifying State
function showVerifyingState() {

    heading.textContent = "Verifying Your Account";

    iconWrapper.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#292b51" class="bi bi-gear" viewBox="0 0 16 16">
            <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/>
            <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"/>
        </svg>
    `;

    cardSubWrapper.style.display = "none";

    cardNotice.textContent = "Please wait while we confirm your email address.";

    emailLink.removeAttribute("href");
    emailLink.removeAttribute("target");
    emailLink.removeAttribute("rel");

    emailLink.setAttribute("aria-disabled", "true");
    
    emailLink.style.display = "flex";
    emailLink.innerHTML = `
        <span class="loader-2"></span>
    `;
    
    resendWrapper.style.display = "none";

    cardSpam.style.display = "none";

}


// Verification Successful State
function showVerificationSuccess() {

    heading.textContent = "Email Verified Successfully";

    cardNotice.textContent =
        "Your PurseLens account is ready. Redirecting you to your dashboard...";

    emailLink.removeAttribute("href");
    emailLink.removeAttribute("target");
    emailLink.removeAttribute("rel");

    emailLink.setAttribute("aria-disabled", "true");
    emailLink.classList.remove("disabled");

    emailLink.innerHTML = `✓ Verified`;

    resendWrapper.style.display = "none";

    if (messageOutput) {

        messageOutput.style.display = "none";
    }
}


// Verification Failure State
function showVerificationError() {

    heading.textContent = "Unable to Verify Your Email";

    iconWrapper.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#f20b0b" class="bi bi-ban" viewBox="0 0 16 16">
            <path d="M15 8a6.97 6.97 0 0 0-1.71-4.584l-9.874 9.875A7 7 0 0 0 15 8M2.71 12.584l9.874-9.875a7 7 0 0 0-9.874 9.874ZM16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0"/>
        </svg>
    `;
    
    iconWrapper.classList.add("failure");

    cardSubWrapper.style.display = "none";

    cardNotice.textContent =
        "The verification link may be have expired or is invalid.";

    emailLink.removeAttribute("href");
    emailLink.removeAttribute("target");
    emailLink.removeAttribute("rel");

    emailLink.setAttribute("aria-disabled", "true");
    emailLink.classList.remove("disabled");

    emailLink.style.display = "none";

    resendWrapper.style.display = "flex";

    cardSpam.style.display = "none";

    resendNotice.textContent = "Request new verification mail here 👇";
    
    messageOutput.textContent =
        "We couldn't verify your email address. Please request a new verification email.";
    
    messageOutput.style.display = "flex";
    messageOutput.classList.add("error");
    
    setTimeout(() => {
        
        messageOutput.textContent = "";
        messageOutput.style.display = "none";
        messageOutput.classList.remove("error");

    }, 10000);
}


// Backend Error Message
function getVerificationError(error) {

    if (error?.data?.detail) {
        
        return error.data.detail;
    }

    if (error?.data?.message) {

        return error.data.message;
    }

    return (
        "We couldn't verify your email address. Please request a new verification email."
    );
}


