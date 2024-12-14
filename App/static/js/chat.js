// Replace with the correct user ID of the receiver
let receiverId = 2; 
const currentUser = document.getElementById('loggedUser').dataset.current_user;

//Connect to WebSocket
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

function updateReceiverId(newId){
    receiverId = newId;
    fetchChatHistory(newId)

}
// Fetch chat history on page load
function fetchChatHistory(receivedId){
    const selectScreen = document.getElementById('select-chat')
    const chatScreen = document.getElementById('screen')
    selectScreen.style.display = 'none';
    chatScreen.style.display = 'block';
    const messageScreen = document.getElementById('messages')
    messageScreen.innerHTML = '';
    //alert(receivedId)

    fetch(`/chat-history/${receivedId}/`)
    .then(response => response.json())
    .then(data => {
        const receiverPicture = document.getElementById('receiverImage');
        const receiverName = document.getElementById('receiverName');
        receiverPicture.src = `${data.receiverImage}`
        receiverName.textContent = `${data.receiverFirstName} ${data.receiverLastName}`
        console.log(data)
        const messagesDiv = document.getElementById('messages');
        data.messages.forEach(msg => {
            const newMessage = document.createElement('div');
            const newSpan = document.createElement('span');
            const msgtime = document.createElement('i');

            //newMessage.classList.add('message');
            newSpan.textContent = `${msg.message}`;
            msgtime.textContent = `${msg.timestamp}`;
            
            // Align messages
            if (msg.sender === currentUser) {  // Replace `currentUser` with the logged-in user's username
                newMessage.classList.add('sender');
                newMessage.appendChild(newSpan);
                newMessage.appendChild(msgtime);
            } else {
                newMessage.classList.add('receiver');
                newMessage.appendChild(msgtime);
                newMessage.appendChild(newSpan);
            }

            messagesDiv.appendChild(newMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        });
    });
}


// Handle incoming WebSocket messages
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // console.log('****************************************')
    // console.log(`${data.senderId}`)
    // console.log(data.senderId==receiverId)
    if (data.senderId == receiverId){
    const messagesDiv = document.getElementById('messages');
    const newMessage = document.createElement('div');
    const newSpan = document.createElement('span');
    const msgtime = document.createElement('i');
    //newMessage.classList.add('message');
    newSpan.textContent = `${data.message}`;
    //newMessage.textContent = `${data.message}`;

    // Align messages
    if (data.sender === currentUser) {
        newMessage.classList.add('sender');
        newMessage.appendChild(newSpan);
    } else {
        newMessage.classList.add('receiver');
        newMessage.appendChild(newSpan);
    }

    messagesDiv.appendChild(newMessage);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
};

// Handle message sending
document.getElementById('sendButton').onclick = function(e) {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;
    const now = new Date(); // Get the current date and time
    const hour = now.getHours(); // Get the current hour (0-23)
    const minute = now.getMinutes(); // Get the current minute (0-59)

    chatSocket.send(JSON.stringify({
        'message': message,
        'receiver_id': receiverId
    }));

    //Appending The Messaage in the Container
    const messagesDiv = document.getElementById('messages');
    const newMessage = document.createElement('div');
    const newSpan = document.createElement('span');
    const msgtime = document.createElement('i');
    newSpan.textContent = `${message}`;
    msgtime.textContent = `${hour}:${minute}`;
    newMessage.classList.add('sender');
    newMessage.appendChild(newSpan);
    newMessage.appendChild(msgtime);
    messagesDiv.appendChild(newMessage);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    messageInput.value = '';
};
