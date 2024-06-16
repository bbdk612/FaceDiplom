$(document).ready(() => {
  $(".lesson__button-delete").click((e) => {
    let id = e.target.id;

    $.ajax({
      method: "DELETE",
      url: `/lesson/delete/${id}`,
      dataType: "json",
      success: (data) => {
        $(`#lesson_${id}`).hide(20);
      },
      error: (xhr, status, error) => {
        alert(xhr.responseText);
      },
    });
  });

  $(".course__button-delete").click((e) => {
    let id = e.target.id;

    $.ajax({
      method: "DELETE",
      url: `/course/delete/${id}`,
      dataType: "json",
      success: (data) => {
        console.log(data);
        $(`#course_${id}`).hide(20);
      },
    });
  });

  $(".logout").click(() => {
    $.ajax({
      method: "POST",
      url: "/logout",
      dataType: "json",
      success: (data) => {
        alert(data.message);
        window.location.replace("/login");
      },
    });
  });
});
