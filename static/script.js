// Confirm before submitting student details
const studentForm = document.querySelector(
    'form[action="/add"]'
);

if (studentForm) {
    studentForm.addEventListener("submit", function(event) {
        const roll = document.querySelector(
            'input[name="roll"]'
        ).value.trim();

        const name = document.querySelector(
            'input[name="name"]'
        ).value.trim();

        if (!roll || !name) {
            event.preventDefault();
            alert("Please enter student details.");
            return;
        }

        const confirmAdd = confirm(
            "Do you want to add this student?"
        );

        if (!confirmAdd) {
            event.preventDefault();
        }
    });
}

// Confirm before searching
const searchForm = document.querySelector(
    '.search-form'
);

if (searchForm) {
    searchForm.addEventListener("submit", function(event) {
        const searchInput = searchForm.querySelector(
            'input[name="search"]'
        );

        if (!searchInput.value.trim()) {
            event.preventDefault();
            alert("Please enter a name or roll number.");
            searchInput.focus();
        }
    });
}