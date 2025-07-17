import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Страницы
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Orders from './pages/Orders';
import CourierMap from './pages/CourierMap';

// Компоненты
import Header from './components/Header';

// Защита маршрутов
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Login />;
};

function App() {
  return (
    <Router>
      <>
        <Header />
        <main style={{ padding: '20px' }}>
          <Routes>
            {/* Публичные маршруты */}
            <Route path="/login" element={<Login />} />

            {/* Приватные маршруты */}
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/orders"
              element={
                <PrivateRoute>
                  <Orders />
                </PrivateRoute>
              }
            />
            <Route
              path="/courier/:id"
              element={
                <PrivateRoute>
                  <CourierMap />
                </PrivateRoute>
              }
            />

            {/* Редирект на главную, если маршрут не найден */}
            <Route path="*" element={<Dashboard />} />
          </Routes>
        </main>
      </>
    </Router>
  );
}

export default App;