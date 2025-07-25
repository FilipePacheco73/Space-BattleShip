import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import Home from './pages/Home';
import Users from './pages/Users';
import Ships from './pages/Ships';
import Market from './pages/Market';
import Battle from './pages/Battle';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { SidebarProvider } from './contexts/SidebarContext';
import { LanguageProvider } from './contexts/LanguageContext';
import PrivateRoute from './components/PrivateRoute';
import ErrorBoundary from './components/ErrorBoundary';
import SessionExpiredModal from './components/SessionExpiredModal';
import './App.css';

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const { showSessionExpired, setShowSessionExpired } = useAuth();
  
  // Routes that use the sidebar layout (game pages)
  const sidebarRoutes = ['/dashboard', '/users', '/ships', '/market', '/battle'];
  const useSidebar = sidebarRoutes.includes(location.pathname);

  const handleSessionExpiredClose = () => {
    setShowSessionExpired(false);
    navigate('/');
  };

  const handleSessionExpiredLogin = () => {
    setShowSessionExpired(false);
    navigate('/login');
  };

  return (
    <div className="w-full min-h-screen">
      <div className={useSidebar ? "text-slate-50" : "w-full text-slate-50"}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Navigate to="/" replace />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={
            <PrivateRoute>
              <ErrorBoundary>
                <Dashboard />
              </ErrorBoundary>
            </PrivateRoute>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/ships" element={<Ships />} />
          <Route path="/market" element={<Market />} />
          <Route path="/battle" element={<Battle />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
      
      {/* Session Expired Modal */}
      <SessionExpiredModal 
        isOpen={showSessionExpired}
        onClose={handleSessionExpiredClose}
        onLogin={handleSessionExpiredLogin}
      />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <SidebarProvider>
          <Router>
            <AppContent />
          </Router>
        </SidebarProvider>
      </LanguageProvider>
    </AuthProvider>
  );
}

export default App;
