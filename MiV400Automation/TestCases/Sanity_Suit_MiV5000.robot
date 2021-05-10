*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py

Test Timeout  25 minutes
Suite Setup  RUN KEYWORDS    Phones Initialization     Get DUT Details
Test Setup   RUN KEYWORDS    Check Phone Connection
Test Teardown  RUN KEYWORDS    MiV5000 Default Configuration    Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Generic Test Teardown

*** Test Cases ***

750165:TC002 Phone De-Registration
    [Tags]   Owner:Ram    Reviewer:     DeRegisterPhone
    Given unregister the ${phone1} from ${MiV5000} pbx
    And On ${phone1} verify display message No Service
    [Teardown]  Default Phone state

750186: TC025 Call Waiting
    [Tags]    Owner:Ram    Reviewer:    CallWaiting     750186
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify display message ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone3} and ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

750187:TC026 Call waiting disable
    [Tags]    Owner:Ram    Reviewer:    disableCallWaiting
    &{Details}=    Create Dictionary    CallWaiting=0
    Given I want to configure GlobalSettings parameters using ${Details} for ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify display message ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then On ${phone3} enter number ${phone1}
    Then On ${phone3} press the softkey ${dial} in DialingState
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then On ${phone3} verify display message Busy
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone2}
    [Teardown]    Default Preferences settings

750167: TC004 Incoming call in ringing state
    [Tags]    Owner:Ram    Reviewer:    IncomingCall    750167
    Given Add number of ${phone2} in the directory of ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${line1} on ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} verify display message ${phone2}
    Then disconnect the call from ${phone2}

750168: TC005 Cancel an incoming call
    [Tags]    Owner:Ram    Reviewer:    CancelIncomingCall  750168
    Given On ${phone1} verify display message ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${line1} on ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} verify display message ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then On ${phone1} verify display message ${phone1}
    And disconnect the call from ${phone2}

750169: TC006 Answer an incoming call
    [Tags]    Owner:Ram    Reviewer:   answerIncomingCall    750169
    [Timeout]    35 minutes
    Given Add number of ${phone2} in the directory of ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${line1} on ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} verify display message SECNUM
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then in directory search ${phone2} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

    Given On ${phone1} verify display message ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${line1} on ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} verify display message SECNUM
    Then answer the call on ${phone1} using ${offHook}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then in directory search ${phone2} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

    Given On ${phone1} verify display message ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${line1} on ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} verify display message SECNUM
    Then answer the call on ${phone1} using ${line1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    And Delete ${phone2} entries from directry of ${phone1}

750180: TC017 Consultative Xfer (Attended Xfer)
    [Tags]    Owner:Aman    Reviewer:     transfer    750180
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750172: TC009 Cancel an outgoing call
    [Tags]    Owner:Aman    Reviewer:     call
    Given Add number of ${phone2} in the directory of ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then On ${phone1} wait for 3 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
	Then On ${phone1} verify display message SECNUM
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Press hookMode ${onHook} on phone ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Verify ringing state on ${phone1} and ${phone2}
	Then On ${phone1} verify display message SECNUM
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then disconnect the call from ${phone1}
    Then verify the led state of ${loudspeaker} as ${off} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
	Then On ${phone1} verify display message SECNUM
    Then verify the led state of ${line1} as ${on} on ${phone1}
	Then press hardkey as ${goodBye} on ${phone1}
    Then verify the led state of ${loudspeaker} as ${off} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
	And Verify extension ${number} of ${phone1} on ${phone1}

750176: TC014 Unhold a call
    [Tags]   Owner:Aman     Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then On ${phone1} verify display message ${pickup}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then press hardkey as GoodBye on ${phone2}
    Then Verify the line state as idle on ${phone1}
    And Verify the line state as idle on ${phone2}

750181: TC018 Two-line Xfer - Attended Xfer
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    1
    Then i want to make a two party call between ${phone2} and ${phone1} using ${programkey1}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programkey2}
    Then answer the call on ${phone3} using ${line1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone3}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then I want to press line key ${line1} on phone ${phone1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

750182: TC019 Two-line Xfer - Semi Attended Xfer
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    bug
    Then i want to make a two party call between ${phone2} and ${phone1} using ${programkey1}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programkey2}
    Then Verify ringing state on ${phone1} and ${phone3}
    Then Press hardkey on ${phone1} as ${scrollUp} 1 of times for navigation between calls
    Then on ${phone1} press the softkey ${transfer} in RingingState
    Then I want to press line key ${line1} on phone ${phone1}
    Then On ${phone1} verify display message ${callTransferred}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

750185: TC024 Leave Conference Test leave a normal conference,then test leave a 2-line conference
    [Tags]  Owner:Abhishekkhanchi    Reviewer:    xfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then I want to press line key ${line2} on phone ${phone1}
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${line1} on phone ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${leave}
    Then I want to verify on ${phone2} negative display message ${leave}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} verify display message Drop
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}

750175: TC021 Conference initiator hold/unhold the conference
    [Tags]    Owner:Vikhyat    Reviewer:    mv5000
    [Timeout]    30 minutes
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${leave}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${unHold}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

750177: TC022 Conference leg hold/unhold the conference
    [Tags]    Owner:Vikhyat    Reviewer:    mv5000
    [Timeout]    30 minutes
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone1} using ${offHook}
    Then I want to make a conference call between ${phone2},${phone1} and ${phone3} using ${consultiveConference}
    Then On ${phone2} verify display message ${drop}
    Then On ${phone2} verify display message ${leave}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

750184: TC023 Two-line Conference
    [Tags]    Owner:Vikhyat    Reviewer:    mv5000
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${programKey1}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} press ${softKey} ${programKey1} for 1 times
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${leave}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

750171: TC008 Outgoing call: Outgoing call in alerting state
    [Tags]    Owner:Anuj    Reviewer:     MiV5000    750171
    Given On ${phone1} verify display message ${phone1}

    #Make an outgoing call using offhook
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}

    #Make an outgoing call using line key1
    Then I want to make a two party call between ${phone1} and ${phone2} using ${programkey1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}

    #Make an outgoing call using loudspeaker
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}

750178: TC015 Blind Xfer
	[Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    And Press hardkey as ${goodBye} on ${phone2}

750179:TC016-a Blind Xfer - When Ringing (Semi-Attended Xfer) - by dial
    [Tags]    Owner:AbhishekPathak    Reviewer:    semi_attended_transfer    750179
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${semiAttendedTransfer}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone3}
    And Press hardkey as ${goodBye} on ${phone2}

750188:TC027 BLF - Test BLF LED in outgoing, ringing, answer, hold
    [Tags]    Owner:AbhishekPathak    Reviewer:    BLF    750188
    &{configurationDetails}=    CREATE DICTIONARY    directed call pickup=0     collapsed softkey screen=0
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify ringing state on ${phone3} and ${phone2}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    And I want to program ${none} key on position 4 on ${phone1}

750189: TC028 Directed Call Pickup
    [Tags]    Owner:AbhishekPathak    Reviewer:    BLF    750189
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0     directed call pickup=1     directed call pickup prefix=*02
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify ringing state on ${phone3} and ${phone2}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone3}
    And Press hardkey as ${goodBye} on ${phone3}

750170: TC007-a End the call in connected state - local
    [Tags]   Owner:Surender    Reviewer:    750170
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify the line state as idle on ${phone1}
    And Verify the line state as idle on ${phone2}

750291: TC007-b End the call in connected state - remote
    [Tags]   Owner:Surender    Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then press hardkey as GoodBye on ${phone2}
    Then Verify the line state as idle on ${phone1}
    And Verify the line state as idle on ${phone2}

750174: TC013 hold a call
    [Tags]   Owner:Surender    Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as blink on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then On ${phone1} verify display message ${pickup}
    Then press hardkey as GoodBye on ${phone2}
    Then Verify the line state as idle on ${phone1}
    Then Verify the line state as idle on ${phone2}

750236: TC035 Redial list
    [Tags]    Owner:Avishek    Reviewer:    notApplicableFor6865    750236
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${delete}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then i want to verify on ${phone1} negative display message ${phone2}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then disconnect the call from ${phone1}

750235: TC034 Caller list
    [Tags]    Owner:Avishek    Reviewer:    750235
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone1}

    Then Press the call history button on ${phone1} and folder ${received} and ${offHook}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}

    Then Press the call history button on ${phone1} and folder ${received} and ${delete}
    Then press hardkey as ${goodBye} on ${phone1}

    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then i want to verify on ${phone1} negative display message ${phone2}
    Then disconnect the call from ${phone1}

    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${received} and ${delete}
    Then press hardkey as ${goodBye} on ${phone1}

750173: TC010 Remote answer the outgoing call
    [Tags]    Owner:Vikhyat    Reviewer:    miv5000
    Given On ${phone1} verify display message ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then On ${phone1} wait for 3 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then On ${phone1} wait for 3 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then On ${phone1} wait for 3 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}

750183: TC020 Normal Conference
    [Tags]    Owner:Vikhyat    Reviewer:    miv5000    Vikhyat05    30/04/2020
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then On ${phone1} verify display message ${leave}
    Then On ${phone1} verify display message ${drop}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}





