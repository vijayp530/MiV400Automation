*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot

Library    ../lib/MyListner.py
Library    Collections

Suite Setup    RUN KEYWORDS    Phones Initialization    Get DUT Details
Test Setup    Check Phone Connection
Test Teardown    Generic Test Teardown
#Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Default Availability State    Generic Test Teardown
Test Timeout    25 minutes

*** Test Cases ***

Sample Test 1:
    [Tags]    sample
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    And Disconnect the call from ${phone3}

Sample Test 2:
    [Tags]    sample
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    And Disconnect the call from ${phone3}

Sample Test 3:
    [Tags]    sample
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    And Disconnect the call from ${phone3}

Sample Test 4:
    [Tags]    sample
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    And Disconnect the call from ${phone3}

139108: Call VM from Voicemail page
    [Tags]    Owner:Ram    Reviewer:Avishek    Voicemail    notApplicableFor6910    139108
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} verify the softkeys in ${voicemail}
    Then on ${phone1} press the softkey ${callVMInbox} in VoiceMailState
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${voiceMailLogin}
    And Press hardkey as ${goodBye} on ${phone1}

156040: CHM "In a Meeting" Call Forward Mode - No Answer
    [Tags]    Owner:Ram    Reviewer:Avishek    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${inMeeting}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify the softkeys in ${settings}
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then on ${phone1} navigate to Default settings
    And Change the phone state to default state on ${phone1}
    [Teardown]    Default Availability State

281022: Incoming call while Playing Ringtone
    [Tags]    Owner:Ram    Reviewer:Avishek    Audio    notApplicableFor6910    281022
    Given on ${phone1} move to ${audio} to ${ringTones} settings
    Then On ${phone1} verify display message ${playInt}
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
    And Disconnect the call from ${phone2}

177429: Press Log Issue key multiple times
    [Tags]    Owner:Ram    Reviewer:Avishek    LogIssue    notApplicableFor6910
    Given on ${phone1} navigate to ${login} settings
    Then on ${phone1} press the softkey ${logIssue} in SettingState
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} press the softkey ${logIssue} in SettingState
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} press the softkey ${logIssue} in SettingState
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    And Verify ringing state on ${phone2} and ${phone1}
    And Disconnect the call from ${phone2}

139163: TC01: new unheard voicemail message number (increase 0 to 1)
    [Tags]    Owner:Ram    Reviewer:Avishek    Voicemail    notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    And On ${phone1} verify display message ${play}

128967: Assign and Unassign a user with cas.authenticatorUrl
    [Tags]    Owner:Ram    Reviewer:Avishek    assignUser    notApplicableFor6910
    [Setup]   Assign Extension Custom Setup
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} dial number ${voicemailPassword}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} verify display message ${assigned}
    Then on ${phone1} Wait for 5 seconds
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 1 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    And on ${phone1} wait for 10 seconds
    [Teardown]   Assign Extension Custom Teardown

140299: Outgoing call with FIlter open in Call History
    [Tags]    Owner:Ram    Reviewer:Avishek    CallHistory    140299
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${received} and ${loudspeaker}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And disconnect the call from ${phone1}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${missed} and ${loudspeaker}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And disconnect the call from ${phone1}

138501: Call Handling mode(CHM) options set to Out of Office
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${all}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 3 times
    Then on ${phone1} verify display message ${outOfOffice}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And on ${phone1} press the softkey ${quit} in SettingState
    [Teardown]    Default Availability State

138499: Call Handling mode(CHM) options set to Custom
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${all}
    Then press hardkey as ${scrollLeft} on ${phone1}
    Then on ${phone1} verify display message ${custom}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And on ${phone1} press the softkey ${quit} in SettingState
    [Teardown]    Default Availability State

145747: incoming call view
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Call
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
    And disconnect the call from ${phone2}

147261: Press Park enter destination from Directory or History
    [Tags]    Owner:Ram    Reviewer:    Park    notApplicableFor6910    147261
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${directory} and ${timeout}
    Then Verify extension ${number} of ${phone2} on ${phone3}
    And disconnect the call from ${phone2}

175593: Pressing Hold then UnHold interchangeably
    [Tags]    Owner:Ram    Reviewer:    HoldUnhold
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    And disconnect the call from ${phone2}

145503: Authentication popup Assign User
    [Tags]    Owner:Ram    Reviewer:    assignUser    notApplicableFor6910
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press the softkey ${assign} in SettingState
    Then on ${phone1} verify display message ${assignUser}
    Then on ${phone1} verify display message ${extension}
    Then on ${phone1} verify display message ${password}
    And press hardkey as ${goodBye} on ${phone1}

139103: TC05: Move Voicemail from Inbox-Saved-Delete-Inbox
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Move voicemail message from ${inboxToSaved} folder for ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}

    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Move voicemail message from ${DeleteToInbox} folder for ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}

    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Move voicemail message from ${SavedToDelete} folder for ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

145613: Place or Receive a call while VM password popup is displaying
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then on ${phone1} press ${softKey} ${programKey1} for 1 times
    Then Verify the led state of Line1 as ${off} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

145451: All call appearances are on Hold
    [Tags]    Owner:Ram    Reviewer:    HoldUnhold    145451
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${programKey2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${programKey3}
    Then Verify audio path between ${phone1} and ${phone4}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Put the linekey ${line3} of ${phone1} on ${hold}
    Then on ${phone1} press ${softKey} ${programKey2} for 1 times
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Disconnect the call from ${phone4}
    And Disconnect the call from ${phone2}

217345: TC015 Check participants list when new member join the conference
    [Tags]    Owner:Ram    Reviewer:    CallConference    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone3} and ${phone4} using ${line2}
    Then answer the call on ${phone4} using ${line1}
    Then Verify audio path between ${phone3} and ${phone4}
    Then on ${phone3} press the softkey ${merge} in ConferenceCallState
    Then on ${phone3} verify display message ${show}
    Then I want to make a two party call between ${phone3} and ${phone5} using ${line2}
    Then answer the call on ${phone5} using ${line1}
    Then Verify audio path between ${phone3} and ${phone5}
    Then on ${phone3} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone5} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone6} using ${line2}
    Then answer the call on ${phone6} using ${line1}
    Then Verify audio path between ${phone3} and ${phone6}
    Then on ${phone3} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then Verify extension ${number} of ${phone6} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

139675: phone presses Show to view conference parties
    [Tags]    Owner:Ram    Reviewer:    CallConference    notApplicableFor6910    139675
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

139114: Incoming call while in Voicemail (not playing vm)
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910
    Given login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then press hardkey as ${goodBye} on ${phone1}
    Then answer the call on ${phone1} using ${line1}
    Then verify the caller id on ${phone1} and ${phone2} display
    And disconnect the call from ${phone2}

    Given login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone2} verify display message ${drop}
    And disconnect the call from ${phone2}

139061: Press Settings. Enter VM password. Scroll to a Time/Date. Press Voicemail or History or Directory
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910
    Given On ${phone1} move to ${timedate} to ${timeZone} settings
    Then press hardkey as ${voicemail} on ${phone1}
    Then on ${phone1} verify display message ${voicemailUserLogin}

563666: active call view, call held
    [Tags]    Owner:Ram    Reviewer:    CallHeld
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    And disconnect the call from ${phone2}

563670: active call view, transfer call
    [Tags]    Owner:Ram    Reviewer:    TransferCall    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} verify display message >
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    And disconnect the call from ${phone2}

560636: CHM Out of Office edit mode-Always option
    [Tags]    Owner:Ram    Reviewer:    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${Always} in ${outOfOffice}
    Then on ${phone1} verify display message ${alwaysDestination}
    Then on ${phone1} verify display message ${simulRing}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then on ${phone1} verify display message ${backSpace}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then on ${phone1} navigate to Default settings
    And Change the phone state to default state on ${phone1}
    [Teardown]    Default Availability State

561611: Play and Pause a message
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910    561611
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} verify the softkeys in ${VoiceMail}
    Then on ${phone1} press the softkey ${play} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${playVoicemail}
    Then on ${phone1} press the softkey ${pause} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${pauseVoicemail}
    Then on ${phone1} press the softkey ${play} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${playVoicemail}
    Then on ${phone1} press the softkey ${pause} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${pauseVoicemail}
    Then on ${phone1} press the softkey ${play} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${playVoicemail}
    Then on ${phone1} press the softkey ${pause} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${pauseVoicemail}
    And press hardkey as ${goodBye} on ${phone1}

557069: active call is up - user navigates to directory- second incoming call, user leaves directory- call goes to VM
    [Tags]    Owner:Ram    Reviewer:Vikhyat    activeCall    557069
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${directory} on ${phone1}
    Then On ${phone1} verify display message ${directory}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then I want to verify on ${phone1} negative display message ${directory}
    Then on ${phone3} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

558210: History works normally while error message shown
    [Tags]    Owner:Ram    Reviewer:Vikhyat    transfer   inValidExtensionTransfer    notApplicableFor6910    558210
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the softkeys in ${talk}
    Then On ${phone2} verify the softkeys in ${talk}
    Then On ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} enter number ${invalidNumber}
    Then On ${phone1} press the softkey ${transfer} in TransferState
    Then On ${phone1} verify display message ${invalidPhoneNumber}
    Then Press hardkey as ${callersList} on ${phone1}
    Then On ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${callHistory}
    And Disconnect the call from ${phone2}

558093: phone dials *11 to park a call
    [Tags]    Owner:Ram    Reviewer:Vikhyat    Park     holdCall    558093
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then I want to Park the call from ${phone1} on ${phone3} using ${FAC} and ${dial}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then on ${phone3} press ${softkey} ${bottomKey1} for 1 times
    Then verify audio path between ${phone3} and ${phone2}
    And disconnect the call from ${phone2}

558094: phone dials *12 to unpark a call
   [Tags]    Owner:Ram    Reviewer:Vikhyat    Unpark    holdCall    558094
   Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
   Then Answer the call on ${phone2} using ${loudSpeaker}
   Then verify audio path between ${phone1} and ${phone2}
   Then Put the linekey ${line1} of ${phone1} on ${Hold}
   Then I want to press line key ${line2} on phone ${phone1}
   Then I want to Park the call from ${phone1} on ${phone3} using ${FAC} and ${dial}
   Then I want to unPark the call from ${phone3} on ${phone1} using ${FAC} and ${dial}
   Then Verify audio path between ${phone1} and ${phone2}
   Then Verify the led state of ${line1} as ${off} on ${phone3}
   And Disconnect the call from ${phone1}

558244: Transferor hangs up after consult call goes to VM
    [Tags]    Owner:Ram    Reviewer:    Transfer    ReduceNumberofRings    notApplicableFor6910
    Given Set number of rings to 2 on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 20 seconds
    Then disconnect the call from ${phone1}
    Then on ${phone1} verify display message ${callTransferred}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then on ${phone2} verify display message ${displayVoiceMail}
    And disconnect the call from ${phone2}
    [Teardown]    Default Number of Rings

560624:Call Handling mode(CHM) options set to Do Not Disturb
    [Tags]    Owner:Ram    Reviewer:    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${all}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    And Change the phone state to default state on ${phone1}
    [Teardown]     Default Availability State

185808: APT - (Transfer) make call on HEADSET, answer on HEADSET
    [Tags]    Owner:Ram    Reviewer:    Call Transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then On ${phone1} verify display message ${pickup}
    Then Verify audio path between ${phone3} and ${phone2}
    Then Disconnect the call from ${phone2}

560628:Call Handling mode(CHM) options set to Standard
    [Tags]    Owner:Ram    Reviewer:    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${all}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 5 times
    Then on ${phone1} verify display message ${available}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    And disconnect the call from ${phone2}
    [Teardown]    Default Availability State

556956: APT - (Transfer) make call on SPEAKER, answer on SPEAKER
    [Tags]    Owner:Ram    Reviewer:Vikhyat    callTransfer    556956
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Verify audio path between ${phone3} and ${phone2}
    Then On ${phone1} verify the softkeys in ${idle}
    And Disconnect the call from ${phone2}

560892: Delete Call History
    [Tags]    Owner:Ram    Reviewer:Vikhyat    CallHistory    notApplicableFor6910    560892
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Disconnect the call from ${phone1}
    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey1}
    Then Disconnect the call from ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} verify display message ${delete}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} verify display message ${delete}
    And press hardkey as ${goodBye} on ${phone1}

560642: CHM Do Not Disturb edit mode-Never option
   [Tags]    Owner:Ram    Reviewer:    CHM    notApplicableFor6910
   Given on ${phone1} navigate to ${availability} settings
   Then Modify call handler mode on ${phone1} to ${never} in ${doNotDisturb}
   Then on ${phone1} verify display message ${save}
   Then on ${phone1} verify display message ${cancel}
   Then press hardkey as ${scrollDown} on ${phone1}
   Then press hardkey as ${enter} on ${phone1}
   Then on ${phone1} verify display message ${save}
   Then on ${phone1} verify display message ${cancel}
   Then press hardkey as ${enter} on ${phone1}
   Then on ${phone1} verify display message ${save}
   Then on ${phone1} verify display message ${cancel}
   And press hardkey as ${goodBye} on ${phone1}
   [Teardown]    Default Availability State

177474: Backspace and Cancel soft keys display for each audio path
    [Tags]    Owner:Ram    Reviewer:Avishek    Dial
    Given Press hookMode ${offHook} on phone ${phone1}
    Then On ${phone1} verify display message ${dial}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${cancel}
    And Press hookMode ${onHook} on phone ${phone1}
	Given Press hardkey as ${handsFree} on ${phone1}
    Then On ${phone1} verify display message ${dial}
    Then On ${phone1} verify display message ${backspace}
    And On ${phone1} verify display message ${cancel}

145260: Change audio path (from Headset-offhook) while dialing
    [Tags]    Owner:Ram    Reviewer:Avishek    Dial
     Given Press hookMode ${offHook} on phone ${phone1}
     Then On ${phone1} dial partial number of ${phone2} with firstTwo
     Then on ${phone1} press the softkey ${dial} in dialingstate
     Then On ${phone1} verify display message ${requestDenied}
     And Press hookMode ${onHook} on phone ${phone1}

193280: TC03: in FORWARD, press Settings button
    [Tags]    Owner:Ram    Reviewer:Avishek    Voicemail   notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${forward} in VoiceMailState
    Then on ${phone1} verify display message ${edit}
    Then on ${phone1} verify display message ${start}
    Then Press hardkey as ${menu} on ${phone1}
    Then On ${phone1} verify display message ${userSettings}
    And Press hardkey as ${goodBye} on ${phone1}

193279: TC02: in FORWARD, press Directory or Call History button
    [Tags]    Owner:Ram    Reviewer:Avishek    Voicemail    notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${forward} in VoiceMailState
    Then on ${phone1} verify display message ${edit}
    Then on ${phone1} verify display message ${start}
    Then Press hardkey as ${CallersList} on ${phone1}
    Then On ${phone1} verify display message ${CallHistory}
    And Press hardkey as ${goodBye} on ${phone1}

193896: FORWARD, with return receipt
    [Tags]    Owner:Ram    Reviewer:Manoj    Voicemail    notApplicableFor6910    193896    checkthis
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${forward} in VoiceMailState
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} press the softkey ${back} in VoiceMailState
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 4 times
    Then Press hardkey as ${enter} on ${phone1}
    Then on ${phone1} press the softkey ${start} in VoiceMailState
    Then on ${phone1} press the softkey ${stop} in VoiceMailState
    Then on ${phone1} press the softkey ${send} in VoiceMailState
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone2}
    Then on ${phone2} press the softkey ${play} in VoiceMailState
    Then on ${phone2} press the softkey ${stopPlay} in VoiceMailState
    Then on ${phone2} wait for 5 seconds
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then On ${phone1} verify display message ${receiptConfirmation}
    And on ${phone1} press the softkey ${delete} in VoiceMailState

139089: Navigate to Visual VM details screen
    [Tags]    Owner:Ram    Reviewer:Avishek    Voicemail    notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then On ${phone1} verify display message ${voicemailDisplay['inbox']}
    Then On ${phone1} verify display message ${voicemailDisplay['saved']}
    Then On ${phone1} verify display message ${voicemailDisplay['deleted']}
    Then On ${phone1} verify display message ${voicemailDisplay['quit']}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} verify display message ${voicemailscreen['play']}
    Then On ${phone1} verify display message ${voicemailscreen['callback']}
    And On ${phone1} verify display message ${voicemailscreen['delete']}

156046: CHM "Extended Absence" Call Forward Mode - No Answer
    [Tags]    Owner:Ram    Reviewer:Avishek    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${extendedAbsence}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify the softkeys in ${settings}
    Then on ${phone1} press the softkey ${quit} in SettingState
    And on ${phone1} navigate to Default settings
    [Teardown]   Default Availability State

156052: CHM "Do not Disturb" Call Forward Mode - No Answer
    [Tags]    Owner:Ram    Reviewer:Avishek    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${doNotDisturb}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify the softkeys in ${userAvailability}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify the softkeys in ${settings}
    Then on ${phone1} press the softkey ${quit} in SettingState
    And on ${phone1} navigate to Default settings
    [Teardown]   Default Availability State

281021: Incoming call while Setting Ringtone
    [Tags]    Owner:Ram    Reviewer:Avishek    Audio    281021
    Given on ${phone1} move to ${audio} to ${ringTones} settings
    Then press hardkey as ${enter} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${standard}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    And Verify ringing state on ${phone2} and ${phone1}
    And Disconnect the call from ${phone2}

177442: Basic functions during Log Upload or Capture Upload
    [Tags]    Owner:Ram    Reviewer:Avishek    LogUpload    notApplicableFor6910
    Given on ${phone1} move to ${diagnostics} to ${startCapture} settings
    Then on ${phone1} verify display message ${capture}
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${capturing}
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${callersList} on ${phone1}
    Then on ${phone1} verify display message ${callHistory}
    And press hardkey as ${goodBye} on ${phone1}

185050: TC_01 Verify call establishment on Analog handset
    [Tags]    Owner:Ram    Reviewer:Avishek    Call    notApplicableFor6910
    Given on ${phone1} move to ${audio} to ${audioMode} settings
    Then on ${phone1} press ${hardKey} ${scrollUp} for 3 times
    Then Press hardkey as ${enter} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    And Press hookMode ${onHook} on phone ${phone1}

139208: TC03: REPLY, with priority or urgency
    [Tags]    Owner:Ram    Reviewer:    Voicemail   notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then on ${phone1} verify display message ${visualVoicemailScreen}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then on ${phone1} press the softkey ${reply} in VoiceMailState
    Then on ${phone1} press ${hardKey} ${scrollDown} for 2 times
    Then Press hardkey as ${enter} on ${phone1}
    Then on ${phone1} press the softkey ${start} in VoiceMailState
    Then on ${phone1} press the softkey ${stop} in VoiceMailState
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then on ${phone1} press the softkey ${moreBack} in VoiceMailState
    Then Press hardkey as ${scrollLeft} on ${phone1}
    Then On ${phone1} verify display message ${voicemailDisplay['inbox']}
    Then On ${phone1} verify display message ${voicemailDisplay['saved']}
    Then On ${phone1} verify display message ${voicemailDisplay['deleted']}
    And press hardkey as ${goodBye} on ${phone1}

176765: PressMute button while phone receives incoming unanswered call
    [Tags]    Owner:Ram    Reviewer:    Call
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone1}
    Then disconnect the call from ${phone2}

175584: TC010 Deleting all voice msgs
    [Tags]    Owner:Ram    Reviewer:    Voicemail
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Verify the led state of messageWaitingIndicator as ${blink} on ${phone1}
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    And Verify the led state of messageWaitingIndicator as ${off} on ${phone1}

138977: CAS Caller ID strings - “VmDN”
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910
    Given on ${phone1} dial number ${${pbx}voicemailNumber}
    Then on ${phone1} verify display message ${displayVoiceMail}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${all} and ${Details}
    And on ${phone1} verify display message ${displayVoiceMail}

185842: APT - Go off hook from SPEAKER, make call , answer on SPEAKER
    [Tags]    Owner:Ram    Reviewer:    Call    loudSpeaker
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of speaker as ${on} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of speaker as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

177472: Verify Conf. softkey is not shown when audio path or hard keys are in use
    [Tags]    Owner:Ram    Reviewer:    Call
    Given press hardkey as ${handsFree} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${conference}

175597: new incoming call lands on the first available call appearance
    [Tags]    Owner:Ram    Reviewer:    Call
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of Line2 as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then Verify the led state of Line1 as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

185833: APT -(Mute alternate) Go off hook from SPEAKER, make call , answer on SPEAKER
    [Tags]    Owner:Ram    Reviewer:    Call    loudSpeaker
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the led state of speaker as ${off} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of speaker as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone1}
    Then Verify the led state of speaker as ${on} on ${phone2}
    And disconnect the call from ${phone2}

135292: HoldUnhold after transfer
    [Tags]    Owner:Ram    Reviewer:    Transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}

    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}

223239: Xfer error display on the phone test2
    [Tags]    Owner:Ram    Reviewer:    Xfer
    Given on ${phone1} dial number ${${pbx}voicemailNumber}
    Then on ${phone1} wait for 5 seconds
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} verify display message ${xferNotAllowed}
    Then Verify Sip message NOXFER on ${phone1} for SIP/2.0 200 OK method and Contact header using incoming sip message

223240: Conf error display on the phone test2
    [Tags]    Owner:Ram    Reviewer:    Xconf
    Given on ${phone1} dial number ${${pbx}voicemailNumber}
    Then on ${phone1} wait for 5 seconds
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} verify display message ${xconfNotAllowed}
    Then Verify Sip message NOCONF on ${phone1} for SIP/2.0 200 OK method and Contact header using incoming sip message

145754: Focus view for a single session and a held call
    [Tags]    Owner:Ram    Reviewer:    Call
    Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${programKey1}
    Then verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${programKey1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${programKey2}
    Then verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

138800: Press Headset in Call history
    [Tags]    Owner:Ram    Reviewer:    CallHistory
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${all} and ${loudspeaker}
    Then on ${phone1} wait for 3 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}

175576: TC002 Phone MWI when DUT diconnects the the call
    [Tags]    Owner:Ram    Reviewer:    Call
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then Disconnect the call from ${phone1}
    Then on ${phone2} verify display message ${busy}
    And Verify the led state of messageWaitingIndicator as ${off} on ${phone1}

175575: TC001 Phone MWI is idle when no voicemail
    [Tags]    Owner:Ram    Reviewer:    Voicemail
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone2} wait for 10 seconds
    Then Disconnect the call from ${phone2}
    And Verify the led state of messageWaitingIndicator as ${off} on ${phone1}

177817: Verify 69xx username is truncated and phone extension is in parentheses
    [Tags]    Owner:Ram    Reviewer:    Call
    Given Verify extension ${number} of ${phone1} on ${phone1}

145744: active call view, call selected
    [Tags]    Owner:Ram    Reviewer:    Call
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${name} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}

139486: Mesh to Make Me Conference; Call on Hold
    [Tags]    Owner:Ram    Reviewer:    MeshConference    notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${line2}
    Then answer the call on ${phone4} using ${line1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then Put the linekey ${line1} of ${phone4} on ${hold}
    Then on ${phone1} press the softkey ${merge} in ConferenceCallState
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone4}
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

139474: Blind Make me Conference call between 6 parties
    [Tags]    Owner:Ram    Reviewer:    CallConference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then Verify audio path between ${phone4} and ${phone2}
    Then Add the ${phone5} in 4 parties conference call on ${phone2}
    Then Verify audio path between ${phone5} and ${phone3}
    Then Add the ${phone6} in 5 parties conference call on ${phone3}
    Then Verify audio path between ${phone6} and ${phone1}
    Then on ${phone2} verify display message Conferenced 5 calls
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}

176910: Receive an incoming call while in Show parties list
    [Tags]    Owner:Ram    Reviewer:    ConferenceCall    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${line1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} verify display message ${pickUp}
    Then on ${phone1} press ${softKey} ${programKey1} for 1 times
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} press the softkey ${drop} in conferencecallstate
    Then I want to verify on ${phone1} negative display message ${phone2}
    And disconnect the call from ${phone1}

138770: phone receives or places a call (extension)
    [Tags]    Owner:Ram    Reviewer:    CallHistory    notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then press hardkey as ${callersList} on ${phone1}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}

    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then disconnect the call from ${phone2}
    Then press hardkey as ${callersList} on ${phone1}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}

    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then disconnect the call from ${phone1}
    Then press hardkey as ${callersList} on ${phone1}
    Then press hardkey as ${scrollUp} on ${phone1}
    Then press hardkey as ${scrollRight} on ${phone1}
    And Verify extension ${number} of ${phone2} on ${phone1}

154050: invalid hostname in field (phone)
    [Tags]    Owner:Ram    Reviewer:    invalidHostname
    Given Go to ${ping} settings and enter invalid_ip on ${phone1}
    Then on ${phone1} verify display message ${invalidHostName}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Go to ${ping} settings and enter invalid_dns on ${phone1}
    And on ${phone1} verify display message ${invalidHost}

139014: Incoming call while viewing Visual Voicemail is open
    [Tags]    Owner:Ram    Reviewer:    Voicemail    notApplicableFor6910
    Given login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then verify the led state of messageWaitingIndicator as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}

139562: MERGE held calls to conference with other users
    [Tags]    Owner:Ram    Reviewer:    MergeCalls    notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${line1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Put the linekey ${line2} of ${phone1} on ${hold}
    Then on ${phone1} verify display message ${conference}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} verify display message ${conference}
    Then on ${phone1} verify display message Consult
    Then on ${phone1} verify display message ${cancel}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} verify display message >
    Then on ${phone1} press the softkey ${cancel} in DialingState
    Then on ${phone1} verify display message ${merge}
    Then on ${phone1} press the softkey ${merge} in ConferenceCallState
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

164569: Answer a new call while one or more call are on hold using handset_left_call_apperance
    [Tags]    Owner:Ram    Reviewer:    Call
    Given I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${line1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone3}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then on ${phone1} verify display message ${pickUp}
    And disconnect the call from ${phone2}


185824: APT -(Hold alternate) Go off hook from SPEAKER, make call , answer on SPEAKER
    [Tags]    Owner:Ram    Reviewer:    Onhold
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    And Disconnect the call from ${phone2}

177363: Dial from Call History
    [Tags]    Owner:Ram    Reviewer:    CallHistory
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${missed} and ${dial}
    Then verify the caller id on ${phone1} and ${phone2} display

139478: Merge calls in a Make me conference
    [Tags]    Owner:Ram    Reviewer:    CallConference    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then I want to make a two party call between ${phone5} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify audio path between ${phone2} and ${phone5}
    Then on ${phone2} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone5} on ${phone1}
    Then I want to make a two party call between ${phone6} and ${phone3} using ${line1}
    Then answer the call on ${phone3} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then Verify audio path between ${phone3} and ${phone6}
    Then on ${phone3} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then on ${phone1} press ${hardkey} ${scrollDown} for 4 times
    Then Verify extension ${number} of ${phone6} on ${phone1}
    Then I want to make a two party call between ${phone7} and ${phone3} using ${line1}
    Then answer the call on ${phone3} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    And Verify audio path between ${phone3} and ${phone7}

752276:Answer call via call appearance
     [Tags]    Owner:Ram    Reviewer:    Call   notApplicableFor6910
     Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
     Then On ${phone1} verify ${line1} icon state as ${callAppearanceIncoming}
     Then verify the led state of ${line1} as ${blink} on ${phone1}
     Then answer the call on ${phone1} using ${offHook}
     Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
     Then On ${phone1} verify ${line2} icon state as ${callAppearanceIncoming}
     Then verify the led state of ${line2} as ${blink} on ${phone1}
     Then answer the call on ${phone1} using ${softKey}
     Then I want to make a two party call between ${phone4} and ${phone1} using ${offHook}
     Then On ${phone1} verify ${line3} icon state as ${callAppearanceIncoming}
     Then verify the led state of ${line3} as ${blink} on ${phone1}
     Then answer the call on ${phone1} using ${softKey}
     Then I want to make a two party call between ${phone5} and ${phone1} using ${offHook}
     Then On ${phone1} verify ${line4} icon state as ${callAppearanceIncoming}
     Then verify the led state of ${line4} as ${blink} on ${phone1}
     Then answer the call on ${phone1} using ${softKey}
     Then press hardkey as ${holdState} on ${phone1}
     Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
     Then On ${phone1} verify ${line2} icon state as ${callAppearanceLocalHold}
     Then On ${phone1} verify ${line3} icon state as ${callAppearanceLocalHold}
     Then On ${phone1} verify ${line4} icon state as ${callAppearanceLocalHold}
     Then I want to make a two party call between ${phone6} and ${phone1} using ${offHook}
     Then On ${phone1} verify ${line5} icon state as ${callAppearanceIncoming}
     Then verify the led state of ${line5} as ${blink} on ${phone1}
     Then answer the call on ${phone1} using ${softKey}
     Then On ${phone1} verify ${line5} icon state as ${callAppearanceActive}
     Then verify audio path between ${phone1} and ${phone6}
     Then disconnect the call from ${phone6}
     Then disconnect the call from ${phone2}
     Then disconnect the call from ${phone3}
     Then disconnect the call from ${phone4}
     And disconnect the call from ${phone5}

752248: Answer call via handset while focused call on Hold
    [Tags]    Owner:Ram    Reviewer:    Call   notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Answer the call on ${phone2} using ${offHook}
    Then on ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${offHook}
    Then on ${phone1} verify ${line2} icon state as ${callAppearanceActive}
    Then verify audio path between ${phone1} and ${phone3}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${programKey3}
    Then Answer the call on ${phone4} using ${offHook}
    Then on ${phone1} verify ${line3} icon state as ${callAppearanceActive}
    Then verify audio path between ${phone1} and ${phone4}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify extension number of ${phone4} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone4}
    Then press hardkey as ${scrollUp} on ${phone1}
    Then press hardkey as ${scrollUp} on ${phone1}
    Then verify extension number of ${phone2} on ${phone1}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then on ${phone1} verify display message ${dial}
    Then press hardkey as ${goodBye} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

756191: TC06: Voicemail icons - Inbox
    [Tags]    Owner:Ram    Reviewer:    VM   notApplicableFor6910
    Given delete voicemail message on ${inbox} for ${phone1} using ${voicemailpassword}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then verify voicemail windows ${VMInbox} icons value as 0 on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

756192: TC07: Voicemail icons - Saved
    [Tags]    Owner:Ram    Reviewer:    VM   notApplicableFor6910
    Given delete voicemail message on ${save} for ${phone1} using ${voicemailpassword}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then verify voicemail windows ${VMSaved} icons value as 0 on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

756193: TC08: Voicemail icons - Deleted
    [Tags]    Owner:Ram    Reviewer:    VM   notApplicableFor6910
    Given delete voicemail message on ${delete} for ${phone1} using ${voicemailpassword}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then verify voicemail windows ${VMDeleted} icons value as 0 on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

755811: Press Voicemail when Filter is open in Call History
    [Tags]    Owner:Ram    Reviewer:    VM   notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offhook}
    Then disconnect the call from ${phone2}
    Then press the call history button on ${phone1} and folder ${missed} and ${details}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone1}

752168: Pressing Conf. on IDLE 69xx phone(s) dials conference extension
     [Tags]    Owner:Ram    Reviewer:    UCB
     Given on ${phone1} press ${softKey} ${bottomKey3} for 1 times
     Then on ${phone1} dial number ${accessCode}
     Then On ${phone1} verify the softkeys in ${talk}
     And disconnect the call from ${phone1}

754988: TC003 Holding whisper call
    [Tags]   Owner:Ram    Reviewer:Vikhyat    whisperCall
    Given I want to use fac ${whisperPageFAC} on ${phone1} to ${phone2}
    Then I want to verify on ${phone2} negative display message ${transfer}
    Then I want to verify on ${phone2} negative display message ${conference}
    Then verify the led state of speaker as ${on} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify display message Hold not permitted on this call
    And disconnect the call from ${phone1}
	
751772: TC003 when "active" calls goes disconnected while phone is having second incoming call
    [Tags] 	  owner:Ram    Reviewer:     callWaitingTone
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify CallWaiting tone is played on ${phone1} #check for callwaiting tone
    Then disconnect the call from ${phone1}
    Then Verify Ring tone is played on ${phone1} #check for ring tone
    And disconnect the call from ${phone1}

751773: TC004 When "active" calls goes on hold while phone is having second incoming call
    [Tags] 	  owner:Ram    Reviewer:     callWaitingTone
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify CallWaiting tone is played on ${phone1} #check for callwaiting tone
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Verify CallWaiting is not played on ${phone1} #check for callwaiting tone
    And disconnect the call from ${phone1}

751770: TC001 On Active call make one more incoming call
    [Tags] 	  owner:Ram    Reviewer:     callWaitingTone
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify CallWaiting tone is played on ${phone1} #check for callwaiting tone
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

139459: Torture Test - Make Me Conference Hold Test 3
    [Tags]    Owner:Surender    Reviewer:self   Torturetest    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${offHook}
    Given I want to make a two party call between ${phone1} and ${phone4} using ${programKey3}
    Then Answer the call on ${phone4} using ${offHook}
    When The ${phone1} Merged ${phone2} and ${phone3} and ${phone4} using Softkey3
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone3} on ${hold}
    Then Put the linekey ${line1} of ${phone4} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone3} on ${unhold}
    Then Put the linekey ${line1} of ${phone4} on ${unhold}
    Then Check Connection and disconnect the ${phone3}
    Then Check Connection and disconnect the ${phone2}
    And Check Connection and disconnect the ${phone1}

139462: Torture Test - Make Me Conference Hold Test 6
    [Tags]    Owner:Surender    Reviewer:Self   Torturetest    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${offHook}
    Given I want to make a two party call between ${phone1} and ${phone4} using ${programKey3}
    Then Answer the call on ${phone4} using ${offHook}
    Then The ${phone1} Merged ${phone2} and ${phone3} and ${phone4} using Softkey3
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Put the linekey ${line1} of ${phone4} on ${hold}
    Then Put the linekey ${line1} of ${phone3} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone3} on ${unhold}
    Then Put the linekey ${line1} of ${phone4} on ${unhold}
    Then Check Connection and disconnect the ${phone1}
    Then Check Connection and disconnect the ${phone2}
    And Check Connection and disconnect the ${phone3}

145857:CA status When call state is idle
    [Tags]    Owner:Surender    Reviewer:Self   CAidle
    When Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify the line state as ${IdleState} on ${phone1}
    And On ${phone1} verify display message ${pickUp}

145861:CA status When the call state is active
    [Tags]    Owner:Surender    Reviewer:Self   CAstatus
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    And Disconnect the call from ${phone1}

126833:With idle phone, answer incoming call from another phone caller
     [Tags]    Owner:Surender    Reviewer:Self   idle
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    And Disconnect the call from ${phone2}

126834:With idle phone, answer incoming call from SIP caller
     [Tags]    Owner:Surender    Reviewer:Self   idle
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    And Disconnect the call from ${phone2}

138968:CAS Caller ID strings - Caller ID Blocked
     [Tags]    Owner:Surender    Reviewer:Self   CallerId
    Given I want to use fac ${privateCall} on ${phone1} to ${phone2}
    Then On ${phone2} verify display message ${callerId_blocked}
    Then disconnect the call from ${phone1}
    Then Press the call history button on ${phone2} and folder ${missed} and ${nothing}
    And On ${phone2} verify display message ${callerId_blocked}

126841: place a call to a phone user, but hang up before it is answered
    [Tags]    Owner:Surender    Reviewer:Self    hangup
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    And Verify the line state as ${IdleState} on ${phone2}

139491: Mesh to Make Me Conference; press Call History or Directory
    [Tags]    Owner:Surender    Reviewer:Self    conference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    When on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then On ${phone1} display verify ${conferenceDisplay}
    Then On ${phone1} press directory and ${dial} of ${phone4}
    Then Answer the call on ${phone4} using ${offHook}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone4} verify display message ${conference}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}

139457: Torture Test - Make Me Conference Hold Test 1
    [Tags]    Owner:Surender    Reviewer:Self    Torture Test    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${offHook}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${programKey3}
    Then Answer the call on ${phone4} using ${offHook}
    Then The ${phone1} Merged ${phone2} and ${phone3} and ${phone4} using Softkey3
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Put the linekey ${line1} of ${phone3} on ${hold}
    Then Put the linekey ${line1} of ${phone3} on ${unhold}
    Then Put the linekey ${line1} of ${phone4} on ${hold}
    Then Put the linekey ${line1} of ${phone4} on ${unhold}
    Then Check Connection and disconnect the ${phone1}
    Then Check Connection and disconnect the ${phone2}
    And Check Connection and disconnect the ${phone3}

139465:Consult Make me Conference call between 4 parties
    [Tags]    Owner:Surender    Reviewer:Self   ConferenceCall    0001
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Add the ${phone4} in 4 parties conference call on ${phone3}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Check Connection and disconnect the ${phone1}
    Then Check Connection and disconnect the ${phone2}
    Then Check Connection and disconnect the ${phone3}

137788:Make a call (two way audio) using handset button as hookswitch
    [Tags]    Owner:Surender    Reviewer:Self   hookswitch    0001
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    When Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone1}

145705: Press # or Voicemail button on the first ring
    [Tags]    Owner:Surender    Reviewer:Self   Voicemail    0001
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    When Press hardkey as ${voicemail} on ${phone2}
    Then On ${phone1} verify display message ${displayVoiceMail}
    And Check Connection and disconnect the ${phone1}

126866: Answer incoming call via audio path buttons while there is existing active call
    [Tags]    Owner:Surender    Reviewer:Self   Speaker    0001    126866
    Given Press hookMode ${offHook} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify the Caller id on ${phone3} and ${phone1} display
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Press hardkey as ${handsFree} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${speaker} as ${on} on ${phone1}
    And Check Connection and disconnect the ${phone1}

126870:Main screen prompt for an incoming call
    [Tags]    Owner:Surender    Reviewer:Self   screen    0001
    Given Press hookMode ${offHook} on phone ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line2} as blink on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}

139464: Blind Make me Conference call between 4 parties
    [Tags]    Owner:Surender    Reviewer:Self   Conference    0001
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    When Add the ${phone4} in 4 parties conference call on ${phone3}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Check Connection and disconnect the ${phone1}
    Then Check Connection and disconnect the ${phone2}
    Then Check Connection and disconnect the ${phone3}

139106:TC01-a:Move Voicemail to Saved folder
	[Tags]    Owner:Manoj    notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then On ${phone1} Press The Softkey ${save} In VoiceMailState
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} verify the softkeys in ${voicemailDisplay['saved']}

177469 : Verify Conf. softkey displays on IDLE 69xx phones
    [Tags]    Owner:Saurabh    Reviewer:Avishek    VerifySoftkey    0003
    Given On ${phone1} verify the softkeys in ${idle}

176690 : TC002 Drop and Leave in conference
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Conference    0003    notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${programKey1}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then On ${phone1} verify display message ${Drop}
    Then On ${phone1} verify display message ${Leave}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}

176908 : Drop from the conference list
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Conference    0003    notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${programKey1}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then On ${phone1} verify display message ${Drop}
    Then On ${phone1} verify display message ${Leave}
    Then on ${phone1} press the softkey ${drop} in ConferenceCallState
    Then On ${phone1} verify display message ${Transfer}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Disconnect the call from ${phone1}

188342: TC003 Check Directory_when searching
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    0004
    Given On ${phone1} verify directory with ${directoryAction['searchMultiple']} of ${phone2}
    Then On ${phone1} verify extension ext1 in directory
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify extension ext2 in directory
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify extension ext3 in directory
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify extension ext4 in directory
    Then Press hardkey as ${goodBye} on ${phone1}

188341: TC002 Check Directory contact for 'Copy' softkey
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    0004    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone4}
    Then On ${phone1} verify extension ext1 in directory
    Then I want to verify on ${phone1} negative display message ${copy}
    Then Press hardkey as ${goodBye} on ${phone1}

188343: TC004 Check Directory contact for 'Edit' softkey
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    0004    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone4}
    Then On ${phone1} verify extension ext1 in directory
    Then I want to verify on ${phone1} negative display message ${edit}
    Then Press hardkey as ${goodBye} on ${phone1}

188344: TC005 Check Directory contact for 'Speed' softkey
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    0004    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone4}
    Then On ${phone1} verify extension ext1 in directory
    Then I want to verify on ${phone1} negative display message ${speed}
    Then Press hardkey as ${goodBye} on ${phone1}

188188: Check the directory folders
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    0004    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['mainMenu']} of ${none}
    Then I want to verify on ${phone1} negative display message ${local}
    Then Press hardkey as ${goodBye} on ${phone1}

158339: TC050-From Directory, select a user lift HANDSET
    [Tags]    Owner:Saurabh    Reviewer: Avishek    Directory    0004
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Press hardkey as ${goodBye} on ${phone1}

158341: TC052-From Directory, select a user press SPEAKER button
    [Tags]    Owner:Saurabh    Reviewer: Avishek    Directory    000
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone4}
    Then Press hardkey as ${handsFree} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone4} display
    Then Press hardkey as ${goodBye} on ${phone1}

127645: TC07: The transfer screen should display Transfer
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Answer the call on ${phone2} using ${programKey1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} verify display message ${transfer}
    And Disconnect the call from ${phone2}

297470: TC015 Blind Conference to Phone
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Conference
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${programKey1}
	Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then Disconnect the call from ${phone1}
	And Disconnect the call from ${phone2}

176697: TC009 Make a new call during 3 way conference
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Conference
	Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Answer the call on ${phone1} using ${programKey1}
	Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
	Then I want to press line key ${programkey2} on phone ${phone1}
	Then On the ${phone1} verify softkeys in different state using ${dial}
	Then Press hardkey as ${goodBye} on ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

158289: TC001 Open Micloud Directory
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone1}
    Then On ${phone1} verify extension ext1 in directory
    And Press hardkey as ${goodBye} on ${phone1}

158292: TC004 DUT crashes when attempt to dial extension from Directory list
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['searchWithDial']} of ${phone2}
    Then Verify extension Number of ${phone2} on ${phone1}
    When Verify ringing state on ${phone1} and ${phone2}
    And Disconnect the call from ${phone1}

158314: TC026 From Directory,use close to exit
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone1}
    Then On ${phone1} verify extension ext1 in directory
    Then On ${phone1} verify directory with ${directoryAction['close']} of ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

158315: TC026 Exiting from directory to Home screen
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone1}
    Then On ${phone1} verify extension ext1 in directory
    Then On ${phone1} verify directory with ${directoryAction['close']} of ${phone1}
    Then On ${phone1} verify directory with ${directoryAction['quit']} of ${phone1}
    And On the ${phone1} verify softkeys in different state using ${idle}

195203: TC054 Directory search screen in 6930/6940
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

158332: TC043 Directory contacts detail view
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone1}
    Then On ${phone1} verify extension ext1 in directory
    And Press hardkey as ${goodBye} on ${phone1}

188347: TC008 Press 'Quit'
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['mainMenu']} of ${phone1}
    Then On ${phone1} verify directory with ${directoryAction['quit']} of ${phone1}
    And On the ${phone1} verify softkeys in different state using ${idle}

188348: TC009 Press ' Details'
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then On ${phone1} verify directory with ${directoryAction['close']} of ${phone1}
    And On ${phone1} verify directory with ${directoryAction['quit']} of ${phone1}

158319: TC030-Select a Directory user, press Dial
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['searchWithDial']} of ${phone2}
    When Verify ringing state on ${phone1} and ${phone2}
    Then Disconnect the call from ${phone1}
    And On the ${phone1} verify softkeys in different state using ${idle}

185026: TC001 Dialing a whisper page
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    onlyApplicableFor6930   notApplicableFor6910
    Then On ${phone1} verify directory with ${directoryAction['whisper']} of ${phone2}
    Then On ${phone2} verify display message ${drop}
    And Press hardkey as ${goodBye} on ${phone1}

158333: TC044-Directory filter
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['searchInvalid']} of ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

195204: TC053 No Reset key -Directory search screen
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910    onlyApplicableFor6920
    Given On ${phone1} verify directory with ${directoryAction['reset']} of ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

158296: TC008 Numeric search
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Numeric    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['searchMultiple']} of ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify extension ext2 in directory
	And Press hardkey as ${goodBye} on ${phone1}

158304: TC016 UI List crash
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910
    Given On ${phone1} verify directory with ${directoryAction['mainMenu']} of ${none}
    Then on ${phone1} Press ${hardKey} ${ScrollDown} for 1 times
    Then on ${phone1} Press ${hardKey} ${ScrollUp} for 1 times
    Then on ${phone1} Press ${hardKey} ${ScrollLeft} for 1 times
    Then on ${phone1} Press ${hardKey} ${ScrollRight} for 1 times
    Then On ${phone1} verify display message ${directory}
    Then On ${phone1} verify display message ${enterprise}
    Then On ${phone1} verify display message ${quit}
    And Press hardkey as ${goodBye} on ${phone1}

158328: TC039 From Phone press Directory button then Exit
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Num    notApplicableFor6910
    Given On ${phone1} navigate to ${directoryFormat} settings
    Then Change the directory format to ${lastFirst} on ${phone1}
    Given On ${phone1} verify directory with ${directoryAction['mainMenu']} of ${none}
	And Press hardkey as ${goodBye} on ${phone1}

158334 : TC045-Incoming call while in Directory - pick up the handset
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['default']} of ${phone4}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    Then Answer the call on ${phone1} using ${programKey1}
    Then On ${phone1} verify the softkeys in Talk
    And Disconnect the call from ${phone2}

188565 : Dial from Directory - lift Handset
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then Answer the call on ${phone2} using ${programKey1}
    And Disconnect the call from ${phone2}

138911 : Navigate to History-All Press and Hold History
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory
    Given Press the call history button on ${phone1} and folder ${All} and ${nothing}
    Then on ${phone1} Press ${hardKey} ${CallersList} for 1 times
    Then Verify extension ${number} of ${phone1} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

138765 : Call History delete does not erase entry
    [Tags]    Owner:Saurabh    Reviewer:Avishek    Directory    notApplicableFor6910
	Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    Then Disconnect the call from ${phone2}
    Given I want to make a two party call between ${phone3} and ${phone1} using ${programKey1}
    Then Disconnect the call from ${phone3}
    Then Press the call history button on ${phone1} and folder ${All} and ${delete}
    Then Press softkey ${details} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

557998: TC01: Verify that call can be unparked successfully while there is held call
    [Tags]    Owner:Vikhyat    Reviewer:Ram    notApplicableFor6910    vikh
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${park}
    Then I want to unPark the call from ${phone3} on ${phone1} using ${default} and ${dial}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}

561605: TC004: Phone receives call while VM detail screen is open
    [Tags]    Owner:Vikhyat    Reviewer:Ram    notApplicableFor6910    voicemail
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then On ${phone1} verify display message ${visualVoicemailScreen}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

754344: Monitoring the Intercom extension "Idle or Offering Call" DND is ON
    [Tags]    Owner:Vikhyat    Reviewer:    CHM    notApplicableFor6910
    Given On ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${always} in ${doNotDisturb}
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} press the softkey ${quit} in SettingState
    And On ${phone1} verify ${line1} icon state as ${callAppearanceDND}
    [Teardown]    Default Availability State

751537: Answer incoming call after lifting handset (dialing from Directory)
    [Tags]    Owner:Vikhyat    Reviewer:    answerCall
    Given On ${phone1} press directory and ${offHook} of ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

755765: Exit Call History; FIlter resets to All
    [Tags]    Owner:Vikhyat    Reviewer:    callHistory    notApplicableFor6910    Vikhyat08    31/01/2020
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Press hardkey as ${goodBye} on ${phone1}
    Given Press hardkey as ${callersList} on ${phone1}
    Then Verify ${callHistoryReceived} icons on ${phone1}
    Then Press hardkey as ${scrollUp} on ${phone1}
    Then Verify ${callHistoryOutgoing} icons on ${phone1}
    Then Press hardkey as ${scrollUp} on ${phone1}
    Then Verify ${callHistoryMissed} icons on ${phone1}
    Then Press hardkey as ${scrollUp} on ${phone1}
    Then Verify ${callHistoryAll} icons on ${phone1}
    Then On ${phone1} press the key ${quit} in state ${callHistory}
    Then Press hardkey as ${callersList} on ${phone1}
    Then On ${phone1} verify display message ${callHistory}
    Then Press the call history button on ${phone1} and folder ${all} and ${nothing}
    Then On ${phone1} verify display message ${phone2}
    Then On ${phone1} press the key ${quit} in state ${callHistory}

798581: Ping to invalid target (on phone)
    [Tags]    Owner:Vikhyat    Reviewer:    ping
    Given Go to ${ping} settings and enter invalid_ip on ${phone1}
    Then On ${phone1} verify display message ${invalidHostName}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Go to ${ping} settings and enter invalid_dns on ${phone1}
    Then I want to verify on ${phone1} negative display message ${numberOfPackets}
    Then Press hardkey as ${goodBye} on ${phone1}

755654: Placing a call exits to main screen (Hold)
    [Tags]    Owner:Vikhyat    Reviewer:    callHistory
    Given I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press the call history button on ${phone1} and folder ${missed} and ${dial}
    Then Verify ringing state on ${phone1} and ${phone3}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone2}

177419: Dialing from call history screen
   [Tags]    Owner:Avishek    Reviewer:Vikhyat    Transfer
   Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
   Then Verify ringing state on ${phone2} and ${phone1}
   Then Disconnect the call from ${phone2}
   Then Press the call history button on ${phone1} and folder ${all} and ${dial}
   Then Verify ringing state on ${phone1} and ${phone2}
   Then Disconnect the call from ${phone1}
   And On ${phone1} verify the softkeys in ${idleState}

177416 : Exiting from call history screen
   [Tags]    Owner:Avishek    Reviewer:Vikhyat
   Given Press the call history button on ${phone1} and folder ${All} and ${quit}
   Then Press the call history button on ${phone1} and folder ${All} and ${goodBye}
   And On ${phone1} verify the softkeys in ${idleState}

178565: Phone registered - Assign User - Goodbye
   [Tags]    Owner:Avishek    Reviewer:Vikhyat    assignUser    notApplicableFor6910
   [Setup]    Assign Extension Custom Setup
   Given Go to assign user on ${phone1} and ${goodBye} in ${assigned}
   And On ${phone1} verify the softkeys in ${idleState}
   [Teardown]    Assign Extension Custom Teardown

127701: DIversion Transfer - Transfer incoming call with held call on phone
  [Tags]    Owner:Avishek    Reviewer:    Transfer    0002
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Answer the call on ${phone1} using ${programKey1}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Put the linekey ${line1} of ${phone1} on ${hold}
  Then I want to make a two party call between ${phone3} and ${phone1} using ${programKey1}
  Then Initiate Transfer on ${phone1} to ${phone4} using ${consult}
  Then verify the led state of ${line1} as ${blink} on ${phone4}
  Then verify the led state of ${line1} as ${blink} on ${phone1}
  Then Disconnect the call from ${phone3}
  Then Put the linekey ${line1} of ${phone1} on ${unHold}
  Then Disconnect the call from ${phone1}

127616: receive a blind transfer (transfer target)
   [Tags]    Owner:Avishek    Reviewer:Vikhyat    Transfer
   Given I want to make a two party call between ${phone3} and ${phone2} using ${programKey1}
   Then Initiate Transfer on ${phone2} to ${phone1} using ${consult}
   Then Verify extension ${number} of ${phone1} on ${phone3}
   Then Answer the call on ${phone1} using ${loudSpeaker}
   Then Verify audio path between ${phone3} and ${phone1}
   Then Disconnect the call from ${phone1}

558161: Auto-Transfer - Blind transfer
   [Tags]    Owner:Avishek    29/07/19    0010
   Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
   Then Answer the call on ${phone2} using ${offHook}
   Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
   Then Answer the call on ${phone3} using ${loudspeaker}
   And Disconnect the call from ${phone2}

558162 : Auto-Transfer - Cancel transfer before timeout
   [Tags]    Owner:Avishek    Reviewer:Vikhyat    30/07/19    0010
   Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
   Then Answer the call on ${phone1} using ${offHook}
   Then Initiate Transfer on ${phone1} to ${phone3} using ${cancel}
   Then Verify the led state of ${line1} as ${blink} on ${phone1}
   And Disconnect the call from ${phone2}

558163 : Auto-Transfer - Consult transfer
   [Tags]    Owner:Avishek    Reviewer:Vikhyat    30/07/19    0010
   Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
   Then Answer the call on ${phone1} using ${offHook}
   Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
   Then Verify ringing state on ${phone2} and ${phone3}
   Then Disconnect the call from ${phone3}
   And Disconnect the call from ${phone2}

558203: Blind Transfer to invalid number using hangup
   [Tags]    Owner:Avishek    Reviewer:
   Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
   Then answer the call on ${phone1} using ${offHook}
   Then Verify audio path between ${phone1} and ${phone2}
   Then on ${phone1} press the softkey ${transfer} in answerstate
   Then On ${phone1} enter number ${invalidNumber}
   Then On ${phone1} Wait for 3 seconds
   Then Press hardkey as ${goodBye} on ${phone1}
   Then Verify the led state of ${line1} as ${blink} on ${phone1}
   Then Disconnect the call from ${phone2}

127589: TC05: Cancel transfer from Consult screen while ringing
  [Tags]    Owner:Avishek    Reviewer:    Transfer
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${programKey1}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then on ${phone1} press the softkey ${cancel} in DialingState
  Then Put the linekey ${line1} of ${phone1} on ${unhold}
  And Disconnect the call from ${phone2}

127750 : Transferee hangs up while Consult is ringing
  [Tags]    Owner:Avishek    Reviewer:    Transfer
  Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
  Then Answer the call on ${phone2} using ${programKey1}
  Then initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then Disconnect the call from ${phone2}
  When Verify ringing state on ${phone1} and ${phone3}
  Then Verify the led state of ${line1} as ${off} on ${phone2}
  Then Disconnect the call from ${phone1}


127738 : Consultative Transfer - Transfer fixed key during consult
  [Tags]    Owner:Avishek    Reviewer:    Transfer
  Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
  When Verify ringing state on ${phone1} and ${phone2}
  Then Answer the call on ${phone2} using ${programKey1}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
  Then Disconnect the call from ${phone2}
  Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
  When Verify ringing state on ${phone1} and ${phone2}
  Then Answer the call on ${phone2} using ${programKey1}
  Then on ${phone1} press the softkey ${Transfer} in AnswerState
  Then On ${phone1} Wait for 5 seconds
  Then on ${phone1} press the softkey ${Transfer} in AnswerState
  Then Disconnect the call from ${phone2}
  Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
  When Verify ringing state on ${phone1} and ${phone2}
  Then Answer the call on ${phone2} using ${programKey1}
  Then initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then On ${phone1} Wait for 25 seconds
  Then On ${phone1} verify display message ${displayVoiceMail}
  Then on ${phone1} press the softkey ${Transfer} in AnswerState
  Then On ${phone2} verify display message ${displayVoiceMail}
  Then Disconnect the call from ${phone2}


176700 : TC012 Pressing Leave DUT while in conference
  [Tags]    Owner:Avishek    Reviewer:    conference
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${programKey1}
  Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${ConsultiveConference}
  Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
  Then on ${phone1} press the softkey ${Leave} in ConferenceCallState
  Then Disconnect the call from ${phone2}

177809: TC05: Verify that active call can be parked via park call timeout dial
  [Tags]    Owner:Avishek    Reviewer:    callPark    timeout    notApplicableFor6910
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${programKey1}
  Then Verify audio path between ${phone1} and ${phone2}
  Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${timeout}
  Then Verify the Caller id on ${phone2} and ${phone3} display
  Then Disconnect the call from ${phone2}

177484: TC06: Unpark - 1 call parked at the extension
  [Tags]    Owner:Avishek    Reviewer:    unPark    notApplicableFor6910
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${programKey1}
  Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
  Then I want to unPark the call from ${phone3} on ${phone1} using ${default} and ${dial}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Disconnect the call from ${phone1}

127506 : Transfer incoming call (internalexternal)
  [Tags]    Owner:Avishek    Reviewer:    Transfer
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  When Verify ringing state on ${phone2} and ${phone1}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
  Then Disconnect the call from ${phone2}

139445 : Caller ID displays when call is transferred(consult)
  [Tags]    Owner:Avishek    Reviewer:    Transfer
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then on ${phone3} press the softkey ${ToVm} in RingingState
  Then On ${phone1} verify display message ${displayVoiceMail}
  Then Disconnect the call from ${phone2}
  Then Disconnect the call from ${phone1}

177461 : Add a new missed call
  [Tags]    Owner:Avishek    Reviewer:
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Then Press the call history button on ${phone1} and folder ${missed} and ${details}
  Then Verify extension ${number} of ${phone2} on ${phone1}

138796: Lift Handset while in Call History
    [Tags]    Owner:Avishek    Reviewer:Vikhyat    CallHistory
    Given Press the call history button on ${phone1} and folder ${all} and ${offHook}
    Then Verify ringing state on ${phone1} and ${phone2}
    And Disconnect the call from ${phone1}

188584 : Options in Call History Panel
    [Tags]    Owner:Avishek
    Given Press the call history button on ${phone1} and folder ${All} and ${goodBye}

193473 : Details View - Outgoing Call
  [Tags]    Owner:Avishek
  Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
  Then Disconnect the call from ${phone1}
  Then Press the call history button on ${phone1} and folder ${Outgoing} and ${details}
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Then Press hardkey as ${goodBye} on ${phone1}

193474 : Details View - Received Call
  [Tags]    Owner:Avishek
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then Disconnect the call from ${phone2}
  Then Press the call history button on ${phone1} and folder ${Received} and ${details}
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Then Press hardkey as ${goodBye} on ${phone1}

138849 : Missed call indicator after phone reboots
    [Tags]   Reboot    Owner:Avishek
  Given Press the call history button on ${phone1} and folder ${Missed} and ${goodBye}
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Then Reboot ${phone1}
  Then On ${phone1} verify display message Missed Calls
  Then Press the call history button on ${phone1} and folder ${Missed} and ${details}
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Then Press hardkey as ${goodBye} on ${phone1}

127735 : Consultative Transfer - CANCEL
  [Tags]    Cancel    Owner:Avishek
  Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
  Then Answer the call on ${phone2} using ${loudspeaker}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
  Then Answer the call on ${phone3} using ${loudspeaker}
  Then Initiate Transfer on ${phone3} to ${phone4} using ${timeout}
  Then Answer the call on ${phone4} using ${loudspeaker}
  Then on ${phone1} press the softkey ${drop} in TransferState
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Then Verify extension ${number} of ${phone4} on ${phone3}
  Then Disconnect the call from ${phone2}
  Then Disconnect the call from ${phone3}

127742 : Consultative Transfer - UnHold after consult is connected
  [Tags]    Owner:Avishek
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then Answer the call on ${phone3} using ${loudspeaker}
  Then On ${phone1} Wait for 5 seconds
  Then I want to press line key ${programKey1} on phone ${phone1}
  Then on ${phone1} Press ${hardkey} ${ScrollDown} for 1 times
  Then on ${phone1} press the softkey ${pickup} in TransferState
  Then on ${phone1} press the softkey ${transfer} in TransferState
  Then Disconnect the call from ${phone2}

140119 : Boot phone with no issues
    [Tags]    restart    Owner:Avishek
    Given Reboot ${phone1}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    And Disconnect the call from ${phone2}

176606 : Incoming call answered and put on hold while in active call
  [Tags]    Owner:Avishek
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then Verify audio path between ${phone1} and ${phone2}
  Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${programKey2}
  Then Verify the led state of ${line1} as ${blink} on ${phone1}
  Then Disconnect the call from ${phone3}
  Then Disconnect the call from ${phone2}

175599 : Place a new call while one or more calls on hold
  [Tags]    Owner:Avishek
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
  When Verify ringing state on ${phone1} and ${phone3}
  Then Verify the led state of ${line1} as ${blink} on ${phone1}
  Then Answer the call on ${phone3} using ${loudspeaker}
  Then Disconnect the call from ${phone3}
  Then Verify the led state of ${line1} as ${blink} on ${phone1}
  Then Put the linekey ${Line1} of ${phone1} on ${UnHold}
  Then Disconnect the call from ${phone1}

193472 : Details View - Missed Call
  [Tags]    Owner:Avishek

  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Then Press the call history button on ${phone1} and folder ${Missed} and ${details}
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Then Press hardkey as ${goodBye} on ${phone1}

127617 : receive a blind transfer (transfer target) negative Test case
  [Tags]    Owner:Avishek    Reviewer:    Transfer
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then on ${phone3} press the softkey ${ToVm} in RingingState
  Then On ${phone2} verify display message ${displayVoiceMail}
  Then Disconnect the call from ${phone2}

138848 : Missed call indicator
  [Tags]    Owner:Avishek    Reviewer:    CallHistory    count

  Given Press the call history button on ${phone1} and folder ${Missed} and ${goodBye}
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Then On ${phone1} verify display message 2
  Press the call history button on ${phone1} and folder ${Missed} and ${details}
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Press hardkey as ${goodBye} on ${phone1}

127700:Diversion Transfer - Transfer incoming call with active call on phone
    [Tags]    0001    Owner:Avishek    Avishek01
    Given I want to make a two party call between ${phone1} and ${phone2} using ProgramKey1
    Then Answer the call on ${phone2} using Loudspeaker
    Then I want to make a two party call between ${phone3} and ${phone1} using ProgramKey1
    Then Answer the call on ${phone1} using ProgramKey2
    Then Transfer call from ${phone1} to ${phone4} using ${blindTransfer}
    Then Verify the led state of Line1 as ${blink} on ${phone1}


127755 : Consult call transferred while ringing
  [Tags]    Owner:Avishek    Reviewer:    Transfer    Passed
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    When Verify ringing state on ${phone2} and ${phone1}
    Then Answer the call on ${phone1} using ${programKey1}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Disconnect the call from ${phone3}


185018 : TC04: Verify that call can be unparked using DID
  [Tags]    Owner:Avishek    Reviewer:    unPark    notApplicableFor6910    0002
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${programKey1}
  Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
  Then I want to unPark the call from ${phone3} on ${phone1} using ${default} and ${dial}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Disconnect the call from ${phone1}

185017 : TC03: Verify that call can be unparked when using "#" to terminate digit collection #Marked Automated
    [Tags]    Owner:Avishek    Reviewer:    unPark    DigitTerminator    0002    notApplicableFor6910    Avishek04
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${programKey1}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
    Then I want to unPark the call from ${phone3} on ${phone1} using ${digitTerminator} and ${TerminatorString}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone1}

139879 : unpark - call history
    [Tags]    Owner:Avishek    Reviewer:    unPark    CallHistory    0002    notApplicableFor6910    Avishek05
    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey1}
    Then Disconnect the call from ${phone1}
    Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    Then Answer the call on ${phone1} using ${programKey1}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
    Then I want to unPark the call from ${phone3} on ${phone1} using ${CallHistory} and ${dial}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone1}

127509: Transfer incoming call with active call on phone
    [Tags]    Owner:Avishek    Reviewer:    Transfer    0002
    Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${programKey1}
    Then Initiate Transfer on ${phone1} to ${phone4} using ${consult}
    Then Answer the call on ${phone4} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone4}
    Then Disconnect the call from ${phone4}
    Then On ${phone1} verify display message ${Drop}
    And Disconnect the call from ${phone1}

127625 : Phone is the transferee in a blind transfer operation
  [Tags]    Owner:Avishek    Reviewer:    Transfer    0002
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then Verify audio path between ${phone1} and ${phone2}
  Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
  Then Verify audio path between ${phone2} and ${phone3}
  Then Disconnect the call from ${phone3}

177417 : Off hook handset while in call history screen
  [Tags]    Owner:Avishek    Reviewer:    CallHistory    0002
   Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
   Then Disconnect the call from ${phone2}
   Given Press the call history button on ${phone1} and folder ${missed} and ${offHook}
   Then Verify ringing state on ${phone1} and ${phone2}
   Then Disconnect the call from ${phone1}


138802 : Press Speaker in Call history
  [Tags]    Owner:Avishek    Reviewer:    CallHistory    0003
  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Given Press the call history button on ${phone1} and folder ${All} and ${loudspeaker}
  Then Verify ringing state on ${phone1} and ${phone2}
  Then Disconnect the call from ${phone1}


177411 : Call History - Delete
  [Tags]    Owner:Avishek    0003    notApplicableFor6910    Avishek12

  Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone2}
  Given I want to make a two party call between ${phone3} and ${phone1} using ${programKey1}
  Then Disconnect the call from ${phone3}
  Then Press the call history button on ${phone1} and folder ${All} and ${delete}
  Then Press softkey ${details} on ${phone1}
  Then Verify extension ${number} of ${phone2} on ${phone1}
  Then Press hardkey as ${goodBye} on ${phone1}

193475 : Open Call History and hit Goodbye
  [Tags]    Owner:Avishek    CallHistory    0003

  Given Press the call history button on ${phone1} and folder ${All} and ${goodBye}
  And On ${phone1} verify the softkeys in Idle


127795 : UnHold call after consult is connected
  [Tags]    check    Owner:Avishek    0003
  Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
  Then Answer the call on ${phone1} using ${loudspeaker}
  Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
  Then Answer the call on ${phone3} using ${loudspeaker}
  Then On ${phone1} Wait for 5 seconds
  Then I want to press line key ${programKey1} on phone ${phone1}
  Then Verify audio path between ${phone1} and ${phone2}
  Then on ${phone1} Press ${hardkey} ${ScrollDown} for 1 times
  Then on ${phone1} press the softkey ${pickup} in TransferState
  Then On ${phone1} verify display message ${Drop}
  Then on ${phone1} press the softkey ${transfer} in TransferState
  Then Disconnect the call from ${phone2}

147961 : Assign-Unassign multiple times at the same time
  [Tags]    Owner:Avishek    assign    Reviewer:Surender    assignUser    notApplicableFor6910
  Given Go to assign user on ${phone1} and ${phone3} in ${assigned}
  Then Verify extension ${number} of ${phone3} on ${phone1}
  Then Go to assign user on ${phone4} and ${phone3} in ${assigned}
  Then Verify extension ${number} of ${phone3} on ${phone4}
  Then Go to assign user on ${phone4} and ${phone4} in ${unAssigned}
  Then Go to assign user on ${phone1} and ${phone1} in ${unAssigned}
  Then Verify extension ${number} of ${phone3} on ${phone3}
  Then Verify extension ${number} of ${phone4} on ${phone4}
  Then Verify extension ${number} of ${phone1} on ${phone1}

561565 : TC01-a: in FORWARD, lift handset or Press Speaker or Headset button
   [Tags]    Owner:Avishek    notApplicableFor6910
   Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
   Leave voicemail message from ${phone2} on ${phone1}
   Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
   Then Press hardkey as ${scrollRight} on ${phone1}
   Then on ${phone1} press the softkey ${forward} in VoiceMailState
   Then on ${phone1} press the softkey ${edit} in VoiceMailState
   Then on ${phone1} enter number ${phone2}
   press hardkey as ${handsFree} on ${phone1}

561566 :TC01-b: in FORWARD, play the message. Lift handset or Press Speaker or Headset button
   [Tags]    Owner:Avishek    Reviewer:Surender    notApplicableFor6910    forwardPlay    Avishek20
   Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
   Then Leave voicemail message from ${phone2} on ${phone1}
   Then Record a reply message for ${phone2} on ${phone1} and ${play}
   And verify the led state of speaker as ${on} on ${phone1}
   And press hookmode ${offHook} on phone ${phone1}
   And verify the led state of speaker as ${off} on ${phone1}
   And press hardkey as ${goodBye} on ${phone1}
   Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}


558325 : Recursive Transfer - Blind Transfer or wait for timeout
   [Tags]    Owner:Avishek    recursiveTransfer
   Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
   Then answer the call on ${phone1} using ${loudSpeaker}
   initiate transfer on ${phone1} to ${phone3} using ${timeout}
   Then Answer the call on ${phone3} using ${loudSpeaker}
   Then Transfer call from ${phone3} to ${phone4} using ${blindTransfer}
   Then Answer the call on ${phone4} using ${loudSpeaker}
   on ${phone1} press the softkey ${transfer} in TransferState
   verify the caller id on ${phone2} and ${phone4} display
   Then Disconnect the call from ${phone2}

558327 :Recursive Transfer - Press Consult or wait for timeout
   [Tags]    Owner:Avishek    recursiveTransfer
   Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
   Then answer the call on ${phone1} using ${loudSpeaker}
   initiate transfer on ${phone1} to ${phone3} using ${timeout}
   Then Answer the call on ${phone3} using ${loudSpeaker}
   Then Transfer call from ${phone3} to ${phone4} using ${consultiveTransfer}
   on ${phone1} press the softkey ${transfer} in TransferState
   verify the caller id on ${phone2} and ${phone4} display
   Then Disconnect the call from ${phone2}

558195 : TC04: Blind Transfer call with another call on the phone
   [Tags]    Owner:Avishek
   Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
   Then answer the call on ${phone1} using ${loudSpeaker}
   Given I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
   Then answer the call on ${phone1} using ${programKey2}
   transfer call from ${phone1} to ${phone4} using ${blindTransfer}
   Then Disconnect the call from ${phone4}
   Then Verify the led state of Line1 as blink on ${phone1}
   Then Disconnect the call from ${phone2}

560626: Call Handling mode(CHM) options set to In a Meeting
   [Tags]    Owner:Avishek    Reviewer:    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${Always} in ${In a meeting}
   Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
   and i want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
   On ${phone2} verify display message ${voicemail}
   disconnect the call from ${phone2}
   [Teardown]    Default Availability State

560761 : TC022 From Directory, use 5 way nav to right-arrow to display the contacts detailed view
   [Tags]    Owner:Avishek    directoryDetails    notApplicableFor6910
   Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone4}

557871: Auto Unmute when there are N locally held calls
   [Tags]    Owner:Avishek    Avishek30
   and i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
   then answer the call on ${phone1} using ${loudspeaker}
   and i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
   then answer the call on ${phone1} using ${programKey2}
   and i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
   then answer the call on ${phone1} using ${programKey3}
   and put the linekey ${line3} of ${phone1} on ${hold}
   and verify the led state of ${line3} as ${blink} on ${phone1}
   press hardkey as ${mute} on ${phone1}
   and verify the led state of mute as ${off} on ${phone1}
   disconnect the call from ${phone1}
   and verify the led state of ${line1} as ${blink} on ${phone1}
   and verify the led state of ${line2} as ${blink} on ${phone1}
   and verify the led state of ${line3} as ${blink} on ${phone1}
   disconnect the call from ${phone4}
   disconnect the call from ${phone3}
   disconnect the call from ${phone2}

560835: Dial from Directory - Headset hook button
   [Tags]    Owner:Avishek    recursiveTransfer    Avishek23
   Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
   Then press hardkey as ${offHook} on ${phone1}
   Then verify the caller id on ${phone1} and ${phone2} display
   And disconnect the call from ${phone2}

561536: TC07: Phone crashes and reboots after pressing VM button.
   [Tags]    Owner:Avishek    Avishek24    voiceMailCrash    notApplicableFor6910
   Login into voicemailBox for ${phone1} using ${invalidPassword}
   press hardkey as ${voiceMail} on ${phone1}
   when on ${phone1} wait for 3 seconds
   given on ${phone1} verify display message Pickup
   given on ${phone1} verify display message UnPark
   press hardkey as Menu on ${phone1}
   Then on ${phone1} dial number ${invalidPassword}
   and on ${phone1} press ${softkey} ${bottomKey1} for 1 times
   given on ${phone1} verify display message Error
   press hardkey as ${voiceMail} on ${phone1}
   given on ${phone1} verify display message Voicemail
   Then on ${phone1} dial number ${invalidPassword}
   and on ${phone1} press ${softkey} ${bottomKey1} for 1 times
   given on ${phone1} verify display message Error
   press hardkey as ${goodBye} on ${phone1}

560492: CAS Caller ID strings - "Caller ID Unknown"
   [Tags]    Owner:Avishek    Reviewer:    assignUser    casUnknown
   [Setup]    Assign Extension Custom Setup
   on ${phone2} navigate to Unassign user settings
   I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
   disconnect the call from ${phone2}
   then press the call history button on ${phone1} and folder ${missed} and ${nothing}
   given on ${phone1} verify display message Unknown
   press hardkey as ${goodBye} on ${phone1}
   then on ${phone2} wait for 2 seconds
#   Given Go to assign user on ${phone2} and ${phone2} in ${UnAssigned}
   [Teardown]    Assign Extension Custom Teardown

557524: Mesh to Make Me Conference; MERGE
	[Tags]    Owner:Avishek    Avishek26    Merge    notApplicableFor6910
	Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Answer the call on ${phone2} using ${loudspeaker}
	Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
	Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then i want to make a two party call between ${phone1} and ${phone4} using ${programKey2}
	Then answer the call on ${phone4} using ${loudspeaker}
	Then verify audio path between ${phone1} and ${phone4}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then on ${phone1} press the softkey ${Merge} in AnswerState
	Then on ${phone1} verify display message ${Show}
	Then disconnect the call from ${phone1}
	Then disconnect the call from ${phone3}
	And disconnect the call from ${phone4}

560943: Scroll to an extension in call history; press History
    [Tags]    Owner:Avishek    Reviewer:Vikhyat    callHistory
    Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    Then Disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${All} and ${details}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${All} and ${Nothing}
    Then press hardkey as ${callersList} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then I want to verify on ${phone1} negative display message Call History
    And On ${phone1} verify the softkeys in ${idleState}

752212: Incoming call hangs up, while first call on hold and dialing another call
	[Tags]    Owner:Avishek    03/02/2020    cc    checkneed    11
	Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
	Then answer the call on ${phone2} using ${programKey1}
    Then put the linekey ${line1} of ${phone1} on ${hold}
	Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
	Then i want to press line key ${programKey2} on phone ${phone1}
	Then On ${phone1} dial partial number of ${phone3} with ${firstTwo}
	Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
	Then Verify the led state of ${Line1} as ${blink} on ${phone1}
	Then Verify the Caller id on ${phone1} and ${phone3} display
	Then Verify the led state of ${Line3} as ${blink} on ${phone1}
	Then disconnect the call from ${phone3}
	Then On ${phone1} dial partial number of ${phone3} with ${lastTwo}
	Then Verify the Caller id on ${phone1} and ${phone3} display
	Then Verify the led state of ${Line1} as ${blink} on ${phone1}
	Then disconnect the call from ${phone3}
	And disconnect the call from ${phone2}

755651: Incoming calls offered behind Call History screen
	[Tags]    Owner:Avishek    03/02/2020    cc    checkneed    cc
	press hardkey as ${CallersList} on ${phone1}
	when on ${phone1} wait for 3 seconds
	I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
	verify the caller id on ${phone1} and ${phone2} display
	disconnect the call from ${phone2}

	I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
	press hardkey as ${CallersList} on ${phone1}
	when on ${phone1} wait for 5 seconds
	press hookmode ${OffHook} on phone ${phone1}
	when on ${phone1} wait for 2 seconds
	Verify the led state of ${line1} as ${on} on ${phone1}
	verify the caller id on ${phone1} and ${phone2} display
	disconnect the call from ${phone2}

	I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
	press hardkey as ${CallersList} on ${phone1}
	when on ${phone1} wait for 3 seconds
	and i want to press line key ${line1} on phone ${phone1}
	Then I want to verify on ${phone1} negative display message ${phone2}
	Verify the led state of ${line1} as ${on} on ${phone1}
	disconnect the call from ${phone2}
	press hardkey as ${goodBye} on ${phone1}

757344 : CHM "Do not Disturb" Call Forward Mode - Never
	[Tags]    Owner:Avishek    Reviewer:    CHM    notApplicableFor6910
	Modify call handler mode on ${phone1} to ${never} in ${doNotDisturb}
	press hardkey as ${goodBye} on ${phone1}

562764: CHM "Standard" Call Forward Mode - Always
    [Tags]     Owner:Aman      Reviewer:    CHM    call_handling    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${always} in ${available}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message ${save}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${cancel}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} wait for 2 seconds
    Then On ${phone1} verify display message ${displayMessage['userSettings']}
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then on ${phone1} verify the softkeys in ${idleState}
    Then on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noAnswer} in ${available}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    And on ${phone1} press the softkey ${quit} in SettingState
    [Teardown]    Default Availability State

556960: APT - (Hold alternate) Go off hook from HANDSET, make call , answer on SPEAKER
    [Tags]      Owner:Aman      Reviewer:      audio_path_test
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then Disconnect the call from ${phone2}

556969: APT - (Mute alternate) Go off hook from HANDSET, make call , answer on SPEAKER
    [Tags]      Owner:Aman      Reviewer:      audio_path_test
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of speaker as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Press hardkey as ${mute} on ${phone2}
    Then Verify the led state of mute as ${blink} on ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then Verify one way audio from ${phone1} to ${phone2}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone1}
    Then Verify the led state of mute as ${blink} on ${phone2}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then Press hardkey as ${mute} on ${phone1}
    Then Press hardkey as ${mute} on ${phone2}
    Then Verify the led state of speaker as ${on} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}

557086: Verify that idle phone will show on hook telephone icon for each call appearance
    [Tags]      Owner:Aman      Reviewer:      call_appearance
    Given On ${phone1} verify the softkeys in ${idle}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} verify display message >
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then on ${phone1} verify display message >
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then on ${phone1} verify display message >
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify the led state of ${line4} as ${on} on ${phone1}
    Then on ${phone1} verify display message >
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone1} verify display message >
    Then Press hardkey as ${goodBye} on ${phone1}

557082: Pickup from CA while the auto off hook is Speaker
    [Tags]      Owner:Aman      Reviewer:      call_appearance
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of speaker as ${on} on ${phone1}
    Then Disconnect the call from ${phone1}

557355: Conference Held Calls
    [Tags]      Owner:Aman      Reviewer:      merge    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Verify no audio path from ${phone3} to ${phone1}
    Then on ${phone1} press the softkey ${merge} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}

557494: Show parties on users in a 4 party Make Me Blind conference
    [Tags]      Owner:Aman      Reviewer:      make_me_conference    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone3} using ${loudSpeaker}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone2} press the softkey ${conference} in ConferenceCallState
    Then on ${phone2} enter number ${phone4}
    Then on ${phone2} press the softkey ${conference} in ConferenceCallState
    Then Answer the call on ${phone4} using ${loudspeaker}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}

557359: MERGE calls in a MakeMe Conference
    [Tags]    Owner:Aman    Reviewer:    merge    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then I want to make a two party call between ${phone5} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify audio path between ${phone2} and ${phone5}
    Then on ${phone2} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone5} on ${phone1}
    Then I want to make a two party call between ${phone6} and ${phone3} using ${line1}
    Then answer the call on ${phone3} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then Verify audio path between ${phone3} and ${phone6}
    Then on ${phone3} press the softkey ${merge} in ConferenceCallState
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then on ${phone1} press ${hardkey} ${scrollDown} for 4 times
    Then Verify extension ${number} of ${phone6} on ${phone1}
    Then I want to make a two party call between ${phone7} and ${phone3} using ${line1}
    Then answer the call on ${phone3} using ${line2}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then Verify audio path between ${phone3} and ${phone7}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    Then disconnect the call from ${phone6}

558182: TC01-a: Cancel from Cancel softkey
    [Tags]    Owner:Aman    Reviewer:    transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} press the softkey ${cancel} in TransferState
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}

558183: TC01-b: Cancel from Goodbye hardkey
    [Tags]    Owner:Aman    Reviewer:    transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then press hardkey as ${goodBye} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}

558287: Directory Transfer_Blind Transfer call with another call on the phone
    [Tags]    Owner:Aman    Reviewer:    semi_attended_transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Given I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then on ${phone1} ${semiAttendedTransfer} call to ${phone4} using directory
    Then Verify the Caller id on ${phone3} and ${phone4} display
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

558288: Directory Transfer_Consultive Transfer call with another call on the phone
    [Tags]    Owner:Aman    Reviewer:    consultive_transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Given I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then on ${phone1} ${consultiveTransfer} call to ${phone4} using directory
    Then Verify the Caller id on ${phone3} and ${phone4} display
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

562365: Verify GUI Log Upload in progress message
    [Tags]    Owner:Aman    Reviewer:    log_upload     notApplicableFor6910
    Given on ${phone1} navigate to ${diagnostics} settings
    Then upload log from ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

561184: Intercom does not display for Anonymous calls
    [Tags]    Owner:Aman    Reviewer:    anonymous_call
    Given I want to use fac ${privateCall} on ${phone2} to ${phone1}
    Then On ${phone1} Wait for 6 seconds
    Then press hardkey as ${goodBye} on ${phone1}
    Then press the call history button on ${phone1} and folder ${missed} and ${details}
    Then On ${phone1} verify display message ${callerId_blocked}
    Then I want to verify on ${phone1} negative display message ${intercom}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press the call history button on ${phone1} and folder ${missed} and ${dial}
    And press hardkey as ${goodBye} on ${phone1}

561283: Assign & Unassigned user multiple times on same phone
    [Tags]    Owner:Aman    Reviewer:    assignUser
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 10 seconds
    And On ${phone1} verify display message ${available}
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 10 seconds
    And Verify extension ${number} of ${phone1} on ${phone1}

561284: Assign & Unassigned user multiple times on same phone (with reboot)
    [Tags]    Owner:Aman    Reviewer:    assignUser
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 10 seconds
    And On ${phone1} verify display message ${available}
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 10 seconds
    And Verify extension ${number} of ${phone1} on ${phone1}
    Then Reboot ${phone1}
    And Verify extension ${number} of ${phone1} on ${phone1}

    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 10 seconds
    And On ${phone1} verify display message ${available}
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 10 seconds
    And Verify extension ${number} of ${phone1} on ${phone1}
    Then Reboot ${phone1}
    And Verify extension ${number} of ${phone1} on ${phone1}

561292: Assign-Unassign from phone and from voicemail prompts
    [Tags]    Owner:Aman    Reviewer:    assignUser    notApplicableFor6910
   [Setup]    Assign Extension Custom Setup
    Given on ${phone1} navigate to ${unassignUser} settings
    Then press hardkey as ${scrollLeft} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} Wait for 10 seconds
    And On ${phone1} verify display message ${available}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 10 seconds
    And Verify extension ${number} of ${phone1} on ${phone1}

    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 10 seconds
    Then On ${phone1} verify display message ${available}
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 10 seconds
    And Verify extension ${number} of ${phone1} on ${phone1}
   [Teardown]    Assign Extension Custom Teardown

557375: Make a new call during 3 way conference
    [Tags]    Owner:Aman    Reviewer:    conference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Given I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Press hardkey as ${holdState} on ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then I want to make a two party call between ${phone2} and ${phone4} using ${line2}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone4}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${holdState} on ${phone2}
    Then Verify the led state of ${line2} as ${blink} on ${phone2}
    Then I want to press line key ${programKey1} on phone ${phone2}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    And disconnect the call from ${phone1}
    And disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

561458: TC04: Play
    [Tags]    Owner:Aman    Reviewer:    voicemail     notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Given Delete voicemail message on ${save} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Move voicemail message from ${inboxToSaved} folder for ${phone1}
    Then On ${phone1} Press The Softkey ${play} In VoiceMailState
    And On ${phone1} verify display message ${pause}
    And press hardkey as ${goodBye} on ${phone1}

561460: TC06: Delete
    [Tags]    Owner:Aman    Reviewer:    voicemail     notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Given Delete voicemail message on ${save} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Move voicemail message from ${inboxToSaved} folder for ${phone1}
    Then On ${phone1} Press The Softkey ${delete} In VoiceMailState
    Then I want to verify on ${phone1} negative display message ${phone2}
    And press hardkey as ${goodBye} on ${phone1}

561476: TC04: Move Voicemail from Deleted to Inbox folder
    [Tags]    Owner:Aman    Reviewer:    voicemail     notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Move voicemail message from ${deleteToInbox} folder for ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

557633: Answer call via pickup key while focused call on Hold (speaker)
    [Tags]    Owner:Aman    Reviewer:    hold
    Given I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey2}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Given I want to make a two party call between ${phone1} and ${phone4} using ${programKey3}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone4}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line3} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone4}
    Given I want to make a two party call between ${phone1} and ${phone5} using ${programKey4}
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone5}
    Then Verify the led state of ${line4} as ${on} on ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone5}
    Then Verify extension ${number} of ${phone5} on ${phone1}
    Then on ${phone1} Press ${hardkey} ${scrollUp} for 2 times
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line3} as ${blink} on ${phone1}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    And disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    And disconnect the call from ${phone4}
    And disconnect the call from ${phone5}

177234: Consult transfer to Extension via timeout
    [Tags]     Owner:Aman      Reviewer:       consult_transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press the softkey ${Transfer} in AnswerState
    Then on ${phone2} enter number ${phone3}
    Then On ${phone2} Wait for 5 seconds
    Then on ${phone2} press the softkey Blind Transfer in TransferState
    Then On ${phone2} verify display message ${displayMessage['callTransferred']}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    And disconnect the call from ${phone1}

562759: Call Handling mode(CHM) options set to "In a Meeting"
    [Tags]     Owner:Aman      Reviewer:       CHM    call_handling    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${all} in ${all}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Change the phone state to default state on ${phone1}
    Then on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${inMeeting}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${displayMessage['userSettings']}
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then on ${phone1} verify the softkeys in ${idle}
    And Change the phone state to default state on ${phone1}
   [Teardown]    Default Availability State

560126: Park call to destination on active call
    [Tags]    Owner:Aman    Reviewer:    park       notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Given I want to make a two party call between ${phone3} and ${phone4} using ${loudspeaker}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone4}
    Then I want to Park the call from ${phone3} on ${phone1} using ${default} and ${park}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then on ${phone3} verify the softkeys in ${idle}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}

560135: Press Park while 2 calls are on Hold
    [Tags]    Owner:Aman    Reviewer:    park      notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Given I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programKey2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then on ${phone1} Press ${hardkey} ${scrollUp} for 1 times
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press the softkey ${park} in answerstate
    Then on ${phone1} press the softkey ${parkCancel} in answerstate
    Then I want to verify on ${phone1} negative display message ${cancel}
    Then I want to verify on ${phone1} negative display message >
    Then Transfer call from ${phone1} to ${phone4} using ${blindTransfer}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then Verify the Caller id on ${phone3} and ${phone4} display
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}

562166: Navigate to Status screen
    [Tags]    Owner:Aman    Reviewer:    settings
    Given on ${phone1} move to settings ${diagnostics} to ${traceroute} settings with 1
    Then On ${phone1} press the key ${cancel} in state ${diagnostics}
    Then on ${phone1} verify display message ${traceroute}
    Then on ${phone1} press the softkey ${quit} in settingstate
    And on ${phone1} verify the softkeys in ${idle}

558274: Pressing call appearance key
    [Tags]    Owner:Aman    Reviewer:    call_appearance
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${transfer}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

558192: TC01-c: Blind Transfer - by hanging up the Call
    [Tags]    Owner:Aman    Reviewer:    transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}
    Then on ${phone2} verify the softkeys in ${idle}
    And on ${phone3} verify the softkeys in ${idle}

558189: TC10:Cancel transfer with another call on phone
    [Tags]    Owner:Aman    Reviewer:    transfer
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programKey2}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then On ${phone1} dial partial number of ${phone4} with ${firstTwo}
    Then on ${phone1} press the softkey ${cancel} in TransferState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

562331: Pop up screen after pressing Log Issue key
    [Tags]    Owner:Aman    Reviewer:    log_issue     notApplicableFor6910
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then On ${phone1} verify display message ${logging_issue}
    Then On ${phone1} Wait for 20 seconds
    And On ${phone1} verify the softkeys in ${idle}

560803: TC016 Making a transfer/conference call after sending a whisper page call
    [Tags]    Owner:Aman    Reviewer:       whisper_page
    Given I want to use fac Whisperpage on ${phone1} to ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then On ${phone1} verify display message ${drop}
    Then i want to verify on ${phone1} negative display message ${transfer}
    Then i want to verify on ${phone1} negative display message ${conference}
    And disconnect the call from ${phone1}

561315: phone in Available/Anonymous state; Assign a User
    [Tags]    Owner:Aman    Reviewer:    assignUser    notApplicableFor6910
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 10 seconds
    Then On ${phone1} verify display message ${available}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${extension}
    Then On ${phone1} verify display message ${password}
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} dial number ${voicemailPassword}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} Wait for 5 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    And Disconnect the call from ${phone2}

557521: Press Merge key on a Make me conference call
 removed from execution by Alka: DTP-56749
    Owner:Aman    Reviewer:    merge      notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${programKey2}
    Then I want to make a two party call between ${phone5} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${programKey3}
    Then I want to make a two party call between ${phone6} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${programKey4}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify the led state of ${line3} as ${blink} on ${phone1}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${merge} in ConferenceCallState
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then Verify extension ${number} of ${phone5} on ${phone1}
    Then Verify extension ${number} of ${phone6} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then Disconnect the call from ${phone6}
    Then Disconnect the call from ${phone5}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone2}

558333: Phone acts as TransferOR in a blind transfer using the Transfer
    [Tags]    Owner:Aman    Reviewer:    blind_transfer      notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Disconnect the call from ${phone2}

563661: Focus view behavior during Transfer Scenario
    [Tags]    Owner:Aman    Reviewer:    transfer
    Given I want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then On ${phone1} verify the softkeys in ${idle}
    And Disconnect the call from ${phone2}

560505: Internal incoming call from Anonymous or Available phone
    [Tags]    Owner:Aman    Reviewer:    available_state
    Given on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 10 seconds
    Then On ${phone1} verify display message ${available}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then On ${phone2} verify display message ${callerIdUnknown}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone2} verify display message ${callerIdUnknown}
    Then Disconnect the call from ${phone2}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    And on ${phone1} dial number 1

752272: Far-end (phone) places phone on remote hold (local hold, remote hold, remote unhold, local unhold) answer via SPEAKER
    [Tags]    Owner:Aman    Reviewer:       hold
    Given Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify the led state of ${line1} as ${on} and led color as ${red}
    Then On ${phone1} verify display message 01:
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone1} verify the led state of ${line1} as ${blink} and led color as ${red}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then On ${phone2} verify the led state of ${line1} as ${on} and led color as ${red}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone1} verify the led state of ${line1} as ${blink} and led color as ${red}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone2} verify the led state of ${line1} as ${blink} and led color as ${red}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone1} verify the led state of ${line1} as ${blink} and led color as ${red}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then On ${phone2} verify the led state of ${line1} as ${on} and led color as ${red}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify the led state of ${line1} as ${on} and led color as ${red}
    Then On ${phone2} verify the led state of ${line1} as ${on} and led color as ${red}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    And disconnect the call from ${phone1}

752273: Far-end (phone) places phone on remote hold, answer via HANDSET
    [Tags]    Owner:Aman    Reviewer:       hold
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    And disconnect the call from ${phone1}

756013: TC013 2 Incoming calls while the phone is Idle
    [Tags]    Owner:Aman    Reviewer:       voicemail    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then on ${phone1} press the softkey ${toVm} in RingingState
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then on ${phone1} press the softkey ${toVm} in RingingState
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then on ${phone3} verify display message ${displayVoiceMail}
    Then on ${phone1} wait for 15 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then On ${phone1} verify the led state of ${messageWaitingIndicator} as ${blink} and led color as ${red}
    Then Press hardkey as ${goodBye} on ${phone1}

752310: TC01: Far-end (phone) places phone on remote hold, answer via HANDSET
    [Tags]    Owner:Aman    Reviewer:       hold    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    And disconnect the call from ${phone1}

557562:Press MERGE during UCB Call
    [Tags]    Owner:Anuj    Reviewer:    merge_ucb_Call    0007    notApplicableFor6910    557562
    Given on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then I want to verify on ${phone1} negative display message ${merge}
    Then Disconnect the call from ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} dial number ${wrongAccessCode}
    Then I want to verify on ${phone1} negative display message ${merge}
    Then Disconnect the call from ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} dial number ${accessCode}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${Line2}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify display message ${merge}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then On ${phone1} verify display message ${ucbNumber}
    Then On ${phone2} verify display message ${ucbNumber}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone1}

557563:Press Park during UCB Call
    [Tags]    Owner:Anuj    Reviewer:    park_ucb_Call    0007    notApplicableFor6910    123321
    Given on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then I want to verify on ${phone1} negative display message ${park}
    Then Disconnect the call from ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} dial number ${wrongAccessCode}
    Then I want to verify on ${phone1} negative display message ${park}
    Then Disconnect the call from ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} dial number ${accessCode}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} press the softkey ${park} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then On ${phone2} verify display message ${ucbNumber}
    Then press hardkey as ${holdState} on ${phone2}
    And Disconnect the call from ${phone2}

557555:Answer new calls during UCB Call
    [Tags]    Owner:Anuj    Reviewer:    ucb_Call    557555
    Given On ${phone1} press the key ${conference} in state ${idle}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then disconnect the call from ${phone1}
    Then On ${phone1} press the key ${conference} in state ${idle}
    Then on ${phone1} dial number ${wrongAccessCode}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then disconnect the call from ${phone1}
    Then On ${phone1} press the key ${conference} in state ${idle}
    Then on ${phone1} dial number ${accessCode}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Disconnect the call from ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    And Disconnect the call from ${phone1}

556997: Connect call with another user then terminate call by putting SPEAKER on-hook using Goodbye button
    [Tags]    Owner:Anuj    Reviewer:    speaker_on_hook
    Given press hardkey as ${handsfree} on ${phone1}
    Then On ${phone1} verify display message >
    Then verify the led state of speaker as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then verify the caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudspeaker}
    Then On ${phone1} verify display message 00
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    And On ${phone1} verify the softkeys in ${idle}

557109:CA display while in Off -hook for multiple call appearances
    [Tags]    Owner:Anuj    Reviewer:    multiple_call_appearances    557109
    Given I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then verify the led state of speaker as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then verify the led state of speaker as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone1}
    And disconnect the call from ${phone1}

557095: Verify if the screen displays the name or the number when the user switches between calls
    [Tags]    Owner:Anuj    Reviewer:    switches_between_calls    557095
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then i want to press line key ${programKey1} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone3} press the softkey ${drop} in AnswerState
    Then on ${phone1} press the softkey ${drop} in AnswerState
    And on ${phone1} verify the softkeys in ${idle}

557503:TC003 Party List window after press show key
    [Tags]    Owner:Anuj    Reviewer:    Party_List_window    29/07/2019    0010    notApplicableFor6910
    [Timeout]    35 minutes
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${ConsultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then on ${phone3} press the softkey ${conference} in conferencecallstate
    Then on ${phone3} enter number ${phone4}
    Then On ${phone4} Wait for 5 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone4}
    Then on ${phone3} press the softkey ${conference} in conferencecallstate
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone3} verify display message ${show}
    Then on ${phone3} press ${softkey} ${bottomkey3} for 1 times
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then verify extension ${number} of ${phone4} on ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone4}

557506:TC006 Party can be dropped by Drop key
    [Tags]    Owner:Anuj    Reviewer:    drop_by_drop_key    29/07/2019    0010    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${ConsultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then on ${phone3} press the softkey ${conference} in conferencecallstate
    Then on ${phone3} enter number ${phone4}
    Then on ${phone4} wait for 3 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone4}
    Then on ${phone3} press the softkey ${conference} in conferencecallstate
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone1} verify display message ${show}
    Then on ${phone3} press ${softkey} ${bottomkey3} for 1 times
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then verify extension ${number} of ${phone4} on ${phone3}
    Then on ${phone3} verify display message ${drop}
    Then on ${phone3} verify display message ${back}
    Then press hardkey as ${scrollDown} on ${phone3}
    Then press hardkey as ${scrollDown} on ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}


557980:TC03: Verify that call can be parked when using # to terminate digit collection
    [Tags]    Owner:Anuj    Reviewer:    call_parked_with_#    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to park the call from ${phone2} on ${phone3} using ${default} and ${TerminatorString}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone3}
    And disconnect the call from ${phone1}

563714:Test scroll behavior while on-hold list
    [Tags]    Owner:Anuj    Reviewer:Aman    scroll_on_hold
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${line2}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then Press hardkey on ${phone1} as ${scrollUp} 1 of times for navigation between calls
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

561517: TC01: Authentication page
    [Tags]    Owner:Anuj    Reviewer:Aman    Authentication    notApplicableFor6910
    Given press hardkey as ${voicemail} on ${phone1}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then on ${phone1} verify display message ${login}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${callVM}
    And on ${phone1} verify display message ${quit}



561511: TC01: Send incoming call to Voicemail using key
    [Tags]    Owner:Anuj    Reviewer:Aman    voicemail     notApplicableFor6910
    Given leave voicemail message from ${phone2} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${open} in VoiceMailState
    Then verify extension ${number} of ${phone2} on ${phone1}
    And press hardkey as ${goodbye} on ${phone1}



561501: TC01-b: in REPLY, play the message. Lift handset or Press Speaker or Headset button
    [Tags]    Owner:Anuj    Reviewer:Aman    voicemail     notApplicableFor6910
    Then leave voicemail message from ${phone2} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then press hardkey as ${scrollright} on ${phone1}
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then on ${phone1} press the softkey ${reply} in VoiceMailState
    Then on ${phone1} press the softkey ${start} in VoiceMailState
    Then on ${phone1} wait for 20 seconds
    Then on ${phone1} press the softkey ${stop} in VoiceMailState
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${startplay} in VoiceMailState
    Then on ${phone1} verify display message ${pause}
    Then press hardkey as ${offhook} on ${phone1}
    Then on ${phone1} verify display message ${voicemailReply}
    And press hardkey as ${goodbye} on ${phone1}


561500:TC01-a: in REPLY, lift handset or Press Speaker or Headset button
    [Tags]    Owner:Anuj    Reviewer:Aman    voicemail     notApplicableFor6910
    Then leave voicemail message from ${phone2} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then press hardkey as ${scrollright} on ${phone1}
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then on ${phone1} press the softkey ${reply} in VoiceMailState
    Then press hardkey as ${offhook} on ${phone1}
    Then on ${phone1} verify display message ${voicemailReply}
    And press hardkey as ${goodbye} on ${phone1}

560755: TC014 Off-hook handset while being on directory screen
    [Tags]    Owner:Anuj    Reviewer:    directory     notApplicableFor6910
    Given press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then press hardkey as ${offHook} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    And press hardkey as ${goodBye} on ${phone1}

560754: TC013 Placing a call exits to main screen (Hold)
    [Tags]    Owner:Anuj    Reviewer:    directory     notApplicableFor6910    560754
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${directory} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    And disconnect the call from ${phone2}

557616: With multiple calls on HANDSET, ACTIVE Far-End hangs up
    [Tags]    Owner:Anuj    Reviewer:    handset
    Given press hardkey as ${offHook} on ${phone1}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then on ${phone1} verify display message >
    Then i want to make a two party call between ${phone1} and ${phone2} using ${programKey3}
    Then answer the call on ${phone2} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programKey4}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then answer the call on ${phone3} using ${line1}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then on ${phone3} press the softkey ${drop} in AnswerState
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

557625: With multiple calls on SPEAKER,ACTIVE Far-End hangs up
    [Tags]    Owner:Anuj    Reviewer:    speaker    557625
    Given press hardkey as ${handsFree} on ${phone1}
    Then verify the led state of speaker as ${on} on ${phone1}
    Then on ${phone1} verify display message >
    Then i want to make a two party call between ${phone1} and ${phone2} using ${programKey3}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programKey4}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then on ${phone3} press the softkey ${drop} in AnswerState
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of speaker as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line3} as ${on} on ${phone1}
    And disconnect the call from ${phone2}


558001: TC05: Verify that parked call can be unparked via unpark call timeout dial [DTP-32383]
    [Tags]    Owner:Anuj    Reviewer:    park_unpark    notApplicableFor6910    558001
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to Park the call from ${phone2} on ${phone3} using ${default} and ${Park}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone2} press ${softkey} ${bottomKey2} for 1 times
    Then I want to unPark the call from ${phone3} on ${phone2} using ${default} and ${timeout}
    Then on ${phone2} wait for 6 seconds
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}

557561: Press Conference during UCB Call
    [Tags]    Owner:Anuj    Reviewer:    ucb_call639    notApplicableFor6910
    &{pmargst} =  Create Dictionary  key=${conference}
    &{pressHardkey} =  Create Dictionary  action_name=pressHardkey   pmargs=&{pmargst}
    Given on ${phone1} dial number ${ucbNumber}
    Then on ${phone1} verify display message ${conferenceExt}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} due to action ${pressHardkey} popup raised verify message ${xconfNotAllowed} with wait of 0
    Then disconnect the call from ${phone1}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} dial number ${wrongAccessCode}
    Then on ${phone1} due to action ${pressHardkey} popup raised verify message ${xconfNotAllowed} with wait of 0
    Then disconnect the call from ${phone1}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} dial number ${accessCode}
    Then on ${phone1} wait for 4 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then disconnect the call from ${phone1}



561687: Phone Rejects Invalid VM PIN
    [Tags]    Owner:Anuj    Reviewer:    ucb_call    notApplicableFor6910
    Given press hardkey as ${voicemail} on ${phone1}
    Then On ${phone1} verify display message ${enterVoicemailPassword}
    Then on ${phone1} dial number ${wrongVoicemailpassword}
    Then on ${phone1} verify display message ${incorrectPassword}
    Then on ${phone1} dial number ${voicemailpassword}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${voicemailDisplay['inbox']}
    Then on ${phone1} verify display message ${voicemailDisplay['saved']}
    Then on ${phone1} verify display message ${voicemailDisplay['deleted']}
    And press hardkey as ${goodBye} on ${phone1}


556917: Answer incoming call (while Directory is open) by pressing Headset or Speaker button
    [Tags]    Owner:Anuj    Reviewer:    directory    notApplicableFor6910
    Then Set number of rings to 10 on ${phone1}
    Then On ${phone1} verify directory with ${default} of ${firstPhone}
    Then On ${phone1} verify display message ${autoUser1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then i want to verify on ${phone1} negative display message ${directory}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then i want to verify on ${phone1} negative display message ${directory}
    Then verify audio path between ${phone1} and ${phone2}
    Then Set number of rings to 5 on ${phone1}
    And disconnect the call from ${phone2}

562080: Call Park
    [Tags]    Owner:Anuj    Reviewer:    publish_messages    notApplicableFor6910
    &{sipmessagedetail} =  Create Dictionary    sip_message=PUBLISH    sip_message_value=VQSessionReport
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone2} on ${phone3} using ${default} and ${Park}
    Then on ${phone2} wait for 5 seconds
    Then press hardkey as ${holdState} on ${phone3}
    Then verify audio path between ${phone1} and ${phone3}
    Then Capture the ${outgoing} packets from ${phone2} and verifiy the ${sipmessagedetail} on ${phone3}
    And disconnect the call from ${phone3}

561082: Call History: Voicemail
    [Tags]    Owner:Anuj    Reviewer:    voicemail    notApplicableFor6910
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then press the call history button on ${phone1} and folder ${missed} and ${details}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} wait for 15 seconds
    Then Press hardkey as ${goodBye} on ${phone1}
    Then login into voicemailbox for ${phone2} using ${voicemailpassword}
    Then press hardkey as ${scrollRight} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    And Press hardkey as ${goodBye} on ${phone2}

562082: Call Unpark
    [Tags]    Owner:Anuj    Reviewer:    publish message    notApplicableFor6910    562082
    &{sipmessagedetail} =  Create Dictionary    sip_message=PUBLISH    sip_message_value=VQSessionReport
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${park}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then I want to unPark the call from ${phone3} on ${phone1} using ${default} and ${dial}
    Then verify audio path between ${phone1} and ${phone2}
    Then Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone3}
    And disconnect the call from ${phone1}

562077: Call Pickup + Hold + Retrieve + Hang-up
    [Tags]    Owner:Anuj    Reviewer:    publish message
    &{sipmessagedetail} =  Create Dictionary    sip_message=PUBLISH    sip_message_value=VQSessionReport
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then disconnect the call from ${phone1}
    Then on ${phone1} wait for 6 seconds
    And Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone2}

562070: Calling Towards Invalid Destination and then press goodbye key
    [Tags]    Owner:Anuj    Reviewer:    publish_messages
    &{sipmessagedetail} =  Create Dictionary    sip_message=${EMPTY}    sip_message_value=${EMPTY}
    Given i want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} dial number ${invalidExtension}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${requestDenied}
    Then on ${phone1} wait for 5 seconds
    And Capture the ${outgoing} packets from ${phone1} and verifiy the ${sipmessagedetail} on ${phone2}



560632: CHM Extended Absence edit mode-Never option
    [Tags]    Owner:Anuj    Reviewer:    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${never} in ${extendedAbsence}
    Then on ${phone1} verify display message ${callForwardMode}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Default Availability State

560635: CHM In a Meeting edit mode-Never option
    [Tags]    Owner:Anuj    Reviewer:    CHM    560635    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${never} in ${inMeeting}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Default Availability State


560507: Internal incoming call with blocked number
    [Tags]    Owner:Anuj    Reviewer:    blocked_number
    Given I want to use fac ${privateCall} on ${phone2} to ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} verify display message ${callerBlocked}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} verify display message ${callerBlocked}
    And disconnect the call from ${phone2}

736665: Publish on Consultative Transfer
    [Tags]    Owner:Anuj    Reviewer:    publish message    736665
    &{sipmessagedetail} =  Create Dictionary    sip_message=PUBLISH    sip_message_value=VQSessionReport
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Transfer call from ${phone2} to ${phone3} using ${consultiveTransfer}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then Capture the ${outgoing} packets from ${phone2} and verifiy the ${sipmessagedetail} on ${phone3}
    And Disconnect the call from ${phone1}

755476: Dial from Call History with different dialing mode
    [Tags]    Owner:Anuj    call_history    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then press hardkey as ${goodbye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} verify display message ${callHistory}
    Then press hardkey as ${goodbye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${missed} and ${dial}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${missed} and ${Loudspeaker}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} verify display message ${callHistory}
    Then press hardkey as ${enter} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${offHook} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    And press hardkey as ${goodbye} on ${phone1}


752313: TC04: Far-end (phone) places phone on remote hold, answer via HEADSET or SPEAKER
    [Tags]    Owner:Anuj    Reviewer:    notApplicableFor6910    752313
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then Press hardkey as ${handsFree} on ${phone1}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    And disconnect the call from ${phone1}


752007: 3-way mesh conference is not repeatable
    [Tags]    Owner:Anuj    conference    notApplicableFor6910    752007
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 3 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${drop} in ConferenceCallState
    Then on ${phone2} verify the softkeys in ${idleState}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

754986: TC001 Make a call with prefix "*19 + Ext. No."
    [Tags]      Owner:Anuj     Reviewer:Vikhyat    whisperPage
    Given i want to use fac Whisperpage on ${phone1} to ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

752246: Answer call via Pickup key while focused call on Hold (headset)
    [Tags]    Owner:Anuj    Reviewer:    PICKUP_KEY    notApplicableFor6910    752246
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${line2}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceActive}
    Then press hardkey as ${holdState} on ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceLocalHold}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then press hardkey as ${scrollUp} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then on ${phone1} press ${softKey} ${bottomkey1} for 1 times
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceLocalHold}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

798690: Nav keys on Options screen
    [Tags]    Owner:Anuj    Reviewer:    MENU    798690    notApplicableFor6910
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then On the ${phone1} verify softkeys in different state using ${restart}
    Then on ${phone1} verify display message ${restart}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} verify display message ${restart}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then On the ${phone1} verify softkeys in different state using ${availability}
    Then on ${phone1} verify display message ${availability}
    Then press hardkey as ${scrollLeft} on ${phone1}
    Then on ${phone1} verify display message ${availability}
    Then press hardkey as ${scrollUp} on ${phone1}
    Then on ${phone1} verify display message ${availability}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} verify display message ${availability}
    And press hardkey as ${goodBye} on ${phone1}


757378: Backspace during password entry
    [Tags]    Owner:Anuj    Reviewer:    option    notApplicableFor6910    757378
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number 1234
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then i want to verify on ${phone1} negative display message 1234
    Then on ${phone1} press ${softkey} ${bottomkey2} for 3 times
    Then on ${phone1} dial number ${fivedigitnumber}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then on ${phone1} press ${softkey} ${bottomkey1} for 1 times
    Then on ${phone1} verify display message ${status}
    And press hardkey as ${goodBye} on ${phone1}

753093: dial key, invalid external number
    [Tags]    Owner:Anuj    Reviewer:    invalid_externam_number
    Given I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} enter number 55555
    Then on ${phone1} press ${softkey} ${bottomkey1} for 1 times
    Then on ${phone1} wait for 8 seconds
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then press hardkey as ${offhook} on ${phone1}
    Then on ${phone1} enter number 55555
    Then on ${phone1} press ${softkey} ${bottomkey1} for 1 times
    Then on ${phone1} wait for 8 seconds
    Then on ${phone1} verify the softkeys in ${IdleState}

752809: TC05: Hang up Transferee while transferring
    [Tags]    Owner:Anuj    transfer    752809    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then press hardkey as ${goodBye} on ${phone3}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then on ${phone1} wait for 4 seconds
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then press hardkey as ${goodBye} on ${phone2}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then on ${phone1} wait for 4 seconds
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone1} enter number ${phone2}
    Then press hardkey as ${goodBye} on ${phone2}
    And on ${phone1} verify the softkeys in ${IdleState}

750965: Usage of Hold key to place a call on hold
    [Tags]    Owner:Anuj    holdUnhold     750965
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And press hardkey as ${goodBye} on ${phone1}

730842: Torture Test - Point-to-Point HOLD Test 3
    [Tags]    Owner:Anuj    holdUnhold     730842
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    And on ${phone1} verify the softkeys in ${IdleState}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    And on ${phone1} verify the softkeys in ${IdleState}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    And on ${phone1} verify the softkeys in ${IdleState}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    And on ${phone1} verify the softkeys in ${IdleState}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    And on ${phone1} verify the softkeys in ${IdleState}

750971: Far-end party places phone on remote hold, answer via HEADSET or SPEAKER
    [Tags]    Owner:Anuj    holdUnhold    notApplicableFor6910    750971
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then on ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then press hardkey as ${offHook} on ${phone1}
    Then on ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

750941: TC01-d: Put Transferor on-hook while transferring
    [Tags]    Owner:Anuj    holdUnhold    notApplicableFor6910    750941
    Given press hardkey as ${offHook} on ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} verify display message >
    Then press hardkey as ${onHook} on ${phone1}
    Then i want to verify on ${phone1} negative display message >
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} verify display message >
    Then on ${phone1} enter number ${phone3}
    Then press hardkey as ${onHook} on ${phone1}
    Then i want to verify on ${phone1} negative display message >
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

750946: Unhold call by pressing HOLD key after blind transfer to invalid #
    [Tags]    Owner:Anuj    holdUnhold    750946
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} dial number 3336
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And press hardkey as ${goodBye} on ${phone1}

750935: TC09: Digits entered on the dialing window should be cleared when a transfer call is aborted
    [Tags]    Owner:Anuj    holdUnhold    750935
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} dial number 3336
    Then press hardkey as ${goodBye} on ${phone2}
    And on ${phone1} verify the softkeys in ${IdleState}


TC018: Ping to valid IP (on phone)
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan   ValidIPPing
    Given on ${phone1} move to ${diagnostics} to ${ping} settings
    Then on ${phone1} Wait for 3 seconds
    Then Enter ${ipaddrstr} on ${phone1} to ${ping} settings
    Then On ${phone1} verify display message ${numberOfPackets}
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times

154053: start traceroute (phone)
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    traceroute
    Given on ${phone1} move to ${diagnostics} to ${traceroute} settings
    Then On ${phone1} Wait for 4 seconds
    Then Enter ${ipaddrstr} on ${phone1} to ${traceroute} settings
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} verify display message ${tracerouting}
    Then validate ip object in phone display content on ${phone1}
    Then on ${phone1} Wait for 4 seconds
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times
    Given on ${phone1} move to ${diagnostics} to ${traceroute} settings
    Then On ${phone1} Wait for 4 seconds
    Then Enter ${ipaddrstr_two} on ${phone1} to ${traceroute} settings
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} verify display message ${tracerouting}
    Then validate ip object in phone display content on ${phone1}
    Then on ${phone1} Wait for 4 seconds
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times

558106: Silent Coach with call in progress. Initiation active in COS
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    silentcoach    notApplicableFor6910
    Given I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to use fac ${silentCoachFAC} on ${phone1} to ${phone2}
    Then Verify one way audio from ${phone1} to ${phone3}
    Then on ${phone1} Wait for 3 seconds
    Then Verify audio path between ${phone3} and ${phone2}
    Then on ${phone1} Wait for 3 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} verify display message ${consult}
    Then on ${phone2} press ${softkey} ${bottomkey2} for 1 times
    Then verify no audio path from ${phone3} to ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} verify display message ${resume}
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times
    Then on ${phone2} press ${hardKey} ${goodBye} for 1 times

557530: Conf key when focus is on Active call - UCB configured
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan   UCB_configured       notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} display verify ${conferenceDisplay}
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times
    Then on ${phone2} press ${hardKey} ${goodBye} for 1 times

557556: Hold during UCB Call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan   UCB_configured    notApplicableForMiCloud
     &{pmargst} =  Create Dictionary  key=${holdState}
     &{pressHardkey} =  Create Dictionary  action_name=pressHardkey   pmargs=&{pmargst}
     Given on ${phone1} press the key ${conference} in state ${idle}
     Then on ${phone1} due to action ${pressHardkey} popup raised verify message Hold not permitted with wait of 0
     Then disconnect the call from ${phone1}
     Then on ${phone1} press the key ${conference} in state ${idle}
     Then on ${phone1} enter number ${wrongAccessCode}
     Then on ${phone1} due to action ${pressHardkey} popup raised verify message Hold not permitted with wait of 0
     Then disconnect the call from ${phone1}
     Then on ${phone1} press the key ${conference} in state ${idle}
     Then on ${phone1} enter number ${accessCode}
     Then Put the linekey ${line1} of ${phone1} on ${hold}
     Then on ${phone1} verify display message ${conference}
     Then Put the linekey ${line1} of ${phone1} on ${unhold}
     Then disconnect the call from ${phone1}


558247: Press Transfer key to transfer while consult is ringing
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    transfer       notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of Line 1 as blink on ${phone1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Transfer call from ${phone1} to ${phone3} using ${semiAttendedTransfer}
    Then Verify the led state of Line 1 as blink on ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then Verify the line state as ${IdleState} on ${phone1}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}
    Then on ${phone1} press ${hardKey} ${goodBye} for 1 times
    Then on ${phone2} press ${hardKey} ${goodBye} for 1 times

558249: Able to consult-transfer an incoming call without answering
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    consult-transfer
     Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
     Then on ${phone1} press the softkey ${transfer} in RingingState
     Then on ${phone1} enter number ${phone3}
     Then I want to verify on ${phone1} negative display message ${consult}
     Then on ${phone1} wait for 3 seconds
     Then Verify the Caller id on ${phone2} and ${phone3} display
     Then disconnect the call from ${phone2}

558273: presses Hold
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    Hold       notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify display message PickUp
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone1} verify display message Drop
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

561559: TC01: Forward message to UserB, w/o forwarding remarks
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    notApplicableFor6910
    Given Leave voicemail message from ${phone3} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${forward} in VoiceMailState
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} press the softkey ${back} in VoiceMailState
    Then on ${phone1} press the softkey ${sendf} in VoiceMailState
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then On ${phone2} verify display message ${voicemailDisplay['inbox']}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then on ${phone2} press the softkey ${play} in VoiceMailState
    Then On ${phone2} verify display message Pause
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}

558295: Transfer incoming call by navigating the focus session
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    focusmove    notApplicableFor6910
    Given on ${phone2} navigate to ${availability} settings
    Then on ${phone2} verify display message ${numberofrings}
    Then on ${phone2} press ${hardKey} ${scrolldown} for 1 times
    Then on ${phone2} press ${hardKey} ${scrollRight} for 1 times
    Then on ${phone2} press ${softkey} ${bottomkey1} for 1 times
    Then I want to make a two party call between ${phone1} and ${phone2} using ${OffHook}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${OffHook}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then on ${phone2} verify display message Answer
    Then I want to press line key ${programKey1} on phone ${phone2}
    Then on ${phone2} verify display message Drop
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then Transfer call from ${phone2} to ${phone4} using ${BlindTransfer}
    Then Verify the Caller id on ${phone4} and ${phone1} display
    Then Verify the Caller id on ${phone3} and ${phone2} display
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then press hardkey as ${goodBye} on ${phone2}
    Then disconnect the call from ${phone1}
    [Teardown]   Default Availability State


558178: TC02-a: Fifth digit deleted using backspace - After time out phone places a call - Using handset
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    delete-transfer     notApplicableFor6910
     Given I want to make a two party call between ${phone1} and ${phone2} using ${OffHook}
     Then On ${phone1} Wait for 5 seconds
     Then Answer the call on ${phone2} using ${loudspeaker}
     Then Verify audio path between ${phone1} and ${phone2}
     Then on ${phone1} press the softkey ${transfer} in AnswerState
     Then on ${phone1} dial partial number of ${phone3} with ${fivedigit}
     Then On ${phone1} Wait for 1 seconds
     Then Verify the Caller id on ${phone3} and ${phone1} display
     Then verify the led state of ${line1} as ${blink} on ${phone3}
     Then press hardkey as ${goodBye} on ${phone1}
     Then press hardkey as ${goodBye} on ${phone2}
     And press hardkey as ${goodBye} on ${phone3}

561290: Assign phone with invalid credentials, press Cancel
    [Tags]    Owner:Abhishekkhanchi    Reviewer:     assignUser    notApplicableFor6910
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press the softkey ${assign} in SettingState
    Then on ${phone1} verify display message ${assignUser}
    Then on ${phone1} verify display message ${extension}
    Then on ${phone1} verify display message ${password}
    Then on ${phone1} dial number 123456
    Then on ${phone1} press ${hardKey} ${scrolldown} for 1 times
    Then on ${phone1} dial number 123456
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${assignUser}
    Then Press softkey cancel on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone1}

561285: Assign user to Phone multiple times (i.e. move user around)
    [Tags]    Owner:Abhishekkhanchi    Reviewer:     assignUser    notApplicableFor6910
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} verify display message ${available}
    Then On ${phone1} Wait for 2 seconds
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 5 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then on ${phone2} dial number #
    Then on ${phone2} Wait for 5 seconds
    Then on ${phone2} dial number ${loginVoicemail}
    Then on ${phone2} Wait for 3 seconds
    Then on ${phone2} dial number 7
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 3
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 2
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} verify display message ${available}
    Then On ${phone2} Wait for 2 seconds
    Then on ${phone2} dial number #
    Then on ${phone2} Wait for 5 seconds
    Then on ${phone2} enter number ${phone2}
    Then on ${phone2} dial number ${loginVoicemail}
    Then on ${phone2} Wait for 3 seconds
    Then on ${phone2} dial number 7
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 3
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 1
    Then on ${phone2} Wait for 1 seconds
    Then Verify extension ${number} of ${phone2} on ${phone2}

557556: Reboot when full logging on
     [Tags]    Owner:Abhishekkhanchi    Reviewer:   Reboot    notApplicableFor6910
     Given on ${phone1} move to ${diagnostics} to ${log_upload} settings
     Then On ${phone1} Wait for 8 seconds
     Then on ${phone1} verify display message ${debugon}
     Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
     Then Reboot ${phone1}
     Then on ${phone1} Wait for 120 seconds
     Then on ${phone1} move to ${diagnostics} to ${log_upload} settings
     Then on ${phone1} verify display message ${debugoff}
     Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

557054:call Offering press Voicemail
    [Tags]    Owner:Abhishekkhanchi    Reviewer:
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Press hardkey as ${voicemail} on ${phone2}
    Then verify the led state of ${line1} as ${off} on ${phone2}
    Then On ${phone2} verify the softkeys in ${IdleState}
    Then On ${phone1} verify display message ${displayVoiceMail}
    Then press hardkey as ${goodBye} on ${phone1}

561600:TC008: Navigate out of Visual VM details screen using Quit
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan     notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} verify the softkeys in ${voicemailInbox}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press the softkey ${quit} in VoiceMailState
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}


561500: TC01-a: in REPLY, lift handset or Press Speaker or Headset button
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan      notApplicableFor6910
    Given leave voicemail message from ${phone2} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailPassword}
    Then press hardkey as ${scrollright} on ${phone1}
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then on ${phone1} press the softkey ${reply} in VoiceMailState
    Then on ${phone1} press the softkey ${edit} in VoiceMailState
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} press the softkey ${back} in VoiceMailState
    Then press hardkey as ${offHook} on ${phone1}
    Then on ${phone1} verify display message Voicemail
    And press hardkey as ${goodbye} on ${phone1}
    Given delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Given delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}

560629:CHM Custom edit mode-Always option
   [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${always} in ${custom}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    And Press hardkey as ${goodBye} on ${phone1}
   [Teardown]   Default Availability State

558340: Transferred call rings target if Consult on remote hold (Directory)
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then on ${phone1} ${consultiveTransfervp} call to ${phone3} using directory
    Then On ${phone1} verify the softkeys in ${IdleState}
    Then Verify ringing state on ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}

561299: Verify CAS authentication in VM, Directory, History
    [Tags]    Owner:Abhishekkhanchi    Reviewer:       notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} press ${softKey} ${scrollRight} for 1 times
    Then On ${phone1} verify the softkeys in ${voicemailInbox}
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then On ${phone1} verify display message ${save}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${redial} on ${phone1}
    Then On ${phone1} press ${softKey} ${scrollRight} for 2 times
    Then On ${phone1} verify display message ${details}
    Then Press hardkey as ${goodBye} on ${phone1}

757389: Verify opening Options and, without authenticating, quickly navigating, scrolling, and quickly exit
    [Tags]    Owner:Abhishekkhanchi    Reviewer:   notApplicableFor6910
     Given on ${phone1} navigate to ${availability} settings
     Then on ${phone1} press ${hardKey} ${scrolldown} for 5 times
     Then Press hardkey as ${goodBye} on ${phone1}
     Then on ${phone1} navigate to ${diagnostics} settings
     Then on ${phone1} press ${hardKey} ${scrolldown} for 4 times
     Then Press hardkey as ${goodBye} on ${phone1}
     Then on ${phone1} navigate to ${audio} settings
     Then on ${phone1} press ${hardKey} ${scrolldown} for 3 times
     Then Press hardkey as ${goodBye} on ${phone1}
     Then On ${phone1} move to ${timedate} to ${timeZone} settings
     Then Press hardkey as ${goodBye} on ${phone1}
     Then on ${phone1} verify the softkeys in ${idle}

557052: Enter invalid digit length, with call on Hold
    [Tags]    Owner:AbhishekPathak    Reviewer:    invaliddigit_hold
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to press line key ${programkey2} on phone ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then On ${phone2} dial partial number of ${phone3} with ${firsttwo}
    Then on ${phone2} press the softkey ${dial} in DialingState
    Then on ${phone2} verify display message ${backupAutoAttendant}
    Then disconnect the call from ${phone1}
    Then press hardkey as ${goodbye} on ${phone2}

556982: APT - Go off hook from SPEAKER, make call , answer on HANDSET
    [Tags]    Owner:AbhishekPathak    Reviewer:    makecall_speaker_handset
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of speaker as ${on} on ${phone1}
    Then Verify the led state of speaker as ${off} on ${phone2}
    Then disconnect the call from ${phone1}

557246: TC13 - Forward incoming call to another extension's VM
    [Tags]    Owner:AbhishekPathak    Reviewer:    incomingcall_voicemail
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${Transfer} in AnswerState
    Then on ${phone1} dial number ${${pbx}voicemailNumber}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone2} verify display message Voice Mail
    Then Press hardkey as ${goodBye} on ${phone2}

557328: TC001 Make a conference call
    [Tags]    Owner:AbhishekPathak    Reviewer:    make_conference
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

557330: TC003 DUT Drop a call while in conference
    [Tags]    Owner:AbhishekPathak    Reviewer:    make_conference_drop    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${leave}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}

557331: TC005 Receive an incoming call while in Conference
    [Tags]    Owner:AbhishekPathak    Reviewer:    make_conference_ring
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

557332: TC006 Answer the incoming call while in Conference
    [Tags]    Owner:AbhishekPathak    Reviewer:    make_conference_receive
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then I want to press line key ${line2} on phone ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify audio path between ${phone1} and ${phone4}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

557586: Answer a new call while one or more call are on hold using handset
    [Tags]    Owner:AbhishekPathak    Reviewer:    holdcall_newcall
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone3} and ${phone1}
    Then disconnect the call from ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}

558111: Whisper page user on a call, initiation allowed.
    [Tags]    Owner:AbhishekPathak    Reviewer:    whisperpage_initiation_allowed
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to use fac ${whisperPageFAC} on ${phone3} to ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify no audio path from ${phone3} to ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}

558191: TC01-a: Blind Transfer - using the transfer key
    [Tags]    Owner:AbhishekPathak    Reviewer:    blind_transfer_transfer
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone2} to ${phone3} using ${blindTransfer}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone2} verify the softkeys in ${IdleState}
    Then verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${HoldState} on ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then Press hardkey as ${HoldState} on ${phone3}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}

560486: Caller ID displays when cal is transferred (blind)
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer_blind
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Transfer call from ${phone2} to ${phone3} using ${blindTransfer}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone3}

560627: Call Handling mode(CHM) options set to "Out of Office"
    [Tags]    Owner:AbhishekPathak    Reviewer:    call_handling_mode    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${All}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${cancel}
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Press softkey ${Save} on ${phone1}
    Then on ${phone1} press the softkey ${quit} in SettingState
    Then on ${phone2} enter number ${phone1}
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then on ${phone1} navigate to ${availability} settings
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press softkey ${Save} on ${phone1}
    Then on ${phone1} press the softkey ${quit} in SettingState
    [Teardown]    Default Availability State

557566: TO-VM or # (other calls) during UCB call
    [Tags]    Owner:AbhishekPathak    Reviewer:    tovm_ucb_call
    Given on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} dial number ${wrongAccessCode}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} dial number ${accessCode}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then On ${phone2} verify display message ${displayVoiceMail}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}

557978: TC01: Verify that active call can be parked successfully while there is held call
    [Tags]    Owner:AbhishekPathak    Reviewer:    park_active_call    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then i want to press line key ${programkey2} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then I want to Park the call from ${phone1} on ${phone4} using ${default} and ${Park}
    Then verify extension ${number} of ${phone3} on ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

557984: TC07: Verify that held call can be parked successfully
    [Tags]    Owner:AbhishekPathak    Reviewer:    park_held_call    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then disconnect the call from ${phone2}

558297: Divert the incoming call to Target's VM
    [Tags]    Owner:AbhishekPathak    Reviewer:    incomingcall_to_vm    notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then on ${phone1} press the softkey ${ToVm} in Transfertovm
    Then on ${phone3} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    Then on ${phone3} wait for 15 seconds
    Then on ${phone3} Press ${softKey} ${bottomKey1} for 1 times
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}

562333: Phone Power reboots while collecting logs
    [Tags]    Owner:AbhishekPathak    Reviewer:    log_reboot
    Given on ${phone1} navigate to ${diagnostics} settings
    Then on ${phone1} press the softkey ${logIssue} in SettingState
    Then reboot ${phone1}

562353: start button on hide
    [Tags]    Owner:AbhishekPathak    Reviewer:    start
    Given on ${phone1} navigate to ${diagnostics} settings
    Then upload log from ${phone1}
    Then i want to verify on ${phone1} negative display message ${start}
    Then press hardkey as ${goodBye} on ${phone1}

562848: phone receives a call while in False DND or edit mode
    [Tags]    Owner:AbhishekPathak    Reviewer:    false_dnd
    Given on ${phone1} navigate to ${advanced} settings
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}

561463:TC09: Reply
    [Tags]    Owner:AbhishekPathak    Reviewer:    reply    notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then on ${phone2} wait for 20 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${save} in VoiceMailState
    Then on ${phone1} wait for 2 seconds
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
	Then on ${phone1} press the softkey ${savereply} in VoiceMailState
    Then on ${phone1} press the softkey ${start} in VoiceMailState
    Then on ${phone1} wait for 20 seconds
    Then on ${phone1} press the softkey ${stop} in VoiceMailState
    Then on ${phone1} press the softkey ${send} in VoiceMailState
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then on ${phone2} press the softkey ${play} in VoiceMailState
    Then on ${phone2} verify display message ${pause}
    Then Press hardkey as ${goodBye} on ${phone2}

557514: TC014 Check participants list when call dropped by phone itself
    [Tags]    Owner:AbhishekPathak    Reviewer:    conference_dropbyphone    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone3} press the softkey ${conference} in conferencecallstate
    Then on ${phone3} enter number ${phone4}
    Then on ${phone4} wait for 5 seconds
    Then answer the call on ${phone4} using ${line1}
    Then verify audio path between ${phone3} and ${phone4}
    Then on ${phone3} press the softkey ${conference} in conferencecallstate
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone3}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then disconnect the call from ${phone4}

560752: TC011 Placing a call exits to main screen (Conference/transfer)
    [Tags]    Owner:AbhishekPathak    Reviewer:    conference_transfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${conference} in conferencecallstate
    Then On ${phone1} verify display message ${conference}
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${conference}
    Then on ${phone3} wait for 10 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then on ${phone1} verify display message ${transfer}
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${transfer}
    Then on ${phone1} wait for 10 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}


560753: TC012 Placing a call exits to main screen (Transfer)
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then on ${phone1} verify display message ${transfer}
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

557614: With multiple calls, press the HOLD button to hold, unhold
    [Tags]    Owner:AbhishekPathak    Reviewer:    hold1
    Given Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} wait for 4 seconds
    Then i want to make a two party call between ${phone1} and ${phone2} using ${programkey3}
    Then answer the call on ${phone2} using ${line1}
    Then verify the led state of ${line3} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${programkey4}
    Then answer the call on ${phone3} using ${line1}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then i want to press line key ${programkey3} on phone ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then i want to press line key ${programkey4} on phone ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

561597: TC02: new unheard voicemail message number (decrease 1 to 0)
    [Tags]    Owner:AbhishekPathak    Reviewer:    voicemail_messagenumber    notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone2} press the softkey ${ToVm} in RingingState
    Then on ${phone1} wait for 20 seconds
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone2} wait for 5 seconds
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone2}
    Then login into voicemailbox for ${phone2} using ${voicemailpassword}
    Then press hardkey as ${scrollright} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then on ${phone2} press the softkey ${play} in VoiceMailState
    Then on ${phone2} wait for 2 seconds
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}

558164: Auto-Transfer - Consult transfer to Extension via timeout
    [Tags]    Owner:AbhishekPathak    Reviewer:Vikhyat    transfer_timeout
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${timeout}
    Then On ${phone1} verify display message ${transfer}
    Then on ${phone3} wait for 2 seconds
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}

557870: Auto Unmute when an active muted call gets disconnected
    [Tags]    Owner:AbhishekPathak    Reviewer:    mute
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then Verify the led state of mute as ${blink} on ${phone2}
    Then verify one way audio from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone2}
    Then verify the led state of mute as ${off} on ${phone2}

557063: active call is up - user navigates to call history- history button- second incoming call, call goes to VM
    [Tags]    Owner:AbhishekPathak    Reviewer:    CallHistory
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Press the call history button on ${phone2} and folder ${all} and ${nothing}
    Then on ${phone2} verify display message ${callhistory}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then on ${phone3} wait for 50 seconds
    Then on ${phone3} verify display message ${displayVoiceMail}
    Then verify the led state of ${line2} as ${off} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone3}
    Then disconnect the call from ${phone1}

557985: TC08: Verify that a held call among multiple calls on hold can be parked successfully
    [Tags]    Owner:AbhishekPathak    Reviewer:    park    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then verify audio path between ${phone2} and ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone3} and ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${programkey3}
    Then verify audio path between ${phone4} and ${phone1}
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line3} as ${blink} on ${phone1}
    Then I want to Park the call from ${phone1} on ${phone5} using ${hold} and ${park}
    Then on ${phone5} wait for 2 seconds
    Then verify extension ${number} of ${phone4} on ${phone5}
    Then on ${phone4} wait for 2 seconds
    Then verify extension ${number} of ${phone5} on ${phone4}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

560784: TC049 Directory Sort choice persists through phone reset
    [Tags]    Owner:AbhishekPathak    Reviewer:    directory_bylast    notApplicableFor6910
    Given On ${phone1} verify directory with firstname/lastname
    Then Press hardkey as ${Scrollleft} on ${phone1}
    Then on ${phone1} verify display message ${byLast}
    Then reboot ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} verify display message ${byLast}
    Then Press hardkey as ${goodBye} on ${phone1}

560800: TC013 Make an incoming whisper page when phone is on other call
    [Tags]    Owner:AbhishekPathak    Reviewer:    whisper    notApplicableFor6910
    Given i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify directory with ${directoryAction['whisper']} of ${phone2}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify audio path between ${phone3} and ${phone2}
    Then disconnect the call from ${phone1}
    Then press hardkey as ${goodBye} on ${phone3}

560827: for dial VM, should dial users vm when pressed
    [Tags]    Owner:AbhishekPathak    Reviewer:    voicemail    notApplicableFor6910
    Given Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    Then On ${phone1} verify directory with ${directoryAction['dialvoicemail']} of ${phone2}
    Then on ${phone1} wait for 20 seconds
    Then press hardkey as ${goodbye} on ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then On ${phone2} Press The Softkey ${play} In VoiceMailState
    Then verify extension ${number} of ${phone1} on ${phone2}
    And On ${phone2} verify display message ${pause}
    And press hardkey as ${goodBye} on ${phone2}

558015: unpark - directory
    [Tags]    Owner:AbhishekPathak    Reviewer:    unpark    notApplicableFo6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to park the call from ${phone2} on ${phone3} using ${default} and ${park}
    Then on ${phone3} wait for 2 seconds
    Then i want to unpark the call from ${phone3} on ${phone2} using ${directory} and ${select}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone4} using ${loudspeaker}
    Then answer the call on ${phone4} using ${line1}
    Then verify audio path between ${phone3} and ${phone4}
    Then i want to park the call from ${phone2} on ${phone5} using ${default} and ${park}
    Then i want to park the call from ${phone4} on ${phone5} using ${default} and ${park}
    Then verify the led state of ${line1} as ${blink} on ${phone5}
    Then verify the led state of ${line2} as ${blink} on ${phone5}
    Then i want to unpark the call from ${phone5} on ${phone2} using ${directory} and ${select}
    Then Press hardkey as ${ScrollDown} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then disconnect the call from ${phone5}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

561694: TC001: Verify change text from "Passcode" to "Enter Voicemail Password" on VVM screen
    [Tags]    Owner:AbhishekPathak    Reviewer:    vm    notApplicableFor6910
    Given Press hardkey as VoiceMail on ${phone1}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then on ${phone1} verify display message ${login}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${quit}
    Then press hardkey as ${goodbye} on ${phone1}

560897: Call History detail view
    [Tags]    Owner:AbhishekPathak    Reviewer    callHistory    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone1}
    Then press hardkey as ${goodBye} on ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone1}
    Then press hardkey as ${goodBye} on ${phone3}
    Then press the call history button on ${phone1} and folder ${all} and ${nothing}
    Then on ${phone1} verify display message ${All}
    Then on ${phone1} verify display message ${Missed}
    Then on ${phone1} verify display message ${Outgoing}
    Then on ${phone1} verify display message ${Received}
    Then Press softkey ${details} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press the softkey ${cancel} in DialingState
    Then on ${phone1} verify display message ${callhistory}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} verify display message ${callhistory}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press the softkey ${quit} in SettingState

560902: Make an incoming call while being in history screen
    [Tags]    Owner:AbhishekPathak    Reviewer:    history
    Then Press the call history button on ${phone1} and folder ${all} and ${nothing}
    Then on ${phone1} verify display message ${callhistory}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then on ${phone1} verify the softkeys in ${idle}

561495: TC01: REPLY to the originator of the voicemail
    [Tags]    Owner:AbhishekPathak    Reviewer:    voicemail    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then on ${phone2} wait for 20 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${more} in VoiceMailState
    Then on ${phone1} press the softkey ${reply} in VoiceMailState
    Then on ${phone1} press the softkey ${start} in VoiceMailState
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} press the softkey ${stop} in VoiceMailState
    Then on ${phone1} press the softkey ${send} in VoiceMailState
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then on ${phone2} press the softkey ${play} in VoiceMailState
    Then on ${phone2} verify display message ${pause}
    Then Press hardkey as ${goodBye} on ${phone2}


561482: TC03: Softkeys for selected entry of 'Deleted' tab in Visual VM
    [Tags]    Owner:AbhishekPathak    Reviewer:    voicemail_delete    notApplicableFor6910
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then on ${phone2} wait for 20 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${delete} in VoiceMailState
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} verify the softkeys in ${voicemaildelete}
    Then Press hardkey as ${goodBye} on ${phone1}

561307: Phone registered and assigned Assign to different user followed by reboot
    [Tags]    Owner:AbhishekPathak    Reviewer:    assignUser
    [Setup]    Assign Extension Custom Setup
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone1}
    Then Go to assign user on ${phone1} and ${phone2} in ${assigned}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then Press the call history button on ${phone1} and folder ${missed} and ${details}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify the line state as ${IdleState} on ${phone1}
    Then disconnect the call from ${phone3}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then verify audio path between ${phone3} and ${phone1}
    Then disconnect the call from ${phone3}
    Then reboot ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then Go to assign user on ${phone2} and ${phone2} in ${unassigned}
    Then Go to assign user on ${phone1} and ${phone1} in ${unAssigned}
    [Teardown]    Assign Extension Custom Teardown

561309: User pulled from DUT
    [Tags]    Owner:AbhishekPathak    Reviewer:    assignUser    561309    notApplicableFor6910
    [Setup]    Assign Extension Custom Setup
    Then Go to assign user on ${phone2} and ${phone1} in ${assigned}
    Then on ${phone1} verify display message ${assign}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then Go to assign user on ${phone1} and ${phone1} in ${unassigned}
    Then Go to assign user on ${phone2} and ${phone2} in ${unassigned}
    [Teardown]    Assign Extension Custom Teardown


752927:Mailbox Transfer - Transfer 2 calls to Voicemail starting with an active and held call
    [Tags]    Owner:AbhishekPathak    Reviewer:    voicemail    notApplicableFor6910
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then on ${phone1} press the softkey ${Transfer} in AnswerState
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then on ${phone1} enter number ${phone4}
    Then on ${phone1} press the softkey ${tovm} in TransferState
    Then press hardkey as ${holdstate} on ${phone1}
    Then on ${phone3} verify display message ${displayVoiceMail}
    Then on ${phone3} wait for 15 seconds
    Then press hardkey as ${goodbye} on ${phone3}
    Then on ${phone1} press the softkey ${Transfer} in AnswerState
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} enter number ${phone4}
    Then on ${phone1} press the softkey ${tovm} in TransferState
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then on ${phone2} wait for 15 seconds
    Then press hardkey as ${goodbye} on ${phone2}
    Then login into voicemailbox for ${phone4} using ${voicemailpassword}
    Then press hardkey as ${scrollRight} on ${phone4}
    Then verify extension ${number} of ${phone2} on ${phone4}
    Then verify extension ${number} of ${phone3} on ${phone4}
    Then press hardkey as ${goodbye} on ${phone4}


756043:TC01: 'Deleted' tab in Visual VM
    [Tags]    Owner:AbhishekPathak    Reviewer:    voicemail    notApplicableFor6910
    Given Delete voicemail message from deleted folder on ${phone1}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then press hardkey as ${scrolldown} on ${phone1}
    Then press hardkey as ${scrolldown} on ${phone1}
    Then verify voicemail windows ${VMDeleted} icons value as 1 on ${phone1}
    Then press hardkey as ${scrollright} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}


755814:Invalid password not displayed when user enters incorrect pass for user OPTIONS view
    [Tags]    Owner:AbhishekPathak    Reviewer:    assignUser
    [Setup]    Assign Extension Custom Setup
    Given on ${phone1} navigate to Unassign user settings
    Then on ${phone1} verify display message ${available}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} verify display message ${status}
    Then press hardkey as ${goodbye} on ${phone1}
    Then Go to assign user on ${phone1} and ${phone1} in ${unassigned}
    Then Go to assign user on ${phone1} and ${phone2} in ${assigned}
    Then Go to assign user on ${phone2} and ${phone2} in ${unassigned}
    Then Go to assign user on ${phone1} and ${phone1} in ${unassigned}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number ${wrongVoicemailpassword}
    Then on ${phone1} verify display message ${incorrectPassword}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then press hardkey vas ${goodbye} on ${phone1}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number ${voicemailPassword}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${status}
    Then press hardkey as ${goodbye} on ${phone1}
    [Teardown]    Assign Extension Custom Teardown

756695:Error clears while popup shown
    [Tags]    Owner:AbhishekPathak    Reviewer:Aman    popup_message    notApplicableFor6910
    Given Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then on ${phone1} dial number ${wrongVoicemailpassword}
    Then on ${phone1} verify display message ${error}
    Then on ${phone1} verify display message ${enterVoicemailPassword}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    And on ${phone1} verify the softkeys in ${IdleState}

757340:CHM "Custom" Call Forward Mode - No Answer
    [Tags]    Owner:AbhishekPathak    Reviewer:    custom_noanswer    CHM    notApplicableFor6910
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noanswer} in ${custom}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} dial number 1
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${save}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then Press hardkey as ${enter} on ${phone1}
    Then Press softkey ${Save} on ${phone1}
    Then on ${phone1} verify display message ${availability}
    Then Press softkey ${quit} on ${phone1}

    Then on ${phone1} navigate to ${availability} settings
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${voicemailcustom}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 4 times
    Then on ${phone1} enter number ${voicemailcustom}
    Then Press hardkey as ${Scrolldown} on ${phone1}
    Then Press hardkey as ${enter} on ${phone1}
    Then Press softkey ${Save} on ${phone1}
    Then Press softkey ${quit} on ${phone1}
    And Change the phone state to default state on ${phone1}
    [Teardown]    Default Availability State

758215:Verify Dialing screen keys
    [Tags]    Owner:AbhishekPathak    Reviewer:    dial_digits
    Given on ${phone1} dial number 1
    Then on ${phone1} verify display message ${dial}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then press hardkey as ${goodbye} on ${phone1}

799613: Focus points to oldest call
    [Tags]    Owner:AbhishekPathak    Reviewer:    call_focus
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${line1}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${line2}
    Then answer the call on ${phone2} using ${line2}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${programkey3}
    Then answer the call on ${phone2} using ${programkey3}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line3} as ${blink} on ${phone1}

    Then i want to make a two party call between ${phone1} and ${phone2} using ${programkey4}
    Then answer the call on ${phone2} using ${programkey4}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line4} as ${blink} on ${phone1}

    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    Then verify the led state of ${line4} as ${off} on ${phone1}

    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone1}

    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}

752288: Far end internal extn user puts phone on hold remotely
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat     752288
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then on ${phone1} verify display message 01:
    Then verify no audio path from ${phone2} to ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then verify extension ${number} of ${phone1} on ${phone2}
    And disconnect the call from ${phone1}

756014: TC014 MWI LED status pattern for a held call while the phone has unheard voice messages
    [Tags]    Owner:Gaurav    Reviewer:    756014
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then Leave voicemail message from ${phone3} on ${phone1}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then On ${phone1} verify the led state of ${line1} as ${blink} and led color as ${red}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    And disconnect the call from ${phone2}

758232: active call view, consult offering
    [Tags]    Owner:Gaurav    Reviewer:    758232
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then Initiate Transfer on ${phone1} to ${phone3} using ${consult}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${transfer}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone1} verify the led state of ${line1} as ${blink} and led color as ${red}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${transfer}
    then disconnect the call from ${phone2}
    then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

752283: Put multiple calls on hold by answering an incoming call
    [Tags]    Owner:Gaurav    Reviewer:
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line1} as ${on} on ${phone3}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then verify audio path between ${phone1} and ${phone4}
    Then On ${phone4} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then i want to press line key ${programkey4} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then i want to press line key ${programkey3} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then i want to press line key ${programkey2} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then i want to press line key ${programkey1} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    And on ${phone1} verify the softkeys in ${idleState}

755766: Filter updates with latest call history
    [Tags]    Owner:Gaurav    Reviewer:    notApplicableFor6910
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${all} and ${nothing}
    Then on ${phone1} verify display message ${callHistory}
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey4} for 1 times
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey4} for 1 times
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} press the key ${details} in state ${callHistory}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} press the key ${quit} in state ${callHistory}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    And disconnect the call from ${phone2}

756271: Phone Should Display VVM Inbox Messages
    [Tags]    Owner:Gaurav    Reviewer:    756271    notApplicableFor6910
    Given Delete voicemail message on ${save} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify voicemail windows ${VMInbox} icons value as 1 on ${phone1}
    Then verify voicemail windows ${VMSaved} icons value as 0 on ${phone1}
    And press hardkey as ${goodbye} on ${phone1}


756138: TC03: enter mailbox, play VM
    [Tags]    Owner:Gaurav    Reviewer:
    Given leave voicemail message from ${phone2} on ${phone1}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 5 seconds
    Then On ${phone1} verify display message ${displayVoiceMail}
    Then on ${phone1} dial number 1
    Then On ${phone1} verify display message ${drop}
    Then on ${phone1} Wait for 5 seconds
    Then press hardkey as ${goodbye} on ${phone1}
    And On ${phone1} verify the softkeys in ${IdleState}


756090: TC011: Press Call Back key on VVM
    [Tags]    Owner:Gaurav    Reviewer:     756090    notApplicableFor6910
    Given leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${callBack} in VoiceMailState
    Then on ${phone2} press the softkey ${toVm} in RingingState
    Then on ${phone1} Wait for 50 seconds
    Then press hardkey as ${goodbye} on ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then verify voicemail windows ${VMInbox} icons value as 1 on ${phone2}
    Then press hardkey as ${goodbye} on ${phone2}


755342:TC020 From Directory, filter for a user that does not exist using the 5-way nav left arrow.
    [Tags]    Owner:Gaurav    Reviewer:     755342
    Then On ${phone1} verify the softkeys in ${idle}
    Then press hardkey as ${directory} on ${phone1}
    Then On ${phone1} verify display message Directory
    Then on ${phone1} dial number 12345
    Then On ${phone1} verify display message No Matches Found
    Then press hardkey as ${goodbye} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}

127698: Diversion Transfer -Transfer incoming call by changing the focus session
    [Tags]
    Given I want to make a two party call between ${phone1} and ${phone2} using ProgramKey1
    Then Answer the call on ${phone2} using Loudspeaker
    Then I want to make a two party call between ${phone3} and ${phone1} using ProgramKey1
    Then on ${phone1} press the softkey ${ToVm} in RingingState
    Then Transfer call from ${phone1} to ${phone4} using ${blindTransfer}
    Then On ${phone1} verify the softkeys in ${idle}
    Then Disconnect the call from ${phone3}

127699: Diversion Transfer - Transfer incoming call by navigating the focus session
    [Tags]
    Given I want to make a two party call between ${phone1} and ${phone2} using ProgramKey1
    Then Answer the call on ${phone2} using Loudspeaker
    Then I want to make a two party call between ${phone3} and ${phone1} using ProgramKey1
    Then on ${phone1} press the key ScrollUp in state Ringing
    Then Transfer call from ${phone1} to ${phone4} using ${blindTransfer}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}

185816: APT-(Hold alternate) Go off hook from HANDSET,make call,answer on HANDSET
    [Tags]
    Given I want to make a two party call between ${phone1} and ${phone2} using ProgramKey1
    Then Answer the call on ${phone2} using Loudspeaker
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey Line1 of ${phone1} on hold
    Then Put the linekey Line1 of ${phone1} on unhold

139082: TC05: Call Back
    [Tags]    notApplicableFor6910
    Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${CallBack} in VoiceMailState

188579: TC07: More
    [Tags]    notApplicableFor6910
    Given Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${More} in VoiceMailState

188571:TC08: Open
    [Tags]    notApplicableFor6910
    Given Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${Open} in VoiceMailState
    Then on ${phone1} press the softkey ${Cancel} in VoiceMailState

139105: TC01: Move Voicemail to Deleted folder
    [Tags]    notApplicableFor6910
    Given Leave voicemail message from ${phone3} on ${phone1}
    Given Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${Delete} in VoiceMailState
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then on ${phone1} press the softkey ${Open} in VoiceMailState
    Then Verify extension ${number} of ${phone3} on ${phone1}

127730: Consult Transfer
    [Tags]
	Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
	Then Answer the call on ${phone1} using ${programKey1}
	Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
	Then Verify audio path between ${phone3} and ${phone2}
	Then Disconnect the call from ${phone2}

127621 : Phone acts as TransferOR in a blind transfer to an busy extn
    [Tags]
	Given I want to make a two party call between ${phone2} and ${phone1} using ${programKey1}
    When Verify ringing state on ${phone2} and ${phone1}
    Then Answer the call on ${phone1} using ${programKey1}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then On ${phone1} verify display message ${transfer}
	Then on ${phone1} dial number ${${pbx}voicemailNumber}
	Then on ${phone1} press the softkey ${transfer} in TransferState
	Then on ${phone2} verify display message ${displayVoicemail}

798683: Backspace during password entry
    [Tags]    Owner:Vikhyat    Reviewer:    networkSettings    backSpace
    Given Press hardkey as ${menu} on ${phone1}
    Then On ${phone1} enter number 123456
    Then On ${phone1} press the softkey ${backSpace} in SettingState
    Then Press hardkey as ${enter} on ${phone1}
    Then On ${phone1} verify display message ${status}
    And Press hardkey as ${goodBye} on ${phone1}

797664: Assign-Unassign 802.1x enabled phone
    [Tags]    Owner:Vikhyat    Reviewer:    assignUnassign
    Given On ${phone1} move to ${network} to ${802.1x} settings
    Then Change the eap-type to ${eapmd5} in 802.1x settings on ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then on ${phone1} navigate to ${unassignUser} settings
    And I want to verify on ${phone1} negative display message ${phone1}
    [Teardown]    Assign Extension Custom Teardown

756229: CALL HISTORY window focused, VM badge should update
    [Tags]    Owner:Vikhyat    Reviewer:    vmcount
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then verify voicemail windows ${inbox} icons value as 1 on ${phone1}     # need to verify on idle screen (top right corner)
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Press hardkey as ${callersList} on ${phone1}
    Then Leave voicemail message from ${phone3} on ${phone1}
    Then Disconnect the call from ${phone1}
    And verify voicemail windows ${inbox} icons value as 2 on ${phone1}

751614: Connect call with another user then terminate call by putting HANDSET on-hook using hook flash
    [Tags]    Owner:Vikhyat    Reviewer:    terminateCall
    Given Press hardkey as ${offHook} on ${phone1}
    Then On ${phone1} dial number ${phone2}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} verify display message 00:
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${onHook} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone2}
    And On ${phone1} verify the softkeys in ${idleState}

754816: DTMF Digits when User enters Voicemail Password
    [Tags]    Owner:Vikhyat    Reviewer:    voicemail
    Given On ${phone1} dial number #
    Then On ${phone1} enter number ${loginVoicemail}
    Then On ${phone1} Wait for 3 seconds
    Then Press hardkey as ${DialPad8} on ${phone1}
    Then Press hardkey as ${DialPad1} on ${phone1}
    Then On ${phone1} Wait for 3 seconds
    And I want to verify on ${phone1} negative display message ${voiceMailLogin}

756202: Navigate Visual Voicemail
    [Tags]    Owner:Vikhyat    Reviewer:    notApplicableFor6910
    Given Leave voicemail message from ${phone2} on ${phone1}
    Given Leave voicemail message from ${phone2} on ${phone1}
    Given Leave voicemail message from ${phone2} on ${phone1}
    Given Leave voicemail message from ${phone2} on ${phone1}
    Given Leave voicemail message from ${phone3} on ${phone1}

    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} press ${hardkey} ${scrollDown} for 5 times
    Then On ${phone1} verify display message ${phone3}
    Then On ${phone1} press ${hardkey} ${scrollUp} for 5 times
    Then On ${phone1} verify display message ${phone2}
    Then I want to verify on ${phone1} negative display message ${phone3}
    And Press hardkey as ${goodBye} on ${phone1}

797940: Make Me_Conference_003
    [Tags]    Owner:Vikhyat    Reviewer:    Conference
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${line2}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then On ${phone1} press the softkey ${merge} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${line2}
    Then On ${phone1} press the softkey ${merge} in AnswerState
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}

798583: Ping to valid IP (on phone)
    [Tags]    Owner:Vikhyat    Reviewer:    pingTest
    Given on ${phone1} move to ${diagnostics} to ${ping} settings
    Then on ${phone1} Wait for 3 seconds
    Then Enter ${ipaddrstr} on ${phone1} to ${ping} settings
    Then On ${phone1} verify display message ${numberOfPackets}
    And Press hardkey as ${goodBye} on ${phone1}

798407: Place or receive a call during Capture Upload
    [Tags]    Owner:Vikhyat    Reviewer:    incomingCall    logUpload
    Given On ${phone1} move to ${diagnostics} to ${logUpload} settings
    Then On ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then Disconnect the call from ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

756274: Play a VM message
    [Tags]    Owner:Vikhyat    Reviewer:    notApplicableFor6910    voicemailPlay
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} verify the softkeys in ${VoiceMail}
    Then on ${phone1} press the softkey ${play} in VoiceMailState
    Then On ${phone1} verify the softkeys in ${voicemailPlay}
    Then On ${phone1} Wait for 30 seconds
    Then On ${phone1} verify the softkeys in ${VoiceMail}
    And Press hardkey as ${goodBye} on ${phone1}



756914: Log gathering on default Server
    [Tags]    Owner:Milind    Reviewer:Vikhyat
     &{configurationDetails}=    CREATE DICTIONARY    download protocol=FTP    ftp server=10.112.123.105
    ...                           ftp username=anonymous    ftp password=anonymous
    Then Configure parameters on ${phone1} using ${configurationDetails}
    On ${phone1} Delete existing log file from ${ftp} server
    ${ftpServer}=    SET VARIABLE    10*211*43*105
    Given On ${phone1} move to ${diagnostics} to ${diagnosticsServer} settings
    Then On ${phone1} remove existing diagnostic server ip
    Then On ${phone1} enter diagnostic server ip as ${ftpServer}
    Then on ${phone1} press the softkey ${save} in settingstate
    Then on ${phone1} press the softkey ${quit} in settingstate
    Then on ${phone1} move to settings ${diagnostics} to ${logUpload} settings with 1
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} press the softkey ${upload} in Diagnostics ${logUpload} Settings
    Then Verify display message Logs uploaded successfully On ${phone1} within 120 seconds
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify ${phone1} logs downloaded successfully on ${ftp} Server
    Then On ${phone1} Delete existing log file from ${ftp} server

756917: Log gathering through Http Server
    [Tags]    Owner:diag    Reviewer:Vikhyat
    ${httpServer}=    SET VARIABLE    10*211*43*105
    Given On ${phone1} move to ${diagnostics} to ${diagnosticsServer} settings
    Then On ${phone1} remove existing diagnostic server ip
    Then On ${phone1} enter url prefix for ${http} server
    Then On ${phone1} enter diagnostic server ip as ${httpServer}
    Then on ${phone1} press the softkey ${save} in settingstate
    Then on ${phone1} press the softkey ${quit} in settingstate
    Then on ${phone1} move to settings ${diagnostics} to ${logUpload} settings with 1
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} press the softkey ${upload} in Diagnostics ${logUpload} Settings
    Then Verify display message Logs uploaded successfully On ${phone1} within 120 seconds
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify ${phone1} logs downloaded successfully on ${http} Server

756909: Log gathering through TFTP
    [Tags]    Owner:Milind    Reviewer:Vikhyat
    On ${phone1} Delete existing log file from ${tftp} server
    ${tftpServerip}=    On ${phone1} Get this machine ip
    ${tftpServer}=    REPLACE STRING    ${tftpServerip}  .  *
    Given On ${phone1} move to ${diagnostics} to ${diagnosticsServer} settings
    Then On ${phone1} remove existing diagnostic server ip
    Then On ${phone1} enter url prefix for ${tftp} server
    Then On ${phone1} enter diagnostic server ip as ${tftpServer}
    Then On ${phone1} dial number ${ftpServer}
    Then on ${phone1} press the softkey ${save} in settingstate
    Then on ${phone1} press the softkey ${quit} in settingstate
    Then on ${phone1} move to settings ${diagnostics} to ${logUpload} settings with 1
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} press the softkey ${upload} in Diagnostics ${logUpload} Settings
    Then Verify display message Logs uploaded successfully On ${phone1} within 120 seconds
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify ${phone1} logs downloaded successfully on ${ftp} Server
    Then On ${phone1} Delete existing log file from ${tftp} server

#Ringtone
799297: Other Internal Ringtones
    [Tags]    Owner:Milind    Reviewer:Vikyat    notAbplicableFor6910
    Given on ${phone1} move to ${audio} to ${ringTones} settings
    Then On ${phone1} verify display message ${playInt}
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then Verify ${Tones['Dial']} tone is played on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then Verify ${Tones['Dial']} tone is played on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then Verify ${Tones['Dial']} tone is played on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then Verify ${Tones['Dial']} tone is played on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then Verify ${Tones['Dial']} tone is played on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

799295: Play Internal Ringtone
    [Tags]    Owner:Milind    Reviewer:Vikyat    notAbplicableFor6910
    Given on ${phone1} move to ${audio} to ${ringTones} settings
    Then On ${phone1} verify display message ${playInt}
    Then on ${phone1} press ${softKey} ${bottomkey2} for 1 times
    Then Verify ${Tones['Dial']} tone is played on ${phone1}
    And press hardkey as ${goodBye} on ${phone1}

# New Test Cases after 21 jan 2021
884638: Ringback tone
    [Tags]    Owner:Milind   Reviewer:Vikhyat    Ringtone
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify ${Tones[Ringing]} tone is played on ${phone1}
    Then disconnect the call from ${phone1}

751770: TC001 On Active call make one more incoming call
    [Tags]    Owner:Milind   Reviewer:Vikhyat    Ringtone
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 2 seconds
    Then Verify ${Tones[CallWaiting]} tone is played on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

751385: TC003 - Admin can edit the DNS option with DHCP enable on TUI
    [Tags]    Owner:Milind   Reviewer:Vikhyat    DHCP    notApplicableFor6910
    Given on ${phone1} move to ${network} to ${settings} settings
    Then Press hardkey as ${enter} on ${phone1}
    Then on ${phone1} press the softkey ${save} in SettingState
    Then Press hardkey as ${enter} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} move to ${network} to ${settings} settings
    Then on ${phone1} press ${hardKey} ${scrollDown} for 6 times
    Then On ${phone1} verify display message ${backspace}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} move to ${network} to ${settings} settings
    Then Press hardkey as ${enter} on ${phone1}
    Then on ${phone1} press the softkey ${save} in SettingState
    Then Press hardkey as ${goodBye} on ${phone1}

759750: TC01: Idle Screen Translation
    [Tags]    Owner:Milind   Reviewer:Vikhyat
    Given Press hardkey as ${goodBye} on ${phone1}
    Then On ${phone1} verify display message ${phone1}
    Then Verify ${availabilityIcon['available']} state icon on ${phone1}
    Then On ${phone1} verify the softkeys in Idle

#End Milind Test Cases