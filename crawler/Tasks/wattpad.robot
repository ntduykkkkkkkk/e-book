*** Settings ***
Resource   ../Steps/wattpad/main_steps.robot

*** Test Cases ***
Pulling Content From My Library
    [Tags]   get_all_bhtt
    Log In To Wattpad   ${data['${RESOURCE}']}
    Query By Keyword   bhtt