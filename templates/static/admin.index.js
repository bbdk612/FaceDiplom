$(document).ready(() => {
  $(".user_button-delete").click((e) => {
    let id = e.target.id;
    $.ajax({
      method: "DELETE",
      url: `/user/delete/${id}`,
      dataType: "json",
      success: (data) => {
        $(`li#user_${id}`).hide(20);
        alert(data.message);
      },
      error: () => {
        alert("Что-то пошло не так");
      },
    });
  });
  $(".student_button-delete").click((e) => {
    let id = e.target.id;
    $.ajax({
      method: "DELETE",
      url: `/student/delete/${id}`,
      dataType: "json",
      success: (data) => {
        $(`li#student_${id}`).hide(20);
        alert(data.message);
      },
      error: () => {
        alert("Что-то пошло не так");
      },
    });
  });
  $(".auditory_button-delete").click((e) => {
    let id = e.target.id;
    $.ajax({
      method: "DELETE",
      url: `/auditory/delete/${id}`,
      dataType: "json",
      success: (data) => {
        $(`li#auditory_${id}`).hide(20);
        alert(data.message);
      },
      error: () => {
        alert("Что-то пошло не так");
      },
    });
  });

  $(".group_button-delete").click((e) => {
    let id = e.target.id;

    $.ajax({
      method: "DELETE",
      url: `/group/delete/${id}`,
      dataType: "json",
      success: (data) => {
        console.log(data);
        $(`#group_${id}`).hide(20);
      },
    });
  });
});
