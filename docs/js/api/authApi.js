async function register(userData) {
    return apiPost(
        "/auth/register/",
        userData
    );
}


async function login(email, password) {
    return apiPost(
        "/auth/login/",
        {
            email,
            password
        }
    );
}


async function verifyEmail(token) {
    return apiPost(
        "/auth/verify-email/",
        {
            token
        }
    )
}


async function resendVerificationEmail(email) {
    return apiPost(
        "/auth/resend-verification/",
        {
            email
        }
    )
} 


async function logout() {
    return apiPost(
        "/auth/logout/"
    );
}

