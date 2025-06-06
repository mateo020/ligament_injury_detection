import { NavigateFunction } from 'react-router-dom';

type HeaderProps = {
  navigate: NavigateFunction;
};

function Header({ navigate }: HeaderProps) {
    return (
        <header className="absolute top-4 left-8 font-bold text-4xl z-50 m-0 p-0 ">
            <button 
                onClick={() => navigate('/')}
                className="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md px-6 font-medium duration-500"
            >
                <div className="translate-x-0 opacity-100 transition group-hover:-translate-x-[150%] group-hover:opacity-0">
                    ACL Ligament Helper
                </div>
                <div className="absolute translate-x-[150%] opacity-0 transition group-hover:translate-x-0 group-hover:opacity-100">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-13 w-14">
                        <path d="M2.25 12L11.2045 3.04549C11.6438 2.60615 12.3562 2.60615 12.7955 3.04549L21.75 12M4.5 9.75V19.875C4.5 20.4963 5.00368 21 5.625 21H9.75V16.125C9.75 15.5037 10.2537 15 10.875 15H13.125C13.7463 15 14.25 15.5037 14.25 16.125V21H18.375C18.9963 21 19.5 20.4963 19.5 19.875V9.75M8.25 21H16.5" stroke="#0F172A" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>
            </button>
        </header>
    );
}

export default Header;
