// Get elements
const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Function to add a message to the chat
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.textContent = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll
}

// Function to handle sending messages
async function sendMessage() {
    // reads in text from text box
    const text = userInput.value.trim();
    if (text === "") return;
    // Add user message
    addMessage(text, "user");
    // Clear input
    userInput.value = "";
    // Create the bot bubble up front so we can stream into it
    const botMsg = document.createElement("div");
    botMsg.classList.add("message", "bot");
    botMsg.textContent = "...";
    chatWindow.appendChild(botMsg);

    try {
        // sends POST request to FastAPI
        const response = await fetch("http://localhost:8000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            // turns body into JSON string in the format defined in main
            body: JSON.stringify({ message: text })
        });

        // reads response as it arrives
        const reader = response.body.getReader();
        // converts raw binary chunks into readable strings
        const decoder = new TextDecoder();
        //clears ... fromm earlier
        botMsg.textContent = "";

        let raw = "";
        while (true) {
            // waits for next chunk, returns
            // done true when stream ends, value is binary chunk
            const { done, value } = await reader.read();
            //when stream done, converts markdown into HTML
            if (done) {
                botMsg.innerHTML = marked.parse(raw); // only parse when fully done
                break;
            }
            // decondes binary chunk, appends to raw
            raw += decoder.decode(value);
            // updates w/ text on every chunk, gives typing effect
            botMsg.textContent = raw;
            //autoscrolling as content appears
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    // if anything throws, friendly message outputted for the UI and error message in console
    } catch (err) {
        botMsg.textContent = "Something went wrong. Please try again.";
        console.error(err);
    }
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
