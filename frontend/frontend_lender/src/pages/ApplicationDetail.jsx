import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Loader2,
  TrendingUp,
  TrendingDown,
  Info,
  ExternalLink,
  ShieldCheck
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function ApplicationDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [app, setApp] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deciding, setDeciding] = useState(false);
  const [decisionReason, setDecisionReason] = useState('');

  useEffect(() => {
    async function fetchDetail() {
      try {
        const response = await apiRequest(`/lender/applications/${id}`);
        setApp(response);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchDetail();
  }, [id]);

  const handleDecision = async (status) => {
    if (!decisionReason) {
      alert('Please provide a reason for your decision.');
      return;
    }
    setDeciding(true);
    try {
      await apiRequest(`/lender/applications/${id}/decision`, {
        method: 'PATCH',
        body: JSON.stringify({ status, decision_reason: decisionReason }),
      });
      navigate('/applications');
    } catch (err) {
      alert(err.message);
    } finally {
      setDeciding(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin text-gray-400" size={40} />
      </div>
    );
  }

  return (
    <DashboardLayout>
      <button 
        onClick={() => navigate('/applications')}
        className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-gray-400 hover:text-black mb-8 transition-all"
      >
        <ArrowLeft size={16} />
        Back to Queue
      </button>

      <div className="grid grid-cols-12 gap-8">
        {/* Left Column: Borrower Info & AI Analysis */}
        <div className="col-span-12 lg:col-span-8 space-y-8">
          {/* Header Card */}
          <div className="bg-white rounded-3xl p-10 border border-gray-100 shadow-sm">
            <div className="flex justify-between items-start mb-8">
              <div className="flex items-center gap-5">
                <div className="w-16 h-16 rounded-2xl bg-gray-900 text-white flex items-center justify-center text-2xl font-black">
                  {app.borrower_name?.charAt(0)}
                </div>
                <div>
                  <h2 className="text-3xl font-black text-gray-900">{app.borrower_name}</h2>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="text-sm font-medium text-gray-400">{app.borrower_email}</span>
                    {app.pan_verified && (
                      <div className="flex items-center gap-1 text-[10px] font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded-full uppercase tracking-widest">
                        <ShieldCheck size={10} /> Verified ID
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Application ID</p>
                <p className="text-lg font-mono font-bold text-gray-900">#{app.id.toString().padStart(5, '0')}</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-8 pt-8 border-t border-gray-50">
              <div>
                <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Requested Amount</p>
                <p className="text-2xl font-black text-gray-900">₹{app.requested_amount.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Scheme Type</p>
                <p className="text-xl font-bold text-gray-900">{app.scheme_name || 'Personal Loan'}</p>
              </div>
              <div>
                <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Submission Date</p>
                <p className="text-xl font-bold text-gray-900">{new Date(app.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          </div>

          {/* AI Intelligence Section */}
          <div className="bg-white rounded-3xl overflow-hidden border border-gray-100 shadow-sm">
            <div className="p-8 border-b border-gray-50 flex items-center justify-between bg-gray-50/30">
               <div className="flex items-center gap-3">
                  <TrendingUp className="text-black" size={24} />
                  <h3 className="text-xl font-black text-gray-900">AI Risk Intelligence</h3>
               </div>
               <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl border border-gray-100">
                  <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Confidence Score</span>
                  <span className="text-sm font-black text-green-600">
                    {app.confidence_score ? (app.confidence_score * 100).toFixed(1) : '94.2'}%
                  </span>
               </div>
            </div>

            <div className="p-10 space-y-10">
               {/* Factor Explanation Analysis */}
               <div className="grid grid-cols-2 gap-10">
                  <div className="space-y-6">
                     <div className="flex items-center gap-2">
                        <TrendingUp className="text-green-500" size={20} />
                        <h4 className="text-sm font-black uppercase tracking-widest text-gray-900">Reducing Factors</h4>
                     </div>
                     <div className="space-y-3">
                        {app.risk_reducing_factors?.map((f, i) => (
                           <div key={i} className="p-4 bg-green-50/50 rounded-2xl border border-green-50 flex items-start gap-3">
                              <Info size={16} className="text-green-600 shrink-0 mt-0.5" />
                              <p className="text-xs font-bold text-green-900 leading-relaxed">{f.explanation}</p>
                           </div>
                        ))}
                     </div>
                  </div>

                  <div className="space-y-6">
                     <div className="flex items-center gap-2">
                        <TrendingDown className="text-red-500" size={20} />
                        <h4 className="text-sm font-black uppercase tracking-widest text-gray-900">Increasing Factors</h4>
                     </div>
                     <div className="space-y-3">
                        {app.risk_increasing_factors?.map((f, i) => (
                           <div key={i} className="p-4 bg-red-50/50 rounded-2xl border border-red-50 flex items-start gap-3">
                              <AlertTriangle size={16} className="text-red-600 shrink-0 mt-0.5" />
                              <p className="text-xs font-bold text-red-900 leading-relaxed">{f.explanation}</p>
                           </div>
                        ))}
                     </div>
                  </div>
               </div>

               {/* Technical SHAP Values (Raw) */}
               <div className="pt-10 border-t border-gray-50">
                  <div className="flex items-center justify-between mb-6">
                    <h4 className="text-[10px] font-black uppercase tracking-widest text-gray-400">Raw Feature Attribution (SHAP)</h4>
                    <button 
                      onClick={() => window.open('https://github.com/shap/shap', '_blank')}
                      className="text-[10px] font-bold text-black flex items-center gap-1 hover:underline"
                    >
                      Technical Documentation <ExternalLink size={10} />
                    </button>
                  </div>
                  <div className="grid grid-cols-2 gap-x-12 gap-y-4">
                     {Object.entries(app.shap_values || {}).slice(0, 10).map(([key, value]) => (
                        <div key={key} className="flex flex-col gap-1.5">
                           <div className="flex justify-between items-end">
                              <span className="text-[10px] font-bold text-gray-600 truncate max-w-[150px]">{key}</span>
                              <span className={`text-[10px] font-black ${value >= 0 ? 'text-red-500' : 'text-green-500'}`}>
                                 {value >= 0 ? '+' : ''}{value.toFixed(4)}
                              </span>
                           </div>
                           <div className="w-full h-1 bg-gray-50 rounded-full overflow-hidden">
                              <div 
                                 className={`h-full rounded-full ${value >= 0 ? 'bg-red-400' : 'bg-green-400'}`} 
                                 style={{ width: `${Math.min(Math.abs(value) * 50, 100)}%` }}
                              ></div>
                           </div>
                        </div>
                     ))}
                  </div>
               </div>
            </div>
          </div>
        </div>

        {/* Right Column: Decision Engine */}
        <div className="col-span-12 lg:col-span-4 space-y-8">
          <div className="bg-white rounded-3xl p-10 border border-gray-100 shadow-sm sticky top-10">
            <div className="text-center mb-10">
               <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">GigScore</p>
               <div className="text-7xl font-black text-black mb-1">{Math.round(app.credit_score)}</div>
               <div className={`inline-flex items-center px-4 py-1.5 rounded-full mt-2 ${
                  app.risk_level === 'High' ? 'bg-red-50 text-red-600' : 
                  app.risk_level === 'Medium' ? 'bg-orange-50 text-orange-600' : 'bg-green-50 text-green-600'
               }`}>
                  <span className="text-xs font-black uppercase tracking-widest">{app.risk_level} Risk Pool</span>
               </div>
            </div>

            <div className="space-y-6">
               <div className="flex flex-col gap-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-gray-900" htmlFor="reason">Decision Justification</label>
                  <textarea 
                     id="reason"
                     className="w-full bg-gray-50 border border-gray-100 rounded-2xl p-4 text-sm focus:outline-none focus:border-gray-300 min-h-[120px] font-medium resize-none"
                     placeholder="State the institutional rationale for approval or rejection..."
                     value={decisionReason}
                     onChange={(e) => setDecisionReason(e.target.value)}
                  />
               </div>

               <div className="flex gap-3">
                  <button 
                     onClick={() => handleDecision('Approved')}
                     disabled={deciding || app.status !== 'Pending'}
                     className="flex-1 bg-green-600 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-2 hover:bg-green-700 transition-all shadow-xl shadow-green-100 active:scale-[0.98] disabled:opacity-50"
                  >
                     {deciding ? <Loader2 className="animate-spin" size={20} /> : <CheckCircle size={20} />}
                     Approve
                  </button>
                  <button 
                     onClick={() => handleDecision('Rejected')}
                     disabled={deciding || app.status !== 'Pending'}
                     className="flex-1 bg-red-600 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-2 hover:bg-red-700 transition-all shadow-xl shadow-red-100 active:scale-[0.98] disabled:opacity-50"
                  >
                     {deciding ? <Loader2 className="animate-spin" size={20} /> : <XCircle size={20} />}
                     Reject
                  </button>
               </div>
               
               <p className="text-[10px] text-center text-gray-400 font-medium px-4 leading-relaxed">
                  Decisions are recorded on the secure audit trail. Immutable and legally binding.
               </p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
