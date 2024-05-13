$(document).ready(() => {
  // console.log($("input[id='lesson_id']").val())
  $(".start-capture").click(() => {
    $.ajax({
      method: "POST",
      url: "/start_capture",
      dataType: "html",
      data: {
        lesson_id: $("input[id='lesson_id']").val(),
      },
      success: () => {
        alert("сбор данных успешно запущен");
      },
      error: (xhr, status, error) => {
        alert(xhr.responseText);
      },
    });
  });
  $(".stop-capture").click(() => {
    $.ajax({
      method: "POST",
      url: "/stop_capture",
      dataType: "html",

      success: (data) => {
        alert("сбор данных успешно oстановлен");
        console.log(data);
        data = JSON.parse(data);
        console.log(data);
        htmlStr = "";
        data.students.forEach((element) => {
          htmlStr += `<li>${element}</li>`;
        });
        $(".students-on-lesson").html(`
          <h2>Список студентов на паре</h2>
          <ul>
          ${htmlStr}
          </ul>
          `);
        $.ajax({
          method: "POST",
          dataType: "html",
          url: `/student/check/${$("input[id='lesson_id']").val()}`,
          data: data,
          success: () => {
            window.location.replace("/");
          },
        });
      },
      error: (xhr, status, error) => {
        alert(xhr.responseText);
      },
    });
  });
});
