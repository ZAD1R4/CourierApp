import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import YandexMap from '../components/YandexMap';
import { requestForegroundPermissionsAsync, getCurrentPositionAsync } from 'expo-location';
import { api } from '../services/api';

const CourierMapScreen = () => {
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);

  useEffect(() => {
    const getLocationAndUpdate = async () => {
      const { status } = await requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        alert('Разрешение на доступ к геолокации отклонено');
        return;
      }

      const loc = await getCurrentPositionAsync({});
      setLocation(loc.coords);

      // Отправка геолокации на сервер
      await api.post('/locations/update', {
        courier_id: 'test_courier_1',
        latitude: loc.coords.latitude,
        longitude: loc.coords.longitude,
      });
    };

    const interval = setInterval(getLocationAndUpdate, 10000); // обновлять каждые 10 сек
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      {location ? (
        <YandexMap courier={location} order={{ latitude: 55.751574, longitude: 37.573856 }} />
      ) : (
        <Text>Загрузка карты...</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default CourierMapScreen;