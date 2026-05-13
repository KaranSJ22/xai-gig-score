import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, ArrowRight, Loader2, Landmark } from 'lucide-react';
import { apiRequest } from '../lib/api';
import { saveToken } from '../lib/auth';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    institution_name: '',
    institution_type: 'Bank',
    license_number: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await apiRequest('/auth/lender-register', {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      saveToken(data.access_token);
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  return (
    <div className="bg-[#fcf8fa] min-h-screen flex items-center justify-center p-6 antialiased">
      <main className="w-full max-w-[500px]">
        <div className="flex flex-col items-center justify-center mb-10">
          <div className="flex items-center gap-2 mb-1">
            <Shield className="text-black" size={32} strokeWidth={2.5} />
            <span className="text-2xl font-black tracking-tight">GigScore</span>
          </div>
          <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-gray-400">Institutional Onboarding</span>
        </div>

        <div className="bg-white border border-gray-100 rounded-3xl shadow-[0_4px_32px_rgba(0,0,0,0.04)] overflow-hidden">
          <div className="h-1.5 w-full bg-black"></div>
          <div className="p-10">
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">Platform Enrollment</h1>
              <p className="text-sm text-gray-500 font-medium">Join our network of precision-risk lenders.</p>
            </div>

            {error && (
              <div className="bg-red-50 text-red-600 text-xs p-4 rounded-lg mb-6 border border-red-100 font-bold">
                {error}
              </div>
            )}

            <form onSubmit={handleRegister} className="grid grid-cols-2 gap-5">
              <div className="col-span-2 flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="name">Lead Official Name</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all font-medium" 
                  id="name" 
                  placeholder="Jane Doe" 
                  type="text"
                  value={formData.name}
                  onChange={handleChange}
                  required 
                />
              </div>

              <div className="col-span-2 flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="email">Official Work Email</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all font-medium" 
                  id="email" 
                  placeholder="jane@bank-of-trust.com" 
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required 
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="institution_name">Institution Name</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all font-medium" 
                  id="institution_name" 
                  placeholder="Bank of Trust" 
                  type="text"
                  value={formData.institution_name}
                  onChange={handleChange}
                  required 
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="institution_type">Institution Type</label>
                <select 
                  className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all font-medium" 
                  id="institution_type"
                  value={formData.institution_type}
                  onChange={handleChange}
                >
                  <option>Bank</option>
                  <option>NBFC</option>
                  <option>FinTech</option>
                  <option>Microfinance</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="license_number">License ID</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all font-medium" 
                  id="license_number" 
                  placeholder="RBI-9921-X" 
                  type="text"
                  value={formData.license_number}
                  onChange={handleChange}
                  required 
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="password">Security Key</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all font-medium" 
                  id="password" 
                  placeholder="••••••••" 
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  required 
                />
              </div>

              <div className="col-span-2 mt-4">
                <button 
                  className="w-full bg-black text-white font-bold rounded-xl py-4 flex items-center justify-center gap-2 hover:bg-gray-800 transition-all shadow-xl shadow-black/5 active:scale-[0.98] disabled:opacity-50"
                  type="submit"
                  disabled={loading}
                >
                  {loading ? <Loader2 className="animate-spin" size={20} /> : <Landmark size={18} />}
                  {loading ? 'Processing...' : 'Enroll Institution'}
                  {!loading && <ArrowRight className="ml-1" size={18} />}
                </button>
              </div>
            </form>
          </div>
          <div className="bg-gray-50 border-t border-gray-100 p-6 text-center">
            <p className="text-sm text-gray-500 font-medium">
              Already enrolled? 
              <Link className="text-black font-black hover:underline ml-2" to="/login">Login Console</Link>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
