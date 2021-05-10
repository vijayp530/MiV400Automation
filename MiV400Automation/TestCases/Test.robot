*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Resource    ../RobotKeywords/WebUI_Keywords.robot
Library    ../lib/MyListner.py


Test Timeout  25 minutes
Suite Setup  RUN KEYWORDS    Phones Initialization    Get DUT Details
Test Setup   Check Phone Connection
Test Teardown  Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Generic Test Teardown

*** Test Cases ***
#750191:TC001 Phone Registration
#    [Tags]   Owner: Ram    Reviewer:     RegisterPhonex`
#    Given Register the ${phone1} on MiV400 pbx
#    And On ${phone1} verify display message ${phone1}
#
#750192: TC002 Phone De-Registration
#    [Tags]   Owner: Ram    Reviewer:     DeRegisterPhone
#    Given unregister the ${phone1} from MiV400 pbx
#    Then On ${phone1} verify display message No Service
#    [Teardown]    Default Phone state

#750197: TC008 Outgoing call: Outgoing call in alerting state
#    [Tags]    Owner:Anuj    Reviewer:    miv400    750197
#    Then on ${phone1} verify display message ${phone1}
#    Then i want to make a two party call between ${phone1} and ${phone2} using ${offHook}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then verify the led state of speaker as ${off} on ${phone1}
#    Then answer the call on ${phone2} using ${offHook}
#    Then verify the led state of speaker as ${off} on ${phone1}
#    Then Verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
#    Then verify the caller id on ${phone1} and ${phone2} display
#    Then Verify audio path between ${phone1} and ${phone2}
#    Then disconnect the call from ${phone1}

#    press hardkey as ${goodBye} on ${phone1}
#    Then On ${phone1} verify display message ${phone1}
#    #Then On ${phone1} enter number ${phone2}
#    Then i want to make a two party call between ${phone1} and ${phone2} using ${OffHook}
#    Then Verify ringing state on ${phone1} and ${phone2}
#    Then Answer the call on ${phone2} using ${OffHook}
#    Then Verify the Caller id on ${phone1} and ${phone2} display
#    Then Verify audio path between ${phone1} and ${phone2}
#    Then Disconnect the call from ${phone2}
#    Then Verify no audio path from ${phone1} to ${phone2}


#    Then I want to make a two party call between ${phone1} and ${phone2} using ${line1}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then verify the led state of speaker as ${on} on ${phone1}
#    Then answer the call on ${phone2} using ${loudspeaker}
#    Then verify the led state of speaker as ${on} on ${phone2}
#    Then Verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
#    Then verify the caller id on ${phone1} and ${phone2} display
#    Then disconnect the call from ${phone1}
#
#    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
#    Then verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify the led state of ${line1} as ${blink} on ${phone2}
#    Then verify the led state of speaker as ${on} on ${phone1}
#    Then answer the call on ${phone2} using ${loudspeaker}
#    Then verify the led state of speaker as ${on} on ${phone1}
#    Then Verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
#    Then verify the caller id on ${phone1} and ${phone2} display
#    Then disconnect the call from ${phone2}
#    Then press hardkey as ${directory} on ${phone1}
#    Then in directory search ${phone2} on ${phone1}
#    And disconnect the call from ${phone1}

#750193: TC004 Incoming call in ringing state
#    [Tags]    Owner:Anuj        Reviewer:       miv400    400    750193    215
#    Then on ${phone1} verify display message ${phone1}
#    Then press hardkey as ${increaseVolume} on ${phone1}
#    Then on ${phone1} verify display message Volume
#    Then disconnect the call from ${phone1}
#    Then press hardkey as ${line1} on ${phone1}
#    Then press hardkey as ${increaseVolume} on ${phone1}
#    Then on ${phone1} verify display message Volume
#    Then press hardkey as ${goodbye} on ${phone1}
#
#    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
#    Then press hardkey as ${increaseVolume} on ${phone1}
#    Then on ${phone1} verify display message Volume
#    Then Verify the led state of ${line1} as ${blink} on ${phone1}
#    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
#    Then verify extension ${number} of ${phone2} on ${phone1}
#    Then disconnect the call from ${phone1}
#
#    Then press hardkey as ${directory} on ${phone1}
#    Then in directory search ${phone2} on ${phone1}

#TestCase1: Basic peer to peer call between two terminals.
#    [Tags]    Regression    Owner:Vijay    Reviewer:    01
#
#    Log    Verify extension number on phone1.
#    Then on ${phone1} verify display message ${phone1}
#
#    Log    Verify extension number on phone2.
#    Then on ${phone2} verify display message ${phone2}
#
#    Log    Make call from phone1 to phone2.
#    Then i want to make a two party call between ${phone1} and ${phone2} using ${OffHook}
#
#    Log    Verify that both phones are ringing.
#    Then Verify ringing state on ${phone1} and ${phone2}
#
#    Log    Verify phones showing numbers of each other
#    Then verify the caller id on ${phone1} and ${phone2} display
#
#    Log    Answer call from phone2.
#    Then Answer the call on ${phone2} using ${OffHook}
#
#    Log    Check Audio path between two phones.
#    Then Verify audio path between ${phone1} and ${phone2}
#
#    Log    End call from phone1.
#    Then Disconnect the call from ${phone1}
#
#    Log    Verify extension number on phone1.
#    Then on ${phone1} verify display message ${phone1}
#
#    Log    Verify extension number on phone2.
#    Then on ${phone2} verify display message ${phone2}
#
#    Log    Make call from phone2 to phone1.
#    Then I want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
#
#    Log    Verify that both phones are ringing.
#    Then Verify ringing state on ${phone2} and ${phone1}
#
#    Log    Verify phones showing numbers of each other
#    Then verify the caller id on ${phone1} and ${phone2} display
#
#    Log    Answer call from phone1.
#    Then Answer the call on ${phone1} using ${OffHook}
#
#    Log    Check Audio path between two phones.
#    Then Verify audio path between ${phone2} and ${phone1}
#
#    Log    End call from phone1.
#    Then Disconnect the call from ${phone2}
750209: TC018 Blind Xfer
    [Tags]    Owner:Anuj        Reviewer:       miv400    750209
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
   # Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    sleep   10s
    Then answer the call on ${phone3} using ${loudspeaker}
   # Then verify audio path between ${phone3} and ${phone2}
    And disconnect the call from ${phone2}

750205: TC013 Hold a call
    [Tags]     Owner:Avishek    Reviewer:
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then press hardkey as ${holdState} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
	#Then verify no audio path from ${phone1} to ${phone2}
	Then press hardkey as ${holdState} on ${phone1}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	And disconnect the call from ${phone1}

TestCase2: Hold and Resume call.
    [Tags]    Regression    Owner:Vijay    Reviewer:    02

    Log    Verify extension number on phone1.
    Then on ${phone1} verify display message ${phone1}

    Log    Verify extension number on phone2.
    Then on ${phone2} verify display message ${phone2}

    Log    Make call from phone1 to phone2.
    Then i want to make a two party call between ${phone1} and ${phone2} using ${OffHook}

    Log    Verify that both phones are ringing.
    Then Verify ringing state on ${phone1} and ${phone2}

    Log    Verify phones showing numbers of each other
    Then verify the caller id on ${phone1} and ${phone2} display

    Log    Answer call from phone2.
    Then Answer the call on ${phone2} using ${OffHook}

   #  Log    Check Audio path between two phones.
  #  Then Verify audio path between ${phone1} and ${phone2}

    Log    Hold call from phone1.
    Then press hardkey as ${holdState} on ${phone1}
    Sleep   5s

    Log    Verify hold state for phone1.
    Then Verify the ${line1} of ${phone1} at state hold

  #  Log    Check there is no audio path.
  #  Then Verify no audio path from ${phone1} to ${phone2}

    Log   Unhold call from phone1.
    Then press hardkey as ${holdState} on ${phone1}

   # Log    Check Audio path between two phones.
   # Then Verify audio path between ${phone1} and ${phone2}

    Log    Verify Unhold state for phone1.
    Then Then Verify the ${line1} of ${phone1} at state Unhold

    Log    Hold call from phone2.
    Then press hardkey as ${holdState} on ${phone2}
    Sleep   10s

    Log    Verify hold state for phone2.
    Then Verify the ${line1} of ${phone2} at state hold

  #  Log    Check there is no audio path.
  #  Then Verify no audio path from ${phone1} to ${phone2}

    Log   Unhold call from phone2.
    Then press hardkey as ${holdState} on ${phone2}

  #  Log    Check Audio path between two phones.
  #  Then Verify audio path between ${phone1} and ${phone2}

    Log    Verify Unhold state for phone2.
    Then Verify the ${line1} of ${phone2} at state Unhold

    Then Disconnect the call from ${phone1}

TestCase3: Blind Transfer.
    [Tags]    Regression    Owner:Pooja    Reviewer:    03

    Log    Make call from phon2 to phone1.
    Given i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}

    Log    Verify that both phones are ringing.
    Then Verify ringing state on ${phone2} and ${phone1}

    Log    Verify phones showing numbers of each other
    Then verify the caller id on ${phone2} and ${phone1} display

    Log    Answer call from phone2.
    Then Answer the call on ${phone1} using ${OffHook}

   # Log    Check Audio path between two phones.
   # Then verify audio path between ${phone1} and ${phone2}

    Log    Blind tranfer the call from phone1 to phone3
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}

    Log    Answer call on phone3.
    Then answer the call on ${phone3} using ${OffHook}

    Log    Confirm phone3 number on phone2.
    Then Verify extension ${number} of ${phone3} on ${phone2}

    Log    Confirm phone2 number on phone3.
    Then Verify extension ${number} of ${phone2} on ${phone3}

   # Log    Verify Audio path between phone2 and phone3.
   # Then verify audio path between ${phone3} and ${phone2}

    Log    Disconnect call from phone 2.
    And disconnect the call from ${phone2}

TestCase3: Consultative Transfer.
    [Tags]    Regression    Owner:Pooja1    Reviewer:    03

    Log    Make call from phon2 to phone1.
    Given i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}

    Log    Verify that both phones are ringing.
    Then Verify ringing state on ${phone2} and ${phone1}

    Log    Verify phones showing numbers of each other
    Then verify the caller id on ${phone2} and ${phone1} display

    Log    Answer call from phone2.
    Then Answer the call on ${phone1} using ${OffHook}

   # Log    Check Audio path between two phones.
   # Then verify audio path between ${phone1} and ${phone2}

    Log    Consult tranfer the call from phone1 to phone3
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}

    Log    Answer call on phone3.
    Then answer the call on ${phone3} using ${OffHook}

    Log    Confirm phone3 number on phone2.
    Then Verify extension ${number} of ${phone3} on ${phone2}

    Log    Confirm phone2 number on phone3.
    Then Verify extension ${number} of ${phone2} on ${phone3}

   # Log    Verify Audio path between phone2 and phone3.
   # Then verify audio path between ${phone3} and ${phone2}

    Log    Disconnect call from phone 2.
    And disconnect the call from ${phone2}

TestCase3a: Call Forward Unconditional.
    [Tags]    Regression    Owner:Vijay2    Reviewer:    04

    Log    Verify extension number on phone1.
    Then on ${phone1} verify display message ${phone1}

    Log    Enable unconditional call forwarding from phone1 to phone3.
    Then Enable Call forwarding from ${phone1} to ${phone3} for mode ${Unconditional}

    Log    Make call between phone2 and phone1.
    Then I want to make a two party call between ${phone2} and ${phone1} using ${OffHook}

    Log    Verify call is forwarded to phone3 via ringing.
    Then verify display ringing on ${phone2} and ${phone3} in call forwared from ${phone1} in ${Unconditional} mode

    Log    Answer call from phone3.
    Then Answer the call on ${phone3} using ${OffHook}

#    Log    Verify audio path between phone2 and phone3.
#    Then Verify audio path between ${phone2} and ${phone3}

    Log    Confirm phone3 number on phone2.
    Then Verify extension ${number} of ${phone3} on ${phone2}

    Log    Confirm phone2 number on phone3.
    Then Verify extension ${number} of ${phone2} on ${phone3}

    Log    Disconnect call from phone2.
    Then Disconnect the call from ${phone2}

    Log    Disable call forwarding from phone1.
    Then Disable call forwarding on ${phone1}

TestCase3b: Call Forward If NoResponse.
    [Tags]    Regression    Owner:Vijay3    Reviewer:    05

    Log    Verify extension number on phone1.
    Then on ${phone1} verify display message ${phone1}

    Log    Enable call forwarding when No response, from phone1 to phone3.
    Then Enable Call forwarding from ${phone1} to ${phone3} for mode ${NoResponse}

    Log    Make call between phone2 and phone1.
    Then I want to make a two party call between ${phone2} and ${phone1} using ${OffHook}

    Log    Verify phone1 and phone2 are ringing.
    Then Verify ringing state on ${phone2} and ${phone1}

    Log    Wait till timeout occure.dont pickup the call from phone1.
    Sleep   10s

    Log    Verify call is forwarded to phone3 via ringing.
    Then verify display ringing on ${phone2} and ${phone3} in call forwared from ${phone1} in ${NoResponse} mode

    Log    Answer call from phone3.
    Then Answer the call on ${phone3} using ${OffHook}

#    Log    Verify audio path between phone2 and phone3.
#    Then Verify audio path between ${phone2} and ${phone3}

    Log    Confirm phone3 number on phone2.
    Then Verify extension ${number} of ${phone3} on ${phone2}

    Log    Confirm phone2 number on phone3.
    Then Verify extension ${number} of ${phone2} on ${phone3}

    Log    Disconnect call from phone2.
    Then Disconnect the call from ${phone2}

    Log    Disable call forwarding from phone1.
    Then Disable call forwarding on ${phone1}

TestCase3c: Call Forward If Busy.
    [Tags]    Regression    Owner:Vijay4    Reviewer:    06

    Log    Verify extension number on phone1.
    Then on ${phone1} verify display message ${phone1}

    Log    Enable call forwarding when busy, from phone1 to phone3.
    Then Enable Call forwarding from ${phone1} to ${phone3} for mode ${BusyForward}

    Log    Make call between phone1 and phone4.
    Then I want to make a two party call between ${phone1} and ${phone4} using ${OffHook}

    Log    Verify phone1 and phone4 are ringing.
    Then Verify ringing state on ${phone1} and ${phone4}

    Log    Answer the call from phone4.
    Then Answer the call on ${phone4} using ${OffHook}

#    Log    Verify audio path between phone1 and phone4.
#    Then Verify audio path between ${phone1} and ${phone4}

    Log    Make call between phone2 and phone1.
    Then I want to make a two party call between ${phone2} and ${phone1} using ${OffHook}

    Log    Verify call is forwarded to phone3 via ringing.
    Then verify display ringing on ${phone2} and ${phone3} in call forwared from ${phone1} in ${BusyForward} mode

    Log    Answer call from phone3.
    Then Answer the call on ${phone3} using ${OffHook}

#     Log    Verify audio path between phone2 and phone3.
#     Then Verify audio path between ${phone2} and ${phone3}

    Log    Confirm phone3 number on phone2.
    Then Verify extension ${number} of ${phone3} on ${phone2}

    Log    Confirm phone2 number on phone3.
    Then Verify extension ${number} of ${phone2} on ${phone3}

    Log    Disconnect call from phone2.
    Then Disconnect the call from ${phone2}

    Log    Disconnect call from phone1.
    Then Disconnect the call from ${phone1}

    Log    Disable call forwarding from phone1.
    Then Disable call forwarding on ${phone1}

TestCase3a: Call Forward DND.
    [Tags]    Regression    Owner:Vijay5    Reviewer:    07

    Log    Verify extension number on phone1.
    Then on ${phone1} verify display message ${phone1}

    Log    Set Call forward destination as phone3 on webadmin.

    Log    Enable call forwarding when DND, from phone1 to phone3.
    Then Enable Call forwarding from ${phone1} to ${phone3} for mode ${DNDForward}

    Log    Make call between phone2 and phone1.
    Then I want to make a two party call between ${phone2} and ${phone1} using ${OffHook}

    Log    Verify call is forwarded to phone3 via ringing.
    Then verify display ringing on ${phone2} and ${phone3} in call forwared from ${phone1} in ${DNDForward} mode

    Log    Answer call from phone3.
    Then Answer the call on ${phone3} using ${OffHook}

#    Log    Verify audio path between phone2 and phone3.
#    Then Verify audio path between ${phone2} and ${phone3}

    Log    Confirm phone3 number on phone2.
    Then Verify extension ${number} of ${phone3} on ${phone2}

    Log    Confirm phone2 number on phone3.
    Then Verify extension ${number} of ${phone2} on ${phone3}

    Log    Disconnect call from phone2.
    Then Disconnect the call from ${phone2}

    Log    Disable call forwarding from phone1.
    Then Disable call forwarding on ${phone1}















