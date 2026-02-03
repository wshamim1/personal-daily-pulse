import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

// Gas Map Component
function GasMapView({ stations }) {
  const mapRef = useRef(null);
  const [userLocation, setUserLocation] = useState(null);
  const [selectedStation, setSelectedStation] = useState(null);
  const [map, setMap] = useState(null);
  const [mapError, setMapError] = useState(null);
  const markersRef = useRef([]);

  useEffect(() => {
    // Get user's current location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.log('Location access denied, using default');
          // Default to San Francisco if location not available
          setUserLocation({ lat: 37.7749, lng: -122.4194 });
        }
      );
    } else {
      // Fallback if geolocation not available
      setUserLocation({ lat: 37.7749, lng: -122.4194 });
    }
  }, []);

  useEffect(() => {
    if (mapRef.current && userLocation && stations && stations.length > 0) {
      try {
        // Check if Google Maps is loaded
        if (!window.google || !window.google.maps) {
          setMapError('Google Maps API not loaded. Please add your API key to frontend/public/index.html');
          return;
        }

        // Initialize map
        const newMap = new window.google.maps.Map(mapRef.current, {
          zoom: 13,
          center: userLocation
        });
        setMap(newMap);

        // Clear previous markers
        markersRef.current.forEach(marker => marker.setMap(null));
        markersRef.current = [];

        // Add user location marker
        new window.google.maps.Marker({
          position: userLocation,
          map: newMap,
          title: 'Your Location',
          icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        });

        // Add gas station markers
        stations.forEach((station, idx) => {
          const marker = new window.google.maps.Marker({
            position: {
              lat: userLocation.lat + (Math.random() - 0.5) * 0.05,
              lng: userLocation.lng + (Math.random() - 0.5) * 0.05
            },
            map: newMap,
            title: station.station,
            label: (idx + 1).toString()
          });

          marker.addListener('click', () => {
            setSelectedStation(station);
            newMap.setCenter(marker.getPosition());
            newMap.setZoom(15);
          });

          markersRef.current.push(marker);
        });
      } catch (error) {
        setMapError(`Error loading map: ${error.message}`);
        console.error('Map initialization error:', error);
      }
    }
  }, [userLocation, stations]);

  const getDirections = () => {
    if (!selectedStation || !userLocation) return;
    const destination = `${selectedStation.station}, ${selectedStation.address}`;
    const mapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${userLocation.lat},${userLocation.lng}&destination=${encodeURIComponent(destination)}&travelmode=driving`;
    window.open(mapsUrl, '_blank');
  };

  if (mapError) {
    return (
      <div className="map-error">
        <p>⚠️ {mapError}</p>
        <p style={{ fontSize: '0.9rem', marginTop: '1rem' }}>
          To use the map feature:
          <ol style={{ marginTop: '0.5rem' }}>
            <li>Go to Google Cloud Console</li>
            <li>Enable Maps JavaScript API</li>
            <li>Create an API key</li>
            <li>Replace 'AIzaSyDemoKeyPlaceholder' in frontend/public/index.html</li>
            <li>Refresh the page</li>
          </ol>
        </p>
      </div>
    );
  }

  return (
    <div className="gas-map-container">
      <div className="map-wrapper">
        <div className="map" ref={mapRef} style={{ width: '100%', height: '500px', backgroundColor: '#f0f0f0' }} />
      </div>
      
      {selectedStation ? (
        <div className="selected-station">
          <h3>{selectedStation.station}</h3>
          <p>{selectedStation.address}</p>
          <p>Distance: {selectedStation.distance}</p>
          <div className="gas-prices-small">
            <p><strong>Regular:</strong> {selectedStation.regular}</p>
            <p><strong>Midgrade:</strong> {selectedStation.midgrade}</p>
            <p><strong>Premium:</strong> {selectedStation.premium}</p>
            <p><strong>Diesel:</strong> {selectedStation.diesel}</p>
          </div>
          <p className="rating">⭐ {selectedStation.rating}</p>
          <button className="directions-btn" onClick={getDirections}>
            📍 Get Directions in Google Maps
          </button>
        </div>
      ) : (
        <div className="select-station">Click on a marker to select a gas station</div>
      )}
    </div>
  );
}

// Gas View Component
function GasView({ stations }) {
  const [viewType, setViewType] = useState('list');

  if (!stations || !Array.isArray(stations)) {
    return <div className="empty">No gas stations available</div>;
  }
  
  return (
    <div className="gas-container">
      <div className="view-toggle">
        <button 
          className={`toggle-btn ${viewType === 'map' ? 'active' : ''}`}
          onClick={() => setViewType('map')}
        >
          🗺️ Map View
        </button>
        <button 
          className={`toggle-btn ${viewType === 'list' ? 'active' : ''}`}
          onClick={() => setViewType('list')}
        >
          📋 List View
        </button>
      </div>

      {viewType === 'map' && (
        <GasMapView stations={stations} />
      )}
      
      {viewType === 'list' && (
        <div className="items-list">
          {stations.map((station, idx) => (
            <div key={idx} className="item-card gas-card">
              <h3>{station?.station || 'Gas Station'}</h3>
              {station?.distance && <p className="distance">📍 {station.distance}</p>}
              <div className="gas-prices">
                {station?.regular && <p><strong>Regular:</strong> {station.regular}</p>}
                {station?.midgrade && <p><strong>Midgrade:</strong> {station.midgrade}</p>}
                {station?.premium && <p><strong>Premium:</strong> {station.premium}</p>}
                {station?.diesel && <p><strong>Diesel:</strong> {station.diesel}</p>}
              </div>
              {station?.rating && <p className="rating">⭐ {station.rating}</p>}
              {station?.address && <p className="address">{station.address}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Home Dashboard Component
function HomeMenu({ onNavigate, homeWidgets }) {
  const [homeData, setHomeData] = useState({
    weather: null,
    news: null,
    quote: null,
    trends: null,
    articles: null,
    books: null,
    github: null,
    fashion: null,
    shopping: null,
    gas: null,
    food: null,
    events: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch all data in parallel for faster loading
      const [weatherRes, techNewsRes, quoteRes, booksRes, articlesRes, githubRes, fashionRes, shoppingRes, gasRes, foodRes, eventsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/weather`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/tech/trending`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/quotes/daily`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/books/trending`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/articles/medium`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/github/trending`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/fashion/trending`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/shopping/products`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/gas/prices`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/food/restaurants`).catch(() => ({ ok: false })),
        fetch(`${API_BASE_URL}/events/nearby?location=New York, NY&radius=25&unit=miles&category=music`).catch(() => ({ ok: false }))
      ]);

      const weatherData = weatherRes.ok ? await weatherRes.json() : null;
      const techNewsData = techNewsRes.ok ? await techNewsRes.json() : null;
      const quoteData = quoteRes.ok ? await quoteRes.json() : null;
      const booksData = booksRes.ok ? await booksRes.json() : null;
      const articlesData = articlesRes.ok ? await articlesRes.json() : null;
      const githubData = githubRes.ok ? await githubRes.json() : null;
      const fashionData = fashionRes.ok ? await fashionRes.json() : null;
      const shoppingData = shoppingRes.ok ? await shoppingRes.json() : null;
      const gasData = gasRes.ok ? await gasRes.json() : null;
      const foodData = foodRes.ok ? await foodRes.json() : null;
      const eventsData = eventsRes.ok ? await eventsRes.json() : null;

      setHomeData({
        weather: weatherData?.data,
        news: techNewsData?.data,
        quote: quoteData?.data,
        trends: booksData?.data,
        articles: articlesData?.data,
        books: booksData?.data,
        github: githubData?.data,
        fashion: fashionData?.data,
        shopping: shoppingData?.data,
        gas: gasData?.data,
        food: foodData?.data,
        events: eventsData?.data,
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatContent = (content, maxLength = 200) => {
    if (!content) return 'No data available';
    const text = typeof content === 'string' ? content : JSON.stringify(content);
    
    // Remove URLs and clean up formatting
    const cleaned = text
      .replace(/https?:\/\/[^\s]+/g, '')
      .replace(/\n+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    
    return cleaned.length > maxLength 
      ? cleaned.substring(0, maxLength) + '...' 
      : cleaned;
  };

  const renderWeatherCard = () => {
    if (!homeData.weather) return <p>Loading weather...</p>;
    const w = homeData.weather;
    return (
      <>
        <div className="weather-display">
          <h3>{w.condition}</h3>
          <div className="temp-display">
            <span className="temp-large">{w.temp_f}°F</span>
            <span className="temp-small">({w.temp_c}°C)</span>
          </div>
          <p>Feels like: {w.feels_like_f}°F</p>
          <p>Humidity: {w.humidity}%</p>
        </div>
      </>
    );
  };

  const renderQuoteCard = () => {
    if (!homeData.quote) return <p>Loading quote...</p>;
    return (
      <>
        <p className="quote-text">"{homeData.quote.text}"</p>
        <p className="quote-author">— {homeData.quote.author}</p>
      </>
    );
  };

  const renderNewsCard = () => {
    if (!homeData.news || !Array.isArray(homeData.news)) return <p>Loading news...</p>;
    const topStories = homeData.news.slice(0, 3);
    return (
      <ul className="news-list">
        {topStories.map((item, idx) => (
          <li key={idx}>{item.title}</li>
        ))}
      </ul>
    );
  };

  const renderTrendsCard = () => {
    if (!homeData.trends || !Array.isArray(homeData.trends)) return <p>Loading trends...</p>;
    const topTrends = homeData.trends.slice(0, 3);
    return (
      <ul className="trends-list">
        {topTrends.map((item, idx) => (
          <li key={idx}>{item.title}</li>
        ))}
      </ul>
    );
  };

  const renderArticlesCard = () => {
    if (!homeData.articles || !Array.isArray(homeData.articles)) return <p>Loading articles...</p>;
    const topArticles = homeData.articles.slice(0, 3);
    return (
      <ul className="articles-list">
        {topArticles.map((item, idx) => (
          <li key={idx}>{item.title}</li>
        ))}
      </ul>
    );
  };

  const renderBooksCard = () => {
    if (!homeData.books || !Array.isArray(homeData.books)) return <p>Loading books...</p>;
    const topBooks = homeData.books.slice(0, 3);
    return (
      <ul className="books-list">
        {topBooks.map((item, idx) => (
          <li key={idx}>{item.title}</li>
        ))}
      </ul>
    );
  };

  const renderGithubCard = () => {
    if (!homeData.github || !Array.isArray(homeData.github)) return <p>Loading repos...</p>;
    const topRepos = homeData.github.slice(0, 3);
    return (
      <ul className="github-list">
        {topRepos.map((item, idx) => (
          <li key={idx}>
            {item.name} {item.stars && `⭐ ${item.stars}`}
          </li>
        ))}
      </ul>
    );
  };

  const renderEventsCard = () => {
    if (!homeData.events || !Array.isArray(homeData.events)) return <p>Loading events...</p>;
    const topEvents = homeData.events.slice(0, 3);
    return (
      <ul className="events-list">
        {topEvents.map((item, idx) => (
          <li key={idx}>{item.name}</li>
        ))}
      </ul>
    );
  };

  const renderFashionCard = () => {
    if (!homeData.fashion || !Array.isArray(homeData.fashion)) return <p>Loading fashion...</p>;
    const topFashion = homeData.fashion.slice(0, 3);
    return (
      <ul className="fashion-list">
        {topFashion.map((item, idx) => (
          <li key={idx}>{item.title || item.name}</li>
        ))}
      </ul>
    );
  };

  const renderShoppingCard = () => {
    if (!homeData.shopping || !Array.isArray(homeData.shopping)) return <p>Loading deals...</p>;
    const topDeals = homeData.shopping.slice(0, 3);
    return (
      <ul className="shopping-list">
        {topDeals.map((item, idx) => (
          <li key={idx}>
            {item.title} {item.price && `- ${item.price}`}
          </li>
        ))}
      </ul>
    );
  };

  const renderGasCard = () => {
    if (!homeData.gas || !Array.isArray(homeData.gas)) return <p>Loading gas prices...</p>;
    const topStations = homeData.gas.slice(0, 3);
    return (
      <ul className="gas-list">
        {topStations.map((item, idx) => (
          <li key={idx}>
            {item.station} - {item.regular}
          </li>
        ))}
      </ul>
    );
  };

  const renderFoodCard = () => {
    if (!homeData.food || !Array.isArray(homeData.food)) return <p>Loading restaurants...</p>;
    const topRestaurants = homeData.food.slice(0, 3);
    return (
      <ul className="food-list">
        {topRestaurants.map((item, idx) => (
          <li key={idx}>
            {item.name} {item.rating && `⭐ ${item.rating}`}
          </li>
        ))}
      </ul>
    );
  };

  if (loading) {
    return (
      <div className="menu-section">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading your daily digest...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="home-menu">
      <div className="menu-header">
        <h1>📊 PersonalDailyPulse</h1>
        <button onClick={fetchHomeData} className="refresh-btn">🔄 Refresh</button>
      </div>

      <div className="menu-grid">
        {/* Weather Card */}
        {homeWidgets.weather && (
          <div className="menu-card weather-card" onClick={() => onNavigate('weather')}>
            <h2>☀️ Weather</h2>
            <div className="card-content">
              {renderWeatherCard()}
            </div>
            <div className="card-footer">Click to view details →</div>
          </div>
        )}

        {/* Quote Card */}
        {homeWidgets.quote && (
          <div className="menu-card quote-card" onClick={() => onNavigate('quotes')}>
            <h2>💭 Quote of the Day</h2>
            <div className="card-content">
              {renderQuoteCard()}
            </div>
            <div className="card-footer">Click for more quotes →</div>
          </div>
        )}

        {/* News Card */}
        {homeWidgets.news && (
          <div className="menu-card news-card" onClick={() => onNavigate('news')}>
            <h2>📰 Tech News</h2>
            <div className="card-content">
              {renderNewsCard()}
            </div>
            <div className="card-footer">Click to read more →</div>
          </div>
        )}

        {/* Trends Card */}
        {homeWidgets.trends && (
          <div className="menu-card trends-card" onClick={() => onNavigate('books')}>
            <h2>🔥 Trending</h2>
            <div className="card-content">
              {renderTrendsCard()}
            </div>
            <div className="card-footer">Click to explore trends →</div>
          </div>
        )}

        {/* Articles Card */}
        {homeWidgets.articles && (
          <div className="menu-card articles-card" onClick={() => onNavigate('articles')}>
            <h2>📝 Articles</h2>
            <div className="card-content">
              {renderArticlesCard()}
            </div>
            <div className="card-footer">Click to read articles →</div>
          </div>
        )}

        {/* Books Card */}
        {homeWidgets.books && (
          <div className="menu-card books-card" onClick={() => onNavigate('books')}>
            <h2>📚 Books</h2>
            <div className="card-content">
              {renderBooksCard()}
            </div>
            <div className="card-footer">Click to explore books →</div>
          </div>
        )}

        {/* GitHub Card */}
        {homeWidgets.github && (
          <div className="menu-card github-card" onClick={() => onNavigate('github')}>
            <h2>💻 GitHub</h2>
            <div className="card-content">
              {renderGithubCard()}
            </div>
            <div className="card-footer">Click to view repos →</div>
          </div>
        )}

        {/* Events Card */}
        {homeWidgets.events && (
          <div className="menu-card events-card" onClick={() => onNavigate('events')}>
            <h2>🎟️ Events</h2>
            <div className="card-content">
              {renderEventsCard()}
            </div>
            <div className="card-footer">Click to find events →</div>
          </div>
        )}

        {/* Fashion Card */}
        {homeWidgets.fashion && (
          <div className="menu-card fashion-card" onClick={() => onNavigate('fashion')}>
            <h2>👗 Fashion</h2>
            <div className="card-content">
              {renderFashionCard()}
            </div>
            <div className="card-footer">Click to see fashion →</div>
          </div>
        )}

        {/* Shopping Card */}
        {homeWidgets.shopping && (
          <div className="menu-card shopping-card" onClick={() => onNavigate('shopping')}>
            <h2>🛍️ Shopping</h2>
            <div className="card-content">
              {renderShoppingCard()}
            </div>
            <div className="card-footer">Click to browse deals →</div>
          </div>
        )}

        {/* Gas Card */}
        {homeWidgets.gas && (
          <div className="menu-card gas-card" onClick={() => onNavigate('gas')}>
            <h2>⛽ Gas Prices</h2>
            <div className="card-content">
              {renderGasCard()}
            </div>
            <div className="card-footer">Click to compare prices →</div>
          </div>
        )}

        {/* Food Card */}
        {homeWidgets.food && (
          <div className="menu-card food-card" onClick={() => onNavigate('food')}>
            <h2>🍽️ Restaurants</h2>
            <div className="card-content">
              {renderFoodCard()}
            </div>
            <div className="card-footer">Click to find restaurants →</div>
          </div>
        )}
      </div>

      {error && <div className="error-message">Error: {error}</div>}
    </div>
  );
}

function App() {
  // Load settings from localStorage or use defaults
  const loadSettings = () => {
    const saved = localStorage.getItem('personalDailyPulseSettings');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error('Failed to parse settings:', e);
      }
    }
    return {
      homeWidgets: {
        weather: true,
        quote: true,
        news: true,
        trends: true,
        articles: true,
        events: true,
        books: true,
        github: true,
        fashion: true,
        shopping: true,
        gas: true,
        food: true,
      },
      visibleTabs: {
        home: true,
        articles: true,
        social: true,
        events: true,
        weather: true,
        books: true,
        github: true,
        quotes: true,
        fashion: true,
        shopping: true,
        gas: true,
        food: true,
      },
    };
  };

  const [activeTab, setActiveTab] = useState('home');
  const [activeArticle, setActiveArticle] = useState('medium');
  const [activeNews, setActiveNews] = useState('country');
  const [activeSocial, setActiveSocial] = useState('twitter');
  const [activeFood, setActiveFood] = useState('all');
  const [eventsLocation, setEventsLocation] = useState('New York, NY');
  const [eventsRadius, setEventsRadius] = useState(25);
  const [eventsUnit, setEventsUnit] = useState('miles');
  const [eventsCategory, setEventsCategory] = useState('music');
  const [newsLocation, setNewsLocation] = useState('New York, NY');
  const [newsCountry, setNewsCountry] = useState('US');
  const [newsLang, setNewsLang] = useState('en');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chatOpen, setChatOpen] = useState(true);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState([
    { role: 'assistant', content: 'Hi! Ask me anything.' }
  ]);
  const [settings, setSettings] = useState(loadSettings);
  const [settingsOpen, setSettingsOpen] = useState(false);

  const articleSources = [
    { id: 'medium', label: 'Medium', endpoint: '/articles/medium' },
    { id: 'devto', label: 'Dev.to', endpoint: '/articles/devto' },
    { id: 'hashnode', label: 'Hashnode', endpoint: '/articles/hashnode' },
    { id: 'hackernews', label: 'Hacker News', endpoint: '/articles/hackernews' },
    { id: 'reddit', label: 'Reddit', endpoint: '/articles/reddit' },
  ];

  const newsSources = [
    { id: 'local', label: 'Local News' },
    { id: 'country', label: 'Country News' },
    { id: 'international', label: 'International News' },
    { id: 'tech', label: 'Tech News' },
  ];

  const socialSources = [
    { id: 'twitter', label: '𝕏 Twitter' },
    { id: 'linkedin', label: 'LinkedIn' },
  ];

  const foodSources = [
    { id: 'all', label: 'All', endpoint: '/food/restaurants' },
    { id: 'italian', label: 'Italian', endpoint: '/food/italian' },
    { id: 'indian', label: 'Indian', endpoint: '/food/indian' },
    { id: 'thai', label: 'Thai', endpoint: '/food/thai' },
    { id: 'chinese', label: 'Chinese', endpoint: '/food/chinese' },
    { id: 'asian', label: 'Asian', endpoint: '/food/asian' },
    { id: 'vegan', label: 'Vegan', endpoint: '/food/vegan' },
  ];

  const eventCategories = [
    'music',
    'sports',
    'tech',
    'food',
    'arts',
    'family',
    'business',
    'community',
  ];

  const citySuggestions = [
    'New York, NY',
    'Los Angeles, CA',
    'Chicago, IL',
    'Houston, TX',
    'Phoenix, AZ',
    'Philadelphia, PA',
    'San Antonio, TX',
    'San Diego, CA',
    'Dallas, TX',
    'San Jose, CA',
    'Seattle, WA',
    'Boston, MA',
    'Miami, FL',
    'London, UK',
    'Toronto, CA',
    'Vancouver, CA',
    'Sydney, AU',
    'Melbourne, AU',
    'Berlin, DE',
    'Tokyo, JP',
    'Seoul, KR',
    'Singapore, SG',
  ];

  const countrySuggestions = [
    { code: 'US', label: 'United States' },
    { code: 'GB', label: 'United Kingdom' },
    { code: 'CA', label: 'Canada' },
    { code: 'AU', label: 'Australia' },
    { code: 'IN', label: 'India' },
    { code: 'DE', label: 'Germany' },
    { code: 'FR', label: 'France' },
    { code: 'IT', label: 'Italy' },
    { code: 'ES', label: 'Spain' },
    { code: 'NL', label: 'Netherlands' },
    { code: 'SE', label: 'Sweden' },
    { code: 'NO', label: 'Norway' },
    { code: 'BR', label: 'Brazil' },
    { code: 'MX', label: 'Mexico' },
    { code: 'JP', label: 'Japan' },
    { code: 'KR', label: 'South Korea' },
    { code: 'SG', label: 'Singapore' },
    { code: 'ZA', label: 'South Africa' },
  ];

  const tabs = [
    { id: 'home', label: '🏠 Home' },
    { id: 'articles', label: '📝 Articles' },
    { id: 'news', label: '🗞️ News' },
    { id: 'social', label: '📱 Social' },
    { id: 'events', label: '🎟️ Events' },
    { id: 'weather', label: 'Weather', endpoint: '/weather' },
    { id: 'books', label: 'Books', endpoint: '/books/trending' },
    { id: 'github', label: 'GitHub', endpoint: '/github/trending' },
    { id: 'quotes', label: 'Quote', endpoint: '/quotes/daily' },
    { id: 'fashion', label: 'Fashion', endpoint: '/fashion/trending' },
    { id: 'shopping', label: '🛍️ Shopping', endpoint: '/shopping/products' },
    { id: 'gas', label: '⛽ Gas Prices', endpoint: '/gas/prices' },
    { id: 'food', label: '🍽️ Food', endpoint: '/food/restaurants' },
  ];

  // Save settings to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('personalDailyPulseSettings', JSON.stringify(settings));
  }, [settings]);

  // Toggle home widget
  const toggleHomeWidget = (widget) => {
    setSettings(prev => ({
      ...prev,
      homeWidgets: {
        ...prev.homeWidgets,
        [widget]: !prev.homeWidgets[widget],
      },
    }));
  };

  // Toggle tab visibility
  const toggleTab = (tabId) => {
    setSettings(prev => ({
      ...prev,
      visibleTabs: {
        ...prev.visibleTabs,
        [tabId]: !prev.visibleTabs[tabId],
      },
    }));
  };

  // Reset settings to default
  const resetSettings = () => {
    const defaultSettings = {
      homeWidgets: {
        weather: true,
        quote: true,
        news: true,
        trends: true,
        articles: true,
        events: true,
        books: true,
        github: true,
        fashion: true,
        shopping: true,
        gas: true,
        food: true,
      },
      visibleTabs: {
        home: true,
        articles: true,
        news: true,
        social: true,
        events: true,
        weather: true,
        books: true,
        github: true,
        quotes: true,
        fashion: true,
        shopping: true,
        gas: true,
        food: true,
      },
    };
    setSettings(defaultSettings);
    localStorage.setItem('personalDailyPulseSettings', JSON.stringify(defaultSettings));
  };

  // Filter visible tabs
  const visibleTabs = tabs.filter(tab => settings.visibleTabs[tab.id]);

  useEffect(() => {
    if (activeTab === 'home') return;

    if (activeTab === 'articles') {
      const articleEndpoint = articleSources.find(source => source.id === activeArticle)?.endpoint;
      if (articleEndpoint) {
        fetchEndpoint(articleEndpoint);
      }
      return;
    }

    if (activeTab === 'news') {
      const params = new URLSearchParams();
      if (newsLang) params.append('lang', newsLang);
      if (newsCountry) params.append('country', newsCountry);

      let newsEndpoint = '';
      if (activeNews === 'local') {
        if (newsLocation) params.append('location', newsLocation);
        newsEndpoint = `/news/local?${params.toString()}`;
      } else if (activeNews === 'country') {
        newsEndpoint = `/news/country?${params.toString()}`;
      } else if (activeNews === 'tech') {
        newsEndpoint = `/tech/trending`;
      } else {
        newsEndpoint = `/news/international?${params.toString()}`;
      }

      fetchEndpoint(newsEndpoint);
      return;
    }

    if (activeTab === 'social') {
      let socialEndpoint = '';
      if (activeSocial === 'twitter') {
        socialEndpoint = `/social/twitter`;
      } else if (activeSocial === 'linkedin') {
        socialEndpoint = `/social/linkedin`;
      }

      if (socialEndpoint) {
        fetchEndpoint(socialEndpoint);
      }
      return;
    }

    if (activeTab === 'food') {
      const foodEndpoint = foodSources.find(source => source.id === activeFood)?.endpoint;
      if (foodEndpoint) {
        fetchEndpoint(foodEndpoint);
      }
      return;
    }

    if (activeTab === 'events') {
      const params = new URLSearchParams();
      if (eventsLocation) params.append('location', eventsLocation);
      if (eventsRadius) params.append('radius', eventsRadius);
      if (eventsUnit) params.append('unit', eventsUnit);
      if (eventsCategory) params.append('category', eventsCategory);
      fetchEndpoint(`/events/nearby?${params.toString()}`);
      return;
    }

    const endpoint = tabs.find(t => t.id === activeTab)?.endpoint;
    if (endpoint) {
      fetchEndpoint(endpoint);
    }
  }, [activeTab, activeArticle, activeNews, activeSocial, newsLocation, newsCountry, newsLang, activeFood, eventsLocation, eventsRadius, eventsUnit, eventsCategory]);

  const fetchEndpoint = async (endpoint) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      const result = await response.json();
      
      if (result.success) {
        setData(result);
      } else {
        setError(result.error || 'Failed to fetch data');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderArticles = () => (
    <div className="articles-section">
      <div className="sub-tabs">
        {articleSources.map((source) => (
          <button
            key={source.id}
            className={`sub-tab ${activeArticle === source.id ? 'active' : ''}`}
            onClick={() => setActiveArticle(source.id)}
          >
            {source.label}
          </button>
        ))}
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && !error && !data && <div className="empty">No data available</div>}
      {!loading && !error && data && renderList(data.data)}
    </div>
  );

  const renderNewsSection = () => (
    <div className="news-section">
      <div className="sub-tabs">
        {newsSources.map((source) => (
          <button
            key={source.id}
            className={`sub-tab ${activeNews === source.id ? 'active' : ''}`}
            onClick={() => setActiveNews(source.id)}
          >
            {source.label}
          </button>
        ))}
      </div>

      <div className="news-filters">
        <div className="filter-group">
          <label htmlFor="news-location">City/Location</label>
          <input
            id="news-location"
            className="filter-input"
            list="city-suggestions"
            value={newsLocation}
            onChange={(e) => setNewsLocation(e.target.value)}
            placeholder="Start typing a city..."
            disabled={activeNews !== 'local'}
          />
          <datalist id="city-suggestions">
            {citySuggestions.map((city) => (
              <option key={city} value={city} />
            ))}
          </datalist>
        </div>

        <div className="filter-group">
          <label htmlFor="news-country">Country</label>
          <input
            id="news-country"
            className="filter-input"
            list="country-suggestions"
            value={newsCountry}
            onChange={(e) => setNewsCountry(e.target.value.toUpperCase())}
            placeholder="Start typing a country code..."
            disabled={activeNews === 'tech'}
          />
          <datalist id="country-suggestions">
            {countrySuggestions.map((country) => (
              <option key={country.code} value={country.code}>{country.label}</option>
            ))}
          </datalist>
        </div>

        <div className="filter-group">
          <label htmlFor="news-lang">Language</label>
          <input
            id="news-lang"
            className="filter-input"
            value={newsLang}
            onChange={(e) => setNewsLang(e.target.value.toLowerCase())}
            placeholder="en"
            disabled={activeNews === 'tech'}
          />
        </div>
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && !error && !data && <div className="empty">No data available</div>}
      {!loading && !error && data && (activeNews === 'tech' ? renderTech(data.data) : renderList(data.data))}
    </div>
  );

  const renderSocialSection = () => (
    <div className="news-section">
      <div className="sub-tabs">
        {socialSources.map((source) => (
          <button
            key={source.id}
            className={`sub-tab ${activeSocial === source.id ? 'active' : ''}`}
            onClick={() => setActiveSocial(source.id)}
          >
            {source.label}
          </button>
        ))}
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && !error && !data && <div className="empty">No data available</div>}
      {!loading && !error && data && renderTech(data.data)}
    </div>
  );

  const renderFoodSection = () => (
    <div className="food-section">
      <div className="sub-tabs">
        {foodSources.map((source) => (
          <button
            key={source.id}
            className={`sub-tab ${activeFood === source.id ? 'active' : ''}`}
            onClick={() => setActiveFood(source.id)}
          >
            {source.label}
          </button>
        ))}
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && !error && !data && <div className="empty">No data available</div>}
      {!loading && !error && data && renderFood(data.data)}
    </div>
  );

  const renderEventsSection = () => (
    <div className="events-section">
      <div className="events-filters">
        <div className="filter-group">
          <label htmlFor="events-location">City/Location</label>
          <input
            id="events-location"
            className="filter-input"
            list="city-suggestions"
            value={eventsLocation}
            onChange={(e) => setEventsLocation(e.target.value)}
            placeholder="Start typing a city..."
          />
        </div>

        <div className="filter-group">
          <label htmlFor="events-radius">Radius</label>
          <input
            id="events-radius"
            className="filter-input"
            type="number"
            min="1"
            max="200"
            value={eventsRadius}
            onChange={(e) => setEventsRadius(Number(e.target.value))}
          />
        </div>

        <div className="filter-group">
          <label htmlFor="events-unit">Unit</label>
          <select
            id="events-unit"
            className="filter-input"
            value={eventsUnit}
            onChange={(e) => setEventsUnit(e.target.value)}
          >
            <option value="miles">Miles</option>
            <option value="km">Kilometers</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="events-category">Category</label>
          <input
            id="events-category"
            className="filter-input"
            list="event-category-suggestions"
            value={eventsCategory}
            onChange={(e) => setEventsCategory(e.target.value.toLowerCase())}
            placeholder="music, sports, tech..."
          />
          <datalist id="event-category-suggestions">
            {eventCategories.map((category) => (
              <option key={category} value={category} />
            ))}
          </datalist>
        </div>
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && !error && !data && <div className="empty">No events available</div>}
      {!loading && !error && data && renderEvents(data.data)}
    </div>
  );

  const renderContent = () => {
    if (activeTab === 'home') {
      return <HomeMenu onNavigate={setActiveTab} homeWidgets={settings.homeWidgets} />;
    }

    if (activeTab === 'articles') {
      return renderArticles();
    }

    if (activeTab === 'news') {
      return renderNewsSection();
    }

    if (activeTab === 'social') {
      return renderSocialSection();
    }

    if (activeTab === 'food') {
      return renderFoodSection();
    }

    if (activeTab === 'events') {
      return renderEventsSection();
    }

    if (loading) {
      return <div className="loading">Loading...</div>;
    }

    if (error) {
      return <div className="error">Error: {error}</div>;
    }

    if (!data) {
      return <div className="empty">No data available</div>;
    }

    switch (activeTab) {
      case 'weather':
        return renderWeather(data.data);
      case 'quotes':
        return renderQuote(data.data);
      case 'books':
        return renderBooks(data.data);
      case 'github':
        return renderGitHub(data.data);
      case 'shopping':
        return renderShopping(data.data);
      case 'gas':
        return <GasView stations={data.data} />;
      default:
        return renderList(data.data);
    }
  };

  const renderWeather = (weather) => (
    <div className="weather-card">
      <h2>{weather.condition}</h2>
      <div className="temp">
        <span className="temp-large">{weather.temp_f}°F</span>
        <span className="temp-small">({weather.temp_c}°C)</span>
      </div>
      <p>Feels like: {weather.feels_like_f}°F ({weather.feels_like_c}°C)</p>
      <p>Humidity: {weather.humidity}%</p>
    </div>
  );

  const renderQuote = (quote) => (
    <div className="quote-card">
      <blockquote>"{quote.text}"</blockquote>
      <cite>— {quote.author}</cite>
    </div>
  );

  const renderBooks = (books) => {
    if (!books || !Array.isArray(books)) {
      return <div className="empty">No books available</div>;
    }
    
    return (
      <div className="items-list">
        {books.map((book, idx) => (
          <div key={idx} className="item-card">
            <h3>{book?.title || 'No Title'}</h3>
            <p className="authors">{book?.authors?.join(', ') || 'Unknown Author'}</p>
            {book?.publishedDate && <p className="date">{book.publishedDate}</p>}
            {book?.infoLink && (
              <a href={book.infoLink} target="_blank" rel="noopener noreferrer">
                View Details →
              </a>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderGitHub = (repos) => (
    <div className="items-list">
      {repos?.map((repo, idx) => (
        <div key={idx} className="item-card">
          <h3>{repo?.name || 'Unknown'}</h3>
          {repo?.language && <span className="badge">{repo.language}</span>}
          {repo?.description && <p>{repo.description}</p>}
          <div className="stats">
            <span>⭐ {repo?.stars ? repo.stars.toLocaleString() : '0'}</span>
          </div>
          <a href={repo?.url} target="_blank" rel="noopener noreferrer">
            View on GitHub →
          </a>
        </div>
      ))}
    </div>
  );

  const renderTech = (stories) => {
    if (!stories || !Array.isArray(stories)) {
      return <div className="empty">No stories available</div>;
    }
    
    return (
      <div className="items-list">
        {stories.map((story, idx) => (
          <div key={idx} className="item-card">
            <h3>{story?.title || 'No Title'}</h3>
            <div className="stats">
              <span>⬆️ {story?.score || 0}</span>
              <span>💬 {story?.comments || 0}</span>
            </div>
            {story?.url && (
              <a href={story.url} target="_blank" rel="noopener noreferrer">
                Read Article →
              </a>
            )}
            {story?.hn_link && (
              <a href={story.hn_link} target="_blank" rel="noopener noreferrer" className="secondary-link">
                HN Discussion →
              </a>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderLocalNews = (result) => (
    <div className="items-list">
      {result.location && (
        <div className="location-badge">📍 {result.location}</div>
      )}
      {renderList(result.data)}
    </div>
  );

  const renderShopping = (products) => {
    if (!products || !Array.isArray(products)) {
      return <div className="empty">No products available</div>;
    }
    
    return (
      <div className="items-list">
        {products.map((product, idx) => (
          <div key={idx} className="item-card shopping-card">
            <h3>{product?.title || 'No Title'}</h3>
            <div className="price-section">
              {product?.original_price && (
                <span className="original-price">{product.original_price}</span>
              )}
              {product?.price && (
                <span className="discount-price"><strong>{product.price}</strong></span>
              )}
              {product?.discount && (
                <span className="discount-badge">{product.discount} OFF</span>
              )}
            </div>
            {product?.rating && <p className="rating">⭐ {product.rating}</p>}
            {product?.store && <p className="store">{product.store}</p>}
            {product?.link && (
              <a href={product.link} target="_blank" rel="noopener noreferrer">
                View Product →
              </a>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderFood = (restaurants) => {
    if (!restaurants || !Array.isArray(restaurants)) {
      return <div className="empty">No restaurants available</div>;
    }
    
    return (
      <div className="items-list">
        {restaurants.map((restaurant, idx) => (
          <div key={idx} className="item-card food-card">
            <h3>{restaurant?.name || 'No Name'}</h3>
            <div className="food-info">
              <span className="cuisine-badge">{restaurant?.cuisine || 'Restaurant'}</span>
              {restaurant?.rating && (
                <span className="rating">⭐ {restaurant.rating}</span>
              )}
            </div>
            {restaurant?.reviews && (
              <p className="reviews">📝 {restaurant.reviews} reviews</p>
            )}
            <div className="price-section">
              {restaurant?.price && (
                <span className={`price-indicator price-${restaurant.price.length}`}>
                  {restaurant.price}
                </span>
              )}
            </div>
            {restaurant?.specialties && restaurant.specialties.length > 0 && (
              <div className="specialties">
                {restaurant.specialties.map((specialty, sidx) => (
                  <span key={sidx} className="specialty-tag">{specialty}</span>
                ))}
              </div>
            )}
            {restaurant?.address && <p className="address">📍 {restaurant.address}</p>}
            {restaurant?.hours && <p className="hours">🕐 {restaurant.hours}</p>}
            {restaurant?.link && (
              <a href={restaurant.link} target="_blank" rel="noopener noreferrer">
                Reserve Now →
              </a>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderEvents = (events) => {
    if (!events || !Array.isArray(events)) {
      return <div className="empty">No events available</div>;
    }

    return (
      <div className="items-list">
        {events.map((event, idx) => (
          <div key={idx} className="item-card">
            <h3>{event?.name || 'Event'}</h3>
            {event?.category && <span className="badge">{event.category}</span>}
            <div className="stats">
              {event?.date && <span>📅 {event.date}</span>}
              {event?.time && <span>🕒 {event.time}</span>}
            </div>
            {event?.venue && <p>📍 {event.venue}</p>}
            {event?.city && <p>{event.city}{event.country ? `, ${event.country}` : ''}</p>}
            {event?.url && (
              <a href={event.url} target="_blank" rel="noopener noreferrer">
                View Event →
              </a>
            )}
          </div>
        ))}
      </div>
    );
  };

  const sendChat = async () => {
    const message = chatInput.trim();
    if (!message) return;

    setChatMessages(prev => [...prev, { role: 'user', content: message }]);
    setChatInput('');

    try {
      const response = await fetch(`${API_BASE_URL}/query?q=${encodeURIComponent(message)}`);
      const result = await response.json();
      if (result.success) {
        setChatMessages(prev => [...prev, { role: 'assistant', content: result.response }]);
      } else {
        setChatMessages(prev => [...prev, { role: 'assistant', content: result.error || 'Sorry, something went wrong.' }]);
      }
    } catch (err) {
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Network error. Please try again.' }]);
    }
  };

  const handleChatKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendChat();
    }
  };

  const renderList = (items) => {
    if (!items || !Array.isArray(items)) {
      return <div className="empty">No items available</div>;
    }
    
    return (
      <div className="items-list">
        {items.map((item, idx) => (
          <div key={idx} className="item-card">
            <h3>{item?.title || 'No Title'}</h3>
            {item?.pubDate && <p className="date">{new Date(item.pubDate).toLocaleDateString()}</p>}
            {item?.link && (
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                Read More →
              </a>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📊 PersonalDailyPulse</h1>
        <p>Your personalized dashboard for trending content</p>
        <button className="settings-btn" onClick={() => setSettingsOpen(!settingsOpen)}>
          ⚙️ Settings
        </button>
      </header>

      <nav className="tabs">
        {visibleTabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Settings Modal */}
      {settingsOpen && (
        <div className="settings-modal-overlay" onClick={() => setSettingsOpen(false)}>
          <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
            <div className="settings-header">
              <h2>⚙️ Settings</h2>
              <button onClick={() => setSettingsOpen(false)}>✕</button>
            </div>
            
            <div className="settings-content">
              {/* Home Widgets Section */}
              <div className="settings-section">
                <h3>🏠 Home Dashboard Widgets</h3>
                <p className="settings-description">Choose which widgets to display on the home page</p>
                <div className="settings-options">
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.weather}
                      onChange={() => toggleHomeWidget('weather')}
                    />
                    <span>☀️ Weather</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.quote}
                      onChange={() => toggleHomeWidget('quote')}
                    />
                    <span>💭 Quote of the Day</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.news}
                      onChange={() => toggleHomeWidget('news')}
                    />
                    <span>📰 Tech News</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.trends}
                      onChange={() => toggleHomeWidget('trends')}
                    />
                    <span>🔥 Trending</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.articles}
                      onChange={() => toggleHomeWidget('articles')}
                    />
                    <span>📝 Articles</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.books}
                      onChange={() => toggleHomeWidget('books')}
                    />
                    <span>📚 Books</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.github}
                      onChange={() => toggleHomeWidget('github')}
                    />
                    <span>💻 GitHub</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.events}
                      onChange={() => toggleHomeWidget('events')}
                    />
                    <span>🎟️ Events</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.fashion}
                      onChange={() => toggleHomeWidget('fashion')}
                    />
                    <span>👗 Fashion</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.shopping}
                      onChange={() => toggleHomeWidget('shopping')}
                    />
                    <span>🛍️ Shopping</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.gas}
                      onChange={() => toggleHomeWidget('gas')}
                    />
                    <span>⛽ Gas Prices</span>
                  </label>
                  <label className="settings-option">
                    <input
                      type="checkbox"
                      checked={settings.homeWidgets.food}
                      onChange={() => toggleHomeWidget('food')}
                    />
                    <span>🍽️ Restaurants</span>
                  </label>
                </div>
              </div>

              {/* Visible Tabs Section */}
              <div className="settings-section">
                <h3>📑 Visible Menu Tabs</h3>
                <p className="settings-description">Choose which tabs to show in the navigation menu</p>
                <div className="settings-options">
                  {tabs.map(tab => (
                    <label key={tab.id} className="settings-option">
                      <input
                        type="checkbox"
                        checked={settings.visibleTabs[tab.id]}
                        onChange={() => toggleTab(tab.id)}
                        disabled={tab.id === 'home'} // Can't disable home
                      />
                      <span>{tab.label}</span>
                      {tab.id === 'home' && <span className="required-tag">Required</span>}
                    </label>
                  ))}
                </div>
              </div>
            </div>

            <div className="settings-footer">
              <button className="reset-btn" onClick={resetSettings}>
                🔄 Reset to Defaults
              </button>
              <button className="save-btn" onClick={() => setSettingsOpen(false)}>
                ✓ Save & Close
              </button>
            </div>
          </div>
        </div>
      )}

      <main className="content-layout">
        <div className="content">
          {renderContent()}
        </div>

        {chatOpen ? (
          <aside className="chat-panel open">
            <div className="chat-header">
              <span>💬 Chat</span>
              <button
                className="chat-toggle"
                onClick={() => setChatOpen(false)}
                aria-label="Collapse chat"
              >
                ✕
              </button>
            </div>
            <div className="chat-body">
              {chatMessages.map((msg, idx) => (
                <div key={idx} className={`chat-message ${msg.role}`}>
                  <div className="chat-bubble">{msg.content}</div>
                </div>
              ))}
            </div>
            <div className="chat-input">
              <textarea
                rows={2}
                placeholder="Ask anything..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={handleChatKeyDown}
              />
              <button onClick={sendChat}>Send</button>
            </div>
          </aside>
        ) : (
          <button
            className="chat-fab"
            onClick={() => setChatOpen(true)}
            aria-label="Open chat"
          >
            💬
          </button>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by various free APIs</p>
      </footer>
    </div>
  );
}

export default App;
