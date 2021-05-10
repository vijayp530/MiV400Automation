*** Settings ***
Resource    ../Variables/BossApiDetails.robot

Library    Collections

*** Keywords ***

Using ${bossPortal} I program ${funcKey} on ${phone} using ${buttonDetails} and extension of ${phone2} and softkey position ${position} with ${extMode}
    CALL METHOD    ${bossPortal}    addProgramableButton    functionKey=${funcKey}    phoneA=${phone}    phoneB=${phone2}    positionValue=${position}    extNo=${extMode}    &{buttonDetails}

Using ${bossPortal} remove the function key on ${phoneA} using ${buttonDetails} and softkey position ${positionValue}
    ${result}    CALL METHOD    ${bossPortal}    removeProgramableButton    phoneA=${phoneA}    positionValue=${positionValue}    &{buttonDetails}


Using ${phone1} pickup call of ${phone2_obj} using ${mode} and ${initiateMode}
    CALL METHOD    ${phone1}    pickup_call    ${phone2}    mode=${mode}    initiateMode=${initiateMode}

Using ${bossPortal} I want to create hunt group user extension with ${buttonDetails}
    ${result}=    CALL METHOD    ${bossPortal}    createHuntGroup    &{buttonDetails}
    APPEND TO LIST    ${hgExtensions}    ${result}
    [Return]    ${result}

Using ${bossPortal} I want to remove hunt group user extension ${number}
    ${result}    CALL METHOD    ${bossPortal}    deleteHuntGroup    number=${number}
    LOG TO CONSOLE    ${result}

Using ${bossPortal} I want to create paging groups using ${buttonDetails}
    ${result}    CALL METHOD    ${bossPortal}    createPagingGroups    &{buttonDetails}
    set to dictionary      ${pgExtensions}    ${buttonDetails['PageListName']}    ${result}
    SLEEP    10s
    LOG TO CONSOLE    ${result}
    [Return]    ${result}


Using ${bossPortal} I want to delete paging groups ${number} and paging extension list ${name}
    ${result}    CALL METHOD    ${bossPortal}    deletePagingGroups    number=${number}    pagingListName=${name}
    LOG TO CONSOLE    ${result}

Using ${bossPortal} I program ${value} Call Appearance button on ${phone1}
    CALL METHOD    ${bossPortal}    removeCallAppearance    user_extension=${phone1}    value=${value}

Using ${bossPortal} I remove unused keys on ${phone1}
    CALL METHOD    ${bossPortal}    addCallAppearance    user_extension=${phone1}

Using ${bossPortal} I want to create Bridge Call Appearance extension using ${buttonDetails}
    ${result}    CALL METHOD    ${bossPortal}    createBCA    &{buttonDetails}
    APPEND TO LIST    ${bcaExtensions}    ${result}
    SLEEP    5s
    [Return]    ${result}

Using ${bossPortal} I want to delete Bridge Call Appearance extension using ${extensionNumber}
    ${result}    CALL METHOD    ${bossPortal}    deleteBCA    ExtensionNumber=${extensionNumber}
    SLEEP    5s
    [Return]    ${result}

Using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    CALL METHOD    ${bossPortal}    configBCA    &{BCAdetails}

Using ${bossPortal} I want to change telephony features values using ${CosFeatures}
    CALL METHOD    ${bossPortal}    cosFeature    &{CosFeatures}

Using ${bossPortal} I want to change Delay after collecting digits value to ${value}
    CALL METHOD    ${bossPortal}    modifyTelephoneOptions    DelayAfterCollectDigits=${value}
    SLEEP    5 seconds

Using ${bossPortal} on ${phone} I want to ${change value} using ${telephonydetails}
    APPEND TO LIST    ${phones}    ${phone}
    ${newPassword}=    SET VARIABLE    ${voicemailpassword}
    RUN KEYWORD IF    "${change value}"=="check voicemail password on next login"    SET SUITE VARIABLE    ${newPassword}
    ...    ELSE IF    "${change value}"=="uncheck voicemail password on next login"    SET SUITE VARIABLE    ${newPassword}

    ${result}    CALL METHOD    ${bossPortal}    modifyTelephoneFeature    phone=${phone}    &{telephonydetails}
    [Return]    ${result}

Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${buttonDetails}
    ${result}    CALL METHOD    ${bossPortal}    createBCA    &{buttonDetails}    value=modify
    APPEND TO LIST    ${bcaExtensions}    ${result}
    [Return]    ${result}
    LOG TO CONSOLE    ${result}

Using ${bossPortal} I want to ${modify} MOH features using ${MOHFeatures}
    CALL METHOD    ${bossPortal}    modifyMusicOnHold    &{MOHFeatures}

Using ${bossPortal} I want to modify usergroups MOH for ${ExecutivesName} with filename ${fileName}
    CALL METHOD    ${bossPortal}    create_modify_usergroups    ExecutivesName=${ExecutivesName}    fileName=${fileName}

Using ${bossPortal} I want to create pickup groups using ${buttonDetails}
    ${result}=    CALL METHOD    ${bossPortal}    createPickupGroups    &{buttonDetails}
    LOG TO CONSOLE     PICKUP GROUP EXTENSION: ${result}
    set to dictionary    ${pickupExtension}    ${buttonDetails['pickupListName']}    ${result}
    sleep   10s
    [Return]    ${result}

Using ${bossPortal} I want to delete pickup groups ${number} and pickup extension list ${name}
    ${result}=    CALL METHOD    ${bossPortal}    deletePickupGroups    number=${number}    pickupListName=${name}
    Log to console    ${result}

Using ${bossPortal} I want to ${change} call control options using ${callControlDetails}
    CALL METHOD    ${bossPortal}    modify_call_control_options   &{callControlDetails}

using ${bossPortal} I want to create user using ${telephonydetails}
    ${result}=    CALL METHOD    ${bossPortal}    createUser    &{telephonydetails}
    APPEND TO LIST    ${newlyCreatedUsers}    ${result}
    [Return]    ${result}

using ${bossPortal} I want to delete extension ${extension}
    call method    ${bossPortal}    deleteUser    extension=${extension}