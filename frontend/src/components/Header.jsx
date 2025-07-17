import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header style={styles.header}>
      <div style={styles.container}>
        <h1 style={styles.logo}>Courier Delivery</h1>
        <nav style={styles.nav}>
          <Link to="/" style={styles.link}>Главная</Link>
          <Link to="/orders" style={styles.link}>Заказы</Link>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            Выйти
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;

// Стили (без использования CSS-файла)
const styles = {
  header: {
    backgroundColor: '#2c3e50',
    color: 'white',
    padding: '10px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0 20px',
  },
  logo: {
    margin: 0,
    fontSize: '24px',
  },
  nav: {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    fontWeight: '500',
    fontSize: '16px',
    transition: 'color 0.3s',
  },
  logoutBtn: {
    backgroundColor: '#e74c3c',
    border: 'none',
    color: 'white',
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: '14px',
    transition: 'background-color 0.3s',
  },
};