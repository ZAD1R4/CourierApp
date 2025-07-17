import React, { useEffect, useState } from 'react';
import axios from '../services/api';
import MapComponent from '../components/MapComponent';

const CourierMap = ({ match }) => {
  const courierId = match.params.id;
  const [courier, setCourier] = useState(null);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const locationRes = await axios.get(`/locations/${courierId}`);
      const ordersRes = await axios.get(`/orders/all`);

      setCourier(locationRes.data);
      setOrders(ordersRes.data.filter(order => order.courier_id === courierId));
    };

    fetchData();
  }, [courierId]);

  return (
    <div style={{ padding: 20 }}>
      <h2>Местоположение курьера {courierId}</h2>
      {courier ? (
        <MapComponent couriers={[courier]} orders={orders} />
      ) : (
        <p>Загрузка данных о курьере...</p>
      )}
    </div>
  );
};

export default CourierMap;