# FinAudit Authentication System — Full Documentation

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Technology Stack](#2-technology-stack)
3. [Data Models](#3-data-models)
4. [Authentication Flows](#4-authentication-flows)
   - 4.1 Local Registration
   - 4.2 Email Verification
   - 4.3 Local Login
   - 4.4 Google OAuth Login
   - 4.5 Logout
   - 4.6 Forgot Password
   - 4.7 Reset Password
   - 4.8 Change Password
5. [Edge Case Handling](#5-edge-case-handling)
6. [Security Layers](#6-security-layers)
7. [Signal & Adapter Architecture](#7-signal--adapter-architecture)
8. [API Endpoints Reference](#8-api-endpoints-reference)
9. [Design Decisions & Tradeoffs](#9-design-decisions--tradeoffs)
10. [System Design Blueprint](#10-system-design-blueprint)
11. [Testing Guidelines](#11-testing-guidelines)

---

## 1. System Overview

FinAudit is a Django REST Framework (DRF) backend that supports two authentication pathways:

- **Local (email + password)** — traditional signup with mandatory email verification
- **OAuth (Google)** — social login via django-allauth with automatic account linking

Both pathways converge on the same `User` model and issue **JWT tokens** (via SimpleJWT) as the authentication credential for all subsequent API calls. A custom `UserSocialAccount` table tracks every login method attached to a user account, enabling multi-provider identity management.

The system is designed around four principles:

1. **One identity per verified email** — the same email address across providers always resolves to one user account
2. **Email ownership is the trust anchor** — verified emails from OAuth providers can activate and link accounts
3. **Provider UID beats email for re-identification** — if a user changes their Google email, `provider_user_id` still finds the right account
4. **No lockout** — users can never disconnect their last authentication method

---

## 2. Technology Stack

| Layer | Library | Role |
|---|---|---|
| Framework | Django 6 + DRF | API, ORM, request handling |
| Auth tokens | SimpleJWT | Access + refresh JWT issuance and blacklisting |
| Social auth | django-allauth | OAuth 2.0 flow, provider callbacks, account linking |
| Brute force | django-axes | Login attempt tracking and account lockout |
| Database | MySQL | Persistent storage |
| Email | Django console backend (dev) | Verification and reset emails |

---

## 3. Data Models

### 3.1 User

```
User (AbstractUser, username removed)
├── id            UUID, primary key
├── first_name    CharField
├── last_name     CharField
├── email         EmailField, unique — used as USERNAME_FIELD
├── is_active     BooleanField, default=False (inactive until verified)
├── is_verified   BooleanField, default=False (custom flag, mirrors is_active for local)
├── created_at    DateTimeField
└── updated_at    DateTimeField
```

**Key design decision:** `is_active=False` by default forces email verification before login. Django's authentication system respects `is_active`, so unverified users are automatically blocked from logging in without any additional checks in the login view.

`is_verified` is a custom field that mirrors activation state but is semantically cleaner for API consumers — it communicates "email ownership confirmed" separately from the administrative "account enabled" meaning of `is_active`.

---

### 3.2 UserSocialAccount

```
UserSocialAccount
├── id                    UUID, primary key
├── user                  FK → User
├── provider              CharField (local | google | apple | ...)
├── provider_user_id      CharField — the UID from the provider (e.g. Google sub claim)
├── is_primary            BooleanField — first linked provider is primary
├── email_at_provider_time EmailField, unique — email captured at link time
└── created_at            DateTimeField

Constraints:
  unique_together: (provider, provider_user_id)
```

Every user gets at least one `UserSocialAccount` record. Local signups get `provider=local`, `provider_user_id=user.pk`. OAuth signups get `provider=google` (or other), `provider_user_id=<google_sub>`.

A user with both email/password and Google linked will have two rows. This table is the canonical source of truth for "what login methods does this user have".

---

### 3.3 Supporting Models

**EmailVerificationToken**
```
├── user          OneToOne → User
├── token         CharField(64), unique — stored as SHA-256 hash
├── created_at    DateTimeField
└── expires_at    DateTimeField (15 minutes from creation)
```
Raw token sent by email; only the hash is stored. One token per user — creating a new one deletes the old one automatically.

**Profile**
```
├── user              OneToOne → User
├── profile_picture   ImageField (auto-deleted on update via save() override)
└── timezone          CharField with choices
```

**UserSettings**
```
├── user                      OneToOne → User
├── preferred_language        CharField
├── preferred_currency        CharField
├── is_dark_theme             BooleanField
├── allow_email_notifications BooleanField
└── allow_budget_alerts       BooleanField
```

`Profile` and `UserSettings` are auto-created for every user via the `post_save` signal on `User`.

---

## 4. Authentication Flows

### 4.1 Local Registration

```
Client                          Server
  │                               │
  ├─── POST /api/auth/register/ ──►│
  │    { first_name, last_name,    │
  │      email, password }         │
  │                               │
  │                    RegisterSerializer validates:
  │                    - email lowercased
  │                    - password meets PasswordValidator rules
  │                    - User.objects.create() with set_password()
  │                               │
  │                    post_save signal fires:
  │                    - Profile.objects.create(user)
  │                    - UserSettings.objects.create(user)
  │                    - UserSocialAccount(provider=local) created
  │                               │
  │                    generate_verification_token():
  │                    - secrets.token_urlsafe(24) → raw_token
  │                    - SHA-256 hash stored in EmailVerificationToken
  │                    - expires_at = now + 15 minutes
  │                               │
  │                    send_verification_email():
  │                    - Link: {FRONTEND_URL}/verify-email/?token={raw_token}
  │                               │
  │◄── 201 { user data } ─────────┤
```

**Throttle:** 5 requests per hour (`RegisterThrottle`).

**State after registration:** `is_active=False`, `is_verified=False`. User cannot log in yet.

---

### 4.2 Email Verification

```
Client                          Server
  │                               │
  ├─── POST /api/auth/verify-email/ ►│
  │    { token: "<raw_token>" }    │
  │                               │
  │                    VerifyEmailSerializer:
  │                    - Strip whitespace from token
  │                    - SHA-256 hash the raw token
  │                    - Look up EmailVerificationToken by hash
  │                    - Check is_expired (now > expires_at)
  │                    - Check user.is_active (already verified?)
  │                               │
  │                    VerifyEmailView:
  │                    - user.is_active = True
  │                    - user.is_verified = True
  │                    - user.save()
  │                    - verification.delete() (one-time use)
  │                    - Issue JWT refresh + access token
  │                               │
  │◄── 200 { tokens } ────────────┤
```

**Security notes:**
- Token is never stored raw — only the SHA-256 hash is in the database
- Token expires in 15 minutes
- Token is deleted after use (cannot be replayed)
- Response does not reveal whether the email exists (fail-silent design in ResendVerification)

---

### 4.3 Local Login

```
Client                          Server
  │                               │
  ├─── POST /api/auth/login/ ─────►│
  │    { email, password }         │
  │                               │
  │                    LoginView checks Axes lockout first:
  │                    - AxesProxyHandler.is_locked(request, email)
  │                    - If locked → 403 immediately, no DB query
  │                               │
  │                    LoginSerializer (extends TokenObtainPairSerializer):
  │                    - email lowercased
  │                    - super().validate() → authenticates via Django backend
  │                               │
  │                    On failure:
  │                    - user_login_failed signal → Axes records attempt
  │                    - If user exists but is_active=False → 401 "not verified"
  │                    - Otherwise → 401 "invalid email or password"
  │                               │
  │                    On success:
  │                    - AxesProxyHandler.reset_attempts() (clears failure count)
  │                    - SimpleJWT issues access (15 min) + refresh (7 days)
  │                               │
  │◄── 200 { user, tokens } ──────┤
```

**Lockout policy (Axes):**
- Locks after 5 failed attempts
- Lock key = `(email, ip_address)` pair
- Lockout duration: 30 minutes
- Auto-resets on successful login

---

### 4.4 Google OAuth Login

This is the most complex flow, managed by allauth with custom adapter hooks.

```
Client                          Server                    Google
  │                               │                          │
  ├─ GET /accounts/google/login/ ─►│                          │
  │                               ├─ Redirect to Google ────►│
  │                               │  (state, code_challenge)  │
  │                               │                          │
  │                               │◄─ User selects account ──┤
  │                               │◄─ GET /callback/?code=.. ─┤
  │                               │                          │
  │              SocialAccountAdapter.pre_social_login():
  │              1. Is this sociallogin already linked? → skip
  │              2. Extract verified email from Google's response
  │              3. Does a User with that email exist?
  │                 YES → apply edge case logic (see §5)
  │                 NO  → let allauth create a new user
  │                               │
  │              SocialAccountAdapter.save_user():
  │              - Ensures user.is_active = True
  │              - Ensures user.is_verified = True
  │                               │
  │              post_save signal fires (new user only):
  │              - Profile + UserSettings created
  │              - No local UserSocialAccount (has_social=True)
  │                               │
  │              social_account_added signal fires:
  │              - UserSocialAccount(provider=google, uid=sub) created
  │                               │
  │◄─ Redirect to LOGIN_REDIRECT_URL (/dashboard) ───────────┤
  │   (session cookie set by allauth)
  │                               │
  ├─ Client exchanges session for JWT ────────────────────────┤
  │  (via separate token endpoint or Google token endpoint)
```

**Note:** allauth's OAuth flow is session-based by default. For a pure API setup, you need a mechanism to exchange the allauth session for a JWT after the callback. This is a known integration point that may still need to be wired depending on the frontend architecture.

---

### 4.5 Logout

```
Client                          Server
  │                               │
  ├─── POST /api/auth/logout/ ────►│
  │    { refresh: "<token>" }      │
  │    Authorization: Bearer <access>
  │                               │
  │                    - Validate refresh token
  │                    - RefreshToken(token).blacklist()
  │                    - Token added to OutstandingToken/BlacklistedToken tables
  │                               │
  │◄── 200 { "Logged out" } ──────┤
```

After blacklisting, the refresh token cannot be used to generate new access tokens. The access token remains valid until its 15-minute expiry — this is a standard JWT tradeoff (see §9).

---

### 4.6 Forgot Password

```
Client                          Server
  │                               │
  ├─── POST /api/auth/forgot-password/ ►│
  │    { email }                   │
  │                               │
  │                    - Look up user by email
  │                    - If found: PasswordResetTokenGenerator().make_token(user)
  │                    - uid = base64(user.pk)
  │                    - Send email: {FRONTEND_URL}/reset-password/?uid=&token=
  │                    - If not found: silent (no error revealed)
  │                               │
  │◄── 200 (always, regardless) ──┤
```

**Throttle:** 3 requests per hour (`PasswordResetThrottle`). Fail-silent design prevents email enumeration.

---

### 4.7 Reset Password

```
Client                          Server
  │                               │
  ├─── POST /api/auth/reset-password/ ►│
  │    { uid, token, new_password } │
  │                               │
  │                    ResetPasswordSerializer:
  │                    - Decode uid → user.pk → fetch User
  │                    - PasswordResetTokenGenerator().check_token(user, token)
  │                    - validate_password(new_password)
  │                               │
  │                    ResetPasswordView:
  │                    - user.set_password(new_password)
  │                    - user.save()
  │                    - UserSocialAccount.get_or_create(provider=local)
  │                      (Edge Case 2: Google user now sets a password)
  │                               │
  │◄── 200 { "reset successfully" } ►│
```

---

### 4.8 Change Password

```
Client                          Server
  │                               │
  ├─── POST /api/auth/change-password/ ►│
  │    { old_password, new_password }  │
  │    Authorization: Bearer <access>
  │                               │
  │                    ChangePasswordSerializer:
  │                    - user.check_password(old_password)
  │                    - validate_password(new_password)
  │                    - old != new check
  │                               │
  │                    ChangePasswordView:
  │                    - user.set_password(new_password)
  │                    - user.save()
  │                    - UserSocialAccount.get_or_create(provider=local)
  │                      (Edge Case 2: Google user adding password)
  │                               │
  │◄── 200 { "changed successfully" } ┤
```

---

## 5. Edge Case Handling

All edge cases are handled in `adapters.py` (pre-login) and `signals.py` (post-save).

### Edge Case 1 — Local account + later Google login (same email)

**Scenario:** User registers with `daniel@example.com` locally. Later clicks "Continue with Google" which also returns `daniel@example.com`.

**Handler:** `SocialAccountAdapter.pre_social_login()`

**Logic:**
1. OAuth callback returns, `sociallogin.is_existing = False` (not yet linked)
2. Adapter extracts verified email from Google response
3. Finds existing `User` with that email
4. Calls `sociallogin.connect(request, existing_user)` — links Google to the existing account
5. `social_account_added` signal creates `UserSocialAccount(provider=google)`

**Result:**
```
User: daniel@example.com
UserSocialAccount: provider=local   (from registration)
UserSocialAccount: provider=google  (just linked)
```

---

### Edge Case 2 — Google first, password set later

**Scenario:** User signs up with Google. Later wants to use email/password login.

**Handler:** `ChangePasswordView` and `ResetPasswordView`

**Logic:** After `set_password()` succeeds, `get_or_create(provider=local)` runs. If the local `UserSocialAccount` already exists, nothing happens. If not, it is created.

**Result:**
```
User: daniel@example.com (now has usable password)
UserSocialAccount: provider=google  (original)
UserSocialAccount: provider=local   (newly created, is_primary=False)
```

---

### Edge Case 3 — Multiple providers, same email

**Scenario:** User has Google (`daniel@example.com`) and later adds LinkedIn (`daniel@example.com`).

**Handler:** `SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True` in settings + `pre_social_login` adapter

**Logic:** Same as Edge Case 1 — email match → `sociallogin.connect()` → link to existing user.

**Result:** One user, multiple `UserSocialAccount` rows, one per provider.

---

### Edge Case 4 — Different providers, different emails

**Scenario:** Google (`a@gmail.com`), TikTok (`b@tiktok.com`). No email overlap.

**Handler:** `pre_social_login` returns early (no email match found)

**Logic:** No auto-linking. allauth creates a new user for the TikTok account.

**Result:** Two separate `User` accounts. Manual linking (from an authenticated session) is required if the user wants to merge them.

**Why this is correct:** There is no cryptographic proof that the same human owns both email addresses. Auto-linking would be a security vulnerability.

---

### Edge Case 5 — User changes their Google email

**Scenario:** Google account had `provider_user_id=123456, email=old@gmail.com`. Google now returns `provider_user_id=123456, email=new@gmail.com`.

**Handler:** `social_account_added` signal uses `update_or_create` keyed on `(provider, provider_user_id)`

**Logic:**
```python
UserSocialAccount.objects.update_or_create(
    provider=social.provider,
    provider_user_id=social.uid,    # ← identity key, NOT email
    defaults={
        "email_at_provider_time": email,  # ← updated to new email
    }
)
```

**Result:** The existing `UserSocialAccount` row is updated with the new email. `provider_user_id` is the stable identity anchor.

---

### Edge Case 6 — Unverified local account, Google login same email

**Scenario:** User registers locally but never verifies. Later logs in with Google using same email. Without handling, allauth would see `is_active=False` and redirect to `/accounts/inactive/`.

**Handler:** `SocialAccountAdapter.pre_social_login()`

**Logic:**
```python
if not existing_user.is_active:
    existing_user.is_active = True
    existing_user.is_verified = True
    existing_user.save()
    EmailAddress.objects.filter(user=existing_user, email=email).update(verified=True)
```

Google has verified ownership of this email address — that is stronger evidence than a local unverified registration.

**Result:** Account is activated, Google is linked, user is logged in.

---

### Edge Case 7 — Removing last login method

**Scenario:** User has only Google linked. Tries to disconnect Google.

**Handler:** `social_account_removed` signal

**Logic:**
```python
remaining_social = UserSocialAccount.objects.filter(user=user).exclude(provider=provider).count()
has_local_password = user.has_usable_password()

if remaining_social == 0 and not has_local_password:
    raise ImmediateHttpResponse(HttpResponseBadRequest("Cannot remove only login method."))
```

**Result:** Disconnection is blocked. User must set a password first (via ChangePassword or ResetPassword), which creates a `local` `UserSocialAccount`, after which Google can be safely disconnected.

---

## 6. Security Layers

### 6.1 Password Policy (`validators.py`)

Custom `PasswordValidator` enforces:
- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 symbol from the defined charset

Applied globally via `AUTH_PASSWORD_VALIDATORS` in settings — runs on `validate_password()` calls in serializers.

### 6.2 Brute Force Protection (django-axes)

| Setting | Value | Meaning |
|---|---|---|
| `AXES_FAILURE_LIMIT` | 5 | Lock after 5 failures |
| `AXES_COOLOFF_TIME` | 30 minutes | Lockout duration |
| `AXES_LOCK_PARAMETERS` | `[email, ip_address]` | Locks the (email + IP) pair, not just IP |
| `AXES_RESET_ON_SUCCESS` | True | Clears count on successful login |

The `(email, ip_address)` pair strategy means: the same email from a different IP is treated separately, and a different email from the same IP is also treated separately. This reduces both targeted attacks and collateral lockouts.

Pre-check in `LoginView` returns 403 before the serializer even runs, preventing timing-based enumeration on locked accounts.

### 6.3 Token Security (SimpleJWT)

| Setting | Value |
|---|---|
| Access token lifetime | 15 minutes |
| Refresh token lifetime | 7 days |
| Rotate refresh tokens | True (new refresh issued on each use) |
| Blacklist after rotation | True (old refresh immediately invalidated) |

Short access token lifetime limits exposure if a token is leaked. Rotation + blacklisting ensures a stolen refresh token is detected on first use.

### 6.4 Email Token Security (`utils.py`)

- Raw token generated with `secrets.token_urlsafe(24)` (cryptographically secure)
- Only `SHA-256(raw_token)` stored in the database
- Token deleted after first use
- Token expires after 15 minutes
- If the same user requests a new token, old one is deleted first (no accumulation)

### 6.5 API Throttling

| Scope | Limit | Applied to |
|---|---|---|
| `login` | 10/minute | LoginView |
| `register` | 5/hour | RegisterView |
| `password_reset` | 3/hour | ForgotPasswordView, ResendVerificationView |
| `anon` | 100/day | All anonymous endpoints |
| `user` | 1000/day | All authenticated endpoints |

### 6.6 Account Deactivation (Soft Delete)

`DELETE /api/users/me/` sets `is_active=False` rather than deleting the record. The user's data is preserved, and the associated refresh token is blacklisted. This is a standard production pattern — hard deletes cause referential integrity issues and make recovery impossible.

---

## 7. Signal & Adapter Architecture

### Why signals for account creation?

Using `post_save` on `User` to create `Profile`, `UserSettings`, and `UserSocialAccount` keeps the registration logic clean — `RegisterSerializer.create()` only creates the user. The signal layer handles all side effects, and it fires for every user creation path (local, OAuth, management commands, tests).

### Why an adapter for OAuth edge cases?

`pre_social_login` fires at the right moment in the OAuth lifecycle — after Google has confirmed the user's identity, but before allauth decides whether to create a new account or log in an existing one. This is the only place where account-linking logic can intercept the flow cleanly.

`save_user` in the adapter ensures `is_active=True` on all OAuth-created users, overriding the model default of `False` that exists for local signups (which require email verification).

### Signal execution order

```
User created (any path)
    └── post_save(created=True)
        ├── Profile.create()
        ├── UserSettings.create()
        └── If no SocialAccount yet → UserSocialAccount(provider=local).create()

Google OAuth callback
    └── SocialAccountAdapter.pre_social_login()
        └── Link or activate existing user if email matches
    └── SocialAccountAdapter.save_user()
        └── Force is_active=True, is_verified=True
    └── social_account_added signal
        └── UserSocialAccount(provider=google).update_or_create()

Provider disconnected
    └── social_account_removed signal
        └── Guard: block if last method
        └── UserSocialAccount.delete()
```

---

## 8. API Endpoints Reference

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | None | Create account, send verification email |
| POST | `/api/auth/verify-email/` | None | Verify email with token, get JWT |
| POST | `/api/auth/resend-verification/` | None | Resend verification email |
| POST | `/api/auth/login/` | None | Email/password login, get JWT |
| POST | `/api/auth/logout/` | Bearer | Blacklist refresh token |
| POST | `/api/auth/refresh/` | None | Get new access token from refresh token |
| POST | `/api/auth/change-password/` | Bearer | Change password (authenticated) |
| POST | `/api/auth/forgot-password/` | None | Request password reset email |
| POST | `/api/auth/reset-password/` | None | Reset password with uid+token |

### User & Profile

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/users/me/` | Bearer | Get current user details |
| PATCH | `/api/users/me/` | Bearer | Update first/last name |
| DELETE | `/api/users/me/` | Bearer | Deactivate account (soft delete) |
| GET | `/api/user/settings/` | Bearer | Get user settings |
| PATCH | `/api/user/settings/` | Bearer | Update settings |
| GET | `/api/profile/` | Bearer | Get profile + settings (combined) |
| PATCH | `/api/profile/` | Bearer | Update profile picture, timezone |

### OAuth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/accounts/google/login/` | None | Initiate Google OAuth flow |
| GET | `/accounts/google/login/callback/` | None | Google OAuth callback (handled by allauth) |

---

## 9. Design Decisions & Tradeoffs

### Decision 1: `is_active=False` by default

**Why:** Forces email verification before any login is possible. Django's `ModelBackend` checks `is_active` during authentication, so no extra guard is needed in the login view.

**Tradeoff:** Adds friction to registration. Mitigated by clear error messages and the resend-verification endpoint.

**Alternative considered:** Allow login before verification but restrict access to certain endpoints. Rejected because it adds complexity across every protected view.

---

### Decision 2: Hash-only token storage

**Why:** If the `EmailVerificationToken` table is compromised, raw tokens cannot be extracted and replayed. SHA-256 is a one-way function.

**Tradeoff:** Slightly more computation on verification. Completely negligible in practice.

---

### Decision 3: JWT over session auth for the API

**Why:** Stateless — no session store required. Works naturally with mobile/SPA clients. SimpleJWT's blacklist feature provides logout capability without full statefulness.

**Tradeoff:** Access tokens cannot be instantly revoked. 15-minute lifetime is the compromise between security (short) and usability (not too frequent refresh calls).

---

### Decision 4: allauth for OAuth instead of a custom OAuth flow

**Why:** allauth handles the full OAuth 2.0 lifecycle correctly — PKCE, state parameter (CSRF protection), token exchange, user info fetch. Building this correctly from scratch is significant work with many security pitfalls.

**Tradeoff:** allauth is session-based by default, while the rest of the API is JWT-based. This creates an integration gap at the callback step that needs a token exchange mechanism for pure SPA/mobile clients.

---

### Decision 5: `(email, ip_address)` lock key in Axes

**Why:** IP-only locking can cause collateral damage (shared IPs, NAT). Email-only locking can lock legitimate users from any IP. The pair is more targeted.

**Tradeoff:** A sophisticated attacker using a botnet (different IPs) can bypass IP-based locking. Mitigated by the email component of the key.

---

### Decision 6: `provider_user_id` as the primary identity anchor for OAuth

**Why:** Emails are mutable. Google users can change their Gmail address. Using only email as the identity key would break the link silently. Google's `sub` claim (the UID) is immutable for the lifetime of the account.

**Tradeoff:** Slightly more complex lookup logic. Worth it for correctness.

---

### Decision 7: Soft delete (`is_active=False`) instead of hard delete

**Why:** Preserves audit trail, prevents referential integrity issues with related records (transactions, audit logs), and allows account recovery if the user changes their mind.

**Tradeoff:** Database grows over time with inactive records. Addressed with a periodic cleanup job (not yet implemented).

---

## 10. System Design Blueprint

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT                                   │
│              (React SPA / Mobile App / Postman)                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO (finaudit_backend)                      │
│                                                                   │
│  ┌─────────────┐   ┌────────────────┐   ┌────────────────────┐  │
│  │  accounts/  │   │  allauth URLs  │   │  api/ (DRF)        │  │
│  │  urls.py    │   │  /accounts/    │   │  JWT endpoints     │  │
│  └──────┬──────┘   └───────┬────────┘   └────────┬───────────┘  │
│         │                  │                     │               │
│         ▼                  ▼                     ▼               │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                      VIEWS LAYER                           │  │
│  │  RegisterView  LoginView  LogoutView  VerifyEmailView      │  │
│  │  ForgotPasswordView  ResetPasswordView  ChangePasswordView │  │
│  │  UserDetailView  UserSettingsView  ProfileView             │  │
│  └────────────────────────────┬───────────────────────────────┘  │
│                               │                                   │
│         ┌─────────────────────┼──────────────────┐               │
│         ▼                     ▼                  ▼               │
│  ┌─────────────┐   ┌─────────────────┐  ┌──────────────────┐    │
│  │ SERIALIZERS │   │    ADAPTERS     │  │    SIGNALS       │    │
│  │ Validate +  │   │ pre_social_     │  │ post_save →      │    │
│  │ transform   │   │ login()         │  │ Profile          │    │
│  │ input/output│   │ save_user()     │  │ UserSettings     │    │
│  └──────┬──────┘   └────────┬────────┘  │ UserSocialAcct   │    │
│         │                   │           │                  │    │
│         │                   │           │ social_account_  │    │
│         │                   │           │ added/removed    │    │
│         │                   │           └──────────────────┘    │
│         ▼                   ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                      MODEL LAYER (ORM)                      │  │
│  │  User  UserSocialAccount  Profile  UserSettings             │  │
│  │  EmailVerificationToken                                      │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │  SimpleJWT   │  │  django-axes  │  │  django-allauth       │  │
│  │  Token       │  │  Brute force  │  │  OAuth 2.0 lifecycle  │  │
│  │  issue +     │  │  protection   │  │  Google callback      │  │
│  │  blacklist   │  │               │  │  Account linking      │  │
│  └──────────────┘  └───────────────┘  └──────────────────────┘  │
│                                                                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
┌─────────────────────┐            ┌────────────────────────┐
│   MySQL Database    │            │   Google OAuth         │
│   - User            │            │   - Authorization      │
│   - SocialAccount   │            │     Server             │
│   - Profile         │            │   - UserInfo endpoint  │
│   - Settings        │            │   - provider_user_id   │
│   - EmailToken      │            │     (sub claim)        │
│   - JWT Blacklist   │            └────────────────────────┘
└─────────────────────┘
```

### Identity Resolution Flow

```
OAuth callback arrives
        │
        ▼
Is sociallogin.is_existing?
   YES ──► Already linked, log in directly
        │
       NO
        │
        ▼
Does provider return a verified email?
   NO ──► Create new user (Edge Case 4 path)
        │
       YES
        │
        ▼
Does a User with that email exist?
   NO ──► Create new user, create UserSocialAccount(provider=google)
        │
       YES
        │
        ▼
Is the existing user active?
   NO ──► Activate user + mark verified (Edge Case 6)
        │
       YES (or just activated)
        │
        ▼
sociallogin.connect(request, existing_user)
        │
        ▼
social_account_added signal
        │
        ▼
UserSocialAccount.update_or_create(
    key=(provider, provider_user_id),  ← UID, not email (Edge Case 5)
    defaults={email_at_provider_time}
)
```

---

## 11. Testing Guidelines

### 11.1 Test Setup

```python
# conftest.py or base test class
from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

def create_local_user(email="test@example.com", password="Test@12345678", active=True):
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name="Test",
        last_name="User",
    )
    user.is_active = True
    user.is_verified = True
    user.save()
    return user

def create_google_user(email="google@example.com", uid="google_sub_123"):
    """Creates a user as if they signed up via Google."""
    user = User.objects.create_user(email=email, first_name="Google", last_name="User")
    user.is_active = True
    user.is_verified = True
    user.save(update_fields=["is_active", "is_verified"])
    SocialAccount.objects.create(user=user, provider="google", uid=uid)
    return user
```

---

### 11.2 Registration Tests

```python
class TestRegistration:
    
    def test_register_creates_user_inactive(self):
        # User must be inactive after registration
        response = client.post("/api/auth/register/", {...})
        assert response.status_code == 201
        user = User.objects.get(email="test@example.com")
        assert user.is_active == False
        assert user.is_verified == False

    def test_register_creates_profile_and_settings(self):
        # Signals must fire and create related objects
        user = create_local_user()
        assert hasattr(user, 'profile')
        assert hasattr(user, 'settings')

    def test_register_creates_local_social_account(self):
        # post_save signal must create local UserSocialAccount
        from accounts.models import UserSocialAccount
        user = create_local_user()
        assert UserSocialAccount.objects.filter(user=user, provider="local").exists()

    def test_register_sends_verification_email(self):
        # Email backend must record one outgoing email
        from django.core import mail
        client.post("/api/auth/register/", {...})
        assert len(mail.outbox) == 1

    def test_register_duplicate_email_fails(self):
        create_local_user(email="dupe@example.com")
        response = client.post("/api/auth/register/", {"email": "dupe@example.com", ...})
        assert response.status_code == 400

    def test_weak_password_rejected(self):
        # PasswordValidator must catch weak passwords
        response = client.post("/api/auth/register/", {"password": "password", ...})
        assert response.status_code == 400

    def test_register_throttle(self):
        # 6th request within the hour must be throttled
        for _ in range(5):
            client.post("/api/auth/register/", {...})
        response = client.post("/api/auth/register/", {...})
        assert response.status_code == 429
```

---

### 11.3 Email Verification Tests

```python
class TestEmailVerification:

    def test_valid_token_activates_user(self):
        user = create_local_user(active=False)
        raw_token = generate_verfication_token(user)
        response = client.post("/api/auth/verify-email/", {"token": raw_token})
        user.refresh_from_db()
        assert response.status_code == 200
        assert user.is_active == True
        assert user.is_verified == True

    def test_valid_token_returns_jwt(self):
        user = create_local_user(active=False)
        raw_token = generate_verfication_token(user)
        response = client.post("/api/auth/verify-email/", {"token": raw_token})
        assert "access" in response.data["data"]["token"]
        assert "refresh" in response.data["data"]["token"]

    def test_token_is_deleted_after_use(self):
        from accounts.models import EmailVerificationToken
        user = create_local_user(active=False)
        raw_token = generate_verfication_token(user)
        client.post("/api/auth/verify-email/", {"token": raw_token})
        assert not EmailVerificationToken.objects.filter(user=user).exists()

    def test_expired_token_fails(self):
        from django.utils import timezone
        from datetime import timedelta
        user = create_local_user(active=False)
        raw_token = generate_verfication_token(user)
        # Manually expire the token
        user.verification_token.expires_at = timezone.now() - timedelta(seconds=1)
        user.verification_token.save()
        response = client.post("/api/auth/verify-email/", {"token": raw_token})
        assert response.status_code == 400

    def test_invalid_token_fails(self):
        response = client.post("/api/auth/verify-email/", {"token": "notarealtoken"})
        assert response.status_code == 400

    def test_token_cannot_be_replayed(self):
        user = create_local_user(active=False)
        raw_token = generate_verfication_token(user)
        client.post("/api/auth/verify-email/", {"token": raw_token})
        # Second use of the same token
        response = client.post("/api/auth/verify-email/", {"token": raw_token})
        assert response.status_code == 400
```

---

### 11.4 Login Tests

```python
class TestLogin:

    def test_valid_credentials_return_tokens(self):
        create_local_user(email="login@example.com", password="Test@12345678")
        response = client.post("/api/auth/login/", {
            "email": "login@example.com",
            "password": "Test@12345678"
        })
        assert response.status_code == 200
        assert "access" in response.data["data"]["tokens"]

    def test_unverified_user_cannot_login(self):
        create_local_user(active=False)
        response = client.post("/api/auth/login/", {...})
        assert response.status_code == 401
        assert "not verified" in response.data["message"].lower()

    def test_wrong_password_fails(self):
        create_local_user()
        response = client.post("/api/auth/login/", {"password": "WrongPass@123"})
        assert response.status_code == 401

    def test_axes_lockout_after_5_failures(self):
        create_local_user()
        for _ in range(5):
            client.post("/api/auth/login/", {"password": "WrongPass@123"})
        response = client.post("/api/auth/login/", {"password": "WrongPass@123"})
        assert response.status_code == 403

    def test_axes_resets_on_success(self):
        user = create_local_user()
        for _ in range(4):
            client.post("/api/auth/login/", {"password": "WrongPass@123"})
        # Successful login resets counter
        client.post("/api/auth/login/", {"password": "Test@12345678"})
        # Should not be locked on next failure
        response = client.post("/api/auth/login/", {"password": "WrongPass@123"})
        assert response.status_code == 401   # not 403

    def test_email_case_insensitive_login(self):
        create_local_user(email="case@example.com")
        response = client.post("/api/auth/login/", {"email": "CASE@EXAMPLE.COM", ...})
        assert response.status_code == 200
```

---

### 11.5 Edge Case Tests

```python
class TestEdgeCases:

    def test_edge_case_1_local_then_google_links(self):
        """Local account + Google same email → linked, not duplicate."""
        from allauth.socialaccount.models import SocialAccount
        from accounts.models import UserSocialAccount
        
        user = create_local_user(email="link@example.com")
        initial_count = User.objects.count()
        
        # Simulate Google login with same email (mock pre_social_login)
        # ... (use allauth test helpers or mock the adapter)
        
        assert User.objects.count() == initial_count   # no new user created
        assert UserSocialAccount.objects.filter(user=user, provider="google").exists()
        assert UserSocialAccount.objects.filter(user=user, provider="local").exists()

    def test_edge_case_2_google_user_sets_password(self):
        """Google user sets password → local UserSocialAccount created."""
        from accounts.models import UserSocialAccount
        user = create_google_user()
        client.force_authenticate(user=user)
        client.post("/api/auth/change-password/", {
            "old_password": ...,
            "new_password": "NewPass@12345678"
        })
        assert UserSocialAccount.objects.filter(user=user, provider="local").exists()

    def test_edge_case_4_different_emails_no_autolink(self):
        """Different emails across providers → separate accounts."""
        user_a = create_google_user(email="a@gmail.com", uid="uid_a")
        initial_count = User.objects.count()
        # Simulate TikTok login with b@gmail.com
        # Assert new user is created
        assert User.objects.count() == initial_count + 1

    def test_edge_case_6_unverified_local_activated_by_google(self):
        """Unverified local + Google same email → activates account."""
        user = create_local_user(active=False)
        assert user.is_active == False
        # Simulate Google login with same email via adapter
        # Assert user.is_active == True after adapter runs

    def test_edge_case_7_cannot_remove_last_login_method(self):
        """User with only Google cannot disconnect it."""
        from allauth.socialaccount.models import SocialAccount
        user = create_google_user()
        social = SocialAccount.objects.get(user=user)
        # Attempt disconnect — should raise ImmediateHttpResponse
        from allauth.socialaccount.signals import social_account_removed
        from allauth.exceptions import ImmediateHttpResponse
        import pytest
        with pytest.raises(ImmediateHttpResponse):
            social_account_removed.send(
                sender=SocialAccount,
                request=None,
                socialaccount=social
            )
```

---

### 11.6 Password Tests

```python
class TestPasswordFlows:

    def test_forgot_password_sends_email(self):
        from django.core import mail
        create_local_user(email="forgot@example.com")
        client.post("/api/auth/forgot-password/", {"email": "forgot@example.com"})
        assert len(mail.outbox) == 1

    def test_forgot_password_silent_for_unknown_email(self):
        response = client.post("/api/auth/forgot-password/", {"email": "nobody@example.com"})
        assert response.status_code == 200   # no error revealed

    def test_reset_password_with_valid_token(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import PasswordResetTokenGenerator
        user = create_local_user()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        response = client.post("/api/auth/reset-password/", {
            "uid": uid,
            "token": token,
            "new_password": "NewPass@12345678"
        })
        assert response.status_code == 200

    def test_change_password_wrong_old_password(self):
        user = create_local_user()
        client.force_authenticate(user=user)
        response = client.post("/api/auth/change-password/", {
            "old_password": "WrongPass@123",
            "new_password": "NewPass@12345678"
        })
        assert response.status_code == 400

    def test_change_password_same_as_old(self):
        user = create_local_user()
        client.force_authenticate(user=user)
        response = client.post("/api/auth/change-password/", {
            "old_password": "Test@12345678",
            "new_password": "Test@12345678"
        })
        assert response.status_code == 400
```

---

### 11.7 What to Test Next (Not Yet Covered)

- `UserSettingsView` PATCH validation (invalid currency, language)
- `ProfileView` PATCH — oversized image, wrong format
- `UserDetailView` DELETE — confirm `is_active=False` and token blacklisted
- `LogoutView` — double logout with same refresh token (should fail second time)
- Token refresh — rotated token cannot be reused
- `AccountService.social_login` — fix and test the `is_authenticated` bug before using it
- Email uniqueness on `UserSocialAccount.email_at_provider_time` — verify constraint holds when same email re-registers
- Full OAuth integration test with allauth's `SocialLoginFactory` or `TestClient` helpers

---

*Last updated: May 2026 — FinAudit Backend*
