const assignCategory = () => {
    categories = []
    if (document.getElementById("abs").checked) {
        categories.push(document.getElementById("abs").value)
    }
    if (document.getElementById("arms").checked) {
        categories.push(document.getElementById("arms").value)
    }
    if (document.getElementById("back").checked) {
        categories.push(document.getElementById("back").value)
    }
    if (document.getElementById("calves").checked) {
        categories.push(document.getElementById("calves").value)
    }
    if (document.getElementById("cardio").checked) {
        categories.push(document.getElementById("cardio").value)
    }
    if (document.getElementById("chest").checked) {
        categories.push(document.getElementById("chest").value)
    }
    if (document.getElementById("legs").checked) {
        categories.push(document.getElementById("legs").value)
    }
    if (document.getElementById("shoulders").checked) {
        categories.push(document.getElementById("shoulders").value)
    }
    document.getElementById("category").value = categories.join()
}


function searching() {
    const searchBtn = document.getElementById("search-btn");
    searchBtn.innerText = "Searching..."
}