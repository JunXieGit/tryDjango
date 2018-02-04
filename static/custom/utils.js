/* docCookies function made by Mozilla */
var docCookies = {
    getItem: function (sKey) {
        if (!sKey) {
            return null;
        }
        return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
    },
    setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
        if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) {
            return false;
        }
        var sExpires = "";
        if (vEnd) {
            switch (vEnd.constructor) {
                case Number:
                    sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
                    break;
                case String:
                    sExpires = "; expires=" + vEnd;
                    break;
                case Date:
                    sExpires = "; expires=" + vEnd.toUTCString();
                    break;
            }
        }
        document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
        return true;
    },
    removeItem: function (sKey, sPath, sDomain) {
        if (!this.hasItem(sKey)) {
            return false;
        }
        document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "");
        return true;
    },
    hasItem: function (sKey) {
        if (!sKey) {
            return false;
        }
        return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
    },
    keys: function () {
        var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
        for (var nLen = aKeys.length, nIdx = 0; nIdx < nLen; nIdx++) {
            aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]);
        }
        return aKeys;
    }
};


function callAjax(url, method, callback, callback_context, post) {
    var xmlhttp;
    post = post || '';
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            callback(xmlhttp.responseText, callback_context)
        }
    };

    if (method == 'GET') {
        xmlhttp.open('GET', url, true);
        xmlhttp.send();
    }

    else if (method == 'POST') {
        xmlhttp.open('POST', url, true);
        xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xmlhttp.setRequestHeader("X-CSRFToken", docCookies.getItem('csrftoken'));
        xmlhttp.send(post);
    }
}

function memberId_checker(memberId_checker_url, loading_src, okay_src, bad_src, want_exist) {
    var memberId = document.getElementById('id_memberId').value;
    if (memberId && !window.checker_busy) {
        window.checker_busy = true;
        document.getElementById('id_memberId_checker').src = loading_src;
        var callback_context = {};
        callback_context['okay_src'] = okay_src;
        callback_context['bad_src'] = bad_src;
        callback_context['want_exist'] = want_exist;

        callAjax(memberId_checker_url + '?memberId=' + memberId,
            'GET', memberId_checker_result_callback,
            callback_context);
    }
}

function memberId_checker_result_callback(responseText, context) {
    if (responseText == context['want_exist']) {
        document.getElementById('id_memberId_checker').src = context['okay_src'];
        document.getElementById('id_submit_button').disabled = false;
    }

    else {
        document.getElementById('id_memberId_checker').src = context['bad_src'];
        document.getElementById('id_submit_button').disabled = true;
    }
    window.checker_busy = false;
}

function memberId_delayed_checker(delayTime, memberId_checker_url, loading_src, okay_src, bad_src, want_exist) {
    var currentMemberId = document.getElementById('id_memberId').value;
    setTimeout(function () {
        // Check the value searched is the latest one or not.
        // This will help in figuring out when client stops writing.
        var delayedMemberId = document.getElementById('id_memberId').value;
        if (delayedMemberId == currentMemberId) {
            memberId_checker(memberId_checker_url, loading_src, okay_src, bad_src, want_exist)
        }
    }, delayTime);
}

