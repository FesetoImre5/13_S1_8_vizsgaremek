*** Settings ***
Documentation     Suite for Group Collaboration
Resource          Resources.resource
Suite Setup       Run Keywords    Open Browser To Calentasker    AND    Login To System
Suite Teardown    Close Browser

*** Test Cases ***
Create A Group
    [Documentation]    Test 8: Verify group creation modal.
    [Tags]    Group
    Go To    ${URL}/groups
    Wait And Click    css:.createGroupBtn
    Wait Until Element Is Visible    css:.modalContent    timeout=5s
    Input Text       id:groupTitle    New Automated Group
    Input Text       id:groupDescription    This is a test group
    Wait And Click     css:.createBtn
    Wait Until Page Contains    New Automated Group    timeout=5s

Search For Users
    [Documentation]    Test 9: Verify user search filtering.
    [Tags]    Group
    Go To    ${URL}/groups
    Wait And Click    css:.listGroupItem
    Wait Until Element Is Visible    css:.user-search-container    timeout=5s
    Input Text       css:.search-input    testuser
    Wait Until Element Is Visible    css:.result-item    timeout=5s
    Page Should Contain    testuser