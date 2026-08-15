import axios from 'axios';
import * as ImagePicker from 'expo-image-picker';
import { useEffect, useState } from 'react';
import { Button, Image, StatusBar, StyleSheet, Text, View } from 'react-native';
import AppleHealthKit from 'react-native-health';

// IMPORTANT: Replace with actual local IP of the backend during testing
const BACKEND_URL = 'http://localhost:8000/api/v1';
const MOCK_USER_ID = 1;

export default function App() {
  const [image, setImage] = useState(null);
  const [caloriesBurnt, setCaloriesBurnt] = useState(0);

  useEffect(() => {
    // Initialize HealthKit
    const permissions = {
      permissions: {
        read: [AppleHealthKit.Constants.Permissions.ActiveEnergyBurned],
      },
    };

    AppleHealthKit.initHealthKit(permissions, (error) => {
      if (error) {
        console.log('[ERROR] Cannot grant permissions!');
      } else {
        fetchHealthData();
      }
    });
  }, []);

  const fetchHealthData = () => {
    let options = {
      startDate: new Date(new Date().setHours(0, 0, 0, 0)).toISOString(),
    };

    AppleHealthKit.getActiveEnergyBurned(options, (err, results) => {
      if (err) {
        console.log('Error fetching active energy', err);
        return;
      }
      if (results && results.length > 0) {
        // Just sum it up randomly for display
        const total = results.reduce((acc, curr) => acc + curr.value, 0);
        setCaloriesBurnt(total);
      }
    });
  };

  const pickImage = async () => {
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.5,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
      uploadMeal(result.assets[0]);
    }
  };

  const uploadMeal = async (photoAsset) => {
    let formData = new FormData();
    formData.append('user_id', MOCK_USER_ID);
    formData.append('meal_id', 1);

    let uriParts = photoAsset.uri.split('.');
    let fileType = uriParts[uriParts.length - 1];

    formData.append('file', {
      uri: photoAsset.uri,
      name: `photo.${fileType}`,
      type: `image/${fileType}`,
    });

    try {
      const response = await axios.post(`${BACKEND_URL}/meals/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert(`Meal Logged: ${response.data.item_name} (${response.data.calories_per_item} cal)`);
    } catch (error) {
      alert(`Upload failed: ${error.message}`);
    }
  };

  const syncHealthData = async () => {
    try {
      const payload = {
        user_id: MOCK_USER_ID,
        data: [{
          activity_type: 1,
          activity_date: new Date().toISOString().split('T')[0],
          calories_burnt: caloriesBurnt,
        }]
      };
      await axios.post(`${BACKEND_URL}/health/sync`, payload);
      alert('Health data synced with backend!');
    } catch (error) {
      alert(`Sync failed: ${error.message}`);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Glen Health iOS</Text>

      <View style={styles.card}>
        <Text style={styles.header}>HealthKit Data</Text>
        <Text>Calories Burnt Today: {Math.round(caloriesBurnt)} kcal</Text>
        <View style={styles.spacer} />
        <Button title="Sync Health to Backend" onPress={syncHealthData} />
      </View>

      <View style={styles.card}>
        <Text style={styles.header}>Meal Tracking</Text>
        {image && <Image source={{ uri: image }} style={styles.image} />}
        <Button title="Take Photo of Meal" onPress={pickImage} />
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', alignItems: 'center', paddingTop: 80, paddingHorizontal: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  card: { backgroundColor: 'white', padding: 20, borderRadius: 10, width: '100%', marginVertical: 10, elevation: 3 },
  header: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  image: { width: '100%', height: 200, borderRadius: 10, marginBottom: 10 },
  spacer: { height: 10 },
});
