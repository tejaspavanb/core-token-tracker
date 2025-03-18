import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TokenList() {
  const [tokens, setTokens] = useState([]);
  const [filters, setFilters] = useState({
    minLiquidity: 0,
    maxLiquidity: 1000000,
    minHolderCount: 0,
    maxHolderCount: 10000
  });

  useEffect(() => {
    fetchTokens();
  }, []);

  const fetchTokens = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/tokens');
      setTokens(response.data);
    } catch (error) {
      console.error('Error fetching tokens:', error);
    }
  };

  const applyFilters = (token) => {
    return (
      token.liquidity >= filters.minLiquidity &&
      token.liquidity <= filters.maxLiquidity &&
      token.holderCount >= filters.minHolderCount &&
      token.holderCount <= filters.maxHolderCount
    );
  };

  const predictTokenSuccess = async (token) => {
    try {
      const response = await axios.post('http://localhost:5000/api/predict', {
        liquidity: token.liquidity,
        holderCount: token.holderCount,
        totalSupply: token.totalSupply,
        launchTime: token.launchTime
      });
      return response.data.prediction;
    } catch (error) {
      console.error('Error predicting token success:', error);
      return null;
    }
  };

  return (
    <div className="token-list">
      <div className="filter-panel">
        <label>
          Min Liquidity:
          <input
            type="number"
            value={filters.minLiquidity}
            onChange={(e) => setFilters({...filters, minLiquidity: e.target.value})}
          />
        </label>
        {/* Add other filter inputs */}
      </div>

      <div className="tokens">
        {tokens.filter(applyFilters).map(token => (
          <div key={token.address} className="token-card">
            <h3>Token: {token.address}</h3>
            <p>Launch Time: {new Date(token.launchTime * 1000).toLocaleString()}</p>
            <p>Liquidity: {token.liquidity}</p>
            <p>Holder Count: {token.holderCount}</p>
            <button onClick={() => predictTokenSuccess(token)}>Predict Success</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TokenList;