import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './lib/auth';

// Pages (to be created)
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import Dashboard from './pages/Dashboard';
import Applications from './pages/Applications';
import ApplicationDetail from './pages/ApplicationDetail';
import Schemes from './pages/Schemes';
import SettingsPage from './pages/Settings';
import HelpPage from './pages/Help';

function PrivateRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      <Route path="/" element={
        <PrivateRoute>
          <Dashboard />
        </PrivateRoute>
      } />
      
      <Route path="/applications" element={
        <PrivateRoute>
          <Applications />
        </PrivateRoute>
      } />
      
      <Route path="/applications/:id" element={
        <PrivateRoute>
          <ApplicationDetail />
        </PrivateRoute>
      } />
      
      <Route path="/schemes" element={
        <PrivateRoute>
          <Schemes />
        </PrivateRoute>
      } />

      <Route path="/settings" element={
        <PrivateRoute>
          <SettingsPage />
        </PrivateRoute>
      } />
      <Route path="/help" element={
        <PrivateRoute>
          <HelpPage />
        </PrivateRoute>
      } />
    </Routes>
  );
}
