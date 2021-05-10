*** Settings ***

Library    ../lib/WebUIComponent.py    WITH NAME    UI
Library    Collections

*** Keywords ***
Using ${PhoneWUI} log into ${phone} URL
    CALL METHOD    ${PhoneWUI}    loginWebUI    phone=${phone}

Using ${PhoneWUI} log into ${phone} URL with ${password}
    CALL METHOD    ${PhoneWUI}    loginWebUI    phone=${phone}    password=${password}

Using ${PhoneWUI} log securely into ${phone} URL
    CALL METHOD    ${PhoneWUI}    loginWebUI    phone=${phone}    secured=True

Using ${PhoneWUI} Navigate to go to ${option} page on ${phone} URL
    CALL METHOD    ${PhoneWUI}     goToSection    option=${option}

Using ${PhoneWUI} log into ${phone} URL with ${username} user
    CALL METHOD    ${PhoneWUI}    loginWebUI    phone=${phone}    UserName=${username}

Using ${PhoneWUI} log securely into ${phone} URL with ${username} user
    CALL METHOD    ${PhoneWUI}    loginWebUI    phone=${phone}    secured=True    UserName=${username}

Using ${PhoneWUI} logoff ${phone} URL
    CALL METHOD    ${PhoneWUI}    LogOff

Using ${PhoneWUI} click on the ${option} on ${phone} URL
    CALL METHOD    ${PhoneWUI}     click   ${option}

Close the browser window
    CALL METHOD    ${PhoneWUI}    closeWindow

Verify ${checkbox} is ${value} for ${option}
    CALL METHOD   ${PhoneWUI}   isChecked    option=${option}    value=${value}

Verify the ${filename} file is downloaded
    CALL METHOD  ${PhoneWUI}    verifyFileDownloaded    fileName=${filename}

Read the downloaded ${filename} file of ${phone}
    CALL METHOD    ${PhoneWUI}    verifyFileContents    fileName=${filename}    phone=${phone}

Upload the ${filename} file on ${phone1}
    CALL METHOD  ${PhoneWUI}   uploadFile   fileName=${filename}

Go to the ${option} option and select the ${value} value
    CALL METHOD  ${PhoneWUI}    selectOption    option=${option}    value=${value}

Using ${PhoneWUI} ${fullyORpartial} unregister ${lineNumber} of ${phone}
    CALL METHOD    ${PhoneWUI}    unRegisterPhone    lineToUnregister=${lineNumber}    phone=${phone}    deleteLimit=${fullyORpartial}

Using ${PhoneWUI} register ${line} of ${phone1} with ${phone2}
    APPEND TO LIST    ${phonesToOpen}    ${phone1}
    CALL METHOD    ${PhoneWUI}    registerPhone    linesToRegister=${line}    phoneToOpen=${phone1}    phoneToEnter=${phone2}    pbx=${pbx}

Using ${PhoneWUI} register ${startLine} to ${endLine} of ${phone1} with ${phone2}
    APPEND TO LIST    ${phonesToOpen}    ${phone1}
    CALL METHOD    ${PhoneWUI}    registerPhone    linesToRegister=${line}    phoneToOpen=${phone1}    phoneToEnter=${phone2}    pbx=${pbx}

Using ${PhoneWUI} verify ${line} is registered on ${phone}
    CALL METHOD    ${PhoneWUI}    verifyRegisteredLine    lineToVerify=${line}    phone=${phone}

Using ${PhoneWUI} verify ${element} is present on ${phone} URL
    CALL METHOD    ${PhoneWUI}    verifyElementIsFound    ${element}

Using ${PhoneWUI} verify ${element} is not present on ${phone} URL
    CALL METHOD    ${PhoneWUI}    verifyElementNotFound    ${element}

Using ${PhoneWUI} send ${value} value for ${option} to ${phone} URL
    CALL METHOD    ${PhoneWUI}    sendKeys      value=${value}    option=${option}

Verify text ${value} for ${option} on the ${phone} URL
    CALL METHOD    ${PhoneWUI}    verifyText    value=${value}    option=${option}

Verify ${phoneParameter} of ${phoneA} for ${option} on the ${phoneB} URL
    CALL METHOD    ${PhoneWUI}    verifyText    value=${phoneParameter}    verifiedPhone=${phoneA}    option=${option}

using ${PhoneWUI} select the ${option} and upload file ${fileName} on ${phone1} URL
     CALL METHOD    ${PhoneWUI}    sendFileToUpload     option=${option}    fileName=${fileName}

Adding ${parameter} parameter to ${fileName} CFG file
    CALL METHOD    ${PhoneWUI}    addParamtersToCfgfile    fileName=${fileName}    parameter=${parameter}

Verify ${url} opened on the browser window
    CALL METHOD    ${PhoneWUI}    verifyOpenedURL    url=${URL}

Using ${PhoneWUI} Start the capture on ${portNumber} port with ${hours} hours timeout on ${phone} URL
    CALL METHOD    ${PhoneWUI}    capturePackets      action=Start    portNumber=${portNumber}    phoneObj=${phone}
    ...                           timeout=${hours}

Using ${PhoneWUI} Start the capture on ${portNumber} port on ${phone} URL
    CALL METHOD    ${PhoneWUI}    capturePackets    action=Start    portNumber=${portNumber}    phoneObj=${phone}

Using ${PhoneWUI} ${stopORDownload} the capture from ${phone} URL
    CALL METHOD    ${PhoneWUI}    capturePackets      action=${stopORDownload}    phoneObj=${phone}

Verify ${element} is clickable on the ${phone1} URL
    CALL METHOD    ${PhoneWUI}    verifyElementIsClickable    element=${element}    clickable=True

Verify ${element} is not clickable on the ${phone1} URL
    CALL METHOD    ${PhoneWUI}    verifyElementIsClickable    element=${element}    clickable=False

Verify ${text} option is not present on the Web UI of ${phone}
    CALL METHOD    ${PhoneWUI}    verifyTextNotPresent    text=${text}

Using ${PhoneWUI} Get MAC Address of ${phone}
    ${macAddress}    CALL METHOD    ${PhoneWUI}    getMACAddress    ${phone}
    [Return]    ${macAddress}

Verify text ${value} is present on the Web UI of ${phone}
    CALL METHOD    ${PhoneWUI}    verifyText    value=${value}    OnPage=True

Using ${PhoneWUI} Get text of ${element} on the Web UI of ${phone}
    ${textValue}    CALL METHOD    ${PhoneWUI}    getTextValue    ${element}
    Log  ${textValue}
    [Return]    ${textValue}