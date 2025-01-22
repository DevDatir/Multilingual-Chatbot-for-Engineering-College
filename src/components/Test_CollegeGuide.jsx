import React, { useState, useEffect } from 'react';
import { useNavigate, Link, Routes, Route } from 'react-router-dom';
import { Bell, Search, MapPin, Users, BookOpen, ChevronRight, Star, CheckCircle, ArrowRight } from 'lucide-react';
import About from './About';
import Features from './Features';
import Contact from './Contact';
import ChatPage from './Chatpage';
import Chatbot from './Chatbot';
import { MessageCircle, X } from 'lucide-react';
import VITPuneImage from './VIT-Pune.webp';
import VJTIImage from './VJTI.jpg';
import COEPImage from './COEP-Pune-1.webp';
import FloatingChat from './FloatingChat';



const CollegeGuide = () => {
  const navigate = useNavigate();
  const [isScrolled, setIsScrolled] = useState(false);
  const [activeTab, setActiveTab] = useState('all');
  const [isChatOpen, setIsChatOpen] = useState(false);
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Rest of your existing constants (featuredColleges, etc.)
  const featuredColleges = [
    {
      name: 'COEP Pune',
      description: 'Premier autonomous institute for engineering excellence',
      rating: 4.8,
      details: [
        'Est. 1854',
        '100% Placement',
        'NAAC A+'
      ],
      image: COEPImage,
      tags: ['Engineering', 'Autonomous'],
      courses: ['Computer Science', 'Mechanical', 'Electronics']
    },
    {
      name: 'VJTI Mumbai',
      description: 'Leading technology institute in Maharashtra',
      rating: 4.7,
      details: [
        'Est. 1887',
        '95% Placement',
        'NBA Accredited'
      ],
      image: VJTIImage,
      tags: ['Engineering', 'Research'],
      courses: ['IT', 'Civil', 'Chemical']
    },
    {
      name: 'VIT Pune',
      description: 'Specialized in Computer & IT education',
      rating: 4.6,
      details: [
        'Est. 1983',
        '98% Placement',
        'ISO Certified'
      ],
      image: VITPuneImage,
      tags: ['IT', 'Computer Science'],
      courses: ['AI/ML', 'Data Science', 'IoT']
    }
  ];  
  const MainContent = () => (
    <>
      

      
      {/* Features Section */}
      {/* Featured Colleges Section */}
      {/* CTA Section */}
      {/* (Keep all your existing sections here) */}


      {/* Hero Section */}
      <section className="pt-32 pb-20 bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Find Your Perfect{' '}
              <span className="relative">
                <span className="text-yellow-400">Engineering College</span>
                <svg className="absolute bottom-0 left-0 w-full h-2 text-yellow-400/30" viewBox="0 0 300 12" fill="none" strokeWidth="10">
                  <path d="M2 10c50-8 150-8 296 0" stroke="currentColor" strokeLinecap="round"></path>
                </svg>
              </span>
            </h1>
            <p className="text-xl text-gray-100/90 mb-12 max-w-3xl mx-auto leading-relaxed">
              Explore top engineering colleges in Maharashtra, compare features, and make informed decisions for your future.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
              <button className="group bg-white text-blue-600 px-8 py-4 rounded-md font-medium hover:bg-gray-50 transition-colors flex items-center justify-center gap-2">
                Explore Colleges
                <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="group bg-transparent border-2 border-white text-white px-8 py-4 rounded-md font-medium hover:bg-white/10 transition-colors flex items-center justify-center gap-2">
                Compare Colleges
                <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
            
            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              {[
                { number: '50+', label: 'Partner Colleges' },
                { number: '10,000+', label: 'Student Reviews' },
                { number: '95%', label: 'Placement Rate' }
              ].map((stat, index) => (
                <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-6 transform hover:-translate-y-1 transition-transform">
                  <div className="text-3xl font-bold text-white mb-2">{stat.number}</div>
                  <div className="text-gray-100">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4">Why Choose Our Platform?</h2>
          <p className="text-gray-600 text-center mb-12 max-w-2xl mx-auto">
            Discover the tools and features that make finding your perfect college easier than ever
          </p>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { icon: Search, title: 'Smart Search', color: 'blue', description: 'Find colleges based on your preferences' },
              { icon: MapPin, title: 'Location Insights', color: 'green', description: 'Explore colleges across Maharashtra' },
              { icon: Users, title: 'Community Reviews', color: 'purple', description: 'Read authentic student reviews' },
              { icon: BookOpen, title: 'Course Compare', color: 'red', description: 'Compare courses across colleges' }
            ].map((feature, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow group">
                <div className={`w-12 h-12 mx-auto mb-4 text-${feature.color}-600 transform group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-full h-full" />
                </div>
                <h3 className="text-xl font-semibold mb-2 text-center">{feature.title}</h3>
                <p className="text-gray-600 text-center">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Colleges Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Featured Colleges</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Explore top-rated engineering colleges with excellent placement records and academic programs
            </p>
          </div>

          {/* Filters */}
          <div className="flex justify-center gap-4 mb-12">
            {['All', 'Engineering', 'IT', 'Research'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab.toLowerCase())}
                className={`px-6 py-2 rounded-full transition-colors ${
                  activeTab === tab.toLowerCase()
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {featuredColleges.map((college, index) => (
              <div key={index} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden group">
                <div className="relative">
                  <img src={college.image} alt={college.name} className="w-full h-48 object-cover" />
                  <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="font-medium">{college.rating}</span>
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-semibold group-hover:text-blue-600 transition-colors">{college.name}</h3>
                  </div>
                  <p className="text-gray-600 mb-4">{college.description}</p>
                  
                  {/* Tags */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {college.tags.map((tag, idx) => (
                      <span key={idx} className="bg-blue-50 text-blue-600 text-sm px-3 py-1 rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Details */}
                  <ul className="space-y-2 mb-6">
                    {college.details.map((detail, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        {detail}
                      </li>
                    ))}
                  </ul>

                  <button className="w-full bg-gray-50 hover:bg-gray-100 text-blue-600 font-medium py-2 rounded-md transition-colors flex items-center justify-center gap-2 group">
                    Learn More
                    <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Find Your Dream College?</h2>
          <p className="text-gray-100 mb-8 max-w-2xl mx-auto">
            Join thousands of students who have found their perfect college match through our platform
          </p>
          <button className="bg-white text-blue-600 px-8 py-4 rounded-md font-medium hover:bg-gray-50 transition-colors inline-flex items-center gap-2 group">
            Get Started Now
            <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </button>
          
        </div>
        
      </section>
    </>
  );

  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <header className={`fixed top-0 w-full bg-white z-50 transition-all duration-300 ${isScrolled ? 'shadow-md' : 'shadow-sm'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
              <svg className="w-8 h-8 text-blue-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 14l9-5-9-5-9 5 9 5z"/>
                <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/>
              </svg>
              <span className="text-blue-600 text-2xl font-bold">College Guide</span>
            </Link>
            
            <nav className="hidden md:flex space-x-8">
              <Link
                to="/"
                className="text-gray-600 hover:text-blue-600 transition-colors relative group py-2"
              >
                Home
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
              </Link>
              <Link
                to="/about"
                className="text-gray-600 hover:text-blue-600 transition-colors relative group py-2"
              >
                About
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
              </Link>
              <Link
                to="/features"
                className="text-gray-600 hover:text-blue-600 transition-colors relative group py-2"
              >
                Features
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
              </Link>
              <Link
                to="/contact"
                className="text-gray-600 hover:text-blue-600 transition-colors relative group py-2"
              >
                Contact
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></span>
              </Link>
            </nav>

            <div className="flex items-center gap-6">
              <div className="relative group">
                <Bell className="w-5 h-5 text-gray-600 hover:text-blue-600 transition-colors cursor-pointer" />
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></div>
              </div>
              <button
                onClick={() => navigate('/chat')}
                className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center gap-2 group"
              >
                Get Started
                <ChevronRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Routes */}
      <Routes>
        <Route path="/" element={<MainContent />} />
        <Route path="/about" element={<About />} />
        <Route path="/features" element={<Features />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/chat" element={<ChatPage />} /> 
      </Routes>
      {/* Floating Chat Button */}
      <button
        onClick={() => setIsChatOpen(true)}
        className={`fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 z-50 group ${
          isChatOpen ? 'scale-0' : 'scale-100'
        }`}
      >
        <MessageCircle className="w-6 h-6" />
        <span className="absolute right-full mr-3 top-1/2 -translate-y-1/2 px-4 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
          Chat with us
        </span>
      </button>

      {/* Chat Modal */}
      {isChatOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-end justify-end p-4 md:p-6 z-50">
          <div className="w-full max-w-[400px] h-[600px] bg-white rounded-xl shadow-2xl transform transition-all duration-300 animate-slide-up">
            <div className="absolute top-2 right-2">
              <button
                onClick={() => setIsChatOpen(false)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>
            <div className="h-full">
              <Chatbot />
            </div>
          </div>
        </div>
      )}

      {/* Animation Styles */}
      <style jsx>{`
        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(100%);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-slide-up {
          animation: slide-up 0.3s ease-out;
        }
      `}</style>
      <FloatingChat />
    </div>
  );
};

export default CollegeGuide;