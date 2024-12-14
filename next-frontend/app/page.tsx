'use client'
import Head from 'next/head';
import {FC, useEffect, useRef, useState} from 'react';
import ReactMarkdown from 'react-markdown'; // Markdown rendering library
import remarkGfm from 'remark-gfm'; // GitHub Flavored Markdown support
import SyntaxHighlighter from 'react-syntax-highlighter';
import {solarizedlight} from "react-syntax-highlighter/dist/cjs/styles/prism"; // Syntax highlighting
// Code block theme

type Message = {
    text: string;
    sender: 'ai' | 'human';
};

const Home: FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {text: 'Hello! How can I assist you today? You can send Markdown or code!', sender: 'ai'},
    ]);
    const [input, setInput] = useState<string>('');
    const messageEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messageEndRef.current?.scrollIntoView({behavior: 'smooth'});
    };

    const handleSendMessage = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() === '') return;

        // Add the user's message
        const humanMessage: Message = {text: input, sender: 'human'};
        setMessages((prevMessages) => [...prevMessages, humanMessage]);
        setInput('');

        // Simulate AI response with Markdown content
        setTimeout(() => {
            const aiMessage: Message = {
                text: `Here is a Markdown example:\n\n**Bold Text**\n\n*Italic Text*\n\n\`\`\`javascript\nconst greet = () => console.log('Hello, Markdown!');\n\`\`\`\n\n- List item 1\n- List item 2`,
                sender: 'ai',
            };
            setMessages((prevMessages) => [...prevMessages, aiMessage]);
        }, 1000);
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleFlip = (index: number) => {
        console.log(index);
    };

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
                            {/*for the AI response*/}
                            <div
                                className={`rounded-lg p-4 w-2/5 ${
                                    message.sender === 'ai'
                                        ? 'bg-gray-200 text-gray-900 self-start'
                                        : 'bg-blue-500 text-white self-end mt-2'
                                }`}
                            >
                                {/* Flip Button for AI Messages */}
                                {(message.sender === 'ai' && index !== 0) && (
                                    <div>
                                        <button
                                            className="rounded-2xl bg-blue-200 hover:bg-blue-300 p-2 pr-4 pl-4 mb-2"
                                            onClick={() => handleFlip(index)}
                                        >
                                            Flip &#x2194;
                                        </button>
                                    </div>
                                )}
                                {/* AI Message Rendered as Markdown */}
                                {message.sender === 'ai' ? (
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                        components={{
                                            // eslint-disable-next-line @typescript-eslint/no-unused-vars
                                            code({node, inline, className, children, ...props}) {
                                                const match = /language-(\w+)/.exec(className || '');
                                                return !inline && match ? (
                                                    <SyntaxHighlighter
                                                        style={solarizedlight}
                                                        language={match[1]}
                                                        PreTag="div"
                                                        {...props}
                                                    >
                                                        {String(children).replace(/\n$/, '') /* Trim extra newlines */}
                                                    </SyntaxHighlighter>
                                                ) : (
                                                    <code className={className} {...props}>
                                                        {children}
                                                    </code>
                                                );
                                            },
                                        }}
                                    >
                                        {message.text}
                                    </ReactMarkdown>
                                ) : (
                                    <p>{message.text}</p>
                                )}
                            </div>
                            {message.sender === 'ai' && (
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