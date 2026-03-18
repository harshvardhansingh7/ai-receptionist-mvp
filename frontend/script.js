const API_URL = "https://ai-receptionist-mvp.onrender.com/chat";

let sessionId = Math.random().toString(36).substring(7);
let isSpeaking = false;
let callEnded = false;
let recognition = null;

// ✅ Browser support check
if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert("Speech Recognition not supported. Please use Google Chrome.");
}

// 🎤 TEXT TO SPEECH
function speak(text) {
    isSpeaking = true;

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";

    speech.onend = () => {
        isSpeaking = false;

        if (!callEnded) {
            setTimeout(() => listen(), 500);
        } else {
            updateStatus("✅ Call Ended");
        }
    };

    window.speechSynthesis.speak(speech);
}

// 📡 SEND MESSAGE TO BACKEND
async function sendMessage(text) {
    console.log("Sending to backend:", text);

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                session_id: sessionId
            })
        });

        const data = await res.json();

        console.log("AI Response:", data.response);

        // ✅ Show bot message
        addMessage(data.response, "bot");

        // ✅ Detect completion
        if (data.completed) {
    callEnded = true;
}

        speak(data.response);

    } catch (error) {
        console.error("Fetch error:", error);
        updateStatus("❌ Network Error");
    }
}

// 🎧 SPEECH TO TEXT
function listen() {
    if (isSpeaking || callEnded) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        updateStatus("🎤 Listening...");
    };

    recognition.onresult = async function (event) {
        const text = event.results[0][0].transcript;

        console.log("User said:", text);

        updateStatus("You: " + text);

        // ✅ Show user message
        addMessage(text, "user");

        recognition.stop();

        await sendMessage(text);
    };

    recognition.onerror = function (event) {
        console.error("Speech error:", event.error);

        if (!isSpeaking && !callEnded) {
            setTimeout(() => listen(), 1000);
        }
    };

    recognition.start();
}

// 📞 START CALL
function startCall() {
    callEnded = false;
    sessionId = Math.random().toString(36).substring(7);

    clearChat();

    speak("Hello, this is ABC Clinic. How can I help you?");

    setTimeout(() => {
        listen();
    }, 2000);
}

// 💬 ADD MESSAGE TO UI
function addMessage(text, type) {
    const chatBox = document.getElementById("chatBox");

    if (!chatBox) return; // safety

    const msg = document.createElement("div");
    msg.classList.add("message", type);
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 🔄 CLEAR CHAT
function clearChat() {
    const chatBox = document.getElementById("chatBox");
    if (chatBox) chatBox.innerHTML = "";
}

// 🔄 UPDATE STATUS
function updateStatus(text) {
    const status = document.getElementById("status");
    if (status) status.innerText = text;
}
