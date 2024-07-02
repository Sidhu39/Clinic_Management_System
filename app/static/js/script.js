// Example JS script
document.addEventListener('DOMContentLoaded', function() {
    // Example: Handle form submission
    const form = document.querySelector('#appointmentForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        // Perform form validation or submit via AJAX
        console.log('Form submitted!');
    });

    // Example: AJAX request
    function fetchData(url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Process fetched data
                console.log(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Example: Trigger AJAX request on button click
    const fetchDataBtn = document.querySelector('#fetchDataBtn');
    fetchDataBtn.addEventListener('click', function() {
        fetchData('/api/data');
    });
});
