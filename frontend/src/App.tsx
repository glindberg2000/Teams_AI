import Sidebar from './components/Sidebar';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import SecretsListPage from './pages/SecretsListPage';
import SecretDetailPage from './pages/SecretDetailPage';
import SecretFormPage from './pages/SecretFormPage';
import ProtectedRoute from './components/ProtectedRoute';
import ChatPage from './pages/ChatPage';
import TeamsPage from './pages/TeamsPage';
import RolesPage from './pages/RolesPage';
import SessionsPage from './pages/SessionsPage';
import TasksPage from './pages/TasksPage';
import SettingsPage from './pages/SettingsPage';
import HelpPage from './pages/HelpPage';
import './App.css';

function App() {
  return (
    <div>
      <Sidebar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/chat" element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />
          <Route path="/teams" element={<ProtectedRoute><TeamsPage /></ProtectedRoute>} />
          <Route path="/roles" element={<ProtectedRoute><RolesPage /></ProtectedRoute>} />
          <Route path="/secrets" element={<ProtectedRoute><SecretsListPage /></ProtectedRoute>} />
          <Route path="/secrets/new" element={<ProtectedRoute><SecretFormPage /></ProtectedRoute>} />
          <Route path="/secrets/:id" element={<ProtectedRoute><SecretDetailPage /></ProtectedRoute>} />
          <Route path="/sessions" element={<ProtectedRoute><SessionsPage /></ProtectedRoute>} />
          <Route path="/tasks" element={<ProtectedRoute><TasksPage /></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
          <Route path="/help" element={<HelpPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
