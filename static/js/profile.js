document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('profileForm')
    const saveBtn = document.getElementById('saveBtn')

    if (!form || !saveBtn) return

    // Store initial form values
    const initialValues = {}

    Array.from(form.elements).forEach(el => {
        if (el.name) {
            initialValues[el.name] = el.value
        }
    })

    // Enable save button only if something changes
    function checkChanges() {
        let changed = false

        Array.from(form.elements).forEach(el => {
            if (el.name && el.value !== initialValues[el.name]) {
                changed = true
            }
        })

        saveBtn.disabled = !changed
    }

    form.addEventListener('input', checkChanges)
})
