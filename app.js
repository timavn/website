const assets = [
    { name: "BTC", type: "crypto", id: "bitcoin" },
    { name: "SP500", type: "stock", symbol: "^GSPC" },
    { name: "Gold", type: "commodity", symbol: "XAUUSD" },
];

// fetch function for crypto from coingecko
async function fetchCryptoPrice(id) {
    const res = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${id}&vs_currencies=usd`);
    const data = await res.json();
    return data[id]?.usd;
}

async function fetchStockPrice(symbol) {
    // Make sure you have a correct API endpoint and a valid API key here
    const res = await fetch(`https://api.twelvedata.com/price?symbol=${encodeURIComponent(symbol)}&apikey=YOUR_API_KEY`);
    const data = await res.json();
    return data.price;
}

async function fetchCommodityPrice(symbol) {
    // Update this URL and headers with a real working commodity API and key
    const res = await fetch(`https://api.example.com/commodities?symbol=${encodeURIComponent(symbol)}`, {
        headers: { 'X-RapidAPI-Key': 'YOUR_API_KEY' }
    });
    const data = await res.json();
    return data.price;
}

// main function to update ticker
async function updateTicker() {
    const tickerEl = document.getElementById('ticker');
    let results = [];

    for (const asset of assets) {
        let price;
        try {
            if (asset.type === 'crypto') {
                price = await fetchCryptoPrice(asset.id);
            } else if (asset.type === 'stock') {
                price = await fetchStockPrice(asset.symbol);
            } else if (asset.type === 'commodity') {
                price = await fetchCommodityPrice(asset.symbol);
            }

            if (price !== undefined) {
                results.push(`${asset.name}: $${price}`);
            } else {
                results.push(`${asset.name}: N/A`);
            }
        } catch (error) {
            console.error(`Failed to fetch price for ${asset.name}`, error);
            results.push(`${asset.name}: Error`);
        }
    }

    tickerEl.textContent = results.join(' | ');
}

updateTicker();
setInterval(updateTicker, 30000);