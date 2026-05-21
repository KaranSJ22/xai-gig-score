import React from 'react';
import { 
  HelpCircle, 
  Search, 
  MessageCircle, 
  BookOpen, 
  ShieldCheck, 
  ChevronRight,
  ExternalLink,
  LifeBuoy,
  FileQuestion,
  Database
} from 'lucide-react';
import DashboardLayout from '../components/DashboardLayout';

export default function HelpPage() {
  const faqs = [
    { 
      q: "How is my GigScore calculated?", 
      a: "Our XAI engine analyzes behavioral signals from your connected platforms (Zomato, Uber, Swiggy) including income stability, work discipline, and professional reliability.",
      icon: ShieldCheck 
    },
    { 
      q: "Is my data secure with GigScore?", 
      a: "Yes. We use RSA-4096 encryption and institutional-grade PAN verification. We never sell your data; it's only used to build your credit trust profile.",
      icon: Database 
    },
    { 
      q: "Can I disconnect my platforms?", 
      a: "Absolutely. You can 'Stop Sync' at any time from the Platform Sync page. This will immediately purge your behavioral data from our active signal cache.",
      icon: LifeBuoy 
    }
  ];

  return (
    <DashboardLayout>
      <div className="mb-12">
        <h1 className="text-4xl font-black text-gray-900 mb-2">Help Center</h1>
        <p className="text-gray-500 text-lg font-medium">Find answers, learn about our XAI engine, or contact support.</p>
      </div>

      {/* Hero Search */}
      <div className="bg-gray-900 rounded-[2.5rem] p-12 text-white mb-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -translate-y-32 translate-x-32 blur-3xl"></div>
        <div className="relative z-10 max-w-2xl">
          <h2 className="text-3xl font-black mb-6">How can we help you today?</h2>
          <div className="relative">
            <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400" size={24} />
            <input 
              type="text" 
              placeholder="Search documentation, guides, and FAQs..." 
              className="w-full bg-white/10 border border-white/20 rounded-2xl py-5 pl-16 pr-6 text-lg focus:outline-none focus:bg-white/20 transition-all backdrop-blur-xl"
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Support Channels */}
        <div className="col-span-12 lg:col-span-4 space-y-6">
           <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all group cursor-pointer">
              <div className="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                 <MessageCircle size={24} />
              </div>
              <h3 className="text-xl font-black text-gray-900 mb-2">Live Chat</h3>
              <p className="text-gray-500 text-sm font-medium mb-6">Talk to our credit analysts in real-time for immediate assistance.</p>
              <button className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-black">
                Start Chat <ChevronRight size={14} />
              </button>
           </div>

           <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all group cursor-pointer">
              <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                 <BookOpen size={24} />
              </div>
              <h3 className="text-xl font-black text-gray-900 mb-2">Documentation</h3>
              <p className="text-gray-500 text-sm font-medium mb-6">Deep dive into our XAI methodology and data privacy protocols.</p>
              <button className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-blue-600">
                View Docs <ExternalLink size={14} />
              </button>
           </div>
        </div>

        {/* FAQ Area */}
        <div className="col-span-12 lg:col-span-8">
          <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
             <div className="p-8 border-b border-gray-50 bg-gray-50/30">
                <div className="flex items-center gap-3">
                   <FileQuestion size={24} className="text-black" />
                   <h3 className="text-xl font-black text-gray-900">Frequently Asked Questions</h3>
                </div>
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
