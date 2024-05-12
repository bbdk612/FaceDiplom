$(document).ready(() => {
  $(".lesson__button-delete").click((e) => {
    let id = e.target.id;

    $.ajax({
      method: "POST",
      url: `/lesson/delete/${id}`,
      dataType: "json",
      success: (data) => {
        $(`li#lesson_${id}`).hide(20);
        alert(data.message);
      },
      error: (xhr, status, error) => {
        alert(xhr.responseText);
      },
    });
  });
});
