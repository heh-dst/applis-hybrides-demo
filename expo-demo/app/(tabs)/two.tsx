import { Text, View } from "@/components/Themed";
import React, { useState, useEffect } from "react";
import { StyleSheet, FlatList } from "react-native";

type Attraction = {
  name: string;
  status: string;
  waitingTime: number;
};

export default function TabTwoScreen() {
  const [attractions, setAttractions] = useState<Attraction[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/attractions")
      .then((response) => response.json())
      .then((data) => setAttractions(data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tab Two</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <FlatList
        data={attractions}
        renderItem={({ item, index, separators }) => (
          <View style={styles.row}>
            <Text style={styles.cell}>{item.name}</Text>
            <Text style={styles.cell}>{item.status}</Text>
            <Text style={styles.cell}>{item.waitingTime} min</Text>
          </View>
        )}
        keyExtractor={(item, index) => index.toString()}
        ListHeaderComponent={() => (
          <View style={styles.header}>
            <Text style={styles.headerText}>Name</Text>
            <Text style={styles.headerText}>État</Text>
            <Text style={styles.headerText}>Temps d'attente</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: "80%",
  },
  row: {
    flexDirection: "row",
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
  cell: {
    flex: 1,
    textAlign: "center",
  },
  header: {
    flexDirection: "row",
    padding: 10,
    backgroundColor: "#f0f0f0",
  },
  headerText: {
    flex: 1,
    fontWeight: "bold",
    textAlign: "center",
  },
});
