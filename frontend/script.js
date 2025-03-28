document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatbotWidget = document.getElementById('chatbot-widget');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    
    // Show welcome message
    addBotMessage("What's up Husky? I'm Pawsistant 🐾, How can I help today?");

    // Toggle chatbot open/closed
    chatbotToggle.addEventListener('click', function() {
        chatbotWidget.classList.toggle('chatbot-collapsed');
        chatbotWidget.classList.toggle('chatbot-expanded');
    });

    // Also make the entire header clickable when collapsed
    document.querySelector('.chatbot-header').addEventListener('click', function(e) {
        // Prevent toggling twice if the actual toggle button was clicked
        if (e.target !== chatbotToggle && !chatbotToggle.contains(e.target)) {
            chatbotWidget.classList.toggle('chatbot-collapsed');
            chatbotWidget.classList.toggle('chatbot-expanded');
        }
    });

    // Handle send button click
    chatbotSend.addEventListener('click', handleUserMessage);

    // Handle Enter key press
    chatbotInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            handleUserMessage();
        }
    });

    // Process user message
    function handleUserMessage() {
        const userMessage = chatbotInput.value.trim();
        if (userMessage) {
            addUserMessage(userMessage);
            chatbotInput.value = '';

            const loadingMsgId = addBotMessage("Thinking...");

            callLlmApi(userMessage)
                .then(botResponse => {
                    replaceMessage(loadingMsgId, botResponse);
                })
                .catch(error => {
                    replaceMessage(loadingMsgId, "Sorry, I encountered an error. Please try again later.");
                });
        }
    }

    async function callLlmApi(query) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: query })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get response');
        }

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('API Error:', error);
        return "Sorry, I encountered an error. Please try again later.";
    }
}

    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';

        const messageText = document.createElement('div');
        messageText.textContent = text;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();

        messageDiv.appendChild(messageText);
        messageDiv.appendChild(messageTime);

        chatbotMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function addBotMessage(text) {
        const messageId = 'msg-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.id = messageId;

        const messageText = document.createElement('div');
        messageText.textContent = text;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();

        messageDiv.appendChild(messageText);
        messageDiv.appendChild(messageTime);

        chatbotMessages.appendChild(messageDiv);
        scrollToBottom();

        return messageId;
    }

    function replaceMessage(messageId, newText) {
        const messageDiv = document.getElementById(messageId);
        if (messageDiv) {
            const messageText = messageDiv.querySelector('div:not(.message-time)');
            messageText.textContent = newText;
        }
    }

    function getCurrentTime() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    function scrollToBottom() {
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Show chatbot initially
    setTimeout(() => {
        chatbotWidget.classList.remove('chatbot-collapsed');
        chatbotWidget.classList.add('chatbot-expanded');
    }, 1000);
});