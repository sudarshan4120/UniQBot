document.addEventListener('DOMContentLoaded', function() {
    // Get current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    // 1. Inject header (with current page highlighted)
    const headerHTML = `
        <header>
            <div class="logo">
                <h1>Office Of Global Services @ NEU</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="index.html" ${currentPage === 'index.html' ? 'class="active"' : ''}>Home</a></li>
                    <li><a href="faqs.html" ${currentPage === 'faqs.html' ? 'class="active"' : ''}>FAQs</a></li>
                    <li><a href="f1-students.html" ${currentPage === 'f1-students.html' ? 'class="active"' : ''}>F1-Students</a></li>
                    <li><a href="contact.html" ${currentPage === 'contact.html' ? 'class="active"' : ''}>Contact</a></li>
                </ul>
            </nav>
        </header>
    `;

    // 2. Inject footer
    const footerHTML = `
        <footer>
            <p>&copy; UniQ-Bot DS5500</p>
        </footer>
    `;

    // Insert header at the beginning of body
    document.body.insertAdjacentHTML('afterbegin', headerHTML);

    // Insert footer before the end of body
    document.body.insertAdjacentHTML('beforeend', footerHTML);

    // 3. Inject chatbot widget only if NOT on contact page
    if (currentPage !== 'contact.html') {
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

        // Insert chatbot widget before the end of body
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }
});