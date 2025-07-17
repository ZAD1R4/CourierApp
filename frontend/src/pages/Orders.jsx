import React, { useEffect, useState } from 'react';
import axios from '../services/api';
import OrderCard from '../components/OrderCard';

const Orders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      const res = await axios.get('/orders/all');
      setOrders(res.data);
    };
    fetchOrders();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Заказы</h2>
      {orders.map(order => (
        <OrderCard key={order.id} order={order} />
      ))}
    </div>
  );
};

export default Orders;