async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chat-box");

  // Add user message
  addMessage("user", message);
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Add typing indicator
  const typingDiv = addMessage("bot", "⏳ Typing...");

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();
    typingDiv.remove(); // Remove typing
    addMessage("bot", data.reply);
  } catch (error) {
    typingDiv.remove();
    addMessage("bot", "⚠️ Error contacting server.");
  }

  chatBox.scrollTop = chatBox.scrollHeight;
}

// ✅ Escape HTML to prevent XSS attacks
function escapeHTML(text) {
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}

function addMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${sender}-message`;
  
  // Use escaped text to prevent HTML/script injection
  msgDiv.innerHTML = escapeHTML(text);

  const timestamp = document.createElement("div");
  timestamp.className = "timestamp";
  timestamp.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  msgDiv.appendChild(timestamp);
  chatBox.appendChild(msgDiv);

  // ✅ Always scroll to bottom when a new message arrives
  chatBox.scrollTop = chatBox.scrollHeight;

  return msgDiv;
}

// ENTER to Send
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

document.getElementById("send-btn").addEventListener("click", sendMessage);

// Dark mode toggle
document.getElementById("theme-toggle").addEventListener("change", () => {
  document.body.classList.toggle("dark");
});
