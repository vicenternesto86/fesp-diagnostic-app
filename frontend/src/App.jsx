import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import AssessmentForm from './pages/AssessmentForm';
import AssessmentList from './pages/AssessmentList';
import Admin from './pages/Admin';

// Open access - no login required
function AppRoutes() {
    return (
        <>
            <Navbar />
            <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/assessments" element={<AssessmentList />} />
                <Route path="/assessment/new" element={<AssessmentForm />} />
                <Route path="/assessment/:id" element={<AssessmentForm />} />
                <Route path="/admin" element={<Admin />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/login" element={<Navigate to="/dashboard" replace />} />
            </Routes>
        </>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AppRoutes />
        </BrowserRouter>
    );
}

export default App;
