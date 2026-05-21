import React, { useState } from 'react';
import { Search, Bell, Settings, X, Info } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';

export default function Header({ user }) {
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const notifications = [
    { id: 1, title: 'Risk Alert', message: 'GigScore updated after Zomato sync.', time: '2 mins ago', type: 'alert' },
    { id: 2, title: 'System', message: 'Platform data connection verified.', time: '1 hour ago', type: 'info' },
  ];

  return (
    <header className="bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center h-16 px-6 w-full ml-64 max-w-[calc(100%-16rem)] z-50 sticky top-0">
      <div className="flex items-center">
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            if (searchQuery) navigate(`/predict?search=${searchQuery}`);
          }}
          className="relative w-64"
        >
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input 
            className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border-none rounded-md text-sm focus:ring-1 focus:ring-gray-300 dark:focus:ring-gray-700 transition-all outline-none" 
            placeholder="Search records..." 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </form>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative">
          <button 
            onClick={() => setShowNotifications(!showNotifications)}
            className={`text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors duration-200 p-2 rounded-full active:opacity-80 ${showNotifications ? 'bg-gray-50' : ''}`}
          >
            <Bell size={20} />
            <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-white border border-gray-100 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
              <div className="p-4 border-b border-gray-50 flex items-center justify-between">
                <h3 className="font-black text-sm uppercase tracking-widest">Intelligence Alerts</h3>
                <button onClick={() => setShowNotifications(false)}><X size={14} className="text-gray-400" /></button>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {notifications.map(n => (
                  <div key={n.id} className="p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors cursor-pointer">
                    <div className="flex gap-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${n.type === 'alert' ? 'bg-red-50 text-red-600' : 'bg-blue-50 text-blue-600'}`}>
                        <Info size={14} />
                      </div>
                      <div>
                        <p className="text-xs font-bold text-gray-900">{n.title}</p>
                        <p className="text-[11px] text-gray-500 mt-0.5">{n.message}</p>
                        <p className="text-[9px] font-bold text-gray-400 uppercase mt-1.5">{n.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-3 bg-gray-50 text-center">
                <button className="text-[10px] font-black uppercase tracking-widest text-gray-500 hover:text-black transition-all">View All Activity</button>
              </div>
            </div>
          )}
        </div>

        <Link 
          to="/settings"
          className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors duration-200 p-2 rounded-full active:opacity-80"
        >
          <Settings size={20} />
        </Link>
        
        <div className="flex items-center gap-3 ml-2 border-l pl-4 border-gray-100 dark:border-gray-800">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-bold leading-tight">{user?.name || 'Guest'}</p>
            <p className="text-[10px] text-gray-500 uppercase tracking-tighter">Gig Analyst</p>
          </div>
          <div className="h-8 w-8 rounded-full overflow-hidden bg-gray-100 border border-gray-200">
            <img 
              alt="Gig Worker User Profile" 
              className="w-full h-full object-cover" 
              src={`https://ui-avatars.com/api/?name=${user?.name || 'User'}&background=000&color=fff`}
            />
          </div>
        </div>
      </div>
    </header>
  );
}
