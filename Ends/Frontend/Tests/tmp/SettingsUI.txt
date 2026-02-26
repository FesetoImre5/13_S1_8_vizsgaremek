*** Settings ***
Documentation     Suite for User Profile & Localization
Resource          Resources.resource
Suite Setup       Run Keywords    Open Browser To Calentasker    AND    Login To System
Suite Teardown    Close Browser

*** Test Cases ***
Update Profile
    [Documentation]    Test 10: Change info and verify Success Toast.
    [Tags]    Profile
    Go To    ${URL}/profile
    Wait And Click    css:.editBtn
    Wait Until Element Is Visible    css:.editInput    timeout=5s
    Input Text       css:.editInput    UpdatedName
    Click Button     css:.saveBtn
    Wait For Toast   Success
    
    # Revert the username so that subsequent test suites can still log in
    Wait And Click    css:.editBtn
    Wait Until Element Is Visible    css:.editInput   timeout=5s
    Input Text       css:.editInput    testuser1234
    Click Button     css:.saveBtn
    Wait For Toast   Success

Language Switcher
    [Documentation]    Test 11: Verify i18n changes text to Hungarian.
    [Tags]    i18n
    Go To    ${URL}/tasks
    Wait And Click   css:.langBtn
    Wait Until Page Contains    Feladatok    timeout=10s

Logout Flow
    [Documentation]    Test 12: Verify session clear and redirect.
    [Tags]    Auth
    Wait And Click    css:.logoutBtn
    Wait Until Location Is    ${URL}/auth    timeout=5s
    # Final check: Try to go back to tasks and ensure redirect
    Go To    ${URL}/tasks
    Location Should Be    ${URL}/auth