document.addEventListener('DOMContentLoaded', function() {

    const chatbotHTML = `
        <div id="chatbot-widget" class="chatbot-collapsed">
            <div class="chatbot-header">
                <span>Chat with our husky 🐺</span>
                <button id="chatbot-toggle">
                    <span class="open-icon">▲</span>
                    <span class="close-icon">▼</span>
                </button>
            </div>
            <div class="chatbot-body">
                <div id="chatbot-messages"></div>
                <div class="chatbot-input-container">
                    <input type="text" id="chatbot-input" placeholder="Ask a question...">
                    <button id="chatbot-send">Send</button>
                </div>
            </div>
        </div>
    `;

    // Inject chatbot HTML into the body
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);
});