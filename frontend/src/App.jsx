import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AssessmentForm from './pages/AssessmentForm';
import AssessmentList from './pages/AssessmentList';
import Admin from './pages/Admin';

function ProtectedRoute({ children, requireWriter = false, requireAdmin = false }) {
    const { user, loading } = useAuth();

    if (loading) {
        return <div className="flex items-center justify-center" style={{ minHeight: '100vh' }}>
            <div className="loading">Cargando...</div>
        </div>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (requireAdmin && user.role !== 'admin') {
        return <Navigate to="/dashboard" replace />;
    }

    if (requireWriter && !['admin', 'writer'].includes(user.role)) {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
}

function AppRoutes() {
    const { user } = useAuth();

    return (
        <>
            {user && <Navbar />}
            <Routes>
                <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <Login />} />
                <Route path="/dashboard" element={
                    <ProtectedRoute><Dashboard /></ProtectedRoute>
                } />
                <Route path="/assessments" element={
                    <ProtectedRoute><AssessmentList /></ProtectedRoute>
                } />
                <Route path="/assessment/new" element={
                    <ProtectedRoute requireWriter><AssessmentForm /></ProtectedRoute>
                } />
                <Route path="/assessment/:id" element={
                    <ProtectedRoute><AssessmentForm /></ProtectedRoute>
                } />
                <Route path="/admin" element={
                    <ProtectedRoute requireAdmin><Admin /></ProtectedRoute>
                } />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Routes>
        </>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;
