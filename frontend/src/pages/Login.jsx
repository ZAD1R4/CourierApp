import React, { useState } from 'react';
import axios from '../services/api';

const Login = ({ history }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const res = await axios.post('/users/login', { email, password });
      localStorage.setItem('token', res.data.access_token);
      window.location.href = '/orders';
    } catch (err) {
      alert('Ошибка входа');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Вход</h2>
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Войти</button>
    </div>
  );
};

export default Login;