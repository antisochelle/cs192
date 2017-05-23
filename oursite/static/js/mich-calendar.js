$.getScript('http://arshaw.com/js/fullcalendar-1.6.4/fullcalendar/fullcalendar.min.js',function(){
  
  var date = new Date();
  var d = date.getDate();
  var m = date.getMonth();
  var y = date.getFullYear();

  console.log(d)
  console.log("HELLO WORLD")
  
  $('#calendar').fullCalendar({
    header: {
      left: 'prev,next today'
    },
    editable: true,
    events: [
      {
        title: 'Case No. A145 Complaint SDC Receipt Deadline',
        start: new Date(y, m, 2)
      },
      {
        title: 'Case No. BA1409 Summons Service Date',
        start: new Date(y, m, d-5),
        end: new Date(y, m, d-2)
      },
      {
        title: 'Case No. BA1409 Respondent Answer Date',
        start: new Date(y, m, d, 10, 30),
        allDay: false
      },
      {
        title: 'Case No. BA1409 Prelim Meeting Notice Deadline',
        start: new Date(y, m, d+7, 12, 0),
        end: new Date(y, m, d+7, 14, 0),
        allDay: false
      },
      {
        title: 'Case No. AC1082 Decision Copy to Chancellor Deadline',
        start: new Date(y, m, d+1, 19, 0),
        end: new Date(y, m, d+1, 22, 30),
        allDay: false
      },
      {
        title: 'Case No. XY2140 Respondent Answer Date',
        start: new Date(y, m, d+14, 10, 30),
        allDay: false
      }
    ]
  });
})