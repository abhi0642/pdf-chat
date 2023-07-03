// Get the chat form and messages container
const chatForm = document.getElementById('chat-form');
const messagesContainer = document.querySelector('.messages');

// Event listener for submitting the chat form
chatForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent form submission

    // Get user input message
    const userInput = document.getElementById('message-input').value;

    // Clear the input field
    document.getElementById('message-input').value = '';

    // Display user message in the chat
    displayMessage('user', userInput);

    // Send user message to the server
    sendMessage(userInput);
});

// Function to send user message to the server
function sendMessage(message) {
    // Make an AJAX request to the server
