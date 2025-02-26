const cpuCtx = document.getElementById('cpuChart').getContext('2d');
const memoryCtx = document.getElementById('memoryChart').getContext('2d');
const freqCtx = document.getElementById('freqChart').getContext('2d');

const cpuChart = new Chart(cpuCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'CPU Usage (%)',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
        }]
    }
});

const memoryChart = new Chart(memoryCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Memory Usage (%)',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2
        }]
    }
});

const freqChart = new Chart(freqCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'CPU Frequency (MHz)',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2
        }]
    }
});

const updateCharts = () => {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            const timestamp = new Date().toLocaleTimeString();

            cpuChart.data.labels.push(timestamp);
            cpuChart.data.datasets[0].data.push(data.cpu_percent);
            if (cpuChart.data.labels.length > 20) {
                cpuChart.data.labels.shift();
                cpuChart.data.datasets[0].data.shift();
            }

            memoryChart.data.labels.push(timestamp);
            memoryChart.data.datasets[0].data.push(data.memory_info.percent);
            if (memoryChart.data.labels.length > 20) {
                memoryChart.data.labels.shift();
                memoryChart.data.datasets[0].data.shift();
            }

            freqChart.data.labels.push(timestamp);
            freqChart.data.datasets[0].data.push(data.cpu_frequencies);
            if (freqChart.data.labels.length > 20) {
                freqChart.data.labels.shift();
                freqChart.data.datasets[0].data.shift();
            }

            cpuChart.update();
            memoryChart.update();
            freqChart.update();
        });
};


const saveMetricsToDB = () => {
    fetch('/metrics/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
};

setInterval(updateCharts, 2000);

setInterval(saveMetricsToDB, 60000);
