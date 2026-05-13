import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Trash2, 
  Loader2, 
  Briefcase,
  Percent,
  Calendar,
  IndianRupee,
  Activity,
  AlertCircle
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function Schemes() {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [deleting, setDeleting] = useState(null);
  const [newScheme, setNewScheme] = useState({
    scheme_name: '',
    description: '',
    min_amount: 5000,
    max_amount: 50000,
    interest_rate: 12.5,
    tenure_months: 12,
    min_score_required: 650
  });

  useEffect(() => {
    fetchSchemes();
  }, []);

  const fetchSchemes = async () => {
    try {
      const response = await apiRequest('/schemes/my');
      setSchemes(response);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    try {
      await apiRequest('/schemes/', {
        method: 'POST',
        body: JSON.stringify(newScheme),
      });
      setNewScheme({
        scheme_name: '',
        description: '',
        min_amount: 5000,
        max_amount: 50000,
        interest_rate: 12.5,
        tenure_months: 12,
        min_score_required: 650
      });
      fetchSchemes();
    } catch (err) {
      alert(err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (schemeId) => {
    if (!window.confirm('Are you sure you want to deactivate this loan product? This will prevent new applications.')) {
      return;
    }
    setDeleting(schemeId);
    try {
      await apiRequest(`/schemes/${schemeId}`, {
        method: 'DELETE',
      });
      fetchSchemes();
    } catch (err) {
      alert(err.message);
    } finally {
      setDeleting(null);
    }
  };

  return (
    <DashboardLayout>
      <div className="flex items-center justify-between mb-10">
        <div>
          <h1 className="text-3xl font-black text-gray-900 mb-1">Loan Products</h1>
          <p className="text-gray-500 text-lg font-medium">Design and deploy credit schemes for the gig workforce.</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Create Scheme Form */}
        <div className="col-span-12 lg:col-span-4">
          <div className="bg-white rounded-3xl p-10 border border-gray-100 shadow-sm sticky top-10">
            <h3 className="text-xl font-black text-gray-900 mb-8 flex items-center gap-2">
               <Plus className="text-black" size={24} /> New Product
            </h3>
            
            <form onSubmit={handleCreate} className="space-y-6">
               <div className="flex flex-col gap-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-gray-900">Scheme Name</label>
                  <input 
                     type="text" 
                     className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-300 font-medium"
                     placeholder="e.g., QuickCapital Lite"
                     value={newScheme.scheme_name}
                     onChange={(e) => setNewScheme({...newScheme, scheme_name: e.target.value})}
                     required
                  />
               </div>

               <div className="grid grid-cols-2 gap-4">
                  <div className="flex flex-col gap-2">
                     <label className="text-[10px] font-black uppercase tracking-widest text-gray-900">Min Score</label>
                     <input 
                        type="number" 
                        className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-300 font-medium"
                        value={newScheme.min_score_required}
                        onChange={(e) => setNewScheme({...newScheme, min_score_required: parseInt(e.target.value)})}
                        required
                     />
                  </div>
                  <div className="flex flex-col gap-2">
                     <label className="text-[10px] font-black uppercase tracking-widest text-gray-900">Interest %</label>
                     <input 
                        type="number" step="0.1"
                        className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-300 font-medium"
                        value={newScheme.interest_rate}
                        onChange={(e) => setNewScheme({...newScheme, interest_rate: parseFloat(e.target.value)})}
                        required
                     />
                  </div>
               </div>

               <div className="grid grid-cols-2 gap-4">
                  <div className="flex flex-col gap-2">
                     <label className="text-[10px] font-black uppercase tracking-widest text-gray-900">Min Amount</label>
                     <input 
                        type="number" 
                        className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-300 font-medium"
                        value={newScheme.min_amount}
                        onChange={(e) => setNewScheme({...newScheme, min_amount: parseInt(e.target.value)})}
                        required
                     />
                  </div>
                  <div className="flex flex-col gap-2">
                     <label className="text-[10px] font-black uppercase tracking-widest text-gray-900">Max Amount</label>
                     <input 
                        type="number" 
                        className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-300 font-medium"
                        value={newScheme.max_amount}
                        onChange={(e) => setNewScheme({...newScheme, max_amount: parseInt(e.target.value)})}
                        required
                     />
                  </div>
               </div>

               <button 
                  type="submit"
                  disabled={creating}
                  className="w-full bg-black text-white font-black py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-800 transition-all shadow-xl shadow-black/10 active:scale-[0.98] disabled:opacity-50"
               >
                  {creating ? <Loader2 className="animate-spin" size={20} /> : <Activity size={20} />}
                  Deploy Scheme
               </button>
            </form>
          </div>
        </div>

        {/* Existing Schemes List */}
        <div className="col-span-12 lg:col-span-8">
           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {loading ? (
                 <div className="col-span-2 p-20 flex justify-center">
                    <Loader2 className="animate-spin text-gray-400" size={40} />
                 </div>
              ) : schemes.length > 0 ? (
                 schemes.map((scheme) => (
                    <div key={scheme.id} className={`bg-white rounded-3xl p-8 border shadow-sm group hover:border-black/10 transition-all ${!scheme.is_active ? 'opacity-60 bg-gray-50' : 'border-gray-100'}`}>
                       <div className="flex justify-between items-start mb-6">
                          <div className={`w-12 h-12 rounded-2xl flex items-center justify-center border transition-all ${scheme.is_active ? 'bg-gray-50 text-black border-gray-100 group-hover:bg-black group-hover:text-white' : 'bg-gray-200 text-gray-400 border-gray-200'}`}>
                             <Briefcase size={24} />
                          </div>
                          <div className="flex items-center gap-3">
                             <span className={`text-[8px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full ${scheme.is_active ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`}>
                               {scheme.is_active ? 'Live' : 'Deactivated'}
                             </span>
                             {scheme.is_active && (
                               <button 
                                 onClick={() => handleDelete(scheme.id)}
                                 disabled={deleting === scheme.id}
                                 className="text-gray-300 hover:text-red-500 transition-colors"
                               >
                                 {deleting === scheme.id ? <Loader2 className="animate-spin" size={16} /> : <Trash2 size={16} />}
                               </button>
                             )}
                          </div>
                       </div>
                       
                       <h4 className="text-xl font-black text-gray-900 mb-2">{scheme.scheme_name}</h4>
                       <p className="text-xs text-gray-500 font-medium leading-relaxed mb-8">{scheme.description || 'Institutional credit line designed for flexible gig work performance profiles.'}</p>
                       
                       <div className="grid grid-cols-2 gap-y-6 pt-6 border-t border-gray-50">
                          <div className="flex items-center gap-3">
                             <Percent size={18} className="text-gray-400" />
                             <div>
                                <p className="text-[8px] font-black uppercase tracking-widest text-gray-400">Rate</p>
                                <p className="text-sm font-black text-gray-900">{scheme.interest_rate}% APR</p>
                             </div>
                          </div>
                          <div className="flex items-center gap-3">
                             <Activity size={18} className="text-gray-400" />
                             <div>
                                <p className="text-[8px] font-black uppercase tracking-widest text-gray-400">Min GigScore</p>
                                <p className="text-sm font-black text-gray-900">{scheme.min_score_required}+</p>
                             </div>
                          </div>
                          <div className="flex items-center gap-3">
                             <IndianRupee size={18} className="text-gray-400" />
                             <div>
                                <p className="text-[8px] font-black uppercase tracking-widest text-gray-400">Cap</p>
                                <p className="text-sm font-black text-gray-900">₹{scheme.max_amount.toLocaleString()}</p>
                             </div>
                          </div>
                          <div className="flex items-center gap-3">
                             <Calendar size={18} className="text-gray-400" />
                             <div>
                                <p className="text-[8px] font-black uppercase tracking-widest text-gray-400">Tenure</p>
                                <p className="text-sm font-black text-gray-900">{scheme.tenure_months} Mo</p>
                             </div>
                          </div>
                       </div>
                    </div>
                 ))
              ) : (
                <div className="col-span-2 p-20 bg-gray-50 rounded-3xl border border-dashed border-gray-200 text-center">
                   <AlertCircle className="mx-auto text-gray-300 mb-4" size={40} />
                   <p className="text-gray-500 font-bold">No products deployed. Use the form to launch your first scheme.</p>
                </div>
              )}
           </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
