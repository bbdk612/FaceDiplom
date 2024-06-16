$(document).ready(() => {
  $("#save-data").click(() => {
    let checked = $("input[type='checkbox']:checked");
    checked.each((i, el) => {
      console.log(el.id);
      $.ajax({
        method: "POST",
        dataType: "json",
        url: `/lesson/student/${el.id}/check`,
        success: (data) => {
          console.log(data);
        },
      });
    });

    let unchecked = $("input[type='checkbox']:not(:checked)");
    unchecked.each((i, el) => {
      console.log(el.id);
      $.ajax({
        method: "POST",
        dataType: "json",
        url: `/lesson/student/${el.id}/uncheck`,
        success: (data) => {
          console.log(data);
        },
      });
    });

    alert("Данные успешно обновленны");
    window.location.replace("/");
  });
});
