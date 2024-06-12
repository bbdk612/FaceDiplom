$(document).ready(() => {
  $(".check-all").click(function () {
    // Get the status of the select-all checkbox
    let data = $(this).attr("id");
    let isChecked = $(this).prop("checked");

    // Iterate through each checkbox in the list
    $(`input[data-group-number="${data}"]`).each(function () {
      // Set the checkbox status to the same as the select-all checkbox
      $(this).prop("checked", isChecked);
    });
  });

  $("li.group_item span").click(function () {
    let id = $(this).attr("id");
    console.log(id);
    $(`ul#group_${id}`).toggle(20);
  });
  $("input#submit").click(function(){
    let name = $("input#name").val();
    let students = []
    $("li.student_item input[type=checkbox]:checked").each(function (){
      let student = $(this).attr("id")
      students.push(student);
    });
    console.log(students);
    $.ajax({
      method: "POST",
      dataType: "html",
      data: {
        name:name,
        students: students.join(" "),
      },
      success: function (data) {
        console.log(data);
        window.location.replace("/");
      }
    })
  })
});
