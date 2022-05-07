import React from 'react';
import './App.css';
import Navbar from './layout/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import HeroSection from './components/HeroSection';

export default function App() {
  return (
    <div>
      <Navbar />
      <HeroSection />
    </div>
  );
}