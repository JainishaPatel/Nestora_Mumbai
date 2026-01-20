// static/js/admin-properties.js

document.addEventListener("DOMContentLoaded", function () {
    const rejectModal = document.getElementById("rejectModal");
    const rejectForm = document.getElementById("rejectForm");

    if (!rejectModal || !rejectForm) return;

    rejectModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const propertyId = button.getAttribute("data-property-id");

        rejectForm.action = `/admin/property/reject/${propertyId}`;
    });
});
