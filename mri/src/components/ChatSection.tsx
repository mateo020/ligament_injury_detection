import { useState, useEffect, useRef } from 'react';

function ChatSection() {
    const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; text: string }[]>([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        setMessages(prev => [...prev, { sender: 'user', text: input }]);

        // Simulated response, change in backend later
        setTimeout(() => {
            setMessages(prev => [...prev, { sender: 'bot', text: `I received "${input}"` }]);
        }, 500);

        setInput('');
    };

    // Scroll to bottom on new message
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // ...

    return (
        <aside className="bg-gray-50 w-2/5 flex flex-col items-start justify-start rounded-2xl p-4 relative h-[600px]">
            {/* Chat header */}
            <div className="pt-5 flex justify-center items-center gap-2 absolute left-4 top-2">
                <div className="bg-orange-500/50 py-1 px-3 flex justify-center items-center rounded-lg ">
                    <span className="pr-1 text-orange-800 font-bold">Chat</span>
                    <svg className="fill-orange-800" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 -960 960 960">
                        <path d="M80-80v-720q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H240zm126-240h594v-480H160v525zm-46 0v-480z"/>
                    </svg>
                </div>
            </div>

            {/* Messages */}
            <div className="mt-16 mb-4 w-full flex-1 overflow-y-auto space-y-2 pr-2">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm shadow 
                            ${msg.sender === 'user' 
                                ? 'bg-blue-500 text-white self-end rounded-br-none ml-auto' 
                                : 'bg-gray-300 text-gray-800 self-start rounded-bl-none mr-auto'}`}
                    >
                        {msg.text}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="w-full mt-auto">
                <input
                    name="message"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Message..."
                    className="w-full p-2 border border-orange-300 rounded-md"
                />
            </form>
        </aside>
    );

}

export default ChatSection;
