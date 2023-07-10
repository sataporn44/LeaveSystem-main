
var yyyy = new Date().getFullYear();
// var tommorrow = new Date().getDate() + 1;
var holiday = [
  new Date(yyyy, 0, 1).getTime(), //วันปีใหม่
  new Date(yyyy, 2, 6).getTime(), //วันมาฆบูชา
  new Date(yyyy, 3, 6).getTime(), //วันจักรี
  new Date(yyyy, 3, 13).getTime(), //วันสงกรานต์
  new Date(yyyy, 3, 14).getTime(), //วันสงกรานต์
  new Date(yyyy, 3, 15).getTime(), //วันสงกรานต์
  new Date(yyyy, 4, 4).getTime(), //วันฉัตรมงคล
  new Date(yyyy, 5, 3).getTime(), //วันวิสาขบูชา
  new Date(yyyy, 6, 28).getTime(), //วันเฉลิมพระชนมพรรษา ร.10
  new Date(yyyy, 7, 1).getTime(), //วันอาสาฬหบูชา
  new Date(yyyy, 7, 12).getTime(), //วันแม่
  new Date(yyyy, 9, 13).getTime(), //วันคล้ายวันสวรรคต ร.9
  new Date(yyyy, 9, 23).getTime(), //วันปิยมหาราช
  new Date(yyyy, 11, 5).getTime(), //วันพ่อ
  new Date(yyyy, 11, 10).getTime(), //วันรัฐธรรมนูญ
];

$('#datepicker_1 , #datepicker_2').datepicker({
  dateFormat: "d M yy",
    // minDate: 0,
    // maxDate: "+4M",
    showButtonPanel: true,
    changeMonth: true,
    changeYear: true,
  beforeShowDay: function(date) {
    var showDay = true;
    if (date.getDay() == 0 || date.getDay() == 6) {
      showDay = false; // ไม่แสดงวันเสาร์และวันอาทิตย์
    }
    if ($.inArray(date.getTime(), holiday) > -1) {
      showDay = false;  
    }
    return [showDay];
  }  
});

var formattedHoliday = holiday.map(function(timestamp) {
    var date = new Date(timestamp);
    return date.toLocaleDateString('th-TH');
    });
    console.log(formattedHoliday);


// เพิ่ม event listener ให้กับฟิลด์ From_Date เมื่อมีการเลือกวันที่
$('#datepicker_1').on('change', function() {
  var fromDate = new Date($('#datepicker_1').val());
  $('#datepicker_2').datepicker('setDate', fromDate);
  enableNumberLeave();
  calculateLeaveDays();
});

// เพิ่ม event listener ให้กับฟิลด์ To_Date เมื่อมีการเลือกวันที่
$('#datepicker_2').on('change', function() {
  calculateLeaveDays();
});

function enableNumberLeave() {
  $('#numberLeave').prop('disabled', false);
  $('#datepicker_2').prop('disabled', false);

}

function calculateLeaveDays() {
  var fromDate = new Date($('#datepicker_1').val());
  var toDate = new Date($('#datepicker_2').val());

  if (fromDate && toDate) {
    var millisecondsPerDay = 24 * 60 * 60 * 1000; // จำนวนมิลลิวินาทีในหนึ่งวัน
    var diff = Math.round(((toDate - fromDate) / millisecondsPerDay)+1); // คำนวณจำนวนวันที่ผ่านไป

    var weekends = 0;
    var holidays = 0;

    for (var i = 0; i < diff; i++) {
      var currentDate = new Date(fromDate.getTime() + i * millisecondsPerDay);
      var dayOfWeek = currentDate.getDay();

      if (dayOfWeek === 0 || dayOfWeek === 6) {
        weekends++;
      }

      for (var j = 0; j < holiday.length; j++) {
        var holidayDate = new Date(holiday[j]);

        if (
          holidayDate.getDate() === currentDate.getDate() &&
          holidayDate.getMonth() === currentDate.getMonth() &&
          holidayDate.getFullYear() === currentDate.getFullYear()
        ) {
          holidays++;
          break;
        }
      }
    }
    var adjustedDiff = diff - weekends - holidays;

    $('#numberLeave').val(adjustedDiff); // แสดงผลลัพธ์ที่ปรับแล้วในฟิลด์ numberLeave
  }
}
// {% comment %} 

document.getElementById("datepicker_1").addEventListener("input", movedis);

function movedis() {
  document.getElementById("numberLeave").removeAttribute("disabled");
  document.getElementById("datepicker_2").removeAttribute("disabled");
  
  var fromDateValue = document.getElementById("datepicker_1").value;
  document.getElementById("datepicker_2").value = fromDateValue;
}


document.getElementById("datepicker_1").addEventListener("input", calculateLeaveDays);
document.getElementById("datepicker_2").addEventListener("input", calculateLeaveDays);

function calculateLeaveDays() {
  var fromDateValue = document.getElementById("datepicker_1").value;
  var toDateValue = document.getElementById("datepicker_2").value;
  
  if (fromDateValue && toDateValue) {
    var fromDate = new Date(fromDateValue);
    var toDate = new Date(toDateValue);

    var timeDiff = Math.abs(toDate.getTime() - fromDate.getTime());
    var leaveDays = Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;

    document.getElementById("numberLeave").value = leaveDays;
  } else {
    document.getElementById("numberLeave").value = "";
  }
}  
// {% endcomment %}