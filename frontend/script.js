document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatbotWidget = document.getElementById('chatbot-widget');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotSettings = document.getElementById('chatbot-settings');
    const claudeButton = document.getElementById('claude-button');
    const gptButton = document.getElementById('gpt-button');
    const saveSettings = document.getElementById('save-settings');
    
    // Current model setting (default to claude until we fetch from server)
    let currentModel = 'claude';

    // Fetch the current model setting from the server
    async function fetchCurrentModel() {
        try {
            const response = await fetch('/api/get-model');
            if (response.ok) {
                const data = await response.json();
                currentModel = data.model;

                // Update UI to reflect the current model
                if (currentModel === 'claude') {
                    claudeButton.classList.add('active');
                    gptButton.classList.remove('active');
                } else {
                    gptButton.classList.add('active');
                    claudeButton.classList.remove('active');
                }
            }
        } catch (error) {
            console.error('Failed to fetch model setting:', error);
        }
    }

    // Call this immediately to get the current model
    fetchCurrentModel();

    // Handle model button clicks
    claudeButton.addEventListener('click', function() {
        claudeButton.classList.add('active');
        gptButton.classList.remove('active');
        currentModel = 'claude';
    });

    gptButton.addEventListener('click', function() {
        gptButton.classList.add('active');
        claudeButton.classList.remove('active');
        currentModel = 'gpt';
    });

    // Show welcome message
    addBotMessage("What's up Husky? I'm Pawsistant 🐾, How can I help today?");

    // Toggle settings panel
    chatbotToggle.addEventListener('click', function(e) {
        e.stopPropagation();  // Prevent event bubbling
        toggleSettings();
    });

    // Toggle settings panel function
    function toggleSettings() {
        const isSettingsVisible = chatbotSettings.style.display !== 'none';

        if (isSettingsVisible) {
            chatbotSettings.style.display = 'none';
            chatbotMessages.style.display = 'block';
        } else {
            chatbotSettings.style.display = 'block';
            chatbotMessages.style.display = 'none';
        }
    }

    // Function to update the model on the server
    async function updateModelSetting(model) {
        try {
            const response = await fetch('/api/update-model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ model })
            });

            if (!response.ok) {
                console.error('Failed to update model setting');
                return false;
            }
            return true;
        } catch (error) {
            console.error('Error updating model setting:', error);
            return false;
        }
    }

    // Save settings button
    saveSettings.addEventListener('click', function() {
        updateModelSetting(currentModel).then(success => {
            chatbotSettings.style.display = 'none';
            chatbotMessages.style.display = 'block';

            // Notify user about model change
            if (success) {
                addBotMessage(`I'm now using the ${currentModel.toUpperCase()} model. How can I assist you?`);
            } else {
                addBotMessage(`I couldn't update to the ${currentModel.toUpperCase()} model. Please try again later.`);
            }
        });
    });

    // Also make the header clickable when collapsed (except the settings button)
    document.querySelector('.chatbot-header').addEventListener('click', function(e) {
        // Prevent toggling twice if the actual toggle button was clicked
        if (e.target !== chatbotToggle && !chatbotToggle.contains(e.target)) {
            chatbotWidget.classList.toggle('chatbot-collapsed');
            chatbotWidget.classList.toggle('chatbot-expanded');
            
            // If settings are open and we collapse, close settings
            if (chatbotWidget.classList.contains('chatbot-collapsed') && chatbotSettings.style.display !== 'none') {
                chatbotSettings.style.display = 'none';
                chatbotMessages.style.display = 'block';
            }
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
                body: JSON.stringify({ 
                    message: query,
                    model: currentModel // Send model preference to the backend
                })
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

        // Format the text to handle lists and links better
        const formattedText = formatBotResponse(text);
        
        const messageText = document.createElement('div');
        messageText.innerHTML = formattedText; // Use innerHTML to render HTML formatting

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
            // Format the text to handle lists and links better
            const formattedText = formatBotResponse(newText);
            
            const messageText = messageDiv.querySelector('div:not(.message-time)');
            messageText.innerHTML = formattedText; // Use innerHTML for formatted content
        }
    }

    // Helper function to format bot responses
    function formatBotResponse(text) {
        // Convert URLs to hyperlinks
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        let formattedText = text.replace(urlRegex, '<a href="$1" target="_blank">$1</a>');
        
        // Format numbered lists (1. 2. 3. etc)
        formattedText = formattedText.replace(/(\d+\.\s.*?)(?=(?:\d+\.|$))/g, '<p>$1</p>');
        
        // Format bullet points
        formattedText = formattedText.replace(/(\*\s.*?)(?=(?:\*\s|$))/g, '<p>• $1</p>');
        formattedText = formattedText.replace(/\*\s/g, '');
        
        // Format paragraphs with double line breaks
        formattedText = formattedText.replace(/\n\n/g, '</p><p>');
        
        // Wrap the text in paragraph tags if not already
        if (!formattedText.startsWith('<p>')) {
            formattedText = '<p>' + formattedText + '</p>';
        }
        
        return formattedText;
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