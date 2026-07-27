import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/layouts/AppLayout';
import { Dashboard } from '@/pages/Dashboard';
import { AdminConsole } from '@/pages/AdminConsole';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="admin" element={<AdminConsole />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
