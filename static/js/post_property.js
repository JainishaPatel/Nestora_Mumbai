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


    /* ================= RENT / BUY INFO TEXT ================= */
    const propertyTypeSelect = document.querySelector('select[name="property_type"]')
    const depositInfo = document.getElementById('depositInfo')
    const maintenanceInfo = document.getElementById('maintenanceInfo')

    if (propertyTypeSelect) {
        propertyTypeSelect.addEventListener('change', () => {
            const type = propertyTypeSelect.value

            if (type === 'Rent') {
                depositInfo.textContent =
                    "Advance money paid by the tenant, returned after leaving the house"
                maintenanceInfo.textContent =
                    "Not applicable for renters"
            } else if (type === 'Buy') {
                depositInfo.textContent =
                    "Optional deposit amount (if any)"
                maintenanceInfo.textContent =
                    "Monthly maintenance charges (only for buyers)"
            } else {
                depositInfo.textContent =
                    "Enter deposit if applicable"
                maintenanceInfo.textContent =
                    "Enter maintenance charges if applicable"
            }
        })
    }


    /* ================= AREA DROPDOWN ================= */
    const areaInput = document.getElementById('areaInput')
    const areaDropdown = document.getElementById('areaDropdown')
    const areaRadios = document.querySelectorAll('.area-radio')

    if (areaInput && areaDropdown) {
        // Toggle dropdown
        areaInput.addEventListener('click', () => {
            areaDropdown.classList.toggle('show')
        })

        // Close dropdown when clicking outside
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
})
