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

750191:TC001 Phone Registration
    [Tags]   Owner: Ram    Reviewer:     RegisterPhonex`
    Given Register the ${phone1} on MiV400 pbx
    And On ${phone1} verify display message ${phone1}

750192: TC002 Phone De-Registration
    [Tags]   Owner: Ram    Reviewer:     DeRegisterPhone
    Given unregister the ${phone1} from MiV400 pbx
    Then On ${phone1} verify display message No Service
    [Teardown]    Default Phone state

750197: TC008 Outgoing call: Outgoing call in alerting state
    [Tags]    Owner:Anuj    Reviewer:    miv400    750197
    Then on ${phone1} verify display message ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then answer the call on ${phone2} using ${offHook}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of speaker as ${on} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of speaker as ${on} on ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of speaker as ${on} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of speaker as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then press hardkey as ${directory} on ${phone1}
    Then in directory search ${phone2} on ${phone1}
    And disconnect the call from ${phone1}

750208: TC016 Conference leg hold/unhold the conference
    [Tags]    Owner:Anuj    Reviewer:    miv400    750208
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify audio path between ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

750209: TC018 Blind Xfer
    [Tags]    Owner:Anuj        Reviewer:       miv400    750209
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone2}
    And disconnect the call from ${phone2}

750211: TC020 Consultative Xfer(Attended Xfer)
    [Tags]    Owner:Anuj    Reviewer:    miv400    750211
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750193: TC004 Incoming call in ringing state
    [Tags]    Owner:Anuj        Reviewer:       miv400    400    750193    215
    Then on ${phone1} verify display message ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then disconnect the call from ${phone1}
    Then press hardkey as ${line1} on ${phone1}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then press hardkey as ${goodbye} on ${phone1}

    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${increaseVolume} on ${phone1}
    Then on ${phone1} verify display message Volume
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone1}

    Then press hardkey as ${directory} on ${phone1}
    Then in directory search ${phone2} on ${phone1}

750220: TC038 Call Deflect
    [Tags]    Owner:Anuj        Reviewer:    miv400    750220    notApplicableFor6865
    &{configurationDetails}=    CREATE DICTIONARY    call deflect=1    far end disconnect timer=10    confxfer live dial=1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} verify display message Deflect
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then verify the caller id on ${phone2} and ${phone3} display
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then verify the caller id on ${phone2} and ${phone3} display
    Then disconnect the call from ${phone2}
    &{configurationDetails}=    CREATE DICTIONARY    call deflect=0    far end disconnect timer=10    confxfer live dial=1
    And Configure parameters on ${phone1} using ${configurationDetails}

750194: TC005 Cancel an incoming call
    [Tags]     Owner:Avishek    Reviewer:Vikhyat    cancelIncomingCall
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Verify ringing state on ${phone2} and ${phone1}
	Then press hardkey as ${goodBye} on ${phone1}
	Then I want to verify on ${phone1} negative display message ${phone2}
	Then Verify the led state of ${speaker} as ${off} on ${phone1}
	Then press hardkey as ${goodbye} on ${phone2}

	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then on ${phone1} press the softkey ${ignore} in RingingState
	Then I want to verify on ${phone1} negative display message ${phone2}
	And Verify the led state of ${speaker} as ${off} on ${phone1}

750198: TC009 Cancel an outgoing call
    [Tags]     Owner:Avishek    Reviewer:
	Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then press hardkey as ${goodBye} on ${phone1}
	Then Verify extension ${number} of ${phone1} on ${phone1}
	Then Verify the led state of ${speaker} as ${off} on ${phone1}
	Then Verify extension ${number} of ${phone2} on ${phone2}
	Then Verify the led state of ${speaker} as ${off} on ${phone2}
	Then I want to make a two party call between ${phone1} and ${phone2} using ${offhook}
	Then on ${phone1} press the softkey ${cancel} in DialingState
	Then Verify extension ${number} of ${phone1} on ${phone1}
	Then Verify the led state of ${speaker} as ${off} on ${phone1}
	Then Verify extension ${number} of ${phone2} on ${phone2}
	And Verify the led state of ${speaker} as ${off} on ${phone2}

750205: TC013 Hold a call
    [Tags]     Owner:Avishek    Reviewer:
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then press hardkey as ${holdState} on ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
	Then verify no audio path from ${phone1} to ${phone2}
	Then press hardkey as ${holdState} on ${phone1}
	Then verify the led state of ${line1} as ${on} on ${phone1}
	And disconnect the call from ${phone1}

750213: TC024 Normal conference
    [Tags]     Owner:Avishek    Reviewer:
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then on ${phone1} verify display message Drop
	Then verify the led state of ${line1} as ${on} on ${phone1}
	Then disconnect the call from ${phone1}
	And disconnect the call from ${phone2}

750218: TC031 Test BLFlist LED in outgoing, ringing, answer, hold
    [Tags]    Owner:Avishek    Reviewer:    BLF
    Given On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message blf
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify ringing state on ${phone3} and ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${programkey5} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    And I want to program ${none} key on position 4 on ${phone1}

750212: TC021 Two-line Xfer - Attended Xfer
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
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
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

751158: TC022 Two-line Xfer - Semi Attended Xfer
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer
    Then i want to make a two party call between ${phone2} and ${phone1} using ${programkey1}
    Then answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${line1} as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programkey2}
    Then Verify ringing state on ${phone1} and ${phone3}
    Then press hardkey on ${phone1} as ${scrollUp} 1 of times for navigation between calls
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press the softkey ${transfer} in RingingState
    Then I want to press line key ${line1} on phone ${phone1}
    Then On ${phone1} verify display message ${callTransferred}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

750195: TC006 Answer an incoming call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    answerCall
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${softKey}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then I want to press line key ${line1} on phone ${phone2}
    Then On ${phone2} enter number ${phone1}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${programKey1}
    Then on ${phone1} wait for 2 seconds
    Then verify audio path between ${phone2} and ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then Verify one way audio from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}

750199: TC010 Remote answer the outgoing call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    answerCall
    Given i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${OffHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${softKey}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then I want to press line key ${line1} on phone ${phone2}
    Then On ${phone2} enter number ${phone1}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${programKey1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify audio path between ${phone2} and ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then Verify one way audio from ${phone1} to ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}

750204: TC011 End the outgoing call in connected state
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    answerCall
    Given i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${OffHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${softKey}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then I want to press line key ${line1} on phone ${phone2}
    Then On ${phone2} enter number ${phone1}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${programKey1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify audio path between ${phone2} and ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    And Verify the led state of ${line2} as ${off} on ${phone1}

750221: TC040-Intercom answer
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    intercom
    &{Details} =  Create Dictionary      intercomType=${intercomTypetwo}    AllowAutoAnswer=${disable}
    Then I want to configure ${perferences} parameters using ${details} for ${phone1}
    Then On ${phone1} program key type XML on position 2 to enable icom with ${phone2} value
    Then On ${phone1} program key type XML on position 3 to enable icom with ${phone2} value
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone2} and ${phone1} display
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    &{Details} =  Create Dictionary      intercomType=${disable}    AllowAutoAnswer= ${enable}
    Then I want to configure ${perferences} parameters using ${Details} for ${phone1}
    [Teardown]    Remove program button

750210: TC019 Blind Xfer - When Ringing(Semi-Attended Xfer)
    [Tags]    Owner:Aman    Reviewer:    transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${semiAttendedTransfer}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750207: TC015 Conference initiator hold/unhold the conference
    [Tags]    Owner:Aman        Reviewer:       conference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

750206: TC014 Unhold a call
    [Tags]    Owner:Aman    Reviewer:    unhold
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} verify display message 00:
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    And disconnect the call from ${phone2}

750196: TC007 End the incoming call in connected state
    [Tags]    Owner:Aman    Reviewer:    answerCall
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
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
    Then on ${phone1} wait for 3 seconds
    Then answer the call on ${phone1} using ${offHook}
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

750219: TC033 Directed Call Pickup
    [Tags]    Owner:Aman    Reviewer:    blf
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0     directed call pickup=1     directed call pickup prefix=*86
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} program ${blf} key on position 4 with ${phone2} value
    Then On ${phone1} verify display message ${blf}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${programKey4}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then disconnect the call from ${phone3}
    And I want to program ${none} key on position 4 on ${phone1}

750222: TC041 Far end disconnect timer - basic call
    [Tags]    Owner:Aman        Reviewer:       call
    &{configurationDetails}=    CREATE DICTIONARY    far end disconnect timer=2
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then on ${phone2} press the softkey ${drop} in AnswerState
	Then on ${phone1} verify display message ${callTerminated}
    &{configurationDetails}=    CREATE DICTIONARY    far end disconnect timer=0
    And Configure parameters on ${phone1} using ${configurationDetails}



