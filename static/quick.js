var jqXHR = $.ajax({
    type: "GET",
    url: "/getpoints",
});

response = jqXHR.responseText;
console.log(response)