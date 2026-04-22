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
function sendMessage() {
    const text = userInput.value.trim();
    if (text === "") return;
    // Add user message
    addMessage(text, "user");
    // Clear input
    userInput.value = "";
    // Simulate bot reply
    setTimeout(() => {
        addMessage("You said: " + text, "bot");
    }, 500);
}
// Event listeners
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
