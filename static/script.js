document.getElementById('weatherForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const city = document.getElementById('cityInput').value;
    const response = await fetch(`/weather?city=${city}`);
    const data = await response.json();
    if (response.ok) {
        document.getElementById('result').innerHTML = `
            <div class="alert alert-success">
                <h4>${data.city}</h4>
                <p>Temperature: ${data.temperature} °F</p>
            </div>
        `;            
    } else {
        document.getElementById('result').innerHTML = `
            <div class="alert alert-danger">
                <p>${data.error}</p>
            </div>        
        `;
    }
});