$(document).ready(function () {

    $("#analytic").addClass("active");

    $("#analytic > a:nth-child(1)").attr("href", "#");


     //var data = JSON.parse(received_data);

     item = 0;
var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
            label: '# of Patients',
            data: [1, 2, 4, 8, 16, 4, 8, 2, 16, 1, 4, 2],
            backgroundColor: [
                'rgba(170, 152, 169, .4)',
                'rgba(153, 102, 204, .4)',
                'rgba(127, 255, 212, .4)',
                'rgba(168, 195, 188, .4)',
                'rgba(80, 200, 120, .4)',
                'rgb(184,146,162, .4)',
                'rgba(224, 17, 95, .4)',
                'rgba(230, 226, 0, .4)',
                'rgba(15, 82, 186, .4)',
                'rgba(215, 59, 62, .4)',
                'rgba(255, 165, 0, .4)',
                'rgba(64, 224, 208, .4)'
            ],
            borderColor: [
                'rgba(170, 152, 169, 1)',
                'rgba(153, 102, 204, 1)',
                'rgba(127, 255, 212, 1)',
                'rgba(168, 195, 188, 1)',
                'rgba(80, 200, 120, 1)',
                'rgb(184,146,162, 1)',
                'rgba(224, 17, 95, 1)',
                'rgba(230, 226, 0, 1)',
                'rgba(15, 82, 186, 1)',
                'rgba(215, 59, 62, 1)',
                'rgba(255, 165, 0, 1)',
                'rgba(64, 224, 208, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

});