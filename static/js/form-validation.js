// Show / Hide Password
document.querySelectorAll(".password-toggle").forEach(toggle => {
    const input = document.getElementById(toggle.dataset.target);
    const icon = toggle.querySelector("i");

    toggle.addEventListener("click", function () {
        const isPassword = input.type === "password";
        input.type = isPassword ? "text" : "password";
        icon.classList.toggle("fa-eye");
        icon.classList.toggle("fa-eye-slash");
    });
});

// Glow Validation
function validateInput(input, regex) {
    if (regex.test(input.value)) {
        input.classList.add("input-valid");
        input.classList.remove("input-invalid");
    } else {
        input.classList.add("input-invalid");
        input.classList.remove("input-valid");
    }
}

document.querySelectorAll(".validate-email").forEach(input => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    input.addEventListener("input", () => validateInput(input, regex));
});

document.querySelectorAll(".validate-password").forEach(input => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    input.addEventListener("input", () => validateInput(input, regex));
});