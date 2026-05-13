import React, { useState, useEffect } from 'react';
import { 
  Landmark, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  ArrowRight, 
  Loader2,
  Building2,
  BadgePercent,
  AlertCircle
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function LoansPage() {
  const [loans, setLoans] = useState([]);
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedScheme, setSelectedScheme] = useState(null);
  const [amount, setAmount] = useState('');
  const [purpose, setPurpose] = useState('');

  useEffect(() => {
    async function fetchData() {
      try {
        const [schemesData, loansData] = await Promise.all([
          apiRequest('/schemes/public'),
          apiRequest('/applications/my')
        ]);
        setSchemes(schemesData);
        setLoans(loansData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const handleApply = async (e) => {
    e.preventDefault();
    if (!selectedScheme) {
      alert('Please select a loan scheme first');
      return;
    }
    
    setSubmitting(true);
    try {
      await apiRequest('/applications/', {
        method: 'POST',
        body: JSON.stringify({ 
          scheme_id: selectedScheme.id, 
          requested_amount: parseFloat(amount),
          purpose: purpose || 'Personal use'
        }),
      });
      setSelectedScheme(null);
      setAmount('');
      setPurpose('');
      // Refresh loans
      const updatedLoans = await apiRequest('/applications/my');
      setLoans(updatedLoans);
      alert('Application submitted successfully!');
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Credit Liquidity</h1>
        <p className="text-gray-500 text-lg">Select and deploy institutional credit lines based on your GigScore profile.</p>
      </div>

      {/* Offers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {schemes.length > 0 ? schemes.map((scheme) => (
          <div key={scheme.id} className={`bg-white rounded-3xl p-8 border transition-all flex flex-col justify-between ${selectedScheme?.id === scheme.id ? 'border-black ring-1 ring-black' : 'border-gray-100 shadow-sm hover:shadow-xl hover:shadow-black/[0.02]'}`}>
            <div>
              <div className="flex justify-between items-start mb-6">
                <div className="w-12 h-12 rounded-xl bg-gray-50 flex items-center justify-center border border-gray-100">
                  <Landmark className="text-black" size={24} />
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest px-3 py-1 bg-green-50 text-green-700 rounded-full">
                  {scheme.interest_rate}% APR
                </span>
              </div>
              <h3 className="text-xl font-black text-black mb-1">{scheme.scheme_name}</h3>
              <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-6">Institutional Credit</p>
              <div className="text-3xl font-black text-black mb-2">Up to ₹{scheme.max_amount.toLocaleString()}</div>
              <p className="text-xs font-bold text-gray-900">Min GigScore: {scheme.min_score_required}+</p>
            </div>
            
            <button 
              onClick={() => {
                setSelectedScheme(scheme);
                setAmount(scheme.max_amount.toString());
              }}
              className={`mt-8 w-full font-black py-4 rounded-xl flex items-center justify-center gap-2 transition-all active:scale-[0.98] ${selectedScheme?.id === scheme.id ? 'bg-gray-100 text-black' : 'bg-black text-white hover:bg-gray-800'}`}
            >
              {selectedScheme?.id === scheme.id ? 'Selected' : 'Select Offer'}
              <ArrowRight size={18} />
            </button>
          </div>
        )) : (
          <div className="col-span-3 p-10 bg-gray-50 rounded-3xl border border-dashed border-gray-200 text-center">
            <AlertCircle className="mx-auto text-gray-300 mb-4" size={40} />
            <p className="text-gray-500 font-bold">No active loan offers available in your region.</p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Apply Form */}
        <div className="col-span-12 lg:col-span-4">
          <div className="bg-white rounded-3xl p-10 border border-gray-100 shadow-sm h-full">
            <h3 className="text-xl font-black text-gray-900 mb-8 border-b border-gray-50 pb-4">Disbursement Request</h3>
            <form onSubmit={handleApply} className="space-y-6">
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Selected Scheme</label>
                <div className="relative">
                  <input 
                    className="w-full bg-gray-100 border border-gray-50 rounded-xl px-10 py-3.5 text-sm font-bold text-gray-500 cursor-not-allowed"
                    placeholder="Select an offer from above"
                    value={selectedScheme?.scheme_name || ''}
                    readOnly
                  />
                  <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Request Amount (INR)</label>
                <div className="relative">
                  <input 
                    className="w-full bg-gray-50 border border-gray-100 rounded-xl px-10 py-3.5 text-sm font-black focus:outline-none focus:border-black transition-all"
                    placeholder="1,00,000"
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                  />
                  <BadgePercent className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Purpose of Loan</label>
                <input 
                  className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm font-bold focus:outline-none focus:border-black transition-all"
                  placeholder="e.g. Bike Repair, Laptop Upgrade"
                  value={purpose}
                  onChange={(e) => setPurpose(e.target.value)}
                  required
                />
              </div>
              <button 
                className="w-full bg-black text-white font-black py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-800 transition-all disabled:opacity-50 mt-10 shadow-2xl shadow-black/10"
                type="submit"
                disabled={submitting || !selectedScheme}
              >
                {submitting ? <Loader2 className="animate-spin" size={20} /> : 'Process Disbursement'}
              </button>
            </form>
          </div>
        </div>

        {/* Loan History */}
        <div className="col-span-12 lg:col-span-8">
          <h3 className="text-xl font-black text-gray-900 mb-8 px-2 flex items-center justify-between">
            Your Applications
            <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{loans.length} Total</span>
          </h3>
          <div className="bg-white border border-gray-100 rounded-3xl overflow-hidden shadow-sm">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50/50 border-b border-gray-100">
                  <th className="py-4 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Scheme</th>
                  <th className="py-4 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Requested</th>
                  <th className="py-4 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                   <tr>
                     <td colSpan="3" className="py-20 text-center">
                        <Loader2 className="animate-spin inline-block text-gray-300" size={32} />
                     </td>
                   </tr>
                ) : loans.length > 0 ? (
                  loans.map((app) => (
                    <tr key={app.id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors">
                      <td className="py-6 px-8">
                        <div className="font-black text-gray-900">{app.scheme_name}</div>
                        <div className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{app.lender_name}</div>
                      </td>
                      <td className="py-6 px-8 font-black text-gray-900">₹{app.requested_amount?.toLocaleString()}</td>
                      <td className="py-6 px-8 text-right">
                        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border ${
                          app.status === 'Approved' ? 'bg-green-50 text-green-700 border-green-100' :
                          app.status === 'Rejected' ? 'bg-red-50 text-red-700 border-red-100' :
                          'bg-gray-100 text-gray-600 border-gray-200'
                        }`}>
                          {app.status === 'Approved' ? <CheckCircle2 size={12} /> : 
                           app.status === 'Rejected' ? <XCircle size={12} /> : <Clock size={12} />}
                          {app.status}
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className="py-24 text-center px-8">
                       <p className="text-gray-400 text-sm font-bold uppercase tracking-widest">No active applications</p>
                       <p className="text-gray-300 text-xs mt-2 font-medium">Select a scheme above to begin your disbursement request.</p>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
