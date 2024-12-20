const FINNHUB_API_KEY = "ctiuil9r01qgfbsviq30ctiuil9r01qgfbsviq3g";
const COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3/simple/price";

// Assets to Track
const stockSymbols = ["SPY", "QQQ", "TSLA", "NVDA"]; // SP500, Nasdaq, Tesla, Nvidia
const commoditySymbols = ["XAUUSD", "XAGUSD", "U3O8", "OIL"]; // Gold, Silver, Uranium, Oil
const cryptoIds = ["ethereum", "avalanche-2", "solana"]; // Ethereum, Avalanche, Solana

// Fetch stock prices from Finnhub
async function fetchFinnhubStockPrices(symbols) {
  const stockData = [];
  for (const symbol of symbols) {
    try {
      const response = await fetch(
        `https://finnhub.io/api/v1/quote?symbol=${symbol}&token=${FINNHUB_API_KEY}`
      );
      const data = await response.json();
      if (data.c !== undefined) {
        stockData.push({ name: symbol, price: data.c });
      }
    } catch (error) {
      console.error(`Error fetching stock price for ${symbol}:`, error);
      stockData.push({ name: symbol, price: "Error" });
    }
  }
  return stockData;
}

// Fetch commodity prices from Finnhub
async function fetchFinnhubCommodityPrices(symbols) {
  const commodityData = [];
  for (const symbol of symbols) {
    try {
      const response = await fetch(
        `https://finnhub.io/api/v1/quote?symbol=${symbol}&token=${FINNHUB_API_KEY}`
      );
      const data = await response.json();
      if (data.c !== undefined) {
        commodityData.push({ name: symbol, price: data.c });
      }
    } catch (error) {
      console.error(`Error fetching commodity price for ${symbol}:`, error);
      commodityData.push({ name: symbol, price: "Error" });
    }
  }
  return commodityData;
}

// Fetch cryptocurrency prices from CoinGecko
async function fetchCoinGeckoCryptoPrices(ids) {
  try {
    const response = await fetch(
      `${COINGECKO_BASE_URL}?ids=${ids.join(",")}&vs_currencies=usd`
    );
    const data = await response.json();
    return ids.map((id) => ({
      name: id,
      price: data[id]?.usd ?? "N/A",
    }));
  } catch (error) {
    console.error("Error fetching cryptocurrency prices:", error);
    return ids.map((id) => ({ name: id, price: "Error" }));
  }
}

// Update Ticker Function
async function updateTicker() {
  const tickerEl = document.getElementById("ticker");

  // Fetch all data
  const [stocks, commodities, cryptos] = await Promise.all([
    fetchFinnhubStockPrices(stockSymbols),
    fetchFinnhubCommodityPrices(commoditySymbols),
    fetchCoinGeckoCryptoPrices(cryptoIds),
  ]);

  // Combine and format results
  const allData = [...stocks, ...commodities, ...cryptos];
  const tickerText = allData
    .map((asset) => `${asset.name.toUpperCase()}: $${asset.price}`)
    .join(" | ");

  // Update ticker
  tickerEl.textContent = tickerText;
  console.log("Updated Ticker:", tickerText);
}

// Initial update and periodic refresh
updateTicker();
setInterval(updateTicker, 60000); // Update every 60 seconds