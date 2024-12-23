// Function to start the video stream
function startStream() {
    document.getElementById("video").src = "/start_stream";
}

// Function to stop the video stream
function stopStream() {
    fetch("/stop_stream", { method: "POST" })
        .then(response => response.text())
        .then(data => {
            alert(data);  // Show the stop stream confirmation
            document.getElementById("video").src = "";  // Remove the video feed
        });
}

async function verifyFace() {
    try {
        // Start the verification process
        const response = await fetch('/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Parse the response
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        // Display the verification status
        if (data.status) {
            if (data.status === "Unknown face detected! ALERT!") {
                alert(data.status); // Show an alert for unknown face
            } else {
                console.log(data.status); // Log matched face status
            }
        } else {
            console.error("Unexpected response:", data);
        }
    } catch (error) {
        console.error("Error verifying face:", error);
    }
}

function detectFace() {
    fetch("/detect_face", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.faces) {
                const facesList = document.getElementById("faces");
                facesList.innerHTML = "";
                data.faces.forEach(face => {
                    const img = document.createElement("img");
                    img.src = `detected_faces/${face}`;
                    img.style.border = "2px solid black";
                    img.style.margin = "10px";
                    img.style.width = "100px";
                    facesList.appendChild(img);
                });
            }
        })
        .catch(error => console.error("Error:", error));
}