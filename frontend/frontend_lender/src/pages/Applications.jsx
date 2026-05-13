import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  ExternalLink,
  Loader2,
  Calendar,
  CreditCard
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function Applications() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchApps() {
      try {
        const response = await apiRequest('/lender/applications');
        setApps(response);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchApps();
  }, []);

  const filteredApps = apps.filter(app => 
    app.borrower_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    app.status?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <DashboardLayout>
      <div className="flex items-center justify-between mb-10">
        <div>
          <h1 className="text-3xl font-black text-gray-900 mb-1">Application Queue</h1>
          <p className="text-gray-500 text-lg font-medium">Manage and review incoming credit requests.</p>
        </div>
        
        <div className="flex gap-3">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input 
              type="text" 
              placeholder="Filter by name..." 
              className="bg-white border border-gray-100 rounded-xl py-3 pl-12 pr-4 text-sm focus:outline-none focus:border-gray-300 w-64 shadow-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="flex items-center gap-2 bg-white border border-gray-100 px-6 py-3 rounded-xl font-bold text-sm text-gray-600 hover:text-black transition-all shadow-sm">
            <Filter size={18} />
            Filters
          </button>
        </div>
      </div>

      <div className="bg-white border border-gray-100 rounded-3xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-20 flex justify-center">
            <Loader2 className="animate-spin text-gray-400" size={40} />
          </div>
        ) : (
          <table className="w-full text-left">
            <thead>
              <tr className="bg-gray-50/50 border-b border-gray-100">
                <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Application ID</th>
                <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Borrower</th>
                <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Requested</th>
                <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Scheme</th>
                <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Date</th>
                <th className="py-5 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredApps.map((app) => (
                <tr key={app.id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-all group">
                  <td className="py-6 px-8 text-xs font-mono font-bold text-gray-400 uppercase tracking-wider">
                    #{app.id.toString().padStart(5, '0')}
                  </td>
                  <td className="py-6 px-8">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-gray-50 text-gray-900 border border-gray-100 flex items-center justify-center text-[10px] font-black">
                        {app.borrower_name?.charAt(0)}
                      </div>
                      <span className="font-bold text-gray-900">{app.borrower_name}</span>
                    </div>
                  </td>
                  <td className="py-6 px-8 font-black text-gray-900">₹{app.requested_amount.toLocaleString()}</td>
                  <td className="py-6 px-8">
                     <div className="flex items-center gap-2 text-xs font-bold text-gray-500">
                        <CreditCard size={14} />
                        {app.scheme_name || 'Personal Loan'}
                     </div>
                  </td>
                  <td className="py-6 px-8">
                     <div className="flex items-center gap-2 text-xs font-bold text-gray-400">
                        <Calendar size={14} />
                        {new Date(app.created_at).toLocaleDateString()}
                     </div>
                  </td>
                  <td className="py-6 px-8 text-right">
                    <button 
                      onClick={() => navigate(`/applications/${app.id}`)}
                      className="inline-flex items-center gap-2 px-5 py-2 rounded-xl bg-gray-900 text-white text-[10px] font-black uppercase tracking-widest hover:bg-black transition-all shadow-lg shadow-black/5"
                    >
                      Review
                      <ExternalLink size={12} />
                    </button>
                  </td>
                </tr>
              ))}
              {filteredApps.length === 0 && (
                <tr>
                  <td colSpan="6" className="p-20 text-center">
                    <p className="text-gray-400 font-bold text-sm">No applications found matching your criteria.</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
}
