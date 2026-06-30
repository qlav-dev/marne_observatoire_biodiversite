import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Configure axios base URL
const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [message, setMessage] = useState('');
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch data from backend
  useEffect(() => {
    fetchMessage();
    fetchItems();
  }, []);

  const fetchMessage = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/`);
      setMessage(response.data.message);
    } catch (error) {
      console.error('Error fetching message:', error);
    }
  };

  const fetchItems = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/items`);
      setItems(response.data.items);
    } catch (error) {
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  };

  const addItem = async (e) => {
    e.preventDefault();
    if (!newItem.trim()) return;

    try {
      await axios.post(`${API_BASE_URL}/api/items`, {
        name: newItem,
        description: 'Added from React'
      });
      setNewItem('');
      fetchItems(); // Refresh the list
    } catch (error) {
      console.error('Error adding item:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>React + FastAPI</h1>
        <p>Backend says: {message || 'Loading...'}</p>

        <div className="items-section">
          <h2>Items</h2>
          {loading ? (
            <p>Loading items...</p>
          ) : (
            <ul>
              {items.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          )}

          <form onSubmit={addItem}>
            <input
              type="text"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              placeholder="Enter new item"
            />
            <button type="submit">Add Item</button>
          </form>
        </div>
      </header>
    </div>
  );
}

export default App;