// pages/page.tsx
'use client'
import Head from 'next/head';
import {FC, useEffect, useRef, useState} from 'react';

type Message = {
    text: string;
    sender: 'ai' | 'human';
};

const Home: FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {text: 'Hello! How can I assist you today?', sender: 'ai'},
    ]);
    const [input, setInput] = useState<string>('');
    const messageEndRef = useRef<HTMLDivElement>(null); // Ref for the end of the messages list

    const handleSendMessage = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() === '') return;

        // Add human message to state
        const humanMessage: Message = {text: input, sender: 'human'};
        setMessages((prevMessages) => [...prevMessages, humanMessage]);
        setInput('');

        // Simulate AI response
        setTimeout(() => {
            const aiMessage: Message = {
                text: 'Thanks for your query! Let me look that up for you.',
                sender: 'ai',
            };
            setMessages((prevMessages) => [...prevMessages, aiMessage]);
        }, 1000);


    };

    // Function to scroll to the bottom of the messages
    const scrollToBottom = () => {
        messageEndRef.current?.scrollIntoView({behavior: 'smooth'});
    };

    // Trigger scroll whenever messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleFlip = (index: number) =>{

        console.log(index)
    }

    return (
        <div className="flex flex-col h-screen">
            <Head>
                <title>Smart Search</title>
                <meta name="description" content="The better way to study"/>
            </Head>



            {/* Main Chat View */}
            <main className="flex-grow flex flex-col items-center bg-gray-100 p-6">
                <div className="w-3/4 bg-white rounded-lg shadow-md p-6 gap-4">
                    {/* Render Messages Dynamically */}
                    {messages.map((message, index) => (
                        <div key={index} className="flex flex-col">
                            <div
                                className={`rounded-lg p-4 w-2/5 ${
                                    message.sender === 'ai'
                                        ? 'bg-gray-200 text-gray-900 self-start'
                                        : 'bg-blue-500 text-white self-end mt-2'
                                }`}
                            >
                                {(message.sender === 'ai' && index != 0) && (
                                    <div>
                                        <button
                                            className="rounded-2xl bg-blue-200 hover:bg-blue-300 p-2 pr-4 pl-4 mb-2"
                                            onClick={() => handleFlip(index)}
                                        >Flip &#x2194;</button>
                                    </div>
                                )}
                                {message.text}
                            </div>
                            {message.sender === 'ai'&&(
                                <div className="border-t border-gray-200 w-full self-start mt-4"></div>
                            )}
                        </div>
                    ))}
                    <div ref={messageEndRef}/>
                </div>

                {/* Input Section */}
                <div className="w-full max-w-3xl mt-4">
                    <form className="flex" onSubmit={handleSendMessage}>
                        <input
                            type="text"
                            placeholder="Type your message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            className="flex-grow border rounded-l-lg px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300 focus:text-blue-500"
                        />
                        <button
                            type="submit"
                            className="bg-blue-500 text-white px-6 py-2 rounded-r-lg hover:bg-blue-600"
                        >
                            Send
                        </button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default Home;
