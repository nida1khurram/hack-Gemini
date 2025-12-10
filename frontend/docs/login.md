---
title: Login
sidebar_label: Login
---

import LoginForm from '@site/src/components/LoginForm';
import BrowserOnly from '@docusaurus/BrowserOnly';

# User Login

## Default Credentials

For testing purposes, you can use the following credentials:

- **Username**: `testuser`
- **Password**: `testpass123`

<BrowserOnly>
  {() => (
    <LoginForm />
  )}
</BrowserOnly>

## Need an Account?

If you don't have an account, you can register using the registration API endpoints.
