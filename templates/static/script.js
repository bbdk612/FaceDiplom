$(document).ready(() => {
  $(".start-capture").click(() => {
    $.ajax({
      method: "POST",
      url: "/start_capture",
      dataType: "json",
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
      dataType: "json",
      success: (data) => {
        alert("сбор данных успешно oстановлен");
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
      },
      error: (xhr, status, error) => {
        alert(xhr.responseText);
      },
    });
  });
});
