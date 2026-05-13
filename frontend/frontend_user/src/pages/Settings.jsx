import React, { useState, useEffect } from 'react';
import { 
  User, 
  Shield, 
  Lock, 
  Bell, 
  Database,
  CloudLightning,
  ChevronRight,
  LogOut,
  Save,
  Loader2,
  CheckCircle,
  Key,
  Smartphone,
  Eye,
  Trash2,
  RefreshCw,
  X,
  AlertTriangle
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import { removeToken } from '../lib/auth';
import DashboardLayout from '../components/DashboardLayout';
import { useNavigate } from 'react-router-dom';

export default function SettingsPage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('profile');
  const [modal, setModal] = useState(null);
  
  // Notification States
  const [notifications, setNotifications] = useState({
    'GigScore Updates': true,
    'Platform Sync Alerts': true,
    'Loan Status Notifications': true,
    'Security Alerts': true
  });

  const navigate = useNavigate();

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await apiRequest('/auth/me');
        setUser(response);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchUser();
  }, []);

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const handleSave = (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    setTimeout(() => {
      setSaving(false);
      setMessage('Settings updated successfully.');
    }, 800);
  };

  const executeAction = () => {
    setSaving(true);
    setTimeout(() => {
      setSaving(false);
      setModal(null);
      setMessage(`${modal.title} successfully executed.`);
    }, 1500);
  };

  const toggleNotification = (label) => {
    setNotifications(prev => ({
      ...prev,
      [label]: !prev[label]
    }));
    setMessage(`Preference for "${label}" ${!notifications[label] ? 'enabled' : 'disabled'}.`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin text-gray-400" size={40} />
      </div>
    );
  }

  const tabs = [
    { id: 'profile', label: 'Profile Information', icon: User },
    { id: 'security', label: 'Security & Auth', icon: Lock },
    { id: 'data', label: 'Data Management', icon: Database },
    { id: 'notifications', label: 'Notifications', icon: Bell },
  ];

  return (
    <DashboardLayout user={user}>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Account & Privacy</h1>
        <p className="text-gray-500 text-lg font-medium">Control your digital identity and risk data preferences.</p>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Left Nav */}
        <div className="col-span-12 lg:col-span-3 space-y-2">
          {tabs.map((item) => (
            <button 
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between p-4 rounded-2xl text-sm font-bold transition-all ${activeTab === item.id ? 'bg-black text-white shadow-xl shadow-black/10' : 'text-gray-400 hover:bg-gray-100 hover:text-black'}`}
            >
              <div className="flex items-center gap-3">
                <item.icon size={18} />
                {item.label}
              </div>
              <ChevronRight size={14} className={activeTab === item.id ? 'text-white' : 'text-gray-300'} />
            </button>
          ))}
          
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 p-4 rounded-2xl text-sm font-bold text-red-500 hover:bg-red-50 transition-all mt-8"
          >
            <LogOut size={18} />
            Secure Logout
          </button>
        </div>

        {/* Content Area */}
        <div className="col-span-12 lg:col-span-9">
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden min-h-[500px]">
             <div className="p-8 border-b border-gray-50 flex items-center justify-between bg-gray-50/30">
                <div className="flex items-center gap-3">
                   {activeTab === 'profile' && <Shield className="text-black" size={24} />}
                   {activeTab === 'security' && <Lock className="text-black" size={24} />}
                   {activeTab === 'data' && <Database className="text-black" size={24} />}
                   {activeTab === 'notifications' && <Bell className="text-black" size={24} />}
                   <h3 className="text-xl font-black text-gray-900">
                     {tabs.find(t => t.id === activeTab)?.label}
                   </h3>
                </div>
                {message && (
                  <div className="flex items-center gap-2 text-green-600 text-xs font-bold bg-green-50 px-4 py-2 rounded-xl animate-in fade-in slide-in-from-top-1">
                    <CheckCircle size={14} /> {message}
                  </div>
                )}
             </div>

             <div className="p-10">
                {activeTab === 'profile' && (
                  <form onSubmit={handleSave} className="space-y-8 animate-in fade-in slide-in-from-right-4">
                    <div className="flex items-center gap-8 mb-10">
                       <div className="w-24 h-24 rounded-3xl bg-gray-900 flex items-center justify-center text-white text-3xl font-black shadow-2xl shadow-black/20">
                          {user?.name?.[0]}
                       </div>
                       <div>
                          <h4 className="text-xl font-black text-gray-900">{user?.name}</h4>
                          <p className="text-sm font-medium text-gray-400">Identity verified via PAN Protocol</p>
                          <button type="button" onClick={() => alert('Avatar upload interface coming soon.')} className="mt-2 text-xs font-black uppercase tracking-widest text-black hover:underline">Change Avatar</button>
                       </div>
                    </div>

                    <div className="grid grid-cols-2 gap-8">
                       <div className="flex flex-col gap-2">
                          <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Full Legal Name</label>
                          <input 
                             type="text" 
                             defaultValue={user?.name}
                             className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-900 focus:outline-none focus:border-black transition-all"
                          />
                       </div>
                       <div className="flex flex-col gap-2">
                          <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Email Address</label>
                          <input 
                             type="email" 
                             defaultValue={user?.email}
                             disabled
                             className="w-full bg-gray-100 border border-gray-50 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-400 cursor-not-allowed"
                          />
                       </div>
                    </div>

                    <div className="pt-8 flex justify-end">
                       <button 
                          type="submit"
                          disabled={saving}
                          className="bg-black text-white px-8 py-4 rounded-2xl font-black flex items-center gap-3 hover:bg-gray-800 transition-all shadow-xl shadow-black/10 active:scale-[0.98] disabled:opacity-50"
                       >
                          {saving ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
                          {saving ? 'Processing...' : 'Save Preferences'}
                       </button>
                    </div>
                  </form>
                )}

                {activeTab === 'security' && (
                  <div className="space-y-8 animate-in fade-in slide-in-from-right-4">
                    <div className="space-y-6">
                      <div className="flex items-center justify-between p-6 bg-gray-50 rounded-2xl border border-gray-100">
                        <div className="flex gap-4">
                          <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center shadow-sm">
                            <Key size={20} className="text-black" />
                          </div>
                          <div>
                            <p className="text-sm font-black text-gray-900">Change Password</p>
                            <p className="text-xs text-gray-400 font-medium">Update your account password for better security.</p>
                          </div>
                        </div>
                        <button 
                          onClick={() => setModal({ type: 'password', title: 'Change Password', desc: 'Please enter your new password to secure your institutional account.' })}
                          className="px-4 py-2 border border-gray-200 rounded-lg text-xs font-black uppercase tracking-widest hover:bg-white transition-all"
                        >
                          Update
                        </button>
                      </div>

                      <div className="flex items-center justify-between p-6 bg-gray-50 rounded-2xl border border-gray-100">
                        <div className="flex gap-4">
                          <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center shadow-sm">
                            <Smartphone size={20} className="text-black" />
                          </div>
                          <div>
                            <p className="text-sm font-black text-gray-900">Two-Factor Authentication</p>
                            <p className="text-xs text-gray-400 font-medium text-green-600">Currently enabled via Google Authenticator.</p>
                          </div>
                        </div>
                        <button 
                          onClick={() => alert('MFA settings are managed via our Identity Gateway.')}
                          className="px-4 py-2 bg-black text-white rounded-lg text-xs font-black uppercase tracking-widest hover:bg-gray-800 transition-all"
                        >
                          Manage
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'data' && (
                  <div className="space-y-8 animate-in fade-in slide-in-from-right-4">
                    <div className="p-8 bg-red-50 rounded-3xl border border-red-100">
                       <h4 className="text-lg font-black text-red-900 mb-2">Danger Zone</h4>
                       <p className="text-sm text-red-700 font-medium mb-6">These actions are permanent and cannot be undone. Please proceed with caution.</p>
                       <div className="flex flex-col gap-4">
                          <button 
                            onClick={() => setModal({ type: 'reset', title: 'Reset Signal Cache', desc: 'This will purge all cached platform data. Your next GigScore calculation will require a full resync.' })}
                            className="flex items-center justify-between p-4 bg-white rounded-xl border border-red-100 group transition-all"
                          >
                             <div className="flex items-center gap-3">
                                <RefreshCw size={18} className="text-red-600 group-hover:animate-spin" />
                                <span className="text-xs font-black text-red-900 uppercase tracking-widest">Reset GigScore Signal Cache</span>
                             </div>
                             <ChevronRight size={16} className="text-red-200" />
                          </button>
                          <button 
                            onClick={() => setModal({ type: 'delete', title: 'Delete Identity Records', desc: 'This will permanently remove your PAN and identity links from GigScore. You will need to re-verify to use the platform.' })}
                            className="flex items-center justify-between p-4 bg-white rounded-xl border border-red-100 group transition-all"
                          >
                             <div className="flex items-center gap-3">
                                <Trash2 size={18} className="text-red-600" />
                                <span className="text-xs font-black text-red-900 uppercase tracking-widest">Delete Identity Records</span>
                             </div>
                             <ChevronRight size={16} className="text-red-200" />
                          </button>
                       </div>
                    </div>
                  </div>
                )}

                {activeTab === 'notifications' && (
                  <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
                    {[
                      { label: 'GigScore Updates', desc: 'Alert me when my score changes by more than 10 points.' },
                      { label: 'Platform Sync Alerts', desc: 'Notify me of successful or failed data integrations.' },
                      { label: 'Loan Status Notifications', desc: 'Instant updates on approval/rejection decisions.' },
                      { label: 'Security Alerts', desc: 'Critical alerts for login attempts and password changes.' }
                    ].map((n, i) => {
                      const isActive = notifications[n.label];
                      return (
                        <div key={i} className="flex items-center justify-between p-6 border-b border-gray-50 last:border-0">
                          <div>
                            <p className="text-sm font-black text-gray-900">{n.label}</p>
                            <p className="text-xs text-gray-400 font-medium">{n.desc}</p>
                          </div>
                          <button 
                            onClick={() => toggleNotification(n.label)}
                            className={`w-12 h-6 rounded-full relative cursor-pointer transition-colors duration-300 ${isActive ? 'bg-black' : 'bg-gray-200'}`}
                          >
                             <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all duration-300 ${isActive ? 'right-1' : 'left-1'}`}></div>
                          </button>
                        </div>
                      );
                    })}
                  </div>
                )}
             </div>
          </div>
        </div>
      </div>

      {/* Modal Backdrop */}
      {modal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-6 animate-in fade-in duration-300">
           <div className="bg-white rounded-[2rem] max-w-md w-full p-10 shadow-2xl animate-in zoom-in-95 duration-200">
              <div className="flex items-center justify-between mb-6">
                 <div className="w-12 h-12 rounded-2xl bg-red-50 flex items-center justify-center text-red-600">
                    <AlertTriangle size={24} />
                 </div>
                 <button onClick={() => setModal(null)} className="text-gray-400 hover:text-black transition-all">
                    <X size={24} />
                 </button>
              </div>
              <h3 className="text-2xl font-black text-gray-900 mb-2">{modal.title}</h3>
              <p className="text-gray-500 font-medium leading-relaxed mb-8">{modal.desc}</p>
              
              {modal.type === 'password' && (
                <div className="space-y-4 mb-8">
                  <input type="password" placeholder="Current Password" className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-black" />
                  <input type="password" placeholder="New Password" className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-black" />
                </div>
              )}

              <div className="flex gap-4">
                 <button 
                   onClick={() => setModal(null)}
                   className="flex-1 py-4 rounded-2xl font-black text-gray-400 bg-gray-50 hover:bg-gray-100 transition-all"
                 >
                   Cancel
                 </button>
                 <button 
                   onClick={executeAction}
                   disabled={saving}
                   className="flex-1 py-4 rounded-2xl font-black bg-red-600 text-white hover:bg-red-700 transition-all shadow-xl shadow-red-100 active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2"
                 >
                   {saving ? <Loader2 className="animate-spin" size={18} /> : 'Confirm'}
                 </button>
              </div>
           </div>
        </div>
      )}
    </DashboardLayout>
  );
}
