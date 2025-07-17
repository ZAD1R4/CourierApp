import React, { useEffect } from 'react';

const MapComponent = ({ couriers = [], orders = [] }) => {
  useEffect(() => {
    if (window.ymaps) {
      window.ymaps.ready(() => {
        const map = new window.ymaps.Map('map', {
          center: [55.751574, 37.573856],
          zoom: 10,
        });

        // Добавить курьеров
        couriers.forEach(courier => {
          map.geoObjects.add(new window.ymaps.Placemark(
            [courier.latitude, courier.longitude],
            { balloonContent: `Курьер ${courier.id}` }
          ));
        });

        // Добавить заказы
        orders.forEach(order => {
          map.geoObjects.add(new window.ymaps.Placemark(
            [order.latitude, order.longitude],
            { balloonContent: `Заказ ${order.id}` }
          ));
        });
      });
    }
  }, [couriers, orders]);

  return <div id="map" style={{ width: '100%', height: '500px' }}></div>;
};

export default MapComponent;