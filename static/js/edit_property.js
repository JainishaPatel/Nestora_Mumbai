document.addEventListener('DOMContentLoaded', () => {

    /* ================= BOOTSTRAP VALIDATION ================= */
    (() => {
        'use strict'
        const forms = document.querySelectorAll('.needs-validation')

        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
    })()


    /* ================= AREA DROPDOWN ================= */
    const areaInput = document.getElementById('areaInput')
    const areaDropdown = document.getElementById('areaDropdown')
    const areaRadios = document.querySelectorAll('.area-radio')

    if (areaInput && areaDropdown) {
        // Toggle dropdown
        areaInput.addEventListener('click', () => {
            areaDropdown.classList.toggle('show')
        })

        // Close dropdown on outside click
        document.addEventListener('click', (e) => {
            if (!areaInput.contains(e.target) && !areaDropdown.contains(e.target)) {
                areaDropdown.classList.remove('show')
            }
        })
    }

    // Set selected area
    areaRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            areaInput.value = radio.value
            areaDropdown.classList.remove('show')
        })
    })


    /* ================= REMOVE EXISTING IMAGES ================= */
    const existingImages = document.getElementById('existing-images')

    if (existingImages) {
        existingImages.addEventListener('click', e => {
            if (e.target.classList.contains('remove-btn')) {
                const previewDiv = e.target.closest('.image-preview')
                if (previewDiv) previewDiv.remove()
            }
        })
    }

})
