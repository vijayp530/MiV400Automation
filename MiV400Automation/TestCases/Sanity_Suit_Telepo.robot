*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py


Test Timeout  20 minutes
Suite Setup  RUN KEYWORDS    Phones Initialization    Get DUT Details
Test Setup   Check Phone Connection
Test Teardown    Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Generic Test Teardown

*** Test Cases ***

750296: Redial
    [Tags]    Owner:Ram    Reviewer:Vikhyat    redial    750296
    [Setup]    RUN KEYWORDS    Check Phone Connection    Clear Call History
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Disconnect the call from ${phone1}
    Then press the call history button on ${phone1} and folder ${outgoing} and ${dial}
    Then on ${phone1} verify display message ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    And Disconnect the call from ${phone2}
    [Teardown]  RUN KEYWORDS    Clear Call History    Generic Test Teardown

750297: Call on hold (Internal Call)
    [Tags]    Owner:Ram    Reviewer:Vikhyat    HoldUnhold    750297
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then On ${phone2} Wait for 5 seconds
    Then answer the call on ${phone2} using ${offHook}
    Then Press hardkey as ${holdState} on ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then I want to press line key ${line1} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    And disconnect the call from ${phone2}

750299: Attended transfer (Internal Call)
    [Tags]    Owner:Aman    Reviewer:    transfer    750299
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Verify the Caller id on ${phone3} and ${phone2} display
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750300: Call monitoring and pickup
    [Tags]    Owner:Aman    Reviewer:Vikhya    pickup    750300
    Given I want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then On Telepo verify the led state of ${blf} programmed key as ${blink} on ${phone1}
    Then On Telepo press the ${blf} programmed key on ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    And Disconnect the call from ${phone2}

750301: Speed dial
    [Tags]    Owner:Aman    Reviewer:    speedDial
    Given On Telepo press the ${blf} programmed key on ${phone1}
    Then On ${phone5} Wait for 5 seconds
    Then answer the call on ${phone5} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone5}
    Then Verify the Caller id on ${phone1} and ${phone5} display
    And Disconnect the call from ${phone1}

750675: Blind transfer with BLF key
    [Tags]    Owner:Aman    Reviewer:Vikhyat    transfer    750675
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then On Telepo press the ${blf} programmed key on ${phone1}
    Then On ${phone5} wait for 5 seconds
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then Verify the Caller id on ${phone2} and ${phone5} display
    And Disconnect the call from ${phone5}
	
750302: Line Keys
    [Tags]    Owner:Abhishekkhanchi    Reviewer:Vikhyat    xfer    750302
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 4 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then i want to press line key ${line2} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone3} using ${programKey1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then Verify extension ${number} of ${phone1} on ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

#750303: Long Duration Call
#    [Tags]    Owner:Vikhyat    Reviewer:
#    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
#    Then Answer the call on ${phone2} using ${offHook}
#    Then Verify the Caller id on ${phone1} and ${phone2} display
#    Then Verify audio path between ${phone1} and ${phone2}
#    Then On ${phone1} Wait for 3600 seconds
#    Then Verify the Caller id on ${phone1} and ${phone2} display
#    Then Verify audio path between ${phone1} and ${phone2}
#    And Disconnect the call from ${phone1}

750305: Call from the favorites menu
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    favorites    750305
    Given on ${phone1} verify display message ${favourites}
    Then On Telepo press the ${favourites} programmed key on ${phone1}
    Then On ${phone1} Wait for 3 seconds
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone5}
    Then verify the caller id on ${phone1} and ${phone5} display
    And disconnect the call from ${phone1}

750306: Local conference call 6800i
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    750306
    [Setup]    RUN KEYWORDS    Check Phone Connection    Clear Call History
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then On ${phone2} press the softkey ${dial} in DialingState
    Then On ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${missed} and ${Dial}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And Press the call history button on ${phone1} and folder ${clearLog} and ${quit}


    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${programKey1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${received} and ${dial}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And Press the call history button on ${phone1} and folder ${clearLog} and ${quit}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${programKey1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${dial}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    And disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Clear Call History    Generic Test Teardown

750310: Make intercom call
    [Tags]    Owner:Vikhyat    Reviewer:    makeIntercom    750310
    Given On Telepo press the ${intercom} programmed key on ${phone1}
    Then On ${phone5} wait for 3 seconds
    Then On ${phone1} verify display message ${drop}
    Then Verify the led state of ${mute} as ${blink} on ${phone5}
    Then Press hardkey as ${mute} on ${phone5}
    Then Verify the led state of ${mute} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone5} display
    Then Verify audio path between ${phone1} and ${phone5}
    Then Disconnect the call from ${phone1}

750311: Receive intercom call
    [Tags]    Owner:Vikhyat    Reviewer:    receiveIntercom
    Given On Telepo press the ${intercom} programmed key on ${phone1}
    Then On ${phone5} wait for 3 seconds
    Then On ${phone1} verify display message ${drop}
    Then Verify the led state of ${mute} as ${blink} on ${phone5}
    Then Press hardkey as ${mute} on ${phone5}
    Then Verify the led state of ${mute} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone5} display
    Then Verify audio path between ${phone1} and ${phone5}
    Then Disconnect the call from ${phone1}

750320: Internal call to ACD Group distributed to 6800i desk phone
    [Tags]    Owner:Vikhyat    Reviewer:    acdGroup
    [Setup]    RUN KEYWORDS  Check Phone Connection    Default ACD Group Settings
    Given On ${phone1} dial number *28*11
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} wait for 5 seconds
    Then On ${phone2} dial number 80023
    Then On ${phone2} press the softkey ${dial} in DialingState
    Then On ${phone1} Wait for 3 seconds
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone2} verify display message ACD1
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Default ACD Group Settings    Generic Test Teardown

750321: Internal call to Attendant Group distributed to 6800i desk phone
    [Tags]    Owner:Vikhyat    Reviewer:    attendantGroup    750321
    [Setup]    RUN KEYWORDS  Check Phone Connection    Default Attendant Group Settings
    Given On ${phone1} dial number *28*12
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} wait for 5 seconds
    Then On ${phone2} dial number 80024
    Then On ${phone2} press the softkey ${dial} in DialingState
    Then On ${phone1} wait for 3 seconds
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone2} verify display message AT1
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Default Attendant Group Settings    Generic Test Teardown

750307: Make call via BLF key
    [Tags]    Owner:Anuj   Reviewer:Vikhyat  blf    750307
    Given On Telepo press the ${blf} programmed key on ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then answer the call on ${phone5} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone5}
    Then On Telepo verify the led state of ${blf} programmed key as ${on} on ${phone1}
    And disconnect the call from ${phone2}

750308: Call to BLF monitored user
    [Tags]    Owner:Anuj    Reviewer:    blf    750308
    Given i want to make a two party call between ${phone2} and ${phone5} using ${loudspeaker}
    Then On Telepo verify the led state of ${blf} programmed key as ${blink} on ${phone1}
    Then answer the call on ${phone5} using ${line1}
    Then On Telepo verify the led state of ${blf} programmed key as ${on} on ${phone1}
    Then verify audio path between ${phone2} and ${phone5}
    And disconnect the call from ${phone2}

750309: Parking and retrieval via soft keys
    [Tags]    Owner:Anuj   Reviewer:Vikhyat  blf    750309
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
#    Then I want to press line key ${programKey5} on phone ${phone1} # topsoftkey3 for 6865i for park
    Then On Telepo press the ${park} programmed key on ${phone1}
    Then On ${phone5} Wait for 5 seconds
    Then On Telepo press the ${pickup} programmed key on ${phone5}
#    Then On ${phone5} press ${softkey} ${programKey5} for 1 times
    Then verify audio path between ${phone2} and ${phone5}
    And disconnect the call from ${phone2}

750294: Make outbound call from DUT
    [Tags]    Owner:AbhishekPathak    Reviewer:    outbound_call
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then on ${phone2} wait for 2 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify extension ${name} of ${phone2} on ${phone1}
    Then Verify extension ${name} of ${phone1} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

7502945: Search and make call to contact
    [Tags]    Owner:AbhishekPathak    Reviewer:    call_directory    7502945
    Given On ${phone1} verify directory with ${directoryAction['searchWithDial']} of ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

750298: Blind transfer (Internal call)
    [Tags]    Owner:AbhishekPathak    Reviewer:    blind_transfer    750298
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then on ${phone3} wait for 2 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    And Disconnect the call from ${phone2}

750323 : Recovery after restart
	[Tags]    Owner:Avishek    Reviewer:
	Given Reboot ${phone1}
    And on ${phone1} verify display message Available

750674: call logs - Mitel6800i desk phones
    [Tags]    Owner:Vikhyat    Reviewer:    callHistory    failed
    [Setup]    RUN KEYWORDS    Check Phone Connection    Clear Call History
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then On ${phone2} press the softkey ${dial} in DialingState
    Then On ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${missed} and ${Dial}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And Press the call history button on ${phone1} and folder ${clearLog} and ${quit}


    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone1} using ${programKey1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${received} and ${dial}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And Press the call history button on ${phone1} and folder ${clearLog} and ${quit}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${programKey1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${dial}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    And disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Clear Call History    Generic Test Teardown

750676: attended transfer with blf keys
    [Tags]    Owner:Vikhyat    Reviewer:    blfTransfer    attendedTransfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then On ${phone1} press the softkey ${transfer} in AnswerState
    Then On Telepo press the ${blf} programmed key on ${phone1}
    Then On ${phone5} wait for 5 seconds
    Then Answer the call on ${phone5} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone5}
    Then On ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} verify display message ${callTransferred}
    Then Verify the Caller id on ${phone5} and ${phone2} display
    Then Verify audio path between ${phone5} and ${phone2}
    And Disconnect the call from ${phone5}