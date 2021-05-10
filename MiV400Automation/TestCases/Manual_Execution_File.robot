*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py

Test Timeout  25 minutes
Suite Setup  Phones Initialization
Test Setup   Check Phone Connection
Test Teardown  Generic Test Teardown
Suite Teardown   Check Phone Connection

*** Test Cases ***

TC01: Active call
    [Tags]     MakeActiveCall
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
#    Then verify audio path between ${phone1} and ${phone2}
    And Disconnect the call from ${phone2}
#
#TC02: Transfer call
#    [Tags]     TransferCall
#    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
#    Then answer the call on ${phone1} using ${offHook}
#    Then verify audio path between ${phone1} and ${phone2}
#    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
#    Then Verify audio path between ${phone2} and ${phone3}
#    And disconnect the call from ${phone2}
#
#TC03: Conference call
#    [Tags]     TransferCall
#    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
#    Then answer the call on ${phone1} using ${offHook}
#    Then verify audio path between ${phone1} and ${phone2}
#    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
#    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
#    Then disconnect the call from ${phone2}
#    And disconnect the call from ${phone3}
