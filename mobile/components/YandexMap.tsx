import React from 'react';
import { WebView } from 'react-native-webview';
import { View, StyleSheet } from 'react-native';

interface YandexMapProps {
  courier: { latitude: number; longitude: number };
  order: { latitude: number; longitude: number };
}

const YandexMap: React.FC<YandexMapProps> = ({ courier, order }) => {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
      <script type="text/javascript"
        src="https://api-maps.yandex.ru/2.1/?apikey=ваш_ключ&lang=ru_RU">
      </script>
      <style type="text/css">
        html, body {
          width: 100%;
          height: 100%;
          margin: 0;
          padding: 0;
        }
        #map {
          width: 100%;
          height: 100%;
        }
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script type="text/javascript">
        ymaps.ready(function () {
          var map = new ymaps.Map("map", {
            center: [${courier.latitude}, ${courier.longitude}],
            zoom: 12
          });

          map.geoObjects.add(new ymaps.Placemark([${courier.latitude}, ${courier.longitude}], {
            balloonContent: "Вы здесь"
          }));

          map.geoObjects.add(new ymaps.Placemark([${order.latitude}, ${order.longitude}], {
            balloonContent: "Адрес заказа"
          }));
        });
      </script>
    </body>
    </html>
  `;

  return (
    <WebView
      originWhitelist={['*']}
      source={{ html }}
      style={styles.map}
    />
  );
};

const styles = StyleSheet.create({
  map: {
    flex: 1,
  },
});

export default YandexMap;