import { NavLink, useLocation } from 'react-router-dom';
import logo from '../assets/logo.png';
import { Home, MessageCircle, Users, FileText, KeyRound, Clock, ListChecks, Settings, HelpCircle } from 'lucide-react';

const navLinks = [
    { to: '/', label: 'Dashboard', icon: <Home size={20} /> },
    { to: '/chat', label: 'Chat', icon: <MessageCircle size={20} /> },
    { to: '/teams', label: 'Teams', icon: <Users size={20} /> },
    { to: '/roles', label: 'Role Templates', icon: <FileText size={20} /> },
    { to: '/secrets', label: 'Secrets & Config', icon: <KeyRound size={20} /> },
    { to: '/sessions', label: 'Sessions', icon: <Clock size={20} /> },
    { to: '/tasks', label: 'Tasks', icon: <ListChecks size={20} /> },
    { to: '/settings', label: 'Settings', icon: <Settings size={20} /> },
    { to: '/help', label: 'Help', icon: <HelpCircle size={20} /> },
];

export default function Sidebar() {
    const location = useLocation();
    return (
        <aside className="h-screen w-56 bg-gradient-to-b from-[#4FC3F7] to-[#1565C0] text-white flex flex-col shadow-lg border-r border-blue-200">
            <div className="flex flex-col items-center gap-2 px-6 py-6 border-b border-blue-200">
                <img src={logo} alt="Team AI Logo" className="h-12 w-12 rounded mb-2" />
                <span className="text-2xl font-bold tracking-tight">TEAM AI</span>
            </div>
            <nav className="flex-1 py-6 px-2 flex flex-col gap-1">
                {navLinks.map(link => (
                    <NavLink
                        key={link.to}
                        to={link.to}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-4 py-3 rounded-lg transition-all font-medium text-base${isActive ? ' active' : ''}`
                        }
                        end
                    >
                        {link.icon}
                        {link.label}
                    </NavLink>
                ))}
            </nav>
        </aside>
    );
} 