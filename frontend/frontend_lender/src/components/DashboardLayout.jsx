import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Package, 
  Settings, 
  LogOut, 
  Shield,
  Bell,
  Search,
  User,
  X,
  Info
} from 'lucide-react';
import { removeToken } from '../lib/auth';

export default function DashboardLayout({ children, lender }) {
  const location = useLocation();
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const menuItems = [
    { icon: LayoutDashboard, label: 'Overview', path: '/' },
    { icon: FileText, label: 'Applications', path: '/applications' },
    { icon: Package, label: 'Loan Schemes', path: '/schemes' },
    { icon: Settings, label: 'Configuration', path: '/settings' },
    { icon: HelpCircle, label: 'Help Center', path: '/help' },
  ];

  const notifications = [
    { id: 1, title: 'New Application', message: 'Aman Deep submitted a loan request.', time: '5 mins ago', type: 'info' },
    { id: 2, title: 'Risk Alert', message: 'High volatility detected in Application #1042.', time: '2 hours ago', type: 'alert' },
  ];

  return (
    <div className="flex min-h-screen bg-[#fcf8fa]">
      {/* Sidebar */}
      <aside className="w-72 bg-white border-r border-gray-100 flex flex-col fixed h-screen z-50">
        <div className="p-8 flex items-center gap-2">
          <Shield className="text-black" size={28} strokeWidth={2.5} />
          <span className="text-xl font-black tracking-tight">GigScore</span>
          <span className="bg-black text-white text-[8px] font-bold uppercase px-1.5 py-0.5 rounded ml-1">Lender</span>
        </div>

        <nav className="flex-1 px-4 py-4">
          <div className="space-y-1">
            {menuItems.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-bold transition-all ${
                    isActive 
                      ? 'bg-black text-white shadow-lg shadow-black/10' 
                      : 'text-gray-400 hover:text-black hover:bg-gray-50'
                  }`}
                >
                  <item.icon size={20} strokeWidth={isActive ? 2.5 : 2} />
                  {item.label}
                </Link>
              );
            })}
          </div>
        </nav>

        <div className="p-4 border-t border-gray-50">
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-bold text-red-500 hover:bg-red-50 transition-all"
          >
            <LogOut size={20} />
            Secure Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-72 p-10">
        {/* Header */}
        <header className="flex items-center justify-between mb-12">
          <form 
            onSubmit={(e) => {
              e.preventDefault();
              if (searchQuery) navigate(`/applications?search=${searchQuery}`);
            }}
            className="relative w-96"
          >
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input 
              type="text" 
              placeholder="Search applications, borrowers..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white border border-gray-100 rounded-xl py-3 pl-12 pr-4 text-sm focus:outline-none focus:border-gray-200 transition-all shadow-sm"
            />
          </form>

          <div className="flex items-center gap-6">
            <div className="relative">
              <button 
                onClick={() => setShowNotifications(!showNotifications)}
                className={`relative w-10 h-10 flex items-center justify-center rounded-xl bg-white border border-gray-100 text-gray-400 hover:text-black transition-all ${showNotifications ? 'border-gray-300 text-black' : ''}`}
              >
                <Bell size={20} />
                <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
              </button>

              {showNotifications && (
                <div className="absolute right-0 mt-3 w-80 bg-white border border-gray-100 rounded-2xl shadow-2xl overflow-hidden z-50 animate-in fade-in zoom-in duration-200">
                  <div className="p-4 border-b border-gray-50 flex items-center justify-between">
                    <h3 className="font-black text-xs uppercase tracking-widest text-gray-400">Institutional Alerts</h3>
                    <button onClick={() => setShowNotifications(false)}><X size={14} className="text-gray-400" /></button>
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    {notifications.map(n => (
                      <div key={n.id} className="p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors cursor-pointer">
                        <div className="flex gap-3">
                          <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${n.type === 'alert' ? 'bg-red-50 text-red-600' : 'bg-black text-white'}`}>
                            <Info size={14} />
                          </div>
                          <div>
                            <p className="text-[11px] font-black text-gray-900 uppercase tracking-tighter">{n.title}</p>
                            <p className="text-xs text-gray-500 mt-0.5 leading-snug font-medium">{n.message}</p>
                            <p className="text-[9px] font-bold text-gray-400 uppercase mt-2">{n.time}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="p-3 bg-gray-50 text-center">
                    <button className="text-[10px] font-black uppercase tracking-widest text-gray-500 hover:text-black transition-all">Audit Trail Log</button>
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex items-center gap-3 pl-6 border-l border-gray-100">
              <div className="text-right">
                <p className="text-sm font-black text-gray-900">{lender?.name || 'Lender Console'}</p>
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{lender?.institution_name || 'Verified Institution'}</p>
              </div>
              <Link 
                to="/settings"
                className="w-10 h-10 rounded-xl bg-gray-900 flex items-center justify-center text-white text-xs font-black hover:bg-gray-800 transition-all shadow-xl shadow-black/10 active:scale-95"
              >
                <User size={20} />
              </Link>
            </div>
          </div>
        </header>

        {children}
      </main>
    </div>
  );
}
