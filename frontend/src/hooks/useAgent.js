/**
 * Example React Hook for LangChain Agent Integration
 * Use this in your React components to interact with the My Daily Log Agent
 */

import { useState, useCallback } from 'react';

/**
 * Hook to query the LangChain agent
 * @param {string} baseURL - Backend URL (default: http://localhost:5000)
 * @returns {object} Query function and state
 */
export const useAgentQuery = (baseURL = 'http://localhost:5000') => {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const query = useCallback(async (question) => {
    if (!question) return;

    setLoading(true);
    setError(null);

    try {
      const url = `${baseURL}/api/query?q=${encodeURIComponent(question)}`;
      const res = await fetch(url);

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();

      if (data.success) {
        setResponse(data.response);
      } else {
        setError(data.error || 'Unknown error');
      }
    } catch (err) {
      setError(err.message);
      console.error('Agent query error:', err);
    } finally {
      setLoading(false);
    }
  }, [baseURL]);

  return { query, response, loading, error };
};

/**
 * Hook to get news
 */
export const useNews = (baseURL = 'http://localhost:5000') => {
  const [news, setNews] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getNews = useCallback(async (topic, country = 'US') => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      if (topic) params.append('topic', topic);
      if (country) params.append('country', country);

      const url = `${baseURL}/api/news?${params}`;
      const res = await fetch(url);

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      if (data.success) {
        setNews(data.response);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
      console.error('News fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [baseURL]);

  return { getNews, news, loading, error };
};

/**
 * Hook to get weather
 */
export const useWeather = (baseURL = 'http://localhost:5000') => {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getWeather = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const url = `${baseURL}/api/weather`;
      const res = await fetch(url);

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      if (data.success) {
        setWeather(data.response);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
      console.error('Weather fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [baseURL]);

  return { getWeather, weather, loading, error };
};

/**
 * Hook to get trends
 */
export const useTrends = (baseURL = 'http://localhost:5000') => {
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getTrends = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const url = `${baseURL}/api/trends`;
      const res = await fetch(url);

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      if (data.success) {
        setTrends(data.response);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
      console.error('Trends fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [baseURL]);

  return { getTrends, trends, loading, error };
};

/**
 * Hook to get GitHub trends
 */
export const useGitHubTrends = (baseURL = 'http://localhost:5000') => {
  const [repos, setRepos] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getGitHubTrends = useCallback(async (language) => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      if (language) params.append('language', language);

      const url = `${baseURL}/api/github?${params}`;
      const res = await fetch(url);

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      if (data.success) {
        setRepos(data.response);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
      console.error('GitHub trends fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [baseURL]);

  return { getGitHubTrends, repos, loading, error };
};

/**
 * Hook to get agent information
 */
export const useAgentInfo = (baseURL = 'http://localhost:5000') => {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getAgentInfo = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const url = `${baseURL}/api/agent/info`;
      const res = await fetch(url);

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      if (data.success) {
        setInfo(data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
      console.error('Agent info fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [baseURL]);

  return { getAgentInfo, info, loading, error };
};

// ============ EXAMPLE COMPONENTS ============

/**
 * Example: Simple Query Component
 */
export function AgentQueryExample() {
  const [question, setQuestion] = useState('');
  const { query, response, loading, error } = useAgentQuery();

  const handleSubmit = (e) => {
    e.preventDefault();
    query(question);
  };

  return (
    <div>
      <h2>Ask the Agent</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What would you like to know?"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      {response && (
        <div style={{ marginTop: '20px', whiteSpace: 'pre-wrap' }}>
          {response}
        </div>
      )}
    </div>
  );
}

/**
 * Example: Dashboard Component with Multiple Data Sources
 */
export function DailyLogDashboard() {
  const { response: newsResp } = useNews();
  const { weather } = useWeather();
  const { trends } = useTrends();
  const { repos: github } = useGitHubTrends();

  const handleLoadNews = () => {
    useNews().getNews('TECHNOLOGY', 'US');
  };

  const handleLoadWeather = () => {
    useWeather().getWeather();
  };

  return (
    <div>
      <h1>My Daily Log</h1>
      <button onClick={handleLoadNews}>Load News</button>
      <button onClick={handleLoadWeather}>Load Weather</button>

      {newsResp && <section><h2>News</h2><p>{newsResp}</p></section>}
      {weather && <section><h2>Weather</h2><p>{weather}</p></section>}
      {trends && <section><h2>Trends</h2><p>{trends}</p></section>}
      {github && <section><h2>GitHub</h2><p>{github}</p></section>}
    </div>
  );
}
