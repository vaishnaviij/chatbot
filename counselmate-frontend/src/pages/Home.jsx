import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import ChatInterface from '../components/ChatInterface';
import robo from '../assets/robot.png';
import './Home.css';
import image1 from '../assets/img1.jpg';
import image2 from '../assets/img2.jpg';
import image3 from '../assets/img3.jpg';
import image4 from '../assets/img4.jpg';
import heroVideo from '../assets/main1.mp4';


const images = [image1, image2, image3, image4];

const Home = ({ user, onLogout }) => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHoveringTitle, setIsHoveringTitle] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const titleRef = useRef(null);

  
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (titleRef.current && isHoveringTitle) {
        setMousePosition({ x: e.clientX, y: e.clientY });
      }
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, [isHoveringTitle]);

  const calculateTitleTransform = () => {
    if (!titleRef.current || !isHoveringTitle) return {};
    
    const rect = titleRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const deltaX = (mousePosition.x - centerX) / 15;
    const deltaY = (mousePosition.y - centerY) / 15;
    
    return {
      transform: `perspective(1000px) rotateX(${-deltaY}deg) rotateY(${deltaX}deg)`,
      transition: 'transform 0.1s ease-out'
    };
  };

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
     
    <div className="home-page">
      {/* Navbar */}
      <nav className="main-navbar">
        <div className="navbar-logo">
          <span className="logo-animate">💫CounselMate</span>
        </div>
        <div className="navbar-actions">
          {user ? (
            <>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <button onClick={onLogout} className="nav-link logout">Logout</button>
            </>
          ) : (
            <Link to="/login" className="nav-link login">Login / Register</Link>
          )}
        </div>
      </nav>

     {/* Robot Try Me Icon */}
     <div 
        className="robot-try-me"
        onClick={toggleChat}
        title="Open AI Assistant"
      >
        <div className="robot-icon"> <img 
      src={robo} 
      alt="AI Assistant" 
      style={{ 
        width: '100%', 
        height: '100%', 
        objectFit: 'contain' 
      }} 
    /></div>
      </div>

      {/* Chat Interface */}
      {isChatOpen && (
        <div className="chat-interface-container">
          <ChatInterface 
            userId={user?.user_id} 
            className="medium-chat-size" 
          />
        </div>
      )}


      {/* Hero Section */}
      <header className="hero-section relative">
        {/* Video Background */}
        <video 
          autoPlay 
          loop 
          muted 
          playsInline
          className="absolute inset-0 w-full h-full object-cover opacity-50"
        >
          <source src={heroVideo} type="video/mp4" />
          Your browser does not support the video tag.
        </video>

        <div className="hero-content relative z-10">
          <h1 
            ref={titleRef}
            className="hero-title dynamic-text"
            style={calculateTitleTransform()}
            onMouseEnter={() => setIsHoveringTitle(true)}
            onMouseLeave={() => setIsHoveringTitle(false)}
          >
            CounselMate
          </h1>
          <p className="hero-subtitle">A conversational AI designed to provide knowledge, inspiration, and assistance whenever you need it.</p>
        </div>
      </header>



      {/* Features Section */}
      <section id="features" className="features-section">
      <h1 style={{ color: 'white', textAlign: 'center', margin: '2rem 0', fontSize: '2.5rem', fontWeight: '700', textShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
  How CounselMate Helps You
</h1>
        <div className="features-grid">
          <div className="feature-item">
            <div className="feature-icon">📊</div>
            <h3 >Career Guidance</h3>
            <p>Get personalized career advice based on your skills, interests, and goals.</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">🌐</div>
            <h3>Global Insights</h3>
            <p>Up-to-date industry trends</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">💡</div>
            <h3>Adaptive Learning</h3>
            <p>Continuous career recommendations</p>
          </div>
        </div>
      </section>


      <section className="generated-artwork-section container mx-auto px-4 py-16">
  <h2 className="generated-artwork-title">Generated Artwork</h2>
  <div className="generated-artwork-grid">
    {images.map((image, index) => (
      <img
        key={index}
        src={image}
        alt={`AI Generated Art ${index + 1}`}
        className="generated-artwork-image"
      />
    ))}
  </div>
</section>


      {/* Footer */}
      <footer className="main-footer">
        <div className="footer-content">
          <p>© 2025 CounselMate. All rights reserved.</p>
          <div className="social-links">
            <a href="#" className="social-icon">Twitter</a>
            <a href="#" className="social-icon">LinkedIn</a>
            <a href="#" className="social-icon">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
     
  );
};

export default Home;  