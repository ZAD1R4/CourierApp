import React from 'react';

const OrderCard = ({ order }) => {
  return (
    <div style={{
      border: "1px solid #ccc",
      borderRadius: "8px",
      padding: "15px",
      marginBottom: "10px"
    }}>
      <h3>Заказ #{order.id}</h3>
      <p><strong>Адрес:</strong> {order.address}</p>
      <p><strong>Статус:</strong> {order.status}</p>
      {order.courier_id && <p><strong>Курьер ID:</strong> {order.courier_id}</p>}
    </div>
  );
};

export default OrderCard;