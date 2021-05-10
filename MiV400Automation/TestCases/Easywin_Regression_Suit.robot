*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot

Library    ../lib/MyListner.py
Library    Collections
Library    String

Suite Setup    RUN KEYWORDS    Phones Initialization    Get DUT Details
Test Setup    Check Phone Connection
Test Teardown    Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Default Availability State    Generic Test Teardown
Test Timeout    25 minutes

*** Test Cases ***

542750: Cancel aborts Hang up call that is on Hold
    [Tags]      Owner:Aman      Reviewer:      hold
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then On the ${phone1} verify softkeys in different state using ${talk}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    And Disconnect the call from ${phone2}

535725: Cancel transfer from Consult screen while connected
    [Tags]      Owner:Aman      Reviewer:Vikhyat      transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${drop} in TransferState
    Then on ${phone3} verify the softkeys in ${idleState}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    And Disconnect the call from ${phone2}

537546: CHM Available edit mode-Never option
    [Tags]      Owner:Aman      Reviewer:      CHM     notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${never} in ${available}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Default Availability State

537535: CHM Custom edit mode-No Answer option
    [Tags]      Owner:Aman      Reviewer:      CHM     notApplicableFor6910    6930
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${custom}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 2 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number 1
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone1}

560587: CHM Custom edit mode-No Answer option
    [Tags]      Owner:Aman      Reviewer:      CHM     notApplicableFor6910    6930
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${custom}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone1}

537541: CHM In a Meeting edit mode-No Answer option
    [Tags]      Owner:Aman      Reviewer:      CHM     notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${inMeeting}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number 1
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone1}


560593: CHM In a Meeting edit mode-No Answer option
    [Tags]      Owner:Aman      Reviewer:      CHM     notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${all} in ${inMeeting}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${inMeeting}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone1}

560598: CHM Available edit mode-Never option
    [Tags]      Owner:Aman      Reviewer:Vikhyat      CHM     notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${all} in ${available}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${never} in ${available}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On the ${phone1} verify softkeys in different state using ${settings}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    And Disconnect the call from ${phone2}
    [Teardown]    Default Availability State

536906: Torture Test - Point-to-Point HOLD Test 1
    [Tags]      Owner:Aman      Reviewer:      torture_test    536906
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then put the linekey ${line1} of ${phone1} on ${unhold}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then put the linekey ${line1} of ${phone1} on ${unhold}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then put the linekey ${line1} of ${phone1} on ${unhold}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then put the linekey ${line1} of ${phone1} on ${unhold}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then put the linekey ${line1} of ${phone1} on ${unhold}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    And Disconnect the call from ${phone1}

536907: Torture Test - Point-to-Point HOLD Test 2
    [Tags]      Owner:Aman      Reviewer:      torture_test     536907
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    And Disconnect the call from ${phone1}

536909: Torture Test - Point-to-Point HOLD Test 4
    [Tags]      Owner:Aman      Reviewer:      torture_test
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    And Disconnect the call from ${phone1}

536910: Torture Test - Point-to-Point HOLD Test 5
    [Tags]      Owner:Aman      Reviewer:      torture_test
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}

    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}

    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}

    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}

    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}

    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}

#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone1}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${on} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone1}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${on} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone1}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${on} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone1}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${on} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone1}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone2}
#    Then verify the led state of ${line1} as ${on} on ${phone2}
#    Then press hardkey as ${holdState} on ${phone1}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
    And Disconnect the call from ${phone1}

542623: TC035 Access VoiceMail or Directory from Call History
    [Tags]      Owner:Aman      Reviewer:Vikhyat      directory    notApplicableFor6910
    Given press hardkey as ${callersList} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then On ${phone1} verify display message ${callHistory}
    Then Press hardkey as ${directory} on ${phone1}
    Then Verify ${byFirst} naming directory format on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

560152: Un-park call with 2 or more Held Calls on target extension
    [Tags]      Owner:Aman      Reviewer:Vikhyat      park     notApplicableFor6910
    Given I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${programKey2}
    Then press hardkey as ${holdState} on ${phone2}
    Then I want to unPark the call from ${phone2} on ${phone1} using ${default} and ${dial}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then verify the caller id on ${phone1} and ${phone4} display
    Then verify the caller id on ${phone2} and ${phone3} display
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line2} as ${off} on ${phone2}
    Then Disconnect the call from ${phone1}
    And Disconnect the call from ${phone3}

537318: Un-park progbutton target not set (invalid extension)
    [Tags]      Owner:Aman      Reviewer:      park     notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number 12345
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${displayMessage['noCallsToUnpark']}
    Then verify the caller id on ${phone2} and ${phone3} display
    And Disconnect the call from ${phone2}

539783: Verify Actions keys on Phone
    [Tags]      Owner:Aman      Reviewer:      verify_action_keys
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then On ${phone1} verify the softkeys in ${talk}
    Then press hardkey as ${holdState} on ${phone1}
    Then On ${phone1} verify display message ${pickUp}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    And Disconnect the call from ${phone2}

539563: Rapidly switching between two connected calls ends up with two active calls
    [Tags]      Owner:Aman      Reviewer:      call_appearance
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

535733: Press Transfer while call is ringing
    [Tags]      Owner:Aman      Reviewer:      transfer     notApplicableFor6910    6930
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone3} press the softkey ${transfer} in RingingState
    Then on ${phone3} enter number ${phone4}
    Then on ${phone3} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} wait for 3 seconds
    Then verify extension ${number} of ${phone1} on ${phone4}
    Then Answer the call on ${phone4} using ${loudspeaker}
    Then On ${phone3} verify the softkeys in ${idleState}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then Verify audio path between ${phone2} and ${phone4}
    Then On ${phone1} verify the softkeys in ${idleState}
    And Disconnect the call from ${phone4}

730893: on hook with offhook transition- extension
    [Tags]      Owner:Aman      Reviewer:Vikhyat      dial_plan     notApplicableFor6910
    Given On ${phone1} dial partial number of ${phone2} with ${firstTwo}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${backupAutoAttendant}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} enter number ${phone2}

    Then Press hookMode ${offHook} on phone ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    And Disconnect the call from ${phone2}

730824: Transferor presses Transfer after consult goes to VM
    [Tags]      Owner:Aman      Reviewer:      transfer     notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then on ${phone1} wait for 12 seconds
    Then On ${phone1} verify display message ${displayVoiceMail}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then On ${phone3} verify the softkeys in ${idleState}
    And Disconnect the call from ${phone2}

730795: Transferee hangs up while directory is open
    [Tags]      Owner:Aman      Reviewer:      transfer     notApplicableFor6910    6930
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone3}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then verify ringing state on ${phone1} and ${phone3}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Disconnect the call from ${phone1}
    And Disconnect the call from ${phone3}

730794: Directory display when filtering
    [Tags]      Owner:Aman      Reviewer:      transfer     notApplicableFor6910        730794
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone3}
    Then Press hardkey as ${goodBye} on ${phone1}
    And Disconnect the call from ${phone2}

730855: Display Off Hook in the focused session window
    [Tags]      Owner:Aman      Reviewer:      display    6930
    Given Press hookMode ${offHook} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Press hookMode ${onHook} on phone ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of speaker as ${on} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

751007: Play Visual VM during active call
    [Tags]      Owner:Aman      Reviewer:      voicemail        notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then on ${phone1} Press ${hardkey} ${scrollRight} for 1 times
    Then on ${phone1} press the softkey ${play} in VoiceMailState
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
#    Then On ${phone1} Wait for 15 seconds
    Then On ${phone1} verify the softkeys in ${voiceMailState}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    And Press hardkey as ${goodBye} on ${phone2}

751005: Press 5-way nav left arrow to return to History
    [Tags]      Owner:Aman      Reviewer:      navigation
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${details}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} Press ${hardkey} ${scrollLeft} for 1 times
    Then on ${phone1} verify the softkeys in ${callHistory}
    And Press hardkey as ${goodBye} on ${phone1}

750949: receive a consult transfer (transfer target) negative Test case
    [Tags]      Owner:Aman      Reviewer:      transfer
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then Verify audio path between ${phone2} and ${phone3}
    And Press hardkey as ${goodBye} on ${phone2}

751015: phone uses nav to view conference parties
    [Tags]      Owner:Aman      Reviewer:      conference       notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${ConsultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${hardkey} ${scrollUp} for 1 times
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

537544:CHM Out Of office edit mode-No Answer option
    [Tags]    Owner:Gaurav    Reviewer:Aman         CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${outOfOffice}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone1} verify display message ${save}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone1} verify display message ${save}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 2 times
    Then on ${phone1} enter number 5
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${cancel}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${cancel}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${cancel}
    And press hardkey as ${goodbye} on ${phone1}

537547: CHM Standard edit mode-No Answer option
    [Tags]    Owner:Gaurav    Reviewer:Aman    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${available}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone1} verify display message ${save}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone1} verify display message ${save}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 2 times
    Then on ${phone1} enter number 5
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${cancel}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${cancel}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${cancel}
    And press hardkey as ${goodbye} on ${phone1}

539475: Dial some digits and press #
    [Tags]    Owner:Gaurav    Reviewer:Aman    dialPlan
    Given Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} dial number 12#
    Then On ${phone1} verify display message ${requestDenied}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hookMode ${onHook} on phone ${phone1}
    Then on ${phone1} dial number 12#
    Then On ${phone1} verify display message ${requestDenied}
    And Press hardkey as ${goodBye} on ${phone1}

535928:Consult Transfer via timeout
    [Tags]    Owner:Gaurav    Reviewer:Aman         transfer         notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} verify display message ${transfer}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${transfer}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then On ${phone1} verify the softkeys in ${idle}
    And Disconnect the call from ${phone3}

535924:Consult call is transferred to another user
    [Tags]    Owner:Gaurav    Reviewer:Aman         transfer         notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} verify display message ${transfer}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${transfer}
    Then Initiate Transfer on ${phone3} to ${phone4} using ${consult}
    Then Answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone3} press the softkey ${transfer} in TransferState
    Then verify audio path between ${phone1} and ${phone4}
    Then on ${phone4} verify display message ${transfer}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then On ${phone1} verify the softkeys in ${idle}
    Then verify audio path between ${phone2} and ${phone4}
    And Disconnect the call from ${phone4}

535950: Consult call transferred while active
    [Tags]    Owner:Gaurav    Reviewer:Aman    Consult Transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Disconnect the call from ${phone2}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    And Disconnect the call from ${phone2}

538446:Consult Conf. Cancel
     [Tags]    Owner:Gaurav    Reviewer:         Consult Transfer
     Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
     Then Answer the call on ${phone2} using ${loudspeaker}
     Then verify audio path between ${phone1} and ${phone2}
     Then on ${phone1} press the softkey ${conference} in AnswerState
     Then on ${phone1} enter number ${phone3}
     Then on ${phone1} wait for 5 seconds
     Then press hardkey as ${goodBye} on ${phone1}
     Then On ${phone3} verify the softkeys in ${idle}
     Then put the linekey ${line1} of ${phone1} on ${unhold}
     Then verify audio path between ${phone1} and ${phone2}
     And disconnect the call from ${phone2}


542912:Consult transfer using Consult key
    [Tags]    Owner:Gaurav    Reviewer:                  Consult Transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Disconnect the call from ${phone1}
    And Disconnect the call from ${phone2}


535929:Consult transfer with 2nd call on phone
    [Tags]    Owner:Gaurav    Reviewer:                Consult Transfer      notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then Transfer call from ${phone1} to ${phone4} using ${temp}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} verify display message ${transfer}
    Then Answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${transfer}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then Verify the led state of mute as ${off} on ${phone2}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}



535940:Consultative Transfer - UnHold while Consult ringing
    [Tags]    Owner:Gaurav    Reviewer:               Consult Transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of Line1 as blink on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then i want to press line key ${line1} on phone ${phone1}
    And Disconnect the call from ${phone1}

536772: Pressing hold button multiple times drops call
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    press key
     Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
     Then answer the call on ${phone2} using ${loudspeaker}
     Then verify audio path between ${phone1} and ${phone2}
     Then put the linekey ${line1} of ${phone1} on ${hold}
     Then put the linekey ${line1} of ${phone1} on ${unhold}
     Then put the linekey ${line1} of ${phone1} on ${hold}
     Then put the linekey ${line1} of ${phone1} on ${unhold}
     Then put the linekey ${line1} of ${phone1} on ${hold}
     Then put the linekey ${line1} of ${phone1} on ${unhold}
     And Disconnect the call from ${phone1}

542837:PressMute before answering an incoming call
    [Tags]    Owner:Gaurav    Reviewer:               press key
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone1}

557866: PressMute button while phone receives incoming unanswered call
     [Tags]    Owner:Gaurav    Reviewer:Vikhyat    mute
     Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
     Then verify ringing state on ${phone2} and ${phone1}
     Then press hardkey as ${mute} on ${phone1}
     Then Verify the led state of mute as ${off} on ${phone1}
     Then on ${phone1} wait for 40 seconds
     Then On ${phone2} verify display message ${displayVoiceMail}
     Then press hardkey as ${mute} on ${phone1}
     Then Verify the led state of mute as ${off} on ${phone1}
     And disconnect the call from ${phone2}

557867: PressMute while in Active call Handset
    [Tags]    Owner:Gaurav    Reviewer:                 press key
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    And disconnect the call from ${phone2}

535865: Retry transfer after a blind transfer to invalid #     
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    blindTransfer    notApplicableFor6910    535865
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in answerstate
    Then on ${phone1} enter number ${invalidNumber}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then On ${phone1} verify display message ${invalidPhoneNumber}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    And disconnect the call from ${phone1}

536883: Put on hold by initiating another call via Directory
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    via Directory
     Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
     Then Answer the call on ${phone1} using ${offhook}
     Then verify audio path between ${phone1} and ${phone2}
     Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
     Then Answer the call on ${phone1} using ${programKey2}
     Then verify audio path between ${phone3} and ${phone1}
     Then verify the led state of ${line1} as ${on} on ${phone2}
     Then verify the led state of ${line1} as ${on} on ${phone3}
     Then On ${phone1} press directory and ${dial} of ${phone4}
     Then Answer the call on ${phone4} using ${loudspeaker}
     Then verify audio path between ${phone1} and ${phone4}
     Then verify the led state of ${line1} as ${blink} on ${phone1}
     Then verify the led state of ${line2} as ${blink} on ${phone1}
     Then verify the led state of ${line3} as ${on} on ${phone1}
     Then disconnect the call from ${phone2}
     Then disconnect the call from ${phone3}
     Then disconnect the call from ${phone1}
     And On ${phone1} verify the softkeys in ${idle}

536881:Put multiple calls on hold by pressing another call appearance key
    [Tags]    Owner:Gaurav    Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${programKey2}
    Then verify audio path between ${phone1} and ${phone3}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${programKey3}
    Then verify audio path between ${phone1} and ${phone4}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then i want to press line key ${programkey4} on phone ${phone1}
    Then i want to press line key ${programkey3} on phone ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to press line key ${programkey3} on phone ${phone1}
    Then i want to press line key ${line2} on phone ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to press line key ${line2} on phone ${phone1}
    Then i want to press line key ${line1} on phone ${phone1}
    And press hardkey as ${goodBye} on ${phone1}



542862:Drop a call while in conference from a far end and rejoin
    [Tags]    Owner:Gaurav    Reviewer:                notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then on ${phone1} wait for 2 seconds
    Then press hardkey as ${scrollUp} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${drop} in ConferenceCallState
    Then i want to make a conference call between ${phone3},${phone2} and ${phone1} using ${directConference}
    Then press hardkey as ${goodBye} on ${phone1}
    And disconnect the call from ${phone3}

538256: Enter invalid digit length, press speaker or headset button
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    invalidNumber
    Given Press hardkey as ${handsFree} on ${phone1}
    Then on ${phone1} enter number ${fivedigitnumber}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone1} verify display message ${requestDenied}
    And Press hardkey as ${goodBye} on ${phone1}

536851: Far-end (phone) places phone on remote hold, answer via HEADSET or SPEAKER
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    holdUnhold
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then verify no audio path from ${phone2} to ${phone1}
    Then Press hardkey as ${handsFree} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify no audio path from ${phone1} to ${phone2}
    And disconnect the call from ${phone2}

535958:Hang Up Transferor to transfer while consult is ringing
    [Tags]    Owner:Gaurav    Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${Consult}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then press hardkey as ${goodBye} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    And disconnect the call from ${phone2}



538399:Hangup phone user from the MERGE session
    [Tags]    Owner:Gaurav    Reviewer:         MERGE              notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${programKey3}
    Then Answer the call on ${phone4} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${merge} in AnswerState
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone3}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone4}


536845:Far-end party places phone on remote hold, answer via HANDSET
    [Tags]    Owner:Gaurav    Reviewer:             Far-end
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then Verify the led state of Line1 as blink on ${phone2}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then Verify the led state of Line1 as blink on ${phone2}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    And disconnect the call from ${phone2}


536889:Headset or Speaker answers, press idle call appearance on the left or right
    [Tags]    Owner:Gaurav    Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${line2} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then Verify the led state of Line1 as blink on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    And disconnect the call from ${phone2}



535945:Transferee hangs up while Consult is active
    [Tags]    Owner:Gaurav    Reviewer:        Consult           notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then On ${phone3} Wait for 5 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${transfer}
    Then press hardkey as ${goodbye} on ${phone1}
    And disconnect the call from ${phone2}

535765:Transfer to Voicemail while in active call
    [Tags]    Owner:Gaurav    Reviewer:       Transferor presses       notApplicableFor6910
    Given delete voicemail message on ${inbox} for ${phone3} using ${voicemailpassword}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} press the softkey ${more} in TransferState
    Then Verify the led state of ${line1} as blink on ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${ToVm} in TransferState
    Then on ${phone1} wait for 5 seconds
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then press hardkey as ${goodbye} on ${phone2}


539089:Transfer, Conference, Hold disabled when Filter is open in Call History
    [Tags]    Owner:Gaurav    Reviewer:         Transferor presses      notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${All} and ${details}
    And press hardkey as ${goodbye} on ${phone1}

539775:Verify Call History key order
    [Tags]    Owner:Gaurav    Reviewer:         Verify Call History    notApplicableFor6910
    Then press the call history button on ${phone1} and folder ${all} and ${nothing}
    Then On ${phone1} verify display message ${Quit}
    And Press hardkey as ${goodBye} on ${phone1}


539776:Verify Conference screen keys
    [Tags]    Owner:Gaurav    Reviewer:       Verify Conference    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone1} verify display message ${consult}
    Then On ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone2}

539778:Verify Directory key order
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    directoryKeys    notApplicableFor6910    539778
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

539779:Verify Transfer screen keys
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    transferKeys    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} verify display message ${consult}
    Then On ${phone1} verify display message ${transfer}
    And Press hardkey as ${goodBye} on ${phone2}

540005:Verify that when outbound call is made, display name appears on the screen
    [Tags]    Owner:Gaurav    Reviewer:         key order
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then put the linekey ${line1} of ${phone2} on ${hold}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then verify the caller id on ${phone1} and ${phone2} display
    And Press hardkey as ${goodBye} on ${phone2}


561216:Visual Voicemail, Password Change Checkbox=False
    [Tags]    Owner:Gaurav    Reviewer:         Voicemail    notApplicableFor6910
    Given Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then on ${phone1} verify display message ${inbox}
    Then on ${phone1} verify display message ${visualVoicemailScreen}
    And Press hardkey as ${goodBye} on ${phone1}


540014:Verify the call appearance when an outbound call is answered
    [Tags]    Owner:Gaurav    Reviewer:        Verify
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    When Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    And disconnect the call from ${phone2}

539492:offhook with completed valid numbers- extension
    [Tags]    Owner:Gaurav    Reviewer:
    Given Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    And disconnect the call from ${phone2}

538805:Authentication before Editing - Incorrect password
    [Tags]    Owner:Gaurav    Reviewer:         notApplicableFor6910
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} enter number 11111
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${incorrectPassword}
    Then on ${phone1} enter number 11111
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${incorrectPassword}
    Then on ${phone1} enter number 11111
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${incorrectPassword}
    And press hardkey as ${goodbye} on ${phone1}

558131: Cancel transfer from Consult screen after going to VM
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    cancelTransfer
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${Consult}
    Then Verify ringing state on ${phone1} and ${phone3}
    Then on ${phone3} press the softkey ${ToVm} in RingingState
    Then On ${phone1} Wait for 3 seconds
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then press hardkey as ${holdState} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

536781:place multiple calls on hold
    [Tags]    Owner:Gaurav    Reviewer:    holdUnhold    536781
    Given i want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then verify ringing state on ${phone1} and ${phone3}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then on ${phone2} wait for 1 seconds
    Then i want to press line key ${line1} on phone ${phone1}
    Then on ${phone2} wait for 2 seconds
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    And disconnect the call from ${phone3}

730946:Hang up call that is on Hold by pressing the Drop softkey
    [Tags]    Owner:Gaurav    Reviewer:    endCall
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone2} verify display message ${drop}
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone2} verify display message ${drop}
    And on ${phone2} press the softkey ${drop} in AnswerState

730960: Leave a voicemail on phone
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    voiceMail
    Given Set number of rings to 3 on ${phone1}
    Given Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then on ${phone2} wait for 50 seconds
    Then press hardkey as ${goodbye} on ${phone2}
    And Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    [Teardown]    Default Number of Rings

730971: Call Handling mode(CHM) options set to In a Meeting
    [Tags]    Owner:Gaurav    Reviewer:    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${always} in ${inMeeting}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone1} verify display message ${save}
    Then press softkey ${save} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then press hardkey as ${goodbye} on ${phone2}
    [Teardown]    Default Availability State

536952: Whisper Page not on a call. Initiation allowed.
    [Tags]    Owner:Vikhyat    Reviewer:    Migration    whisperPage
    Given I want to use fac ${whisperPageFAC} on ${phone1} to ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

536782: With call on hold, press Hang up, then press CALL APPEARANCE key to Unhold call
    [Tags]    Owner:Vikhyat    Reviewer:    Migration    holdUnhold    6930
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then I want to verify on ${phone1} negative display message ${drop}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

542847: Auto Unmute when there is 1 active call and N locally held calls
    [Tags]    Owner:AbhishekPathak    Reviewer    heldcalls    542847
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programkey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programkey2}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programkey3}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify the led state of ${line3} as ${on} on ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then verify one way audio from ${phone4} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone4}      # getting failed at this
    Then disconnect the call from ${phone4}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone2}
    And press hardkey as ${goodbye} on ${phone3}

542845:Auto Unmute when an active muted call goes to onhook held state
    [Tags]    Owner:AbhishekPathak    Reviewer    heldcalls    6930
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}

539615:Call Appearance attachment-single call
    [Tags]    Owner:AbhishekPathak    Reviewer    singlecall
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}

539875:Call Offering press #
    [Tags]    Owner:AbhishekPathak    Reviewer    press
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then on ${phone2} dial number #
    Then on ${phone1} verify display message ${displayVoiceMail}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone2}

538289:Caller ID is displayed when ring back is heard
    [Tags]    Owner:AbhishekPathak    Reviewer    callheard
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then disconnect the call from ${phone1}

537696: Call history user with additional numbers
    [Tags]    Owner:AbhishekPathak    Reviewer:    callhistory    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    Then press the call history button on ${phone1} and folder ${all} and ${details}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} verify display message ${dial}
    Then on ${phone1} verify display message ${intercom}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}

539613: Call Appearance attachment-handset
    [Tags]    Owner:AbhishekPathak    Reviewer    callappearance
    Given i want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${programKey1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then disconnect the call from ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}

535851: Blind transfer to nonexistant extension
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    transfer    6930
    &{pmargst} =  Create Dictionary  key=${transfer}
    &{pressHardkey} =  Create Dictionary  action_name=pressHardkey   pmargs=&{pmargst}
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in answerstate
    Then on ${phone1} enter number ${wrong_number}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then on ${phone1} due to action ${pressHardkey} popup raised verify message ${transfer_invalid_number} with wait of 0
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone2}

562829: Option menu screen
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    option    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then on ${phone1} press the softkey ${cancel} in DialingState
    Then on ${phone1} verify the softkeys in ${menu}
    Then press hardkey as ${goodbye} on ${phone1}
    And on ${phone1} verify the softkeys in ${idle}

535818: Phone acts as TransferOR in a blind transfer by hanging up the Call
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    transfer    6930
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then on ${phone1} wait for 5 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 5 seconds
    Then Verify ringing state on ${phone1} and ${phone3}
    Then press hardkey as ${goodbye} on ${phone1}
    Then on ${phone1} verify display message ${callTransferred}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} verify the softkeys in ${idle}
    Then verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone1}

537342:phone completes blind conference
    [Tags]    Owner:AbhishekPathak    Reviewer:    conference
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} verify display message ${conference}
    Then disconnect the call from ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then verify audio path between ${phone2} and ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then disconnect the call from ${phone2}

536927:phone dials *13 to Pickup Unpark a call
    [Tags]    Owner:AbhishekPathak    Reviewer:    facpickup
    Given i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then I want to use fac ${pickup} on ${phone1} to ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then on ${phone2} verify the softkeys in ${idle}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}

558337:Phone is the transferee- transfer target is busy or unavailable
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} press the softkey ${transfer} in answerstate
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} verify the softkeys in ${idle}
    Then on ${phone3} wait for 20 seconds
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}

537614: Press and Hold Back key in Call History sub view
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    callhistory    notApplicableFor6910
    Given press the call history button on ${phone1} and folder ${all} and ${details}
    Then on ${phone1} verify display message ${close}
    Then press softkey ${close} on ${phone1}
    Then on ${phone1} verify display message ${callhistory}
    And press hardkey as ${goodbye} on ${phone1}

537701: Press Back on History detail screen
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    callhistory    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then disconnect the call from ${phone1}
    Then press the call history button on ${phone1} and folder ${all} and ${details}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} verify display message ${close}
    Then on ${phone1} wait for 2 seconds
    Then press softkey ${close} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    And press hardkey as ${goodbye} on ${phone1}

560925:Press dial in call History
    [Tags]    Owner:AbhishekPathak    Reviewer:    callhistory    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press the call history button on ${phone1} and folder ${all} and ${details}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then verify extension ${number} of ${phone3} on ${phone1}
    And disconnect the call from ${phone1}

560927:Press Fire key in call history
    [Tags]    Owner:AbhishekPathak    Reviewer:    callhistory
    Given i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press the call history button on ${phone1} and folder ${all} and ${nothing}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press the call history button on ${phone1} and folder ${all} and ${details}
    Then press hardkey as ${enter} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone1}

560134:Press Park to prompt for destination
    [Tags]    Owner:AbhishekPathak    Reviewer:    park    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to park the call from ${phone1} on ${phone3} using ${default} and ${park}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then disconnect the call from ${phone2}

537313:Press Park then press Cancel key
    [Tags]    Owner:AbhishekPathak    Reviewer:    park
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${cancel}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify the softkeys in ${park}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}

537309: Press Park key enter invalid 5 digit destination
    [Tags]    Owner:AbhishekPathak    Reviewer:    park    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Press softkey ${park} on ${phone1}
    Then on ${phone1} verify the softkeys in ${park}
    Then on ${phone1} dial number ${fivedigitnumber}
    Then On ${phone1} verify display message ${backSpace}
    Then on ${phone1} wait for 10 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}

537307: Press Park key enter destination from Directory or Redial
    [Tags]    Owner:AbhishekPathak    Reviewer:    park    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${directory} and ${timeout}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then disconnect the call from ${phone2}

542836:Press Mute while phone switches from one active call to another call
    [Tags]    Owner:AbhishekPathak    Reviewer:    mute    6930
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then verify the led state of mute as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify the led state of mute as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify one way audio from ${phone3} to ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

542841:Switch to different audio paths while Mute button is enabled
    [Tags]    Owner:AbhishekPathak    Reviewer:    mute
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${offhook}
    Then verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then verify the led state of mute as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Press hardkey as ${handsFree} on ${phone1}
    Then verify the led state of mute as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then disconnect the call from ${phone1}

542815: TC004 Participant Drop from the conference list
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    conference
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${offhook}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${leave}
    Then Press hardkey as ${scrollDown} on ${phone3}
    Then on ${phone3} press the softkey ${drop} in AnswerState
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}

542589: TC002 Phone perfrom numeric search, then Cancel
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    directory    notApplicableFor6910
    Given press hardkey as ${directory} on ${phone1}
    Then On ${phone1} verify display message ${enterprise}
    Then on ${phone1} dial number 1
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${reset}
    Then on ${phone1} verify display message ${quit}
    And press softkey ${quit} on ${phone1}

542596: TC009 Incoming calls offered behind Directory screen
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    directory    notApplicableFor6910
    Given press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify the softkeys in ${directory}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} Wait for 3 seconds
    Then on ${phone1} verify display message ${details}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the softkeys in ${idle}

542620: TC032 Receive a call in empty Directory page
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    directory
    Given On ${phone1} verify directory with ${directoryAction['searchInvalid']} of ${phone1}
    Then on ${phone1} verify display message No Matches Found
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone2}
    And On ${phone1} verify the softkeys in ${idle}

542622: TC034 Access Voicemail or Call History from Directory
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    directory
    Given press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify the softkeys in ${directory}
    Then press hardkey as ${redial} on ${phone1}
    Then on ${phone1} verify display message ${callhistory}
    Then press hardkey as ${goodbye} on ${phone1}

562527: select traceroute from diagnostics
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    traceroute
    Given On ${phone1} move to ${diagnostics} to ${traceroute} settings
    Then on ${phone1} verify display message ${traceroutecommand}
    Then press hardkey as ${goodbye} on ${phone1}

536911: Torture Test - Point-to-Point HOLD Test 6
    [Tags]      Owner:AbhishekPathak      Reviewer:      torture_test
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    And Disconnect the call from ${phone1}

535911: TRANSFER - Consult call is being immediately dialed after full extn is entered in Transfer dialog
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}

535964:Transfer call is consult transferred and canceled.
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer    notApplicableFor6910    6930
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Initiate Transfer on ${phone3} to ${phone4} using ${timeout}
    Then answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}

535944:Transfer target hangs up during Consult
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press the softkey ${transfer} in answerstate
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then on ${phone2} verify display message ${transfer}
    Then on ${phone2} enter number ${phone3}
    Then on ${phone3} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then on ${phone2} verify display message ${drop}
    Then on ${phone2} verify display message ${transfer}
    Then press hardkey as ${goodbye} on ${phone3}
    Then on ${phone3} verify the softkeys in ${idle}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then disconnect the call from ${phone1}

535754: Transfer incoming call with held call on phone
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    transfer    6930
    Given Set number of rings to 6 on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programKey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then Transfer call from ${phone1} to ${phone4} using ${unattendedtransfer}
    Then answer the call on ${phone4} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone4}
    [Teardown]    Default Number of Rings

535956: Transferor presses Transfer while on consult
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programKey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify the softkeys in ${idle}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}

535870: Unhold call with Call Appearance key after blind transfer to invalid #
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programKey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} dial number ${invalidnumber}
    Then press hardkey as ${goodbye} on ${phone1}
    Then i want to press line key ${line1} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}

535801: Transferred call rings target if Consult on remote hold
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${programKey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press the softkey ${transfer} in AnswerState
    Then on ${phone2} enter number ${phone3}
    Then on ${phone3} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then on ${phone2} press the softkey ${transfer} in AnswerState
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then press hardkey as ${goodbye} on ${phone1}

538682: unpark - extension
    [Tags]    Owner:AbhishekPathak    Reviewer:    unpark    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to park the call from ${phone1} on ${phone3} using ${default} and ${park}
    Then on ${phone3} wait for 2 seconds
    Then i want to unpark the call from ${phone3} on ${phone1} using ${default} and ${select}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${programKey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone4} using ${loudspeaker}
    Then answer the call on ${phone4} using ${programKey1}
    Then verify audio path between ${phone3} and ${phone4}
    Then i want to park the call from ${phone1} on ${phone5} using ${default} and ${park}
    Then i want to park the call from ${phone4} on ${phone5} using ${default} and ${park}
    Then verify the led state of ${line1} as ${blink} on ${phone5}
    Then verify the led state of ${line2} as ${blink} on ${phone5}
    Then i want to unpark the call from ${phone5} on ${phone1} using ${default} and ${select}
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone3}


542604: TC017 From contacts detailed view window, press 5-way left nav arrow to return to Directory
    [Tags]    Owner:AbhishekPathak    Reviewer:    directory    notApplicableFor6910
    Given on ${phone1} press directory and ${details} of ${phone2}
    Then on ${phone1} verify display message Email
    Then on ${phone1} wait for 2 seconds
    Then Press hardkey as ${scrollLeft} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then on ${phone1} wait for 2 seconds
    Then press hardkey as ${goodbye} on ${phone1}

542605: TC018 From contacts detailed view window, press Exit softkey to return to Directory
    [Tags]    Owner:AbhishekPathak    Reviewer:    directory    notApplicableFor6910
    Given on ${phone1} press directory and ${details} of ${phone2}
    Then on ${phone1} verify display message Email
    Then on ${phone1} wait for 2 seconds
    Then press softkey ${close} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then on ${phone1} wait for 2 seconds
    Then press hardkey as ${goodbye} on ${phone1}

542802:With partial digit entry, answer incoming call
    [Tags]    Owner:AbhishekPathak    Reviewer:    partial
    Given On ${phone1} dial partial number of ${phone2} with ${firsttwo}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}
    Then On ${phone1} verify the softkeys in ${idle}

560758: TC019 From Directory Detailed Contacts view, use 5-way nav up and down arrows to scrolll thru numbers
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    directory    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message Email
    Then on ${phone1} wait for 2 seconds
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    And press hardkey as ${goodbye} on ${phone1}

566353: Phone cancels logfile upload to FTP Server
    [Tags]    Owner:AbhishekPathak    Reviewer:    logupload    notApplicableFor6910
    Given On ${phone1} move to ${diagnostics} to ${diagnosticsServer} settings
    Then Enter ${ftpServer} on ${phone1} to ${diagnostics} settings
    Then press hardkey as ${goodbye} on ${phone1}
#    Then on ${phone1} navigate to ${diagnostics} settings
    Then On ${phone1} move to ${diagnostics} to ${log_upload} settings
#    Then upload log from ${phone1}
    Then On ${phone1} press the softkey ${upload} in Diagnostics ${log_upload} Settings
    Then On ${phone1} Wait for 3 seconds
    Then on ${phone1} verify display message Collecting Logs
    Then press softkey ${close} on ${phone1}
    Then on ${phone1} verify display message ${Diagnostics}
    Then press hardkey as ${goodbye} on ${phone1}
    Then on ${phone1} move to settings ${diagnostics} to ${diagnosticserverdelete} settings with 1
    Then press hardkey as ${goodbye} on ${phone1}

560108: phone dials 13 + Pickup Group extension
    [Tags]    Owner:AbhishekPathak    Reviewer:    grouppickup    notApplicableForMiCloud
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then i want to use fac ${pickup} on ${phone3} to ${grouppickup}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}

560109: phone dials 13 + Pickup Group extension after call is picked up
    [Tags]    Owner:AbhishekPathak    Reviewer:    grouppickup    notApplicableForMiCloud
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then i want to use fac ${pickup} on ${phone3} to ${grouppickup}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone4} wait for 5 seconds
    Then i want to use fac ${pickup} on ${phone4} to ${grouppickup}
    Then on ${phone4} wait for 2 seconds
    Then on ${phone4} verify display message No calls to pickup
    Then press hardkey as ${goodbye} on ${phone4}
    Then disconnect the call from ${phone3}

562519:Ping to valid IP (on phone)
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat   ipPing
    Given on ${phone1} move to ${diagnostics} to ${ping} settings
    Then on ${phone1} wait for 5 seconds
    Then Enter ${ipaddrstr} on ${phone1} to ${ping} settings
    Then On ${phone1} verify display message ${pinging}
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times

562518:Ping to valid DNS (on phone)
    [Tags]    Owner:AbhishekPathak    Reviewer:Aman   dnsPing
    Given on ${phone1} move to ${diagnostics} to ${ping} settings
    Then on ${phone1} wait for 5 seconds
    Then enter dns string google.com on ${phone1}
    Then On ${phone1} press the key ${ping} in state ${ping}
    Then On ${phone1} verify display message ${pinging}
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times
    And press hardkey as ${goodBye} on ${phone1}

539874 :Active call during call offering
	[Tags]    Owner:Avishek    1    6930
	Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Answer the call on ${phone2} using ${loudspeaker}
	Then Verify audio path between ${phone1} and ${phone2}
	Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then Verify the caller id on ${phone3} and ${phone1} display
	Then Verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the led state of ${line2} as ${blink} on ${phone1}
	Then On ${phone1} press the softkey ${toVm} in RingingState
	Then On ${phone3} verify display message Voice Mail
	Then Disconnect the call from ${phone2}
	Then Disconnect the call from ${phone3}

535703 : active call on hold, second call comes in and is dismissed- far end hangs up
	[Tags]    Owner:Avishek    2
	Given press the call history button on ${phone1} and folder ${missed} and ${goodBye}
	Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then press hardkey as ${holdState} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then verify the caller id on ${phone3} and ${phone1} display
	Then verify the led state of ${line2} as ${blink} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then disconnect the call from ${phone3}
	Then verify the caller id on ${phone1} and ${phone2} display
	Then press hardkey as ${holdState} on ${phone1}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then disconnect the call from ${phone2}
	Then on ${phone1} verify display message Missed Call

535704: active call up on call appearance other than 1st, second call comes in and is dismissed- call goes to VM
    [Tags]    Owner:Avishek    Reviewer:
	Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey3}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line3} as ${on} on ${phone1}
	Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then Verify the Caller id on ${phone3} and ${phone1} display
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then verify the led state of ${line3} as ${on} on ${phone1}
	Then On ${phone1} wait for 50 seconds
	Then on ${phone3} verify display message ${displayVoiceMail}
	Then disconnect the call from ${phone3}
	Then verify the led state of ${line1} as ${off} on ${phone1}
	Then Verify the Caller id on ${phone2} and ${phone1} display
	Then verify the led state of ${line3} as ${on} on ${phone1}
	And disconnect the call from ${phone2}

535705 : active call up on call appearance other than 1st, second call comes in and is dismissed- far end hangs up
	[Tags]    Owner:Avishek    4
	Given press the call history button on ${phone1} and folder ${missed} and ${goodBye}
	Then i want to make a two party call between ${phone1} and ${phone2} using ${programKey3}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line3} as ${on} on ${phone1}
	Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then Verify the Caller id on ${phone3} and ${phone1} display
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then verify the led state of ${line3} as ${on} on ${phone1}
	Then disconnect the call from ${phone3}
	Then verify the led state of ${line1} as ${off} on ${phone1}
	Then Verify the Caller id on ${phone2} and ${phone1} display
	Then verify the led state of ${line3} as ${on} on ${phone1}
	Then disconnect the call from ${phone1}

535707 : active call up, second call comes in and is dismissed- far end hangs up
	[Tags]    Owner:Avishek    5
	Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the caller id on ${phone1} and ${phone2} display
	Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then verify the led state of ${line2} as ${blink} on ${phone1}
	Then verify the caller id on ${phone3} and ${phone1} display
	Then disconnect the call from ${phone3}
	Then verify the led state of ${line2} as ${off} on ${phone1}
	Then verify the caller id on ${phone1} and ${phone2} display
	Then disconnect the call from ${phone1}
	Then on ${phone1} verify display message Missed Call
	Then verify the led state of ${line1} as ${off} on ${phone1}

542843: Auto Unmute when a held muted call gets disconnected
	[Tags]    Owner:Avishek    Reviewer:Vikhyat    muteAfterHold
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then verify audio path between ${phone2} and ${phone1}
	Then press hardkey as ${holdstate} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then press hardkey as ${mute} on ${phone1}
	Then verify the led state of mute as ${off} on ${phone1}
	Then disconnect the call from ${phone2}

542798: Answer incoming call while calls are on Hold
	[Tags]    Owner:Avishek    Reviewer:Vikhyat
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Given I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${programKey1}
	Then Answer the call on ${phone1} using ${programKey2}
	Then Press hardkey as ${holdstate} on ${phone1}
	Then On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone4}
	Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
	Then Verify the caller id on ${phone4} and ${phone1} display
	Then Answer the call on ${phone1} using ${programKey3}
	Then Verify the led state of ${line1} as ${blink} on ${phone1}
	Then Verify the led state of ${line2} as ${blink} on ${phone1}
	Then Disconnect the call from ${phone4}
	And Disconnect the call from ${phone3}

539490: audio path transition- extension
	[Tags]    Owner:Avishek    Reviewer:Vikhyat
	Given press hookmode ${offHook} on phone ${phone1}
	Then On ${phone1} dial partial number of ${phone2} with ${firsttwo}
	Then Press hardkey as ${handsFree} on ${phone1}
	Then On ${phone1} dial partial number of ${phone2} with ${lasttwo}
	Then On ${phone1} wait for 5 seconds
	Then verify ringing state on ${phone1} and ${phone2}
	And disconnect the call from ${phone1}

535711: Incoming call answer through Answer key
	[Tags]    Owner:Avishek    9
	Given press hookmode ${offHook} on phone ${phone1}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then verify the led state of ${line2} as ${blink} on ${phone1}
	Then answer the call on ${phone1} using ${programKey2}
	Then verify the led state of ${line1} as ${off} on ${phone1}
	Then disconnect the call from ${phone2}

535712: Incoming call status for 2 or more simultaneous incoming calls
	[Tags]    Owner:Avishek    Reviewer:Vikhyat    multipleIncomingCalls
	Given Set number of rings to 3 on ${phone1}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${programKey2}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then verify the led state of ${line3} as ${blink} on ${phone1}
	Then verify the led state of ${line2} as ${on} on ${phone1}
	Then On ${phone1} wait for 20 seconds
	Then on ${phone2} verify display message ${displayVoiceMail}
	Then on ${phone4} verify display message ${displayVoiceMail}
	Then verify the caller id on ${phone3} and ${phone1} display
	Then verify audio path between ${phone1} and ${phone3}
	And disconnect the call from ${phone1}
	[Teardown]    Default Number of Rings

540159: Make 2nd call, hang up, unhold 1st call
	[Tags]    Owner:Avishek    11
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
	Then answer the call on ${phone3} using ${loudspeaker}
	Then press hardkey as ${goodBye} on ${phone1}
	Then press hardkey as ${holdstate} on ${phone1}
	Then verify audio path between ${phone1} and ${phone2}
	Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
	Then press hardkey as ${goodBye} on ${phone1}
	Then press hardkey as ${holdstate} on ${phone1}
	Then verify audio path between ${phone1} and ${phone2}
	And disconnect the call from ${phone1}

537757: Missed call indicator for n calls
	[Tags]    Owner:Avishek    12
	Given press the call history button on ${phone1} and folder ${missed} and ${goodBye}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then disconnect the call from ${phone2}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then disconnect the call from ${phone2}
	And on ${phone1} verify display message Missed Calls

560932: Missed call counter for 2 simulataneous incoming missed calls
	[Tags]    Owner:Avishek    13
	Given Set number of rings to 5 on ${phone1}
	Then press the call history button on ${phone1} and folder ${missed} and ${goodBye}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then verify the led state of ${line2} as ${blink} on ${phone1}
	Then disconnect the call from ${phone2}
	Then disconnect the call from ${phone3}
	And on ${phone1} verify display message Missed Calls
    [Teardown]    Default Number of Rings

538407: MERGE the active call to conference
	[Tags]    Owner:Avishek    14    notApplicableFor6910    6930
   Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
   Then answer the call on ${phone1} using ${loudspeaker}
   Then verify audio path between ${phone1} and ${phone2}
   Then press hardkey as ${holdstate} on ${phone1}
   Then and verify the led state of ${line1} as ${blink} on ${phone1}
   Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
   Then answer the call on ${phone3} using ${loudspeaker}
   Then on ${phone1} press the softkey ${merge} in AnswerState
   Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
   Then disconnect the call from ${phone1}
   And disconnect the call from ${phone2}

542849: MUTE LED status when the mute held call goes to active state
	[Tags]    Owner:Avishek    Reviewer:Vikhyat    muteOnHold
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then Put the linekey ${line1} of ${phone1} on ${hold}
	Then press hardkey as ${mute} on ${phone1}
	Then verify the led state of mute as ${off} on ${phone1}
	Then Put the linekey ${line1} of ${phone1} on ${unHold}
	Then verify audio path between ${phone1} and ${phone2}
	And disconnect the call from ${phone1}

535799: No audio on the transfer target after transfer is completed
	[Tags]    Owner:Avishek    16    6930
	Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then answer the call on ${phone2} using ${offhook}
	Then verify audio path between ${phone1} and ${phone2}
	Then Transfer call from ${phone2} to ${phone3} using ${consultiveTransfer}
	Then on ${phone1} wait for 3 seconds
	Then verify audio path between ${phone1} and ${phone3}
	Then disconnect the call from ${phone3}

542907: Auto-Transfer - No transfer timeout with invalid number length
    [Tags]    Owner:Avishek    Reviewer:    transfer
    &{pmargst} =  Create Dictionary  key=${transfer}
    &{pressHardkey} =  Create Dictionary  action_name=pressHardkey   pmargs=&{pmargst}
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press the softkey ${transfer} in answerstate
    Then on ${phone2} enter number ${invalid}
    Then on ${phone2} due to action ${pressHardkey} popup raised verify message ${transfer_invalid_number} with wait of 0
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}

537726: Blind transfer call entry in Call History
    [Tags]    Owner:Avishek    Reviewer    transfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone2}
    Then disconnect the call from ${phone3}
    Then press the call history button on ${phone3} and folder ${received} and ${nothing}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then press hardkey as ${goodbye} on ${phone3}








