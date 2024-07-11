"use strict";

/** Helps display the error in the API response. */
function displayAPIError(error) {
    if (error.response) {
        const responseObject = error.response;
        alert(
            `status: ${responseObject.status}\n${
                responseObject.data?.message || responseObject.statusText
            }`
        );
    } else if (error.request) {
        alert("Did not receive a response from the server.");
    } else {
        alert("Error occurred while setting up request.");
    }
}
