function ChatSection() {
    return (
        <aside className="bg-gray-50 w-2/5 flex flex-col items-start justify-start rounded-2xl p-4 relative">
            {/* chat bubble*/}
            <div className="pt-5 flex justify-center items-center gap-2 absolute left-4 top-2">
                <div className="bg-orange-500/50 py-1 px-3 flex justify-center items-center rounded-lg ">
                    <span className="pr-1 text-orange-800 font-bold">Chat</span>
                    <svg className="fill-orange-800" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 -960 960 960">
                        <path d="M80-80v-720q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H240zm126-240h594v-480H160v525zm-46 0v-480z"/>
                    </svg>
                </div>
            </div>

            {/* TODO: complete the chat section - needs backend*/}
            {/* TODO: Chat Input */}
            <label className='mt-12 w-full'>
                {/* TODO: change it so that it has the temporary text for text input instead of a label!! */}
                Text input: <input name="myInput" className="w-full p-2 border border-orange-300 rounded-md mt-2"/>
            </label>
        </aside>
    );
}

export default ChatSection;
