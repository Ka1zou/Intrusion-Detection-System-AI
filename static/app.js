document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('prediction-result');

    form.onsubmit = function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { data[key] = value; });

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                resultDiv.innerHTML = "Error: " + data.error;
            } else {
                resultDiv.innerHTML = "Prediction: " + data.prediction;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            resultDiv.innerHTML = "Error: " + error;
        });
    };
});
