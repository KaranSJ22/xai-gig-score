import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Lock, 
  Building2, 
  Mail, 
  Bell, 
  Save,
  CheckCircle,
  Loader2,
  ChevronRight,
  Database,
  History,
  Terminal,
  Activity,
  Users,
  X,
  RefreshCw,
  AlertTriangle,
  Key
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function SettingsPage() {
  const [lender, setLender] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('profile');
  const [modal, setModal] = useState(null);
  
  // Notification States
  const [notifications, setNotifications] = useState({
    'Critical Risk Alerts': true,
    'Institutional Audit Summary': true,
    'API Health Status': true,
    'New Loan Queue Alerts': false
  });

  useEffect(() => {
    async function fetchLender() {
      try {
        const response = await apiRequest('/auth/me');
        setLender(response);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchLender();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    setTimeout(() => {
      setSaving(false);
      setMessage('Institutional configuration updated.');
    }, 1000);
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
    setMessage(`Institutional alert for "${label}" ${!notifications[label] ? 'enabled' : 'disabled'}.`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin text-gray-400" size={40} />
      </div>
    );
  }

  const tabs = [
    { id: 'profile', label: 'Institutional Profile', icon: Building2 },
    { id: 'security', label: 'Security & Auth', icon: Lock },
    { id: 'engine', label: 'Risk Engine Params', icon: Terminal },
    { id: 'notifications', label: 'Alert Configurations', icon: Bell },
  ];

  return (
    <DashboardLayout lender={lender}>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Institutional Configuration</h1>
        <p className="text-gray-500 text-lg font-medium">Manage institutional identity, API access, and risk parameters.</p>
      </div>

      <div className="grid grid-cols-12 gap-10">
        {/* Navigation Sidebar */}
        <div className="col-span-12 lg:col-span-3 space-y-2">
          {tabs.map((tab) => (
            <button 
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center justify-between p-4 rounded-2xl text-sm font-bold transition-all ${activeTab === tab.id ? 'bg-black text-white shadow-xl shadow-black/10' : 'text-gray-400 hover:bg-gray-100 hover:text-black'}`}
            >
              <div className="flex items-center gap-3">
                <tab.icon size={18} />
                {tab.label}
              </div>
              <ChevronRight size={14} className={activeTab === tab.id ? 'text-white' : 'text-gray-300'} />
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="col-span-12 lg:col-span-9">
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden min-h-[600px]">
            <div className="p-8 border-b border-gray-50 flex items-center justify-between bg-gray-50/30">
               <div className="flex items-center gap-3">
                  {tabs.find(t => t.id === activeTab)?.icon({ size: 24, className: "text-black" })}
                  <h3 className="text-xl font-black text-gray-900">{tabs.find(t => t.id === activeTab)?.label}</h3>
               </div>
               {message && (
                 <div className="flex items-center gap-2 text-green-600 text-xs font-bold bg-green-50 px-4 py-2 rounded-xl animate-in fade-in slide-in-from-top-1">
                   <CheckCircle size={14} /> {message}
                 </div>
               )}
            </div>

            <div className="p-10">
              {activeTab === 'profile' && (
                <form onSubmit={handleSave} className="space-y-8 animate-in fade-in zoom-in-95 duration-200">
                  <div className="grid grid-cols-2 gap-8">
                     <div className="flex flex-col gap-2">
                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Primary Official</label>
                        <input 
                           type="text" 
                           defaultValue={lender?.name}
                           className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-900 focus:outline-none focus:border-black transition-all"
                        />
                     </div>
                     <div className="flex flex-col gap-2">
                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Official Work Email</label>
                        <input 
                           type="email" 
                           defaultValue={lender?.email}
                           disabled
                           className="w-full bg-gray-100 border border-gray-50 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-400 cursor-not-allowed"
                        />
                     </div>
                  </div>

                  <div className="grid grid-cols-2 gap-8 pt-8 border-t border-gray-50">
                     <div className="flex flex-col gap-2">
                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Institution Name</label>
                        <input 
                           type="text" 
                           defaultValue="GigScore Institutional Bank"
                           className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-900 focus:outline-none focus:border-black transition-all"
                        />
                     </div>
                     <div className="flex flex-col gap-2">
                        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Regulatory ID (RBI/SEC)</label>
                        <input 
                           type="text" 
                           defaultValue="GS-9921-X"
                           className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm font-bold text-gray-900 focus:outline-none focus:border-black transition-all"
                        />
                     </div>
                  </div>

                  <div className="pt-8 flex justify-end">
                    <button 
                       type="submit"
                       disabled={saving}
                       className="bg-black text-white px-8 py-4 rounded-2xl font-black flex items-center gap-3 hover:bg-gray-800 transition-all shadow-xl shadow-black/10 active:scale-[0.98]"
                    >
                       {saving ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
                       Save Changes
                    </button>
                  </div>
                </form>
              )}

              {activeTab === 'security' && (
                <div className="space-y-8 animate-in fade-in zoom-in-95 duration-200">
                  <div className="p-8 bg-gray-900 rounded-3xl text-white">
                    <div className="flex items-center gap-3 mb-6">
                      <Lock className="text-white" size={20} />
                      <h4 className="text-sm font-black uppercase tracking-widest">RSA Key Management</h4>
                    </div>
                    <div className="font-mono text-[10px] bg-white/5 p-4 rounded-xl border border-white/10 break-all leading-loose text-gray-400">
                      -----BEGIN PUBLIC KEY-----
                      MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7Vp...
                    </div>
                    <button 
                      onClick={() => setModal({ type: 'rotate', title: 'Rotate RSA Keys', desc: 'This will invalidate your current API keys and generate new RSA-4096 pairs. All active institutional sessions will be terminated.' })}
                      className="mt-6 px-6 py-2 bg-white text-black rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-gray-100 transition-all active:scale-95"
                    >
                      Rotate Keys
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-6 bg-gray-50 rounded-2xl border border-gray-100">
                    <div className="flex gap-4">
                      <Shield className="text-black" size={24} />
                      <div>
                        <p className="text-sm font-black text-gray-900">Multi-Factor Authentication (MFA)</p>
                        <p className="text-xs text-green-600 font-bold">ACTIVE & ENFORCED</p>
                      </div>
                    </div>
                    <button onClick={() => alert('Viewing audit logs...')} className="text-[10px] font-black uppercase text-gray-400 hover:text-black transition-all">Audit Logs</button>
                  </div>
                </div>
              )}

              {activeTab === 'engine' && (
                <div className="space-y-8 animate-in fade-in zoom-in-95 duration-200">
                  <div className="grid grid-cols-2 gap-6">
                    {[
                      { label: 'Minimum GigScore for Auto-Approval', val: '750' },
                      { label: 'Maximum Daily Application Load', val: '5,000' },
                      { label: 'Intelligence Engine Latency Tolerance', val: '150ms' },
                      { label: 'Data Freshness Requirement', val: '24h' }
                    ].map((item, i) => (
                      <div key={i} className="p-6 bg-gray-50 rounded-2xl border border-gray-100">
                        <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">{item.label}</p>
                        <div className="flex items-center justify-between">
                          <span className="text-xl font-black text-gray-900">{item.val}</span>
                          <button 
                            onClick={() => setModal({ type: 'edit', title: `Edit ${item.label}`, desc: `Update the institutional threshold for ${item.label.toLowerCase()}. This change will take effect immediately.` })}
                            className="text-[10px] font-bold text-black hover:underline"
                          >
                            Edit
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'notifications' && (
                <div className="space-y-6 animate-in fade-in zoom-in-95 duration-200">
                  {[
                    { label: 'Critical Risk Alerts' },
                    { label: 'Institutional Audit Summary' },
                    { label: 'API Health Status' },
                    { label: 'New Loan Queue Alerts' }
                  ].map((n, i) => {
                    const isActive = notifications[n.label];
                    return (
                      <div key={i} className="flex items-center justify-between p-6 bg-gray-50 rounded-2xl border border-gray-100">
                         <span className="text-sm font-black text-gray-900">{n.label}</span>
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
                 <div className="w-12 h-12 rounded-2xl bg-black flex items-center justify-center text-white">
                    <Shield size={24} />
                 </div>
                 <button onClick={() => setModal(null)} className="text-gray-400 hover:text-black transition-all">
                    <X size={24} />
                 </button>
              </div>
              <h3 className="text-2xl font-black text-gray-900 mb-2">{modal.title}</h3>
              <p className="text-gray-500 font-medium leading-relaxed mb-8">{modal.desc}</p>
              
              {modal.type === 'edit' && (
                <div className="space-y-4 mb-8">
                  <input type="text" placeholder="New Value" className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm font-bold focus:outline-none focus:border-black" />
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
                   className="flex-1 py-4 rounded-2xl font-black bg-black text-white hover:bg-gray-800 transition-all shadow-xl shadow-black/10 active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2"
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
