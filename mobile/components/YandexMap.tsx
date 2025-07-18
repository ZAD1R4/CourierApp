import React, { useEffect } from 'react';

const MapComponent = () => {
  useEffect(() => {
    if (window.ymaps) {
      window.ymaps.ready(() => {
        const map = new window.ymaps.Map('map', {
          center: [55.751574, 37.573856],
          zoom: 10,
        });

        // Пример маркера курьера
        map.geoObjects.add(new window.ymaps.Placemark(
          [55.75, 37.57],
          { balloonContent: "Курьер" }
        ));

        // Пример маркера заказа
        map.geoObjects.add(new window.ymaps.Placemark(
          [55.76, 37.58],
          { balloonContent: "Адрес доставки" }
        ));
      });
    }
  }, []);

  return (
    <div>
      <h2>Карта с курьерами и заказами</h2>
      <div id="map" style={{ width: '100%', height: '500px', marginTop: '20px' }}></div>
    </div>
  );
};

export default MapComponent;