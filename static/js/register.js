document.addEventListener("DOMContentLoaded", function () {
    const roleSelect = document.getElementById("role");
    const dynamicFields = document.getElementById("dynamic-fields");
    const registerForm = document.getElementById("register-form");

    roleSelect.addEventListener("change", function () {
        dynamicFields.innerHTML = ""; // Clear existing fields

        if (roleSelect.value === "Patient") {
            dynamicFields.innerHTML = `
                <div class="form-group">
                  <label class="form-label">Age</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-calendar-days icon"></i>
                    <input type="number" class="form-input" name="age" placeholder="Age" required>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Gender</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-venus-mars icon"></i>
                    <select class="form-select" name="gender" required>
                        <option value="">Select Gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Interests / Focus</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-heart icon"></i>
                    <input type="text" class="form-input" name="interests" placeholder="e.g. Anxiety, Stress">
                  </div>
                </div>
            `;
        } else if (roleSelect.value === "Therapist") {
            dynamicFields.innerHTML = `
                <div class="form-group">
                  <label class="form-label">Specialization</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-stethoscope icon"></i>
                    <input type="text" class="form-input" name="specialization" placeholder="e.g. Cognitive Behavioral Therapy" required>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Qualification</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-graduation-cap icon"></i>
                    <input type="text" class="form-input" name="qualification" placeholder="e.g. Psy.D., Licensed Counselor" required>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Experience (Years)</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-briefcase icon"></i>
                    <input type="number" class="form-input" name="experience" placeholder="Years of experience" required>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Contact Number</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-phone icon"></i>
                    <input type="tel" class="form-input" name="contact" pattern="[0-9]{10}" maxlength="10" minlength="10" placeholder="10-digit phone number" required>
                  </div>
                </div>
            `;
        } else if (roleSelect.value === "Caretaker") {
            dynamicFields.innerHTML = `
                <div class="form-group">
                  <label class="form-label">Patient's Email</label>
                  <div class="input-wrapper">
                    <i class="fa-solid fa-user-injured icon"></i>
                    <input type="email" class="form-input" id="patient_email" name="patient_email" placeholder="Email of the patient" required>
                  </div>
                </div>
            `;
        }
    });

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        if (jsonData.password !== jsonData.confirm_password) {
            if (typeof showMsg === "function") showMsg("Passwords do not match!", true);
            else alert("Passwords do not match!");
            return;
        }

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(jsonData),
            });

            const data = await response.json();
            
            if (typeof showMsg === "function") {
                showMsg(data.message || "Account created successfully", !data.success);
            } else {
                alert(data.message);
            }

            if (data.success) {
                setTimeout(() => window.location.href = "/login", 1500);
            }
        } catch (error) {
            if (typeof showMsg === "function") showMsg("Something went wrong. Please try again.", true);
            else alert("Something went wrong. Please try again.");
        }
    });
});
