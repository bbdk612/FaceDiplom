$(".loader_container").hide()
$("button#save").hide()
$(".stop-capture").prop("disabled", true)
$(document).ready(() => {
    $(".start-capture").click((e) => {
        let lesson_id = $("input[id='lesson_id']").val()
        $(e.target).prop("disabled", true)
        $(".loader_container").show()
        $(".stop-capture").prop("disabled", false)
        $.ajax({
            method: "POST", url: `/start_capture/${lesson_id}`, dataType: "html", success: () => {
                alert("сбор данных успешно запущен");
                $(".loader_container").hide()
            }, error: (xhr, status, error) => {
                alert(xhr.responseText);
            },
        });
    });
    $(".stop-capture").click((e) => {
        $(e.target).prop("disabled", true)
        $(".start-capture").prop("disabled", false)
        let lesson_id = $("input[id='lesson_id']").val()
        $.ajax({
            method: "POST", url: `/stop_capture/${lesson_id}`, dataType: "json",

            success: (data) => {
                let findedStudentsHTML = "";
                let unfindedStudentsHTML = ""
                data.responsed.forEach((element) => {
                    let other_students = ""

                    data.all.forEach((el) => {
                        if (el.id !== element.id) {
                            other_students += `<option value='${el.id}'>${el.name}</option>`
                        }
                    })
                    findedStudentsHTML += `<li>
                        <img src="${element.faceUrl}">
                        <select onchange="selectChange(this.value)" name="studentId" class="finded-student">
                            <option  value="${element.id}">${element.name}</option>
                            ${other_students}
                        </select>
                        </li>`;
                });
                data.all.forEach((el) => {
                    unfindedStudentsHTML += `
                    <div class="unfinded-student" id="student_${el.id}">
                        <input type="checkbox" onchange="selectCheck()" id="${el.id}" name="${el.id}">
                        <label for="${el.id}">${el.name}</label>
                    </div>
                    `
                })
                $(".students-on-lesson").html(`
                    <h2>Список студентов на паре</h2>
                    <ul class="finded-student">
                        ${findedStudentsHTML}
                    </ul>
                    <h2>Не найденные студенты</h2>
                    <div class="check-all">
                        <input type="checkbox" onchange="checkAll(this)" name="check-all" id="check-all">
                        <label for="check-all">Отметить всех</label>
                    </div>
                    <div class="unfinded-students">
                        ${unfindedStudentsHTML}
                    </div>
                `);
                data.responsed.forEach((el) => {
                    if ($(`option[value='${el.id}']:checked`)) {
                        $(`option[value='${el.id}']:not(:checked)`).hide()
                        $(`#student_${el.id}`).hide()
                    }
                })
                $("button#save").show()
            }, error: (xhr, status, error) => {
                alert(xhr.responseText);
            },
        });
    });

    $("button#save").click(() => {
        students = []
        $(".finded-student").each((i, el) => {
            if( +$(el).val() > 0)  {
                students.push($(el).val())
            }
        })
        $('.unfinded-student').each((i, el)=>{
            students.push($(el).find("input:checked").attr("id"))
        })

        let lesson_id = $("input[id='lesson_id']").val()
        studentsStr = students.join(";")
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/student/check/${lesson_id}`,
            data: {
                students: studentsStr,
            }, success: () => {
                alert("Все студенты отмечены")
                window.location.replace("/")
            }
        })
    })
});

function checkAll(target) {
        $('.unfinded-student').each((i, el) => {
            let input = $(el).find('input')
            if ($(target).is(":checked")) {
                input.prop("checked", 1)
            } else {
                input.prop("checked", 0)
            }
        })
}

function selectChange(id) {
    $(`option`).show()
    $(`div[id^="student_"]`).show()
    if ($(`option[value='${id}']:checked`)) {
        $(`option[value='${id}']:not(:checked)`).hide()
        $(`#student_${id}`).hide()
    }
}

function selectCheck(id) {
    $(`option`).show()
    $(`div[id^="student_"]`).show()
    if ($(`div[id^="${id}"]:checked`)) {
        $(`option[value='${id}']:not(:checked)`).hide()
    }
}