$(".logout").click(() => {
    $.ajax({
        method: "POST", url: "/logout", dataType: "json", success: (data) => {
            alert(data.message);
            window.location.replace("/login");
        },
    });
});