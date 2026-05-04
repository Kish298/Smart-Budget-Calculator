function renderCharts(categoryLabels, categoryValues, needs, wants, investment, savings) {
    const ctx1 = document.getElementById('categoryChart').getContext('2d');

    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryValues,
                backgroundColor: '#4CAF50'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    const ctx2 = document.getElementById('pieChart').getContext('2d');

    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Needs', 'Wants', 'Investment', 'Savings'],
            datasets: [{
                data: [needs, wants, investment, savings],
                backgroundColor: ['#4CAF50', '#FFC107', '#2196F3', '#9C27B0']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}