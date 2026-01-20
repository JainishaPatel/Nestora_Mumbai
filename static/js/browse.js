document.addEventListener('DOMContentLoaded', () => {
    const areaRadios = document.querySelectorAll('.area-radio');
    const areaInput = document.getElementById('areaInput');
    const areaDropdownBtn = document.getElementById('areaDropdownBtn');

    areaRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            // Set hidden input value
            areaInput.value = this.value;

            // Update dropdown button text
            areaDropdownBtn.innerText = this.value;
        });
    });
});