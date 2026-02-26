*** Settings ***
Documentation     Suite for Authentication and Security
Resource          Resources.resource
Suite Setup       Open Browser To Calentasker
Suite Teardown    Close Browser

*** Test Cases ***
Successful Login
    [Documentation]    Test 1: Verifies redirection to /profile.
    [Tags]    Auth    Critical
    Login To System    ${VALID_USER}    ${VALID_PASS}
    Location Should Be    ${URL}/profile

Failed Login
    [Documentation]    Test 2: Verifies error message appears.
    [Tags]    Auth
    Execute Javascript    window.localStorage.clear()
    Go To    ${URL}/auth
    Input Text        css:input[type="text"]    wrong@example.com
    Input Password    css:.passwordField input     wrongpassword
    Click Button      css:button[type="submit"]
    # Checking for common Vue error indicators
    Wait Until Element Is Visible    css:.toast, .toast-error, .error-message, .errorMessage    timeout=5s
    Location Should Be    ${URL}/auth

Unauthorized Access
    [Documentation]    Test 3: Verify redirection when logged out.
    [Tags]    Auth
    # Ensure session is cleared
    Execute Javascript    window.localStorage.clear()
    Go To    ${URL}/profile
    Wait Until Location Is    ${URL}/auth    timeout=5s
    Wait Until Element Is Visible    css:input[type="text"]    timeout=5s