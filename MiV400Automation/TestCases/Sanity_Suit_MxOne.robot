*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py

Test Timeout  20 minutes
Suite Setup  RUN KEYWORDS    Phones Initialization    Get DUT Details
Test Setup   RUN KEYWORDS    Check Phone Connection
Test Teardown  RUN KEYWORDS    MxOne Default Configuration    Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    MxOne Default Configuration
...                                                               Generic Test Teardown

*** Test Cases ***
750130: TC001 Phone Registration
    [Tags]   Owner:Ram    Reviewer:     RegisterPhone    1234
    Given Register the ${phone1} on ${MxOne} pbx
    And On ${phone1} verify display message ${phone1}
    [Teardown]    Generic Test Teardown

750131: TC002 Phone De-Registration
    [Tags]   Owner:Ram    Reviewer:     DeRegisterPhone
    Given unregister the ${phone1} from ${MxOne} pbx
    Then On ${phone1} verify display message No Service
    And Register the ${phone1} on ${MxOne} pbx
    [Teardown]    RUN KEYWORDS    Default Phone state    Generic Test Teardown

750133: TC005 Cancel an incoming call
    [Tags]   Owner:Ram    Reviewer:     cancelCall
    Given On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then i want to verify on ${phone1} negative display message ${phone2}
    And disconnect the call from ${phone2}

750132: TC004 Incoming call in ringing state
    [Tags]   Owner:Ram    Reviewer:     incomingCall
    Given On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then On ${phone1} wait for 5 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} verify display message ${phone2}
    And disconnect the call from ${phone2}

750134: TC006 Answer an incoming call
    [Tags]   Owner:Ram    Reviewer:    answerCall
    [Timeout]    35 minutes
    Given On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then answer the call on ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

    Given On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then answer the call on ${phone1} using ${line1}
    Then On ${phone1} verify the led state of ${line1} as ${on} and led color as red
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

    Given On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line1} as ${on} and led color as red
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

750140: TC013 Hold a Call
    [Tags]    Owner:AbhishekPathak    Reviewer:    holdCall
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then On ${phone2} wait for 3 seconds
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then Put the linekey ${line1} of ${phone1} on ${unHold}
    And Disconnect the call from ${phone2}

750141: TC014 Unhold a call
    [Tags]    Owner:AbhishekPathak    Reviewer:    holdCall
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

750143: TC016 Blind Xfer
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer    750143
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    And Disconnect the call from ${phone2}

750144: TC017 Blind Xfer - When Ringing(Semi-Attended Xfer)
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer    750144
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${transfer} in DialingState
    Then On ${phone1} verify display message ${callTransferred}
    Then Verify the line state as ${idleState} on ${phone1}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    And Disconnect the call from ${phone2}

750150: TC024 Call Waiting
    [Tags]    Owner:AbhishekPathak    Reviewer:    call_waiting
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify ringing state on ${phone3} and ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone3} and ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

750151: TC025 Call waiting disable
    [Tags]    Owner:AbhishekPathak    Reviewer:    call_waiting_disable    750151
    &{details}=    CREATE DICTIONARY    CallWaiting=0
    Given I want to configure GlobalSettings parameters using ${details} for ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then On ${phone3} verify display message ${busy}
    Then disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}

750142: TC015 DND On/Off
   [Tags]    Owner:AbhishekPathak    Reviewer:    dnd_on_off    750142
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    &{configurationDetails}=    create dictionary    topsoftkey3 type=dnd
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} press ${softkey} ${programKey3} for 1 times
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then On ${phone2} verify display message ${busy}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then On ${phone1} press ${softKey} ${programKey3} for 1 times
    Then Verify the led state of ${line3} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

    &{configurationDetails}=    create dictionary    topsoftkey3 type=none
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then On ${phone2} wait for 3 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

    Given I want to program dnd key on position 3 on ${phone1}
    Then on ${phone1} press ${softKey} ${programKey3} for 1 times
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then on ${phone1} press ${softKey} ${programKey3} for 1 times
    Then Verify the led state of ${line3} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then I want to program ${none} key on position 3 on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then On ${phone2} wait for 3 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    DND Default Configuration

750153: TC027 BLF Multi dialog -DUT recieves incoming and make outbound call.
    [Tags]    Owner:AbhishekPathak    Reviewer:    BLF    750153
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blf
                                ...                  topsoftkey4 label=blf    topsoftkey4 value=${phone2}
                                ...                  prgkey4 type=blf    prgkey4 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} verify display message ${blf}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone2}

750157: TC043 BLF Test BLF LED in outgoing, ringing, answer, hold
   [Tags]    Owner:AbhishekPathak    Reviewer:    BLF    750157
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blf    topsoftkey4 label=blf
                                ...                  topsoftkey4 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} verify display message ${blf}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify ringing state on ${phone3} and ${phone2}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then verify the led state of ${line4} as ${off} on ${phone1}

    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone2}

750135: TC007 End the incoming call in connected state
    [Tags]    Owner:Vikhyat    Reviewer:    mxone
    [Timeout]    40 minutes
    [Setup]   RUN KEYWORDS    Check Phone Connection    Delete Directory Entries
    Given On ${phone1} verify display message ${phone1}
    Then Add number of ${phone2} in the directory of ${phone1}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then On ${phone1} verify display message SECNUM
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${softkey}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then On ${phone1} verify display message SECNUM
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${line1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then On ${phone1} verify display message SECNUM
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    And On ${phone1} verify display message ${phone1}
    [Teardown]    RUN KEYWORDS    Delete Directory Entries    Generic Test Teardown

750136: TC008 Outgoing call: Outgoing call in alerting state
    [Tags]    Owner:Vikhyat    Reviewer:    outgoingCall
    [Timeout]    35 minutes
    [Setup]    Check Phone Connection    Delete Directory Entries
    Given On ${phone1} verify display message ${phone1}
    Then Add number of ${phone2} in the directory of ${phone1}

    #Make an outgoing call using offhook
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone1}

    #Make an outgoing call using line key1
    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone1}

    #Make an outgoing call using loudspeaker
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone1}
    [Teardown]    RUN KEYWORDS    Delete Directory Entries    Generic Test Teardown

750137: TC009 Cancel an outgoing call
    [Tags]    Owner:Vikhyat    Reviewer:    cancelOutgoingCall
    Given On ${phone1} verify display message ${phone1}

    #Make call through offhook
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    # Make call through line key
    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    #Make an outgoing call using loudspeaker
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    And On ${phone1} verify display message ${phone1}

750138: TC010 Remote answer the outgoing call
    [Tags]    Owner:Vikhyat    Reviewer:    answerOutgoingCall
    [Timeout]    35 minutes
    Given On ${phone1} verify display message ${phone1}

    #Make an outgoing call using offhook
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}

    #Make an outgoing call using line key1
    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}

    #Make an outgoing call using loudspeaker
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    And Disconnect the call from ${phone2}

750139: TC011 End the outgoing call in connected state
    [Tags]    Owner:Vikhyat    Reviewer:    endActiveCall
    [Timeout]    35 minutes
    Given On ${phone1} verify display message ${phone1}

    #Make call using offhook
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    #Make an outgoing call using line key1
    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then On ${phone1} wait for 3 seconds
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    #Make an outgoing call using loudspeaker
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    And On ${phone1} verify display message ${phone1}

750145: TC018 Consultative Xfer(Attended Xfer)
    [Tags]    Owner:Vikhyat    Reviewer:    consultiveTransfer    750145
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} Wait for 3 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${transfer} in TransferState
    Then On ${phone1} verify display message ${callTransferred}
    Then Verify audio path between ${phone2} and ${phone3}
    And Disconnect the call from ${phone2}

750146: TC019 Two-line Xfer - Attended Xfer
    [Tags]    Owner:Vikhyat    Reviewer:    twoLineTransfer    750146
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${programKey1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${line2} on phone ${phone1}
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${transfer} in TransferState
    Then I want to press line key ${line1} on phone ${phone1}
    Then On ${phone1} verify display message ${callTransferred}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${phone1}
    And Disconnect the call from ${phone2}

750147: TC021 MX-One type xfer.
    [Tags]    Owner:Vikhyat    Reviewer:    mxoneTransfer    750147
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} enter number ${phone3}
    Then I want to press line key ${line2} on phone ${phone1}
    Then On ${phone3} Wait for 3 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then On ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} verify display message ${callTransferred}
    Then Verify audio path between ${phone2} and ${phone3}
    And Disconnect the call from ${phone2}

750148: TC022 Two-line Conference
    [Tags]    Owner:Vikhyat    Reviewer:    twoLineConference
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then I want to press line key ${line2} on phone ${phone1}
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${line1} on phone ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${leave}
    Then I want to verify on ${phone2} negative display message ${leave}
    Then I want to verify on ${phone3} negative display message ${leave}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

750149: TC023 MX-One type conference.
    [Tags]    Owner:Vikhyat    Reviewer:    mxoneConference
    [Timeout]    30 minutes
    &{configurationDetails}=    CREATE DICTIONARY    map conf key to=3    conference disabled=1    map conf as DTMF=1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then On ${phone1} verify display message ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then On ${phone1} Wait for 3 seconds
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then On ${phone1} dial number 3
    Then On ${phone1} verify display message ${conferenceLeader}
    Then On ${phone2} verify display message ${conferenceMember}
    Then On ${phone3} verify display message ${conferenceMember}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then On ${phone1} press the softkey ${transfer} in ConferenceCallState
    Then On ${phone1} enter number ${phone4}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone4} using ${loudSpeaker}
    Then On ${phone1} dial number 3
    Then On ${phone1} verify display message ${conferenceLeader}
    Then On ${phone2} verify display message ${conferenceMember}
    Then On ${phone3} verify display message ${conferenceMember}
    Then On ${phone4} verify display message ${conferenceMember}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}

    &{configurationDetails}=    CREATE DICTIONARY    conference disabled=0    map conf as DTMF=    map conf key to=
    And Configure parameters on ${phone1} using ${configurationDetails}

750152: TC026 BLF Multi dialog - DUT recieves multiple incoming calls
    [Tags]    Owner:Vikhyat    Reviewer:     BLF
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=0    topsoftkey4 type=blf
                                ...                  topsoftkey4 label=blf    topsoftkey4 value=${phone2}
    Given Configure parameters on ${phone1} using ${configurationDetails}

    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then Verify the Caller id on ${phone3} and ${phone2} display
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then Verify the led state of ${line4} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudSpeaker}
    Then Verify the Caller id on ${phone4} and ${phone2} display
    Then Verify the led state of ${line2} as ${blink} on ${phone2}
    Then Answer the call on ${phone2} using ${programKey2}
    Then Verify audio path between ${phone4} and ${phone2}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    &{configurationDetails}=    CREATE DICTIONARY    collapsed softkey screen=1    topsoftkey4 type=    topsoftkey4 label=
                                ...                  topsoftkey4 value=
    And Configure parameters on ${phone1} using ${configurationDetails}

750292: TC046 MXONE Conference using Xfer key
    [Tags]    Owner:Vikhyat    Reviewer:    mxone
    [Timeout]    30 minutes
    &{configurationDetails}=    CREATE DICTIONARY    map conf key to=3
    Given Configure parameters on ${phone2} using ${configurationDetails}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then On ${phone3} Wait for 3 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then On ${phone1} dial number 3
    Then On ${phone1} verify display message ${conferenceLeader}
    Then On ${phone2} verify display message ${conferenceMember}
    Then On ${phone3} verify display message ${conferenceMember}

    Then On ${phone1} wait for 5 seconds
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Initiate Transfer on ${phone1} to ${phone4} using ${consult}
    Then On ${phone4} Wait for 3 seconds
    Then Answer the call on ${phone4} using ${loudSpeaker}
    Then On ${phone1} dial number 3
    Then On ${phone1} verify display message ${conferenceLeader}
    Then On ${phone2} verify display message ${conferenceMember}
    Then On ${phone3} verify display message ${conferenceMember}
    Then On ${phone4} verify display message ${conferenceMember}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}
