import React, { useState, useEffect } from 'react';
import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
const chatSocket = new WebSocket('ws://localhost:8030/chat/1')

const Chat = () => {
    const [message, setMessage] = useState('');
    const [chatMessages, setChatMessages] = useState([])

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        setChatMessages((prevMessages) => [...prevMessages, data.message])  
    };

    chatSocket.onopen = function(event) {
        console.log('WebSocket is connected.');
      };

    chatSocket.onclose = function(e) {
        console.error(e);
    };

    const sendMessage = (props) => {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
    }

    const handleMessageChange = (e) => {
        Array.from(chatMessages).map((item)=>console.log(item))
        setMessage(e.target.value);
    };

    return (
        <div>
            <ul>
                {Array.from(chatMessages).map((item, pos) => (
                <li key={pos}>
                    <a>{item}</a>
                </li>
                ))}
            </ul>
            <input type="text" onChange={handleMessageChange}></input>
            <button onClick={() => sendMessage({ message })}>Отправить</button>
        </div>
    );
};


export default Chat