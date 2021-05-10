*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py

Suite Setup      RUN KEYWORDS    Phones Initialization    Get Dut Details
Test Setup       Check Phone Connection
Test Teardown    Generic Test Teardown
Suite Teardown   RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Disconnect Terminal
Test Timeout     20 minutes

*** Test Cases ***

TC016: Press HISTORY on active call
	[Tags]    Test2
	Given I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then Verify ringing state on ${phone3} and ${phone1}
	Then Disconnect the call from ${phone3}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${loudspeaker}
	Then Verify audio path between ${phone1} and ${phone2}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then Press the call history button on ${phone1} and folder ${all} and ${nothing}
	Then Verify extension ${name} of ${phone3} on ${phone1}
	Then Disconnect the call from ${phone2}
	And Press hardkey as ${goodBye} on ${phone1}

TC014: CA display while in Off -hook for multiple call appearances
	[Tags]    test3
	Given I want to press line key ${programKey1} on phone ${phone1}
	Then Verify the led state of ${line1} as ${on} on ${phone1}
	Then On ${phone1} verify display message ${dial}
	Then I want to press line key ${programKey2} on phone ${phone1}
	Then Verify the led state of ${line2} as ${on} on ${phone1}
	Then On ${phone1} verify display message ${dial}
	Then Verify the led state of ${line1} as ${off} on ${phone1}
	And press hardkey as ${goodBye} on ${phone1}

TC015: CA status when multiple calls are answered
	[Tags]    Test4
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${loudspeaker}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Then Verify the led state of ${line2} as ${blink} on ${phone1}
	Then Answer the call on ${phone1} using ${programKey2}
	Then Verify audio path between ${phone1} and ${phone3}
	Then Verify the Caller id on ${phone1} and ${phone3} display
	Then Verify the led state of ${line1} as ${blink} on ${phone1}
	Then I want to press line key ${programKey1} on phone ${phone1}
	Then Verify the led state of ${line1} as ${on} on ${phone1}
	Then Verify the led state of ${line2} as ${blink} on ${phone1}
	Then Disconnect the call from ${phone2}
	And Disconnect the call from ${phone3}

TC019: Press Mute while in Active call Handset
	[Tags]    test5
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${loudspeaker}
	Then Verify audio path between ${phone1} and ${phone2}
	Then Press hardkey as ${mute} on ${phone1}
	Then Verify the led state of mute as ${blink} on ${phone1}
	Then Verify one way audio from ${phone2} to ${phone1}
	Then Press hardkey as ${mute} on ${phone1}
	Then Verify audio path between ${phone1} and ${phone2}
	And Disconnect the call from ${phone2}

TC017: Active call up, second call comes in and is dismissed- far end hangs up
	[Tags]    Test6
	I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Answer the call on ${phone2} using ${loudspeaker}
	Verify audio path between ${phone1} and ${phone2}
	I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Verify the Caller id on ${phone1} and ${phone3} display
	Disconnect the call from ${phone3}
	Verify the led state of ${line2} as ${off} on ${phone1}
	Verify the Caller id on ${phone1} and ${phone2} display
	Disconnect the call from ${phone1}

TC006: From Directory, select a user press SPEAKER button
	[Tags]    test7
	Given Press hookMode ${offHook} on phone ${phone1}
	Then Press hookMode ${onHook} on phone ${phone1}
	Then On ${phone1} press directory and ${loudSpeaker} of ${phone2}
	Then Verify ringing state on ${phone1} and ${phone2}
	And Disconnect the call from ${phone1}

TC012: Press dial in call History
	[Tags]    Test8
	I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Disconnect the call from ${phone2}
	Press the call history button on ${phone1} and folder ${all} and ${dial}
	Verify ringing state on ${phone1} and ${phone2}
	Disconnect the call from ${phone2}
	Disconnect the call from ${phone1}


TC010: Open call History #not complete ##############
	[Tags]    test9
	I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
	Disconnect the call from ${phone3}
	I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Answer the call on ${phone1} using ${loudspeaker}
	Verify audio path between ${phone1} and ${phone2}
	Disconnect the call from ${phone2}
	Press the call history button on ${phone1} and folder ${all} and ${details}
	Verify extension ${name} of ${phone2} on ${phone1}
	press hardkey as ${goodBye} on ${phone1}

TC011: Directory blind transfer extension
	[Tags]    test10
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${loudspeaker}
	Then on ${phone1} ${blindTransfer} call to ${phone3} using directory
	Then Answer the call on ${phone3} using ${loudspeaker}
	Then Verify audio path between ${phone3} and ${phone2}
	And Disconnect the call from ${phone3}

TC009: Place outbound call with collected digits when ON-HOOK
	[Tags]    Test11
	Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Answer the call on ${phone2} using ${loudspeaker}
	Then verify the caller id on ${phone1} and ${phone2} display
	Then Verify audio path between ${phone1} and ${phone2}
	And Disconnect the call from ${phone2}

TC002: Verify the call apperance on an inbound call (name is available)
	[Tags]    Test12
	Given Press hookMode ${offHook} on phone ${phone1}
	Then Press hookMode ${onHook} on phone ${phone1}
	Then Verify extension ${number} of ${phone1} on ${phone1}
	Then Verify the led state of speaker as ${off} on ${phone1}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Verify extension ${name} of ${phone2} on ${phone1}
	Then Disconnect the call from ${phone1}
	And Disconnect the call from ${phone2}

TC003: Phone is the transferee in a blind transfer operation
	[Tags]    Test13
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
	Then Answer the call on ${phone3} using ${loudspeaker}
	Verify audio path between ${phone3} and ${phone2}
	Then Disconnect the call from ${phone3}

TC013: Missed call indicator for n calls
	[Tags]    Test14
	Given Press the call history button on ${phone1} and folder ${all} and ${goodBye}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Disconnect the call from ${phone2}
	Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Disconnect the call from ${phone2}
	And On ${phone1} verify display message Missed Calls

TC021: Auto Unmute when an active muted call gets disconnected
	[Tags]    Test15
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then answer the call on ${phone1} using ${loudspeaker}
	Then Verify audio path between ${phone1} and ${phone2}
	Then press hardkey as ${mute} on ${phone1}
	Then Verify the led state of mute as ${blink} on ${phone1}
	Then Disconnect the call from ${phone2}
	And Verify the led state of mute as ${off} on ${phone1}

TC026: Directory Details page displays Telephony presence icon on contacts extension only
	[Tags]    test16
	Given On ${phone1} press directory and ${details} of ${phone2}
	And Press hardkey as ${goodBye} on ${phone1}

TC029: Phone dials star12 to unpark a call
	[Tags]    Test17
	Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
	When Verify ringing state on ${phone2} and ${phone1}
	Then Answer the call on ${phone1} using ${programKey1}
	Then Put the linekey ${line1} of ${phone1} on ${Hold}
	Then I want to press line key ${line2} on phone ${phone1}
    Then I want to Park the call from ${phone1} on ${phone3} using ${FAC} and ${dial}
    Then On ${phone1} verify the softkeys in ${idleState}
	Then I want to unPark the call from ${phone3} on ${phone1} using ${FAC} and ${dial}
	Then Verify audio path between ${phone1} and ${phone2}
	And Disconnect the call from ${phone1}

TC030: Consult Conf. Phone target from initiator and conference established.
	[Tags]    Test18
	Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Answer the call on ${phone2} using ${loudspeaker}
	Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then On ${phone1} verify display on a 3 party conference call
	Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then Disconnect the call from ${phone1}
	Then Verify audio path between ${phone3} and ${phone2}
	And Disconnect the call from ${phone2}

TC023: Ethernet values edit mode display
    [Tags]    test19
	Given Verify Ethernet values edit mode display on ${phone1}

TC028: Press Stop while playing VM message
	[Tags]    Test20    notApplicableFor6910
	Given Leave voicemail message from ${phone2} on ${phone1}
	Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
	Then press hardkey as ${scrollRight} on ${phone1}
	Then On the ${phone1} verify softkeys in different state using ${voicemailInbox}
	Then on ${phone1} press the softkey ${play} in VoiceMailState
	Then On the ${phone1} verify softkeys in different state using ${playVoicemail}
	Then on ${phone1} press the softkey ${pause} in VoiceMailState
	Then On the ${phone1} verify softkeys in different state using ${pauseVoicemail}
	Then on ${phone1} press the softkey ${play} in VoiceMailState
	Then On the ${phone1} verify softkeys in different state using ${playVoicemail}
	Then on ${phone1} press the softkey ${stopPlay} in VoiceMailState
	Then On the ${phone1} verify softkeys in different state using ${voicemailInbox}
	And press hardkey as ${goodBye} on ${phone1}

TC004: Put active call on hold using non handset
	[Tags]    Test21
	Given Verify extension ${number} of ${phone1} on ${phone1}
	Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then Answer the call on ${phone2} using ${loudspeaker}
	Then On ${phone1} verify display message 00:
	Then Put the linekey ${line1} of ${phone1} on ${hold}
	Then Put the linekey ${line1} of ${phone1} on ${unHold}
	Then Verify audio path between ${phone1} and ${phone2}
	And disconnect the call from ${phone2}

TC018: Ping to valid IP (on phone)
    [Tags]    Owner:Abhishek khanchi    Reviewer:Vikhyat    pingIP
    Given on ${phone1} move to ${diagnostics} to ${ping} settings
    Then on ${phone1} Wait for 3 seconds
    Then Enter ${ipaddrstr} on ${phone1} to ${ping} settings
    Then On ${phone1} verify display message ${numberOfPackets}
    And Press hardkey as ${goodBye} on ${phone1}

730977: TC033: Join the Held calls to conference by selecting from 2 or more held calls
    [Tags]    Owner:AbhishekPathak  Reviewer:    merge      notApplicableFor6910    730977
    Given i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${line2}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then i want to make a two party call between ${phone1} and ${phone4} using ${programkey3}
    Then answer the call on ${phone4} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone4}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then press hardkey as ${scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone2}

730946: TC008: Hang up call that is on Hold by pressing the Drop softkey
    [Tags]    Owner:Gaurav    Reviewer:
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone2} verify display message ${drop}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then on ${phone2} verify display message ${drop}
    And on ${phone2} press the softkey ${drop} in AnswerState

730960: TC020: Leave a voicemail on phone
    [Tags]    Owner:Gaurav    Reviewer:    voicemail    notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone2} wait for 60 seconds
    Then press hardkey as ${goodbye} on ${phone2}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And press hardkey as ${goodbye} on ${phone1}

730971: TC027: Call Handling mode(CHM) options set to In a Meeting
    [Tags]    Owner:Gaurav    Reviewer:    assignuser    notApplicableFor6910    730971
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${always} in ${inMeeting}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} press the softkey ${save} in SettingState
    Then press hardkey as ${goodbye} on ${phone1}

    Then On ${phone2} enter number ${phone1}
    Then on ${phone2} press the softkey ${dial} in DialingState
    Then On ${phone2} verify display message ${displayVoiceMail}
    And press hardkey as ${goodbye} on ${phone2}
    [Teardown]    Default Availability State

730975: TC031: Phone completes blind conference
    [Tags]    Owner:AbhishekPathak    Reviewer:    blindconference
    Given i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directconference}
    Then on ${phone1} verify display message ${conference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${goodbye} on ${phone3}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    And on ${phone1} verify the softkeys in ${idleState}