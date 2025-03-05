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


const updateAnalytics = () => {
    const range = document.getElementById('time-range').value;
    let endTime = new Date().toISOString();
    let startTime;

    if (range === '1h') {
        startTime = new Date(Date.now() - 60 * 60 * 1000).toISOString();
    } else if (range === '7d') {
        startTime = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
    } else {
        startTime = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    }

    fetch(`/metrics/analytics?start_time=${startTime}&end_time=${endTime}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('cpuAvg').innerText = data.cpu_percent.average.toFixed(2);
            document.getElementById('cpuMax').innerText = data.cpu_percent.max;
            document.getElementById('cpuMin').innerText = data.cpu_percent.min;

            document.getElementById('memAvg').innerText = data.memory_percent.average.toFixed(2);
            document.getElementById('memMax').innerText = data.memory_percent.max;
            document.getElementById('memMin').innerText = data.memory_percent.min;

            document.getElementById('freqAvg').innerText = data.cpu_frequencies.average.toFixed(2);
            document.getElementById('freqMax').innerText = data.cpu_frequencies.max;
            document.getElementById('freqMin').innerText = data.cpu_frequencies.min;
        });
};

document.getElementById('time-range').addEventListener('change', updateAnalytics);

updateAnalytics();

setInterval(updateCharts, 2000);

setInterval(saveMetricsToDB, 60000);
