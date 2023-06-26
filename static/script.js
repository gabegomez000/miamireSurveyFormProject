window.addEventListener("DOMContentLoaded", function() {
    var starRadios = document.querySelectorAll('.star-rating input[type="radio"]');

    starRadios.forEach(function(radio) {
        radio.addEventListener("change", function() {
            var currentRating = parseInt(this.value);
            var labels = this.parentNode.querySelectorAll("label");

            labels.forEach(function(label, index) {
                if (index < currentRating) {
                    label.classList.add("active");
                } else {
                    label.classList.remove("active");
                }
            });
        });
    });
});