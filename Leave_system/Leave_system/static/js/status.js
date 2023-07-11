document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.getElementsByClassName('alert');
    Array.prototype.forEach.call(alerts, function(alert) {
    setTimeout(function() {
        alert.style.display = 'none';
    }, 5000);
    });
});

var cell = document.getElementById('personIdCell');
var value = cell.textContent;
var paddedValue = value.toString().padStart(6, '0');
cell.textContent = paddedValue;