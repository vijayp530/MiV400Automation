*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py

Test Timeout  25 minutes
Suite Setup  RUN KEYWORDS    Phones Initialization     Get DUT Details
Test Setup   RUN KEYWORDS    Check Phone Connection
Test Teardown  Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Generic Test Teardown

*** Test Cases ***

750287:TC17 : Speeddial/Xfer key
    [Tags]    Owner:Ram    Reviewer:    speedDial     Applicablefor400
    Given On ${phone1} program speeddialxfer key on position 3 with ${phone3} value
    Then On ${phone1} verify display message speeddialxfer
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then On ${phone1} verify display message ${phone3}
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} verify display message ${callTransferred}
    Then On ${phone2} verify display message ${phone3}
    And Disconnect the call from ${phone2}
    [Teardown]   Remove program button


TC18 : BLF/Xfer key
    [Tags]    Owner:Ram    Reviewer:    BLF    Applicablefor400
    Given On ${phone1} program blfxfer key on position 3 with ${phone3} value
    Then On ${phone1} verify display message blfxfer
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then On ${phone1} verify display message ${phone3}
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} verify display message ${callTransferred}
    Then On ${phone2} verify display message ${phone3}
    And Disconnect the call from ${phone2}
    [Teardown]   Remove program button

750289: TC20 : Deflect - Speeddial
    [Tags]    Owner:Ram    Reviewer:    SpeedDial    Applicablefor400
    Given On ${phone1} program speeddial key on position 3 with ${phone3} value
    Then On ${phone1} verify display message speeddial
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then On ${phone1} verify display message ${phone3}
    Then On ${phone1} press the softkey Deflect in RingingState
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} press the softkey Deflect_number in RingingState
    Then On ${phone1} verify display message ${callTransferred}
    Then On ${phone2} verify display message ${phone3}
    And Disconnect the call from ${phone2}
    [Teardown]   Remove program button

750290: TC30 : Deflect view - Answer by line key press
    [Tags]    Owner:Ram    Reviewer:    Deflect    Applicablefor400
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} press the softkey Deflect in RingingState
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And Disconnect the call from ${phone2}

750286 TC09 : Deflect - connected state
    [Tags]    Owner:Ram    Reviewer:    Deflect    Applicablefor400
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then On ${phone1} press the softkey Deflect in RingingState
    Then On ${phone1} enter number ${phone4}
    Then On ${phone1} verify display message ${callTransferred}
    Then On ${phone4} verify display message ${phone3}
    Then Disconnect the call from ${phone4}
    And Disconnect the call from ${phone2}

750285: TC08 : Deflecting to valid number
    [Tags]    Owner:Ram    Reviewer:    Deflect    Applicablefor400
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} press the softkey Deflect in RingingState
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} verify display message ${callTransferred}
    Then On ${phone3} verify display message ${phone2}
    And Disconnect the call from ${phone2}

750284:TC04 : Deflect functionality
    [Tags]    Owner:Ram    Reviewer:    Deflect    Applicablefor400
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} press the softkey Deflect in RingingState
    Then On ${phone1} verify the softkeys in Deflect
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} verify display message ${callTransferred}
    Then On ${phone3} verify display message ${phone2}
    And Disconnect the call from ${phone2}