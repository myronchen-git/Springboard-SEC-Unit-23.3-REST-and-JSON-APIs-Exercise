"use strict";

/** Helps display the error in the API response. */
function displayAPIError(error) {
    if (error.response) {
        const errorObject = error.response.data.error;
        alert(`status: ${errorObject.status}\n${errorObject.title}\n${errorObject.message}`);
    } else if (error.request) {
        alert("Did not receive a response from the server.");
    } else {
        alert("Error occurred while setting up request.");
    }
}
