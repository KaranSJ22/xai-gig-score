import React from 'react';
import { 
  HelpCircle, 
  Search, 
  MessageCircle, 
  BookOpen, 
  Shield, 
  ChevronRight,
  ExternalLink,
  Terminal,
  Activity,
  FileText
} from 'lucide-react';
import DashboardLayout from '../components/DashboardLayout';

export default function HelpPage() {
  const faqs = [
    { 
      q: "How does the Intelligence Engine calculate GigScore?", 
      a: "The engine uses a Random Forest and SHAP-based model to weight behavioral factors from gig platforms. It provides real-time explainability for every score.",
      icon: Terminal 
    },
    { 
      q: "What is the Confidence Score?", 
      a: "Confidence score represents the statistical reliability of the prediction based on the volume and density of the borrower's connected platform data.",
      icon: Activity 
    },
    { 
      q: "How are loan decisions synchronized?", 
      a: "When you approve or reject an application, the borrower is notified instantly via their dashboard, and the decision is recorded in the immutable audit trail.",
      icon: FileText 
    }
  ];

  return (
    <DashboardLayout>
      <div className="mb-12">
        <h1 className="text-4xl font-black text-gray-900 mb-2">Institutional Support</h1>
        <p className="text-gray-500 text-lg font-medium">Technical documentation, API guides, and regulatory support for lenders.</p>
      </div>

      <div className="bg-black rounded-[2.5rem] p-12 text-white mb-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -translate-y-32 translate-x-32 blur-3xl"></div>
        <div className="relative z-10 max-w-2xl">
          <h2 className="text-3xl font-black mb-6">Lender Resource Center</h2>
          <div className="relative">
            <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400" size={24} />
            <input 
              type="text" 
              placeholder="Search institutional guides, API refs..." 
              className="w-full bg-white/10 border border-white/20 rounded-2xl py-5 pl-16 pr-6 text-lg focus:outline-none focus:bg-white/20 transition-all backdrop-blur-xl"
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        <div className="col-span-12 lg:col-span-4 space-y-6">
           <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all group cursor-pointer">
              <div className="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center mb-6">
                 <Shield size={24} />
              </div>
              <h3 className="text-xl font-black text-gray-900 mb-2">Technical Support</h3>
              <p className="text-gray-500 text-sm font-medium mb-6">Contact our engineering team for API integration issues or intelligence engine queries.</p>
              <button className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-black">
                Open Ticket <ChevronRight size={14} />
              </button>
           </div>

           <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all group cursor-pointer">
              <div className="w-12 h-12 rounded-2xl bg-gray-50 text-black flex items-center justify-center mb-6">
                 <BookOpen size={24} />
              </div>
              <h3 className="text-xl font-black text-gray-900 mb-2">API Documentation</h3>
              <p className="text-gray-500 text-sm font-medium mb-6">Explore the full API reference for real-time risk orchestration.</p>
              <button className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400">
                Browse Docs <ExternalLink size={14} />
              </button>
           </div>
        </div>

        <div className="col-span-12 lg:col-span-8">
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
             <div className="p-8 border-b border-gray-50 bg-gray-50/30">
                <h3 className="text-xl font-black text-gray-900">Institutional FAQs</h3>
             </div>
             <div className="divide-y divide-gray-50">
                {faqs.map((faq, i) => (
                  <div key={i} className="p-8 hover:bg-gray-50 transition-colors">
                    <div className="flex gap-6">
                      <div className="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center shrink-0">
                        <faq.icon size={20} className="text-gray-600" />
                      </div>
                      <div>
                        <h4 className="text-lg font-black text-gray-900 mb-2">{faq.q}</h4>
                        <p className="text-gray-500 font-medium leading-relaxed">{faq.a}</p>
                      </div>
                    </div>
                  </div>
                ))}
             </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
