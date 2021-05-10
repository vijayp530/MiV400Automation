*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Resource    ../RobotKeywords/PhoneKeywords.robot
Resource    ../Variables/Clearspan_Initialization.robot
Library    ../lib/MyListner.py


Test Timeout  25 minutes
Suite Setup  Run Keywords    Phones Initialization     Get DUT Details
Test Setup   Check Phone Connection
Test Teardown  Generic Test Teardown
Suite Teardown    Run Keywords   Check Phone Connection    Generic Test Teardown

*** Test Cases ***

750242: TC-02-d End the incoming call in connected state
    [Tags]    Owner:Aman    Reviewer:    call     Clearspan_Ver1.2    750242
    Given Add number of ${phone2} in the directory of ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then On ${phone1} verify display message SECNUM
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${mute} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    And Verify extension ${number} of ${phone1} on ${phone1}

    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudspeaker}
	Then On ${phone1} verify display message SECNUM
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${mute} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then verify the led state of ${line1} as ${off} on ${phone1}
    And Verify extension ${number} of ${phone1} on ${phone1}

    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
	Then On ${phone1} verify display message SECNUM
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${mute} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hookMode ${onHook} on phone ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    And Verify extension ${number} of ${phone1} on ${phone1}

750243: TC-03.a Outgoing call: Outgoing call in alerting state
    [Tags]    Owner:Aman        Reviewer:       call        Clearspan_Ver1.2    750243
    Given Add number of ${phone2} in the directory of ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${message_waiting} as ${off} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then Press hardkey as ${goodBye} on ${phone1}
    And On ${phone1} wait for 5 seconds

    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${message_waiting} as ${off} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then Press hardkey as ${goodBye} on ${phone1}
    And On ${phone1} wait for 5 seconds

    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
	Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${message_waiting} as ${off} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    And Press hardkey as ${goodBye} on ${phone1}

750244: TC-03-b Cancel an outgoing call
    [Tags]    Owner:Aman        Reviewer:       call        Clearspan_Ver1.2
    Given Add number of ${phone2} in the directory of ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify ringing state on ${phone1} and ${phone2}
	Then On ${phone1} verify display message SECNUM
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Press hookMode ${onHook} on phone ${phone1}
    Then verify the led state of ${speaker} as ${off} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Verify ringing state on ${phone1} and ${phone2}
	Then On ${phone1} verify display message SECNUM
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} press the softkey ${cancel} in RingingState
    Then verify the led state of ${speaker} as ${off} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
	Then On ${phone1} verify display message SECNUM
    Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then press hardkey as ${goodBye} on ${phone1}
    Then verify the led state of ${speaker} as ${off} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

750245: TC-03-c Remote answer the outgoing call
    [Tags]    Owner:Aman        Reviewer:       call        Clearspan_Ver1.2
    Given Add number of ${phone1} in the directory of ${phone2}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then press hardkey as ${mute} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    And Press hookMode ${onHook} on phone ${phone2}
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then press hardkey as ${mute} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    And on ${phone2} press the softkey ${drop} in AnswerState
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then press hardkey as ${mute} on ${phone1}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

750246: TC-03-d End the outgoing call in connected state
    [Tags]    Owner:Aman        Reviewer:       call        Clearspan_Ver1.2
    Given Add number of ${phone2} in the directory of ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then Press hookMode ${onHook} on phone ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then On ${phone1} verify display message SECNUM
    Then disconnect the call from ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

750247: TC-05-a hold a call
    [Tags]    Owner:Anuj        Reviewer:       Clearspan    750247
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify the led state of ${line1} as ${blink} and led color 
    Then on ${phone1} verify the led state of ${message_waiting} as ${blink}
    Then verify no audio path from ${phone1} to ${phone2}
    And disconnect the call from ${phone2}

750248: TC-05-b Unhold a call
    [Tags]    Owner:Anuj        Reviewer:       Clearspan    750248
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify the led state of ${line1} as ${blink} and led color 
    Then on ${phone1} verify the led state of ${message_waiting} as ${blink} 
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} verify the led state of ${line1} as ${on} and led color
    Then verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}

750249: TC05c: Unhold using line key followed by offhook event
    [Tags]    Owner:Anuj        Reviewer:       Clearspan    750249
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify the led state of ${line1} as ${blink} and led color 
    Then press hardkey as ${onHook} on ${phone1}
    Then i want to press line key ${line1} on phone ${phone1}
    Then on ${phone1} verify the led state of ${line1} as ${on} and led color
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

750250: TC-06: DND On/Off
   [Tags]    Owner:AbhishekPathak    Reviewer:    dnd_on_off    750250
    &{configurationDetails}=    create dictionary    topsoftkey4 type=dnd
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then on ${phone1} verify the led state of ${line4} as ${on} and led color
    Then on ${phone1} verify the led state of ${message_waiting} as ${on} 
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    &{configurationDetails}=    create dictionary    topsoftkey4 type=none
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then on ${phone1} verify the led state of ${line2} as ${on} and led color 
    Then on ${phone1} verify the led state of ${message_waiting} as ${on} 
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then Press hardkey as ${goodBye} on ${phone2}

    Given I want to program dnd key on position 2 on ${phone1}
    Then i want to press line key ${line2} on phone ${phone1}
    Then on ${phone1} verify the led state of ${line2} as ${on} and led color 
    Then on ${phone1} verify the led state of ${Message_waiting} as ${on}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then I want to program none key on position 2 on ${phone1}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then verify the led state of ${Message_waiting} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}

750259: N way conference - DUT drops
    [Tags]    Owner:Sharma    Reviewer:
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${conference}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}

750260: N way conference - DUT holds
    [Tags]    Owner:Sharma    Reviewer:    clearspan
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${unHold}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}

750261: N way conference - Participant holds
    [Tags]    Owner:Sharma    Reviewer:    clearspan
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone2},${phone1} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${unHold}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}

750262: N way Conference - DUT drops
    [Tags]    Owner:Sharma    Reviewer:    clearspan
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone1} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then I want to verify on ${phone2} negative display message ${phone1}
    Then I want to verify on ${phone3} negative display message ${phone1}

750263: N way Conference - Participant drops
    [Tags]    Owner:Sharma    Reviewer:    clearspan
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then I want to verify on ${phone2} negative display message ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Verify audio path between ${phone1} and ${phone3}
    Then Disconnect the call from ${phone3}

750241: TC-02-c Answer an incoming call
    [Tags]    Owner:Sharma    Reviewer:    clearspan
    Given Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone1} using ${softkey}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone1} using ${programKey1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

810611: Normal conference
    [Tags]  Owner:Abhishekkhanchi    Reviewer:
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} verify display message Drop
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then disconnect the call from ${phone1}
	Then disconnect the call from ${phone2}

750256: Leave Conference
    [Tags]  Owner:Abhishekkhanchi    Reviewer:    xfer
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then on ${phone1} verify display message Drop
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then On ${phone1} verify display message ${leave}
    Then on ${phone1} press the softkey ${leave} in ConferenceCallState
    Then verify the led state of ${line1} as ${off} on ${phone1}
	Then verify the led state of ${line2} as ${off} on ${phone1}
    Then verify audio path between ${phone2} and ${phone3}
	Then disconnect the call from ${phone1}
	Then disconnect the call from ${phone2}

750257: Conference initiator hold/unhold the conference
    [Tags]  Owner:Abhishekkhanchi    Reviewer:    xfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then answer the call on ${phone2} using ${loudspeaker}
	Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
	Then disconnect the call from ${phone1}
	Then disconnect the call from ${phone2}
	Then disconnect the call from ${phone3}

750258: Conference leg hold/unhold the conference
    [Tags]  Owner:Abhishekkhanchi    Reviewer:    xfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then i want to make a conference call between ${phone2},${phone1} and ${phone3} using ${consultiveConference}
	Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink} 
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${message_waiting} as ${off} on ${phone1}
	Then disconnect the call from ${phone1}
	Then disconnect the call from ${phone2}
	Then disconnect the call from ${phone3}
	
750265:Call waiting disable
    [Tags]  Owner:Abhishekkhanchi    Reviewer:    xfer
    &{Details} =  Create Dictionary      callWaiting=${disable}
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then On ${phone3} verify display message Busy
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    &{Details} =  Create Dictionary      callWaiting=${enable}
    Then I want to configure GlobalSettings parameters using ${Details} for ${phone1}

750647:Failed blind transfer
    [Tags]  Owner:Abhishekkhanchi    Reviewer:    xfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then press hardkey as ${enter} on 11111
    Then on ${phone1} wait for 2000 seconds
    Then On ${phone1} verify display message Transfer Failed
    Then on ${phone1} verify display message PickUp
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify display message Drop
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display

750251:TC07 Blind Xfer
    [Tags]    Owner:AbhishekPathak    Reviewer:    blind_transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then on ${phone1} wait for 2 seconds
    Then Verify ringing state on ${phone2} and ${phone3}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Press hardkey as ${goodBye} on ${phone2}

750252:TC-08 Blind Xfer - (Semi-Attended Xfer) + BLFlist key for target
    [Tags]    Owner:AbhishekPathak    Reviewer:    semi_attended_transfer_blf
    Given On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then Verify ringing state on ${phone3} and ${phone2}
    Then on ${phone1} press the softkey ${Transfer} in TransferState
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Press hardkey as ${goodBye} on ${phone3}


750253:TC-09 Consultative Xfer(Attended Xfer) + contact from callist as target
    [Tags]    Owner:AbhishekPathak    Reviewer:    attended_xfer_list
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then Press the call history button on ${phone1} and folder ${all} and ${dial}
    Then on ${phone1} wait for 2 seconds
    Then Verify ringing state on ${phone1} and ${phone3}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${Transfer} in TransferState
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Press hardkey as ${goodBye} on ${phone2}

750254:TC-10a Two-line Xfer - Attended Xfer + contact from Directory as target
    [Tags]    Owner:AbhishekPathak    Reviewer:    attended_xfer_directory
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then On ${phone1} verify directory with ${directoryAction['searchWithDial']} of ${phone3}
    Then on ${phone3} wait for 2 seconds
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone3} wait for 5 seconds
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Press hardkey as ${goodBye} on ${phone2}

750264:Call Waiting
    [Tags]    Owner:AbhishekPathak    Reviewer:    call_waiting
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${line1}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${line1}
    Then verify ringing state on ${phone3} and ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink} 
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone3} and ${phone1}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

750266:TC043 BLF Test BLF LED in outgoing, ringing, answer, hold
    [Tags]    Owner:AbhishekPathak    Reviewer:    BLF
    Given On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone3}
    Then verify the led state of ${programkey5} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${programkey5} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${programkey5} as ${blink} on ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then verify the led state of ${programkey5} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then verify the led state of ${programkey5} as ${on} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    And I want to program ${none} key on position 4 on ${phone1}
