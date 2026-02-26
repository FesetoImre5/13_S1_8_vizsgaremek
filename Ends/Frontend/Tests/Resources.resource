*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            http://localhost:5173
${BROWSER}        Firefox
${VALID_USER}     testuser1234
${VALID_PASS}     password123

*** Keywords ***
Open Browser To Calentasker
    [Arguments]    ${path}=auth
    Open Browser    ${URL}/${path}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    5 seconds

Login To System
    [Arguments]    ${email}=${VALID_USER}    ${pass}=${VALID_PASS}
    Go To    ${URL}/auth
    Wait Until Element Is Visible    css:input[type="text"]    timeout=10s
    Input Text        css:input[type="text"]    ${email}
    Input Password    css:.passwordField input     ${pass}
    Click Button      css:button[type="submit"]
    Wait Until Location Is    ${URL}/profile    timeout=10s

Wait And Click
    [Arguments]    ${locator}
    Wait Until Element Is Visible    ${locator}    timeout=5s
    Click Element    ${locator}

Wait For Toast
    [Arguments]    ${text}
    # Matches common Vue toast classes
    Wait Until Page Contains    ${text}    timeout=5s