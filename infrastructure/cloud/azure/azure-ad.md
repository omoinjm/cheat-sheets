# Azure Active Directory (Azure AD)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the Microsoft Azure cloud services documentation, focusing on identity and access management.

## Contents Overview

This file provides notes and instructions related to managing Azure Active Directory (Azure AD), specifically covering how to locate client IDs and client secrets for application registrations and how to retrieve a list of users from Azure AD.

## Role in System

Azure AD is a critical component for identity and access management in the Azure ecosystem. This document helps developers and administrators configure applications, manage user identities, and secure access to cloud resources within Azure.

## Key Information and Procedures

### 1. Find Client ID and Client Secret Key

**Procedure:**
1.  Log in to the [Azure Portal](https://portal.azure.com/).
2.  Navigate to **Azure Active Directory**.
3.  Select **App Registrations**, then locate the specific Azure AD Application.
4.  Within the Azure AD App's management blade, select **Certificates & Secrets**. Here you can find or generate client secrets.

### 2. How to Get a List of Users from Azure AD?

-   Refer to the Stack Overflow discussion for methods to retrieve a list of users from Azure AD:
    -   [How can I get a list of users from Azure AD?](https://stackoverflow.com/questions/64023983/how-can-i-get-list-of-users-from-azure-ad)