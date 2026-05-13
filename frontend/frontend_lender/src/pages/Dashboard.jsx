import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Clock, 
  CheckCircle, 
  XCircle, 
  TrendingUp,
  ArrowUpRight,
  Loader2,
  AlertTriangle
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

import { useNavigate } from 'react-router-dom';
export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStats() {
      try {
        const response = await apiRequest('/lender/dashboard');
        setData(response);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin text-gray-400" size={40} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-600 p-8 rounded-3xl border border-red-100 flex flex-col items-center justify-center text-center">
        <AlertTriangle size={48} className="mb-4" />
        <h2 className="text-xl font-black mb-2">Sync Interrupted</h2>
        <p className="text-sm font-medium mb-6">{error}</p>
        <button onClick={() => window.location.reload()} className="px-6 py-2 bg-red-600 text-white rounded-xl font-bold">Retry Sync</button>
      </div>
    );
  }

  const stats = [
    { label: 'Total Applications', value: data.total_applications, icon: Users, color: 'text-blue-500', bg: 'bg-blue-50' },
    { label: 'Pending Review', value: data.pending_applications, icon: Clock, color: 'text-orange-500', bg: 'bg-orange-50' },
    { label: 'Approved Today', value: data.approved_applications, icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50' },
    { label: 'Avg Portfolio Score', value: Math.round(data.average_gigscore), icon: TrendingUp, color: 'text-purple-500', bg: 'bg-purple-50' },
  ];

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Institutional Dashboard</h1>
        <p className="text-gray-500 text-lg font-medium">Risk exposure and application pipeline analytics.</p>
      </div>

      <div className="grid grid-cols-4 gap-6 mb-12">
        {stats.map((stat, i) => (
          <div key={i} className="bg-white p-8 rounded-3xl border border-gray-100 shadow-[0_4px_20px_rgba(0,0,0,0.02)]">
            <div className={`w-12 h-12 rounded-2xl ${stat.bg} ${stat.color} flex items-center justify-center mb-6`}>
              <stat.icon size={24} />
            </div>
            <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">{stat.label}</p>
            <h3 className="text-3xl font-black text-gray-900">{stat.value}</h3>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-8">
        <div className="col-span-12 lg:col-span-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-black text-gray-900">Recent Applications</h3>
            <button 
              onClick={() => navigate('/applications')}
              className="text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-black"
            >
              View All Queue
            </button>
          </div>
          
          <div className="bg-white border border-gray-100 rounded-3xl overflow-hidden shadow-sm">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50/50 border-b border-gray-100">
                  <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Borrower</th>
                  <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Amount</th>
                  <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400 text-center">GigScore</th>
                  <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_applications.map((app) => (
                  <tr key={app.id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-all cursor-pointer">
                    <td className="py-6 px-8">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-gray-900 text-white flex items-center justify-center text-[10px] font-black">
                          {app.borrower_name?.charAt(0)}
                        </div>
                        <span className="font-bold text-gray-900">{app.borrower_name}</span>
                      </div>
                    </td>
                    <td className="py-6 px-8 font-black text-gray-900">₹{app.requested_amount.toLocaleString()}</td>
                    <td className="py-6 px-8 text-center">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-[10px] font-black ${
                        app.credit_score > 700 ? 'bg-green-50 text-green-700' : 
                        app.credit_score > 500 ? 'bg-orange-50 text-orange-700' : 'bg-red-50 text-red-700'
                      }`}>
                        {Math.round(app.credit_score)}
                      </span>
                    </td>
                    <td className="py-6 px-8 text-right">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${
                        app.status === 'Pending' ? 'bg-gray-100 text-gray-600' :
                        app.status === 'Approved' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {app.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="col-span-12 lg:col-span-4">
          <h3 className="text-xl font-black text-gray-900 mb-6">Risk Profile Dist.</h3>
          <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
             <div className="space-y-8">
                <div>
                   <div className="flex justify-between items-end mb-2">
                      <span className="text-[10px] font-black uppercase tracking-widest text-red-500">High Risk Bucket</span>
                      <span className="text-xl font-black">{data.high_risk_applications}</span>
                   </div>
                   <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{ width: `${(data.high_risk_applications / data.total_applications) * 100}%` }}></div>
                   </div>
                </div>
                <div>
                   <div className="flex justify-between items-end mb-2">
                      <span className="text-[10px] font-black uppercase tracking-widest text-green-500">Safe Pool</span>
                      <span className="text-xl font-black">{data.approved_applications}</span>
                   </div>
                   <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full bg-green-500 rounded-full" style={{ width: `${(data.approved_applications / data.total_applications) * 100}%` }}></div>
                   </div>
                </div>
             </div>
             
             <div className="mt-12 p-6 bg-gray-900 rounded-2xl text-white">
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-gray-400 mb-2">AI Optimization</p>
                <p className="text-xs font-medium leading-relaxed opacity-80">
                  Your portfolio's average GigScore is trending <span className="text-green-400 font-bold">4% higher</span> than industry average.
                </p>
             </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
