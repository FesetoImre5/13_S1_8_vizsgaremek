*** Settings ***
Documentation     Suite for Task Management
Resource          Resources.resource
Suite Setup       Run Keywords    Open Browser To Calentasker    AND    Login To System
Suite Teardown    Close Browser

*** Test Cases ***
Create A New Task
    [Documentation]    Test 4: Open CreateTaskModal, fill form, verify update.
    [Tags]    Task
    Go To    ${URL}/tasks
    Wait And Click    css:.btnNewTask
    Wait Until Element Is Visible    css:.modalContent    timeout=5s
    Input Text       css:.formGroup input[type="text"]    New Automated Task
    Wait And Click    css:.date-input
    Wait And Click    css:.day-cell.today
    Click Button     css:.btnCreate
    Wait For Toast   New Automated Task

Task Detail View
    [Documentation]    Test 5: Click a task and verify detail modal.
    [Tags]    Task
    Go To    ${URL}/tasks
    Wait Until Element Is Visible    css:.fadeInItem    timeout=5s
    Wait And Click    css:.fadeInItem .viewBtn
    Wait Until Element Is Visible    css:.modal-content    timeout=10s
    Page Should Contain Element      css:.title-row h2

Calendar Toggle
    [Documentation]    Test 6: Verify calendar component is visible.
    [Tags]    Task
    Go To    ${URL}/tasks
    Wait Until Element Is Visible    css:.tasksArea    timeout=5s
    # Attempt to click calendar button if it exists (mobile/toggle mode)
    Run Keyword And Ignore Error    Click Button    xpath://button[contains(., 'Calendar')]
    Wait Until Element Is Visible    css:.calendarArea, .calendar-grid    timeout=5s

Delete Task
    [Documentation]    Test 7: Verify delete confirmation modal.
    [Tags]    Task
    Go To    ${URL}/tasks
    Wait Until Element Is Visible    css:.fadeInItem    timeout=5s
    Wait And Click    css:.fadeInItem .viewBtn
    Wait Until Element Is Visible    css:.modal-content    timeout=5s
    Wait And Click    css:.btn-danger
    Wait Until Element Is Visible    css:.alert-overlay    timeout=5s
    Page Should Contain Element    css:.alert-content