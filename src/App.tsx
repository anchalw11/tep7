import { Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import HomePage from './pages/HomePage';
import Dashboard from './pages/Dashboard';
import SignalsPage from './pages/SignalsPage';
import JournalPage from './pages/JournalPage';
import './App.css';

function App() {
  useEffect(() => {
    console.log('Trader Edge Pro - Application Loaded');
  }, []);

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/signals" element={<SignalsPage />} />
        <Route path="/journal" element={<JournalPage />} />
      </Routes>
    </div>
  );
}

export default App;
