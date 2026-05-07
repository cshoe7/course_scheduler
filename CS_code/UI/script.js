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
        const response = await fetch("http://localhost:8000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        botMsg.textContent = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            botMsg.textContent += decoder.decode(value);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
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
