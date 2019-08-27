// SIGNUP


function signup(username, password) {
    var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/signup"
    var data = {
        username: username,
        password: password
    }
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        crossDomain: true,
        contentType: 'application/json',
        success: function (data) {
            console.log(JSON.stringify(data, null, 2));
            return true
        },
        error: function (e) {
            // alert("failed" + JSON.stringify(e));
            return false
        }
    });
    return true
}


function signupConfirm(username, code) {

    // SIGNUP/CONFIRM
    var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/signup/confirm"
    var data = {
        username: username,
        code: code
    }

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        crossDomain: true,
        contentType: 'application/json',
        success: function (data) {
            console.log(JSON.stringify(data, null, 2));
        },
        error: function (e) {
            // alert("failed" + JSON.stringify(e));
            return false
        }
    });
    return true
}


// LOGIN

function login(username, password) {
    if (checkCookie("tok")) {
        console.log("user already logged in")
    } else {
        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/login"
        var data = {
            username: username,
            password: password
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            dataType: 'json',
            crossDomain: true,
            contentType: 'application/json',
            success: function (d) {
                setCookie("tok", d["id_token"], 3)
                window.location = "/console"
            },
            error: function (e) {
                return false
            }
        });
    }
    return true
}


// USER
function getUserInfo() {
    if (checkCookie("tok")) {
        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/user"
        $.ajax({
            url: url,
            type: 'GET',
            crossDomain: true,
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + getCookie("tok"))
            },
            statusCode: {
                404: function (e) {
                    // logout()
                },
                200: function (d) {
                    console.log(JSON.stringify(d, null, 2));
                    return d
                }
            },
            error: function (e) {
                // alert("failed" + JSON.stringify(e));
                logout()
            }
        });
    } else {
        console.log("user not signed in")
    }
    return true
}

// USER/UPDATE
function updateUserInfo(account_sid, auth_token, phone_number, screen_name) {
    if (checkCookie("tok")) {

        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/user/update"
        var data = {
            account_sid: account_sid,
            auth_token: auth_token,
            phone_number: phone_number,
            screen_name: screen_name,
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            dataType: 'json',
            crossDomain: true,
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + getCookie("tok"))
            },
            statusCode: {
                404: function (e) {
                    // logout()
                },
                200: function (d) {
                    console.log(JSON.stringify(data, null, 2));

                    // do nothing?
                    // maybe load stuff?
                }
            },
            error: function (e) {
                // alert("failed" + JSON.stringify(e));
                // logout()
            }
            // success: function (data) {
            //     console.log(JSON.stringify(data, null, 2));
            //     return data
            // },
            // error: function (e) {
            //     // alert("failed" + JSON.stringify(e));
            //     return null
            // }
        })

    } else {
        console.log("user not signed in")
        return null
    };
}

function messagePull() {
    if (checkCookie("tok")) {
        // MESSAGE/PULL
        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/message/pull"

        $.ajax({
            url: url,
            type: 'GET',
            crossDomain: true,
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + getCookie("tok"))
            },
            statusCode: {
                404: function (e) {
                    // logout()
                },
                200: function (d) {
                    console.log(JSON.stringify(d, null, 2));

                    // do nothing?
                    // maybe load stuff?
                }
            },
            error: function (e) {
                // alert("failed" + JSON.stringify(e));
                // logout()
            }
            // success: function (data) {
            //     console.log(JSON.stringify(data, null, 2));
            // },
            // error: function (e) {
            //     // alert("failed" + JSON.stringify(e));
            // }
        });

    } else {
        console.log("user not signed in")
    }
}


function messageSend(to, message) {
    if (checkCookie("tok")) {
        // MESSAGE/SEND
        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/message/send"
        var data = {
            to: to,
            message: message,
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            dataType: 'json',
            crossDomain: true,
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + getCookie("tok"))
            },
            statusCode: {
                404: function (e) {
                    // logout()
                    return null
                },
                200: function (d) {
                    console.log(JSON.stringify(data, null, 2));
                    // return d
                    // do nothing?
                    // maybe load stuff?
                    return true
                }
            }
        });
    } else {
        console.log("user not signed in")
        return null
    }
    return true
}

function prank(to) {
    if (checkCookie("tok")) {
        // MESSAGE/PRANK
        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/prank"
        var data = {
            to: to,
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            dataType: 'json',
            crossDomain: true,
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + getCookie("tok"))
            },
            statusCode: {
                404: function (e) {
                    // logout()
                    return null
                },
                200: function (d) {
                    console.log(JSON.stringify(d, null, 2));
                    return d
                    // do nothing?
                    // maybe load stuff?
                }
            }
            // error: function (e) {
            //     // alert("failed" + JSON.stringify(e));
            //     logout()
            // }
        });
    } else {
        console.log("user not signed in")
        return null
    }
}




function checkAuthentication() {
    if (checkCookie("tok")) {
        var url = "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api/login/check"
        $.ajax({
            url: url,
            type: 'GET',
            crossDomain: true,
            // dataType: 'json',
            // contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + getCookie("tok"))
            },
            statusCode: {
                404: function (e) {
                    // logout()

                },
                200: function (d) {
                    console.log(d)
                    // do nothing?
                    // maybe load stuff?
                    // return 
                }
            }
        })
    } 
}

function logout() {
    deleteCookie("tok")
    window.location = "/"
}