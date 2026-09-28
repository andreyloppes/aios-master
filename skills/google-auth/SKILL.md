---
name: google-auth
description: Add Google OAuth authentication to any project using Supabase. Generates login UI, callback routes, middleware, and database triggers.
---

# Google Auth

Add Google OAuth authentication to any project with Supabase in minutes.

## Scope

**Use for:** Adding Google (and GitHub) OAuth login to Next.js, React, or any Supabase-backed project.

**Not for:** Custom auth systems without Supabase, enterprise SSO (SAML/OIDC), or API-only auth.

---

# How It Works

Google OAuth via Supabase follows a 3-party flow:

```
User clicks "Sign in with Google"
  → App calls supabase.auth.signInWithOAuth({ provider: 'google' })
  → Supabase redirects to Google consent screen
  → User authorizes → Google redirects to Supabase callback
    (https://<project>.supabase.co/auth/v1/callback)
  → Supabase exchanges code for tokens, creates user in auth.users
  → Supabase redirects to app's Site URL/callback
  → App exchanges code for session → user authenticated
```

---

# What This Skill Generates

## Code (Automated)

| Component | Description |
|-----------|-------------|
| Login page | Email/password + Google + GitHub OAuth buttons |
| OAuth callback route | Exchanges authorization code for session |
| Middleware | Route protection + session refresh |
| Supabase client | Browser + Server clients with cookie management |
| Admin client | Service role client for privileged operations (signup auto-confirm) |
| Database trigger | Auto-creates user profile on signup (captures OAuth metadata) |
| Migration SQL | Users table, board_members, RLS policies |

## Configuration (Manual — guided by setup script)

| Step | Where |
|------|-------|
| Create OAuth credentials | Google Cloud Console |
| Enable Google provider | Supabase Dashboard > Auth > Providers |
| Set Site URL + Redirect URLs | Supabase Dashboard > Auth > URL Configuration |

---

# Stack Detection

Before generating code, detect the project stack:

| File | Stack | Template |
|------|-------|----------|
| `package.json` with `next` | Next.js (App Router) | `references/templates.md#nextjs` |
| `package.json` with `react` (no next) | React SPA (Vite) | `references/templates.md#react-spa` |
| `package.json` with `@remix-run` | Remix | `references/templates.md#remix` |

Check for existing Supabase setup:
- `.env.local` or `.env` with `SUPABASE_URL` → Supabase already configured
- `@supabase/ssr` in dependencies → SSR auth already set up
- `@supabase/supabase-js` only → Need to add `@supabase/ssr` for cookie-based auth

---

# Implementation Steps

## Step 1: Dependencies

```bash
npm install @supabase/supabase-js @supabase/ssr
```

## Step 2: Environment Variables

Create/update `.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
```

## Step 3: Generate Files

Generate all files from templates in `references/templates.md`. Adapt to the project's existing:
- CSS approach (CSS Modules, Tailwind, styled-components)
- File structure (app router vs pages router)
- Language (TypeScript vs JavaScript)
- Naming conventions

## Step 4: Database Migration

Generate migration SQL with:
- Users table (id, name, email, avatar_url, avatar_color)
- Trigger to auto-create profile on signup
- ON CONFLICT handling for OAuth re-login
- RLS policies

## Step 5: Setup Script

Generate an interactive setup script (`scripts/setup-google-auth.sh`) that:
1. Detects Supabase URL from `.env.local`
2. Guides through Google Cloud Console credential creation
3. Guides through Supabase provider configuration
4. Provides exact redirect URIs to copy
5. Lists common troubleshooting steps

---

# Critical Configuration Details

## Redirect URI (Most Common Error)

The authorized redirect URI in Google Cloud Console must be **exactly**:
```
https://<project-ref>.supabase.co/auth/v1/callback
```

Common mistakes:
- Missing `/auth/v1/callback` suffix
- Trailing slash
- Using app URL instead of Supabase URL
- HTTP instead of HTTPS

## Site URL in Supabase

Must match the actual deployed app URL (not localhost for production):
```
https://your-app.vercel.app
```

Also add to Redirect URLs:
```
https://your-app.vercel.app/auth/callback
```

## OAuth Metadata Mapping

Google provides these fields in `raw_user_meta_data`:

| Field | Description |
|-------|-------------|
| `full_name` | User's display name |
| `avatar_url` | Profile picture URL |
| `email` | Email address |
| `email_verified` | Whether email is verified |
| `provider_id` | Google user ID |

GitHub provides:
| Field | Description |
|-------|-------------|
| `user_name` | GitHub username |
| `avatar_url` | Profile picture URL |
| `name` | Display name (may be null) |

The trigger should use COALESCE to handle all providers:
```sql
COALESCE(
  raw_user_meta_data ->> 'full_name',   -- Google
  raw_user_meta_data ->> 'name',         -- Email signup / GitHub
  raw_user_meta_data ->> 'user_name',    -- GitHub fallback
  ''
)
```

---

# Workflow

## If Project Has Supabase Auth

1. Check existing auth implementation
2. Add OAuth buttons to existing login page
3. Verify callback route exists
4. Update trigger to handle OAuth metadata
5. Generate setup script
6. Guide through external configuration

## If Project Has No Auth

1. Install dependencies
2. Generate all auth files from templates
3. Generate migration SQL
4. Generate setup script
5. Guide through Supabase project creation + configuration
6. Guide through Google Cloud Console setup

---

# Commands

- `/google-auth` — Add Google Auth to current project (main entry point)
- `/google-auth:setup` — Run setup guide for external configuration
- `/google-auth:diagnose` — Diagnose common OAuth issues

---

# Troubleshooting Reference

See `references/troubleshooting.md` for common issues and solutions.

# Code Templates

See `references/templates.md` for framework-specific code templates.
