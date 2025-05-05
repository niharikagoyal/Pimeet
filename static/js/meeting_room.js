window.onload = function () {
    // 1. Get URL parameters
    function getUrlParams(url) {
        try {
            let urlStr = url.split('?')[1];
            if (!urlStr) return {};
            const urlSearchParams = new URLSearchParams(urlStr);
            const result = Object.fromEntries(urlSearchParams.entries());
            return result;
        } catch (error) {
            console.error('Error parsing URL parameters:', error);
            return {};
        }
    }

    const params = getUrlParams(window.location.href);

    // 2. Get or Generate Meeting ID (Numeric)
    let meetingID = params.meetingID;

    if (!meetingID) {
        // Generate a random numeric meetingID
        meetingID = Math.floor(Math.random() * 1000000).toString(); // Random number between 0 and 999999
        const newURL = `${window.location.pathname}?meetingID=${meetingID}`;
        window.history.replaceState({}, '', newURL); // update URL without reloading
    }

    // 3. Generate random user info
    const userID = Math.floor(Math.random() * 10000) + "";
    const userName = "Guest" + userID; // or use a prompt to ask for name

    // 4. App credentials (Zego)
    const appID = 1891731441;
    const serverSecret = "c84af70bb6466f70685c7bd0234d0d58";
    let kitToken;

    try {
        kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, meetingID, userID, userName);
    } catch (error) {
        console.error('Error generating token:', error);
        alert('Failed to generate meeting token. Please try again.');
        window.location.href = '/dashboard';
        return;
    }

    // 5. Join Room
    try {
        const zp = ZegoUIKitPrebuilt.create(kitToken);
        zp.joinRoom({
            container: document.querySelector("#root"),
            sharedLinks: [{
                name: 'Personal link',
                url: window.location.protocol + '//' + window.location.host + window.location.pathname + '?meetingID=' + meetingID,
            }],
            scenario: {
                mode: ZegoUIKitPrebuilt.VideoConference,
            },
            onJoinRoom: () => {
                console.log('Successfully joined room');

                // Update meeting details on Flask backend after successful room join
                fetch("/update_meeting_id", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        meetingID: meetingID,
                        title: "Live Meeting with " + userName,
                        date: new Date().toISOString().split("T")[0],
                        time: new Date().toTimeString().split(" ")[0]
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status !== "success") {
                        console.error("Failed to update meeting ID:", data.message);
                    } else {
                        console.log("Meeting ID updated successfully");
                    }
                })
                .catch(err => {
                    console.error("Error updating meeting ID:", err);
                });
            },
            onError: (error) => {
                console.error('Failed to join room:', error);
                alert('Failed to join room. Please check your connection and try again.');
            },
            turnOnMicrophoneWhenJoining: true,
            turnOnCameraWhenJoining: true,
            showMyCameraToggleButton: true,
            showMyMicrophoneToggleButton: true,
            showAudioVideoSettingsButton: true,
            showScreenSharingButton: true,
            showTextChat: true,
            showUserList: true,
            maxUsers: 20,
            layout: "Auto",
            showLayoutButton: false,
        });
    } catch (error) {
        console.error('Error joining room:', error);
        alert('Failed to join the meeting. Please try again.');
        window.location.href = '/dashboard';
    }
}

function toggleCompiler() {
    const compiler = document.getElementById("compiler-wrapper");
    compiler.style.display = (compiler.style.display === "none") ? "block" : "none";
}

function compileCode() {
    const sourceCode = document.getElementById("codeEditor").value;
    const languageId = document.getElementById("language").value;

    fetch("https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
            "x-rapidapi-key": "ed7bb7c430mshe89aeedd2fb4acap124b02jsn87f3df2b49d0" // Replace this!
        },
        body: JSON.stringify({
            source_code: sourceCode,
            language_id: languageId
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = data.stdout || data.stderr || "No output.";
    })
    .catch(err => {
        document.getElementById("output").innerText = "Error: " + err.message;
    });
}
