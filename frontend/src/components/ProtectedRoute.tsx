import { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

// TODO: Replace with real authentication logic
// For development/demo, set to true so protected routes are accessible
const isAuthenticated = true;

export default function ProtectedRoute({ children }: { children: ReactNode }) {
    if (!isAuthenticated) {
        return <Navigate to="/" replace />;
    }
    return <>{children}</>;
} 